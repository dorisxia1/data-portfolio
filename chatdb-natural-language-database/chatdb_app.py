import os
import openai
import pymysql
from pymongo import MongoClient
import ast
import pprint
from dotenv import load_dotenv
import re
from tabulate import tabulate
import traceback

# --- Load environment variables ---
load_dotenv()

# --- Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env")

if not MYSQL_USER or not MYSQL_PASSWORD or not MYSQL_DB:
    raise ValueError("Missing MySQL configuration in .env")

if not MONGO_DB_NAME:
    raise ValueError("Missing MONGO_DB_NAME in .env")

openai.api_key = OPENAI_API_KEY

# --- Database Connections ---
try:
    mysql_conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )
    mysql_cursor = mysql_conn.cursor()
    print("Successfully connected to MySQL.")
except pymysql.Error as e:
    print(f"Error connecting to MySQL: {e}")
    exit(1)

try:
    mongo_client = MongoClient(MONGO_URI)
    mongo_client.admin.command('ping')
    mongo_db_instance = mongo_client[MONGO_DB_NAME]
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    if 'mysql_conn' in locals() and mysql_conn.open:
        mysql_conn.close()
    exit(1)

# --- OpenAI Prompts ---
sql_system_prompt = f"""You are an expert assistant that converts English questions into executable MySQL queries.
Use the given database schema to write correct MySQL SQL queries.
Only output the SQL query, nothing else. No explanations, no markdown formatting.

MySQL Schema (`{MYSQL_DB}` database):
- `City` table:
  Columns: city_id (INT, PK), city_name (VARCHAR), state_name (VARCHAR), population_2020 (INT), population_2010 (INT), land_area_sqmi (FLOAT), density (FLOAT)
  Description: Information about US cities.

- `HouseholdType` table:
  Columns: household_id (INT, PK), description (VARCHAR)
  Description: Defines different household compositions (e.g., 'One Adult, No Kids', 'Two Adults, Two Kids').

- `LivingWage` table:
  Columns: livingwage_id (INT, PK), city_id (INT, FK -> City.city_id), household_id (INT, FK -> HouseholdType.household_id), wage (DECIMAL(5,2))
  Description: Stores the hourly living wage required for a specific household type in a specific city.

- `PovertyGroup` table:
  Columns: group_id (INT, PK), group_name (VARCHAR)
  Description: Defines demographic or wage-level groups for poverty statistics (e.g., 'Total Below Poverty', 'White', 'Black', 'Hispanic').

- `YearlyPovertyThresholds` table:
  Columns: year (INT, PK), annual_poverty_wage (INT), hourly_poverty_wage (DECIMAL(5,2))
  Description: Stores the official poverty wage threshold for each year. (Note: The loading script used placeholder values here, adjust if needed).

- `PovertyWageDistribution` table:
  Columns: pwd_id (INT, PK), year (INT, FK -> YearlyPovertyThresholds.year), group_id (INT, FK -> PovertyGroup.group_id), percentage (DECIMAL(4,1))
  Description: Shows the percentage of workers within a specific poverty group for a given year.

Relationships:
- LivingWage links City and HouseholdType.
- PovertyWageDistribution links YearlyPovertyThresholds and PovertyGroup.

Example User Query: "What is the living wage for one adult with one kid in Los Angeles?"
Example Assistant Output: SELECT lw.wage FROM LivingWage lw JOIN City c ON lw.city_id = c.city_id JOIN HouseholdType ht ON lw.household_id = ht.household_id WHERE c.city_name = 'Los Angeles' AND ht.description = 'One Adult, One Kid';

Example User Query: "Show tables"
Example Assistant Output: SHOW TABLES;

Example User Query: "Update the population of Los Angeles to 4000000"
Example Assistant Output: UPDATE City SET population_2020 = 4000000 WHERE city_name = 'Los Angeles';
"""

