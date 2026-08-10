<template>
  <div class="risk-hotspots">
    <div class="explanation">
      <h1 style="margin-bottom: 0.2rem;">Mismatch Between Dementia Prevalence and Risk Factors</h1>
      <h3 style="margin-top: 0;">Where dementia burden exceeds — or defies — medical expectations</h3>

      <details open>
        <summary><strong>What this map visualizes</strong></summary>
        <p>
          This map shows how much higher or lower <strong>dementia prevalence</strong> is than expected based on a county’s burden of
          <em>stroke</em>, <em>diabetes</em>, and <em>cognitive disability</em>.
        </p>
        <p>
          The <strong>Mismatch Index</strong> is calculated by predicting dementia prevalence using a linear model of these three risk
          factors, then subtracting expected from actual prevalence. A higher value means dementia rates are worse than expected.
        </p>
        <ul>
          <li><strong style="color: #d7191c;">Higher index (+)</strong>: Dementia rates are <strong>higher than expected</strong> — suggesting hidden risk factors, late diagnosis, or care gaps.</li>
          <li><strong style="color: #1a9641;">Lower index (-)</strong>: Dementia is <strong>less common than expected</strong> — possibly due to strong care systems or protective conditions.</li>
        </ul>
        <p>
          <span style="color: #d7191c;"><strong>Red outlines</strong></span> highlight <strong>high-disparity states</strong>: states where the mismatch between expected and actual dementia prevalence is especially large at scale.
        </p>
        <label>
          <input type="checkbox" v-model="showOutlines" /> Show red outlines for high-disparity states
        </label>
      </details>
    </div>

    <div class="legend">
      <strong>Mismatch Index (%)</strong>
      <div class="legend-bar">
        <span>-10%</span>
        <div class="gradient-bar"></div>
        <span>+10%</span>
      </div>
      <div class="legend-labels">
        <span class="green-text">Lower than expected</span>
        <span class="yellow-text">As expected</span>
        <span class="red-text">Higher than expected</span>
      </div>
    </div>

    <div ref="mapContainer" class="map-container"></div>

    <transition name="slide-fade">
      <div v-if="selectedCounty" class="info-panel" @click.stop>
        <button class="close-button" @click="selectedCounty = null">✖</button>
        <h3>{{ selectedCounty.LocationName }}, {{ stateNames[selectedCounty.StateAbbr] }}</h3>
        <ul>
          <li><strong>Mismatch Index:</strong> {{ (+selectedCounty.mismatch_index * 100).toFixed(2) }}%</li>
          <li><strong>Dementia Prevalence:</strong> {{ (+selectedCounty.prevalence_rate * 100).toFixed(2) }}%</li>
          <li><strong>Stroke Rate:</strong> {{ selectedCounty.stroke }}%</li>
          <li><strong>Diabetes Rate:</strong> {{ selectedCounty.diabetes }}%</li>
          <li><strong>Cognitive Disability:</strong> {{ selectedCounty.cog_disability }}%</li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl'
import * as d3 from 'd3'

