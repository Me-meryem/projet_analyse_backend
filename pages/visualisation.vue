<template>
  <div>
    <Headervisua />
  </div>
  <div class="background">
    <!-- Conteneur principal -->
    <div class="main-container">
      <!-- Menu -->
      <Menu class="menu" />

      <!-- Formulaire -->
      <div class="form-container">
        <div class="form-group">
          <h1 class="font-serif">Consulter les Données</h1>

          <!-- Sélection pour les colonnes -->
          <div class="space-y-4">
            <el-select v-model="selectedColumn" placeholder="Sélectionner une colonne" size="large" filterable>
              <el-option v-for="column in columns" :key="column" :label="column" :value="column" />
            </el-select>
            <el-button type="primary" size="large" @click="fetchColumn">
              Consulter Colonne
            </el-button>

            <!-- Sélection pour les types de graphiques -->
            <el-select v-model="selectedChartType" placeholder="Sélectionner un type de graphique" size="large" class="mt-4">
              <el-option v-for="type in chartTypes" :key="type.value" :label="type.label" :value="type.value" />
            </el-select>
            <el-button type="primary" size="large" @click="fetchChart" class="mt-2">
              Générer Graphique
            </el-button>
          </div>

          <!-- Résultats -->
          <div v-if="result" class="p-4 bg-gray-50 rounded-lg shadow">
            <h2 class="text-lg font-semibold text-gray-600">Résultats :</h2>
            <pre class="text-sm text-gray-800">{{ result }}</pre>
          </div>

          <!-- Graphique -->
          <div v-if="chart" class="p-4 bg-gray-50 rounded-lg shadow mt-4">
            <h2 class="text-lg font-semibold text-gray-600">Graphique :</h2>
            <img :src="'data:image/png;base64,' + chart" alt="Graphique" class="w-full h-auto" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Références pour les données
const columns = ref([]) // Liste des colonnes
const analysis = ref({}) // Résultats de l'analyse des colonnes
const selectedColumn = ref(null) // Colonne sélectionnée
const selectedChartType = ref(null) // Type de graphique sélectionné
const chart = ref(null) // Graphique généré
const result = ref(null) // Résultats de la consultation de la colonne
const loading = ref(true) // Indicateur de chargement
const error = ref(null) // Gestion des erreurs
const chartTypes = ref([
  { label: 'Histogramme', value: 'histogram' },
  { label: 'Barplot', value: 'barplot' },
  { label: 'Scatterplot', value: 'scatterplot' },
  { label: 'Boxplot', value: 'boxplot' },
  { label: 'Violinplot', value: 'violinplot' },
  { label: 'Lineplot', value: 'lineplot' },
  { label: 'Heatmap', value: 'heatmap' },
  { label: 'Countplot', value: 'countplot' },
  { label: 'KDE Plot', value: 'kdeplot' },
])

// ID du fichier (fixe ou récupéré dynamiquement)
const fileId = ref(localStorage.getItem("fileId") || 131)

// Charger et analyser les colonnes
onMounted(async () => {
  try {
    // Analyser les colonnes
    const response = await fetch(`http://127.0.0.1:8000/back/files/${fileId.value}/analyze_columns/`)
    if (!response.ok) {
      throw new Error(`Erreur HTTP : ${response.status}`)
    }
    const data = await response.json()

    // Stocker les colonnes et l'analyse
    columns.value = Object.keys(data.analysis || {})
    analysis.value = data.analysis
    loading.value = false
  } catch (err) {
    error.value = `Erreur lors de l'analyse des colonnes : ${err.message}`
    loading.value = false
  }
})

// Consulter les données d'une colonne spécifique
const fetchColumn = async () => {
  if (!selectedColumn.value) {
    alert('Veuillez sélectionner une colonne.')
    return
  }
  try {
    const response = await fetch(`/back/files/${fileId.value}/consult_column/?column=${selectedColumn.value}`)
    const data = await response.json()
    result.value = data.result || null
  } catch (err) {
    console.error('Erreur lors de la récupération des données de la colonne:', err)
  }
}

// Générer un graphique pour une colonne
const fetchChart = async () => {
  if (!selectedColumn.value || !selectedChartType.value) {
    alert('Veuillez sélectionner une colonne et un type de graphique.')
    return
  }

  try {
    // Vérification des paramètres envoyés
    console.log('Colonne sélectionnée:', selectedColumn.value)
    console.log('Type de graphique sélectionné:', selectedChartType.value)

    const response = await fetch(
      `/back/files/${fileId.value}/plot/?chart_type=${selectedChartType.value}&x=${selectedColumn.value}`
    )
    const data = await response.json()

    // Vérification de la réponse de l'API
    console.log('Réponse de l\'API:', data)

    if (data && data.chart) {
      chart.value = data.chart  // Stocker l'image en base64
    } else {
      console.error('Aucun graphique trouvé dans la réponse')
      alert('Aucun graphique disponible pour cette colonne.')
    }
  } catch (err) {
    console.error('Erreur lors de la récupération du graphique:', err)
    alert(`Une erreur est survenue lors de la génération du graphique: ${err.message || 'Erreur inconnue'}`)
  }
}

</script>


<style scoped>
/* Conteneur principal */
.background {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
}

/* Conteneur Flex pour aligner le menu et le formulaire */
.main-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 90%;
  max-width: 1400px;
}

/* Menu */
.menu {
  flex: 1;
  max-width: 250px;
  margin-right: 20px;
}

/* Formulaire */
.form-container {
  flex: 3;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 1000px;
  padding: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  background-color: #f0d0d6;
  border-radius: 50px;
  padding: 40px;
}

.el-input,
.el-select,
.el-button {
  width: 100%;
}

.el-button {
  background-color: #d76ba8;
  color: white;
  border: none;
  border-radius: 60px;
}

.el-button:hover {
  background-color: #d76ba8;
}

h1 {
  font-size: 30px;
  font-weight: bold;
}

.font-serif {
  font-family: 'Times New Roman', serif;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin-top: 20px;
}
</style>