mongo_system_prompt = """You are an expert assistant that converts English questions into executable MongoDB queries for the PyMongo library.
The MongoDB database is '{0}'. It contains multiple collections related to wages by education, split by category.

Available Collections:
1.  `wages_overall`: Contains overall median wages by education level.
    Fields: `year` (INT), `less_than_hs`, `high_school`, `some_college`, `bachelors_degree`, `advanced_degree` (all DECIMAL/FLOAT).
2.  `wages_gender`: Contains median wages broken down by gender and education level.
    Fields: `year` (INT), `men_less_than_hs`, `women_less_than_hs`, `men_high_school`, `women_high_school`, etc.
3.  `wages_race`: Contains median wages broken down by race/ethnicity and education level (may also include gender breakdown within race).
    Fields: `year` (INT), `white_less_than_hs`, `black_less_than_hs`, `hispanic_less_than_hs`, `asian_less_than_hs`, `white_men_bachelors_degree`, `black_women_advanced_degree`, etc.

**IMPORTANT:** You MUST determine the most appropriate collection based on the user's query and **prefix your output with the collection name followed by a dot (.)**.

Output *only* the Python-style MongoDB command snippet required for PyMongo, starting with the collection name.
Use the appropriate method: `.find()`, `.find_one()`, `.aggregate()`, `.insert_one()`, `.update_one()`, `.delete_one()`.

For numeric values, use actual numbers rather than variable placeholders.
For example, write:
wages_overall.insert_one({{'year': 2024, 'less_than_hs': 18.50, 'high_school': 25.20, 'some_college': 28.30, 'bachelors_degree': 44.70, 'advanced_degree': 56.90}})

Instead of:
wages_overall.insert_one({{'year': 2024, 'less_than_hs': value1, 'high_school': value2, 'some_college': value3, 'bachelors_degree': value4, 'advanced_degree': value5}})

Provide necessary arguments (filter, projection, pipeline, document, update).
No explanations, no markdown formatting.

Example User Query: "Show the average bachelor degree wage in 2021."
Example Assistant Output: wages_overall.find_one({{'year': 2021}}, {{'_id': 0, 'bachelors_degree': 1}})

Example User Query: "Compare men vs women high school wage in 2020."
Example Assistant Output: wages_gender.find_one({{'year': 2020}}, {{'_id': 0, 'men_high_school': 1, 'women_high_school': 1}})

Example User Query: "What is the average difference between advanced_degree and bachelors_degree across all years?"
Example Assistant Output: wages_overall.aggregate([{{'$project': {{'_id': 0, 'year': 1, 'diff': {{'$subtract': ['$advanced_degree', '$bachelors_degree']}} }}}}, {{'$group': {{'_id': None, 'average_difference': {{'$avg': '$diff'}} }} }}])

Example User Query: "Add a record for 2023 to the gender wages collection with men_high_school wage 23.0"
Example Assistant Output: wages_gender.insert_one({{'year': 2023, 'men_high_school': 23.0}})

Example User Query: "Update the 2022 black_women_advanced_degree wage to 40.0"
Example Assistant Output: wages_race.update_one({{'year': 2022}}, {{'$set': {{'black_women_advanced_degree': 40.0}}}})
"""

# --- Backend Determination ---
SQL_KEYWORDS = {"city", "cities", "state", "living wage", "poverty", "below poverty", "household", "population", "density", "area", "threshold", "distribution"}
MONGO_KEYWORDS = {"education", "college", "bachelor", "degree", "high school", "men", "women", "race", "gender", "wage", "median", "overall", "black", "white", "hispanic", "asian"}

def determine_backend(user_input: str) -> str:
    text = user_input.lower()
    mongo_score = sum(1 for word in MONGO_KEYWORDS if word in text)
    sql_score = sum(1 for word in SQL_KEYWORDS if word in text)

    if text in ["show tables", "list tables", "sql schema", "show sql tables"]:
        return "sql_schema"
    if text.startswith("describe "):
        return "sql_schema"
    if text in ["show collections", "list collections", "mongo schema", "show mongo collections"] or \
       re.search(r"(show|list)\s+(all\s+)?(the\s+)?collections", text) or \
       re.search(r"(show|list)\s+mongo", text):
        return "mongo_schema"
    if text == "help":
        return "help"

    if mongo_score > sql_score:
        return "mongo"
    elif sql_score > mongo_score:
        return "sql"
    elif mongo_score == 0 and sql_score == 0:
         if 'wage' in text or 'year' in text:
              return "mongo"
         else:
              return "sql"
    else:
        return "sql"