export default {
  name: 'RiskHotspotsView',
  data() {
    return {
      map: null,
      fullData: [],
      countiesGeoJSON: null,
      statesGeoJSON: null,
      selectedCounty: null,
      showOutlines: false,
      highDisparityStateFIPS: ['11', '34', '12', '49', '56', '02', '32'],
      stateNames: {
        AL: "Alabama", AK: "Alaska", AZ: "Arizona", AR: "Arkansas", CA: "California",
        CO: "Colorado", CT: "Connecticut", DE: "Delaware", FL: "Florida", GA: "Georgia",
        HI: "Hawaii", ID: "Idaho", IL: "Illinois", IN: "Indiana", IA: "Iowa",
        KS: "Kansas", KY: "Kentucky", LA: "Louisiana", ME: "Maine", MD: "Maryland",
        MA: "Massachusetts", MI: "Michigan", MN: "Minnesota", MS: "Mississippi", MO: "Missouri",
        MT: "Montana", NE: "Nebraska", NV: "Nevada", NH: "New Hampshire", NJ: "New Jersey",
        NM: "New Mexico", NY: "New York", NC: "North Carolina", ND: "North Dakota", OH: "Ohio",
        OK: "Oklahoma", OR: "Oregon", PA: "Pennsylvania", RI: "Rhode Island", SC: "South Carolina",
        SD: "South Dakota", TN: "Tennessee", TX: "Texas", UT: "Utah", VT: "Vermont",
        VA: "Virginia", WA: "Washington", WV: "West Virginia", WI: "Wisconsin", WY: "Wyoming",
        DC: "District of Columbia"
      }
    }
  },
  async mounted() {
    mapboxgl.accessToken = process.env.VUE_APP_MAPBOX_TOKEN
    const [csv, counties, states] = await Promise.all([
      d3.csv('data/cleaned/dementia_mismatch_index.csv'),
      d3.json('data/cleaned/counties.json'),
      d3.json('data/cleaned/states.json')
    ])
    this.fullData = csv
    this.countiesGeoJSON = counties
    this.statesGeoJSON = states
    this.initMap()
  },
  watch: {
    showOutlines(val) {
      if (this.map && this.map.getLayer('outline-layer')) {
        this.map.setLayoutProperty('outline-layer', 'visibility', val ? 'visible' : 'none')
      }
    }
  },
  methods: {
    initMap() {
      this.map = new mapboxgl.Map({
        container: this.$refs.mapContainer,
        style: 'mapbox://styles/mapbox/light-v10',
        center: [-98, 39],
        zoom: 3.8
      })

      this.map.on('load', () => {
        this.map.addSource('counties', { type: 'geojson', data: this.countiesGeoJSON })
        this.map.addLayer({
          id: 'mismatch-layer',
          type: 'fill',
          source: 'counties',
          paint: {
            'fill-color': [
              'interpolate', ['linear'], ['get', 'value'],
              -0.15, '#1a9641',
              0, '#ffffbf',
              0.10, '#d7191c'
            ],
            'fill-opacity': 0.9,
            'fill-outline-color': '#999'
          }
        })

        this.map.addSource('state-outlines', { type: 'geojson', data: this.statesGeoJSON })
        this.map.addLayer({
          id: 'outline-layer',
          type: 'line',
          source: 'state-outlines',
          paint: {
            'line-color': '#d7191c',
            'line-width': [
              'interpolate', ['linear'], ['zoom'],
              3, 1,
              8, 4
            ]
          },
          filter: ['in', 'STATE', ...this.highDisparityStateFIPS],
          layout: {
            visibility: this.showOutlines ? 'visible' : 'none'
          }
        })

        const popup = new mapboxgl.Popup({ closeButton: false, closeOnClick: false })

        this.map.on('mousemove', 'mismatch-layer', e => {
          const f = e.features[0]
          const fips = f.properties.STATE.padStart(2, '0') + f.properties.COUNTY.padStart(3, '0')
          const record = this.fullData.find(d => d.FIPS === fips)
          if (record) {
            const stateAvg = this.getStateAverages(record.StateAbbr)
            popup.setLngLat(e.lngLat).setHTML(`
              <div style="font-size: ${Math.max(12, Math.min(18, this.map.getZoom() * 2))}px">
                <strong>${this.stateNames[record.StateAbbr]}</strong><br/>
                Avg Mismatch Index: ${(stateAvg.mismatch_index * 100).toFixed(2)}%<br/>
                Dementia: ${(stateAvg.prevalence_rate * 100).toFixed(2)}%<br/>
                Stroke: ${stateAvg.stroke}%<br/>
                Diabetes: ${stateAvg.diabetes}%<br/>
                Cognitive Disability: ${stateAvg.cog_disability}%
              </div>
            `).addTo(this.map)
          }
        })

        this.map.on('mouseleave', 'mismatch-layer', () => popup.remove())

        this.map.on('click', 'mismatch-layer', e => {
          const f = e.features[0]
          const fips = f.properties.STATE.padStart(2, '0') + f.properties.COUNTY.padStart(3, '0')
          this.selectedCounty = this.fullData.find(d => d.FIPS === fips) || null
        })

        this.updateMap()
      })
    },
    getStateAverages(stateAbbr) {
      const records = this.fullData.filter(d => d.StateAbbr === stateAbbr)
      const average = key => (records.length ? (records.reduce((sum, d) => sum + (+d[key] || 0), 0) / records.length) : 0).toFixed(4)
      return {
        mismatch_index: +average('mismatch_index'),
        prevalence_rate: +average('prevalence_rate'),
        stroke: +average('stroke'),
        diabetes: +average('diabetes'),
        cog_disability: +average('cog_disability')
      }
    },
    updateMap() {
      const dataMap = {}
      this.fullData.forEach(d => { dataMap[d.FIPS] = d })

      const updatedGeo = JSON.parse(JSON.stringify(this.countiesGeoJSON))
      updatedGeo.features.forEach(f => {
        const fips = f.properties.STATE.padStart(2, '0') + f.properties.COUNTY.padStart(3, '0')
        const record = dataMap[fips]
        f.properties.value = record ? parseFloat(record.mismatch_index) || 0 : 0
      })

      const source = this.map.getSource('counties')
      if (source) source.setData(updatedGeo)
    }
  }
}
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 80vh;
}
.explanation {
  padding: 1rem;
  background: #f8f8f8;
}
.explanation details summary {
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1rem;
}
.info-panel {
  padding: 1rem;
  background: #fff;
  border-top: 2px solid #ccc;
}
.legend {
  padding: 1rem;
  background: #f1f1f1;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.legend-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0.5rem 0;
}

.gradient-bar {
  flex: 1;
  height: 12px;
  background: linear-gradient(to right, #1a9641, #ffffbf, #d7191c);
  border: 1px solid #ccc;
  border-radius: 4px;
  animation: fadeInGradient 2s ease;
}

.legend-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.green-text { color: #1a9641; }
.yellow-text { color: #c4a000; }
.red-text { color: #d7191c; }

@keyframes fadeInGradient {
  0% { opacity: 0; transform: scaleX(0); transform-origin: left; }
  100% { opacity: 1; transform: scaleX(1); }
}

.info-panel {
  position: fixed;
  top: 120px;
  right: 20px;
  width: 300px;
  background: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  padding: 1.2rem 1.5rem 1rem;
  border-radius: 10px;
  z-index: 10;
  max-height: 75vh;
  overflow-y: auto;
  animation: fadeInSlide 0.5s ease;
}

@keyframes fadeInSlide {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

/* ✖ Close button */
.close-button {
  position: absolute;
  top: 10px;
  right: 12px;
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #666;
}
.close-button:hover {
  color: #d7191c;
}

/* Transition when opening/closing side panel */
.slide-fade-enter-active {
  transition: all 0.4s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