# --- Query Generation ---
def generate_query(natural_language: str, system_prompt: str) -> str:
    try:
        # Simplified prompt formatting that avoids problems with special characters
        if '{0}' in system_prompt:
            prompt_to_use = system_prompt.format(MONGO_DB_NAME)
        elif '{MYSQL_DB}' in system_prompt:
            prompt_to_use = system_prompt.format(MYSQL_DB=MYSQL_DB)
        else:
            prompt_to_use = system_prompt

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt_to_use},
                {"role": "user", "content": natural_language}
            ],
            temperature=0
        )
        query = response.choices[0].message.content.strip()
        query = query.replace('```sql', '').replace('```python', '').replace('```json', '').replace('```', '')
        query = query.strip()
        return query
    except openai.APIError as e:
        print(f"OpenAI API Error: {e}")
        return f"Error: OpenAI API request failed - {e}"
    except Exception as e:
        print(f"Error during OpenAI call: {e}")
        return f"Error: Failed to generate query - {e}"

def generate_sql_query(natural_language: str) -> str:
    query = generate_query(natural_language, sql_system_prompt)
    if isinstance(query, str) and not query.startswith("Error:") and not query.endswith(';'):
         if query.upper().lstrip().startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'SHOW', 'DESCRIBE')):
              query += ';'
    return query

def generate_mongo_query(natural_language: str) -> str:
    return generate_query(natural_language, mongo_system_prompt)

# --- Query Execution ---
def execute_sql_query(sql_query: str):
    if not sql_query or sql_query.startswith("Error:") or not mysql_conn.open:
         return f"Cannot execute query: {sql_query}"
    try:
        cursor = mysql_conn.cursor()
        rows_affected = cursor.execute(sql_query)
        query_type = sql_query.strip().upper().split()[0]

        if query_type in ("SELECT", "SHOW", "DESCRIBE"):
            results = cursor.fetchall()
            if not results:
                return "(No results found)"
            headers = results[0].keys() if results else []
            table_data = [list(row.values()) for row in results]
            return tabulate(table_data, headers=headers, tablefmt="grid")
        else:
            mysql_conn.commit()
            return f"Query OK. {rows_affected if rows_affected is not None else cursor.rowcount} rows affected."
    except pymysql.Error as e:
        mysql_conn.rollback()
        return f"SQL Execution Error: {e}"
    except Exception as e:
        mysql_conn.rollback()
        return f"An unexpected error occurred during SQL execution: {e}"
    finally:
         if 'cursor' in locals() and cursor != mysql_cursor:
              cursor.close()

def execute_mongo_query(mongo_query_str: str):
    if not mongo_query_str or mongo_query_str.startswith("Error:") or not mongo_client:
         return f"Cannot execute query: {mongo_query_str}"

    collection_name = None
    method_name = None
    args_str = None
    evaluated_args = None
    target_coll = None

    try:
        # Stage 1: Parse
        match = re.match(r"(\w+)\.(\w+)\((.*)\)", mongo_query_str, re.DOTALL | re.IGNORECASE)
        if not match:
            return f"Error: Could not parse MongoDB query. Expected format 'collection_name.method(...)', got: {mongo_query_str}"

        collection_name = match.group(1)
        method_name = match.group(2)
        args_str = match.group(3).strip()
        if args_str.endswith(');'):
            args_str = args_str[:-2]
        elif args_str.endswith(')'):
             args_str = args_str[:-1]

        # Stage 2: Get Collection
        actual_collection_names = mongo_db_instance.list_collection_names()
        found_coll_name = None
        for name in actual_collection_names:
            if name.lower() == collection_name.lower():
                found_coll_name = name
                break

        if not found_coll_name:
             return f"Error: MongoDB collection '{collection_name}' does not exist in database '{MONGO_DB_NAME}'. Available: {actual_collection_names}"
        target_coll = mongo_db_instance[found_coll_name]
        collection_name = found_coll_name

        if not hasattr(target_coll, method_name):
            return f"Error: MongoDB collection '{collection_name}' does not have method '{method_name}'"
        method_to_call = getattr(target_coll, method_name)

        # Stage 3: Parse Arguments - IMPROVED VERSION
        evaluated_args = []
        if args_str:
            try:
                # For update operations, correctly handle the $set operator
                if '$set' in args_str:
                    # Safe evaluation approach for update operations
                    args_components = []
                    depth = 0
                    current = ""
                    for char in args_str:
                        if char == '{':
                            depth += 1
                        elif char == '}':
                            depth -= 1
                        
                        current += char
                        
                        if char == ',' and depth == 0:
                            args_components.append(current[:-1].strip())
                            current = ""
                    
                    if current:
                        args_components.append(current.strip())
                    
                    for component in args_components:
                        evaluated_args.append(ast.literal_eval(component))
                # For find_one and similar methods taking two arguments
                elif method_name == 'find_one' and '}, {' in args_str:
                    parts = []
                    brace_count = 0
                    current_part = ""
                    
                    for char in args_str:
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                        
                        current_part += char
                        
                        # If we found a comma at top level (not inside braces)
                        if char == ',' and brace_count == 0:
                            # Remove the comma from the end
                            parts.append(current_part[:-1].strip())
                            current_part = ""
                    
                    # Add the last part if not empty
                    if current_part.strip():
                        parts.append(current_part.strip())
                    
                    # Now evaluate each part separately
                    for part in parts:
                        evaluated_args.append(ast.literal_eval(part))
                # For insert_one operations, provide default values for missing fields
                elif method_name == 'insert_one' and 'year' in args_str:
                    doc = ast.literal_eval(args_str)
                    if isinstance(doc, dict) and 'year' in doc:
                        # Ensure all education fields have values if one is present
                        ed_fields = ['less_than_hs', 'high_school', 'some_college', 'bachelors_degree', 'advanced_degree']
                        for field in ed_fields:
                            if field not in doc:
                                doc[field] = 0.0  # Default value
                        evaluated_args = [doc]
                else:
                    # For single argument methods
                    evaluated_args = [ast.literal_eval(args_str)]
            except (ValueError, SyntaxError) as e_eval:
                return f"Error: Could not safely evaluate MongoDB arguments: {e_eval}"
            except Exception as e_other:
                return f"Error: Unexpected error evaluating MongoDB arguments: {e_other}"

        # Stage 4: Execute
        try:
            # For find_one and similar methods with two arguments
            if method_name == 'find_one' and len(evaluated_args) == 2:
                result = method_to_call(evaluated_args[0], evaluated_args[1])
            else:
                result = method_to_call(*evaluated_args)
        except Exception as e_exec:
            error_details = str(e_exec)
            if hasattr(e_exec, 'details'):
                 error_details += f" | Details: {e_exec.details}"
            return f"MongoDB Execution Error: {error_details}"

        # Stage 5: Format Results
        if method_name in ["find", "aggregate"]:
            results = list(result)
            if not results:
                return "(No documents found)"
            return pprint.pformat(results)
        elif method_name == "find_one":
             if not result:
                  return "(No document found)"
             return pprint.pformat(result)
        elif method_name == "insert_one":
            return f"Inserted document with _id: {result.inserted_id}"
        elif method_name == "insert_many":
            return f"Inserted {len(result.inserted_ids)} documents."
        elif method_name in ["update_one", "update_many", "replace_one"]:
            return f"Query OK. Matched: {result.matched_count}, Modified: {result.modified_count}"
        elif method_name in ["delete_one", "delete_many"]:
            return f"Query OK. Deleted: {result.deleted_count} document(s)."
        else:
            return f"Query executed. Result: {result}"

    except Exception as e:
        error_context = f"Collection: {collection_name}, Method: {method_name}"
        return f"MongoDB Processing Error: {e}\nContext: {error_context}"


# --- Help Function ---
def print_help():
     print("\nChatDB Help:")
     print(" - Ask questions about the data in natural language.")
     print(" - Examples:")
     print("   'What is the population of New York City?' (Uses MySQL)")
     print("   'List living wages for San Francisco' (Uses MySQL)")
     print("   'Show average bachelor degree wage in 2021' (Uses MongoDB - wages_overall)")
     print("   'Compare men vs women high school wage in 2020' (Uses MongoDB - wages_gender)")
     print("   'What was the median wage for black women with advanced degrees in 2022?' (Uses MongoDB - wages_race)")
     print("   'Update the 2020 population for Chicago to 2700000' (Uses MySQL)")
     print(" - Schema commands:")
     print("   'show tables' / 'list tables' - List tables in MySQL.")
     print("   'describe <table_name>' - Show columns of a MySQL table.")
     print("   'show collections' / 'list collections' - List collections in MongoDB.")
     print(" - Type 'exit' or 'quit' to end the session.\n")

# --- Main Chat Loop ---
def chat_loop():
    print("\nWelcome to ChatDB!")
    print("Ask questions about living wages, poverty stats (MySQL), or wages by education (MongoDB - overall, gender, race collections).")
    print("Type 'help' for examples or 'exit' to quit.")

    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "q"}:
                print("Goodbye!")
                break

            backend = determine_backend(user_input)

            if backend == "help":
                 print_help()
                 continue
            elif backend == "sql_schema":
                if user_input.lower() in ["show tables", "list tables", "sql schema", "show sql tables"]:
                    result = execute_sql_query("SHOW TABLES;")
                elif user_input.lower().startswith("describe "):
                    table_name = user_input.split("describe", 1)[1].strip().split(";")[0]
                    if not re.match(r"^[a-zA-Z0-9_]+$", table_name):
                         result = "Invalid table name for DESCRIBE."
                    else:
                         result = execute_sql_query(f"DESCRIBE `{table_name}`;")
                else:
                     result = "Unknown SQL schema command."
                print(f"\nChatDB (SQL Schema):\n{result}")
                continue

            elif backend == "mongo_schema":
                try:
                    collections = mongo_db_instance.list_collection_names()
                    result = f"Collections in '{MONGO_DB_NAME}': {', '.join(collections)}"
                except Exception as e:
                    result = f"Error listing collections: {e}"
                print(f"\nChatDB (Mongo Schema):\n{result}")
                continue

            elif backend == "sql":
                print("--> Routing to MySQL...")
                sql_query = generate_sql_query(user_input)
                if sql_query.startswith("Error:"):
                     print(f"\nChatDB (SQL Generation Error):\n{sql_query}")
                else:
                     # Display the generated SQL code
                     print(f"\nGenerated SQL Query:")
                     print(f"```sql\n{sql_query}\n```")
                     
                     # Execute the query and show results
                     result = execute_sql_query(sql_query)
                     print(f"\nChatDB (SQL Result):\n{result}")

            elif backend == "mongo":
                print("--> Routing to MongoDB...")
                mongo_query_str = generate_mongo_query(user_input)
                if mongo_query_str.startswith("Error:"):
                     print(f"\nChatDB (Mongo Generation Error):\n{mongo_query_str}")
                else:
                     # Display the generated MongoDB code
                     print(f"\nGenerated MongoDB Query:")
                     print(f"```python\n{mongo_query_str}\n```")
                     
                     # Execute the query and show results
                     result = execute_mongo_query(mongo_query_str)
                     print(f"\nChatDB (Mongo Result):\n{result}")

            else:
                print("ChatDB: Sorry, I encountered an internal issue determining how to handle your query.")

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred in the chat loop: {e}")
            traceback.print_exc()

    # --- Cleanup Connections ---
    if 'mysql_conn' in locals() and mysql_conn.open:
        mysql_conn.close()
        print("MySQL connection closed.")
    if 'mongo_client' in locals():
        mongo_client.close()
        print("MongoDB connection closed.")

# --- Main Execution ---
if __name__ == "__main__":
    chat_loop()
