<template>
  <div>
    <Headerstati />
  </div>
  <div class="main-container">
    <!-- Menu -->
    <Menu class="menu" />

    <!-- Contenu principal -->
    <div class="dashboard background">
      <div class="form-container">
        <div class="form-group">
          <div class="column-selector">
            <button @click="analyzeAllColumns" class="el-button">Analyser Toutes les Colonnes</button>
          </div>

          <div v-if="analysis && Object.keys(analysis).length > 0" class="stats-table-container">
            <table class="stats-table">
              <thead>
                <tr>
                  <th>Colonne</th>
                  <th>Type</th>
                  <th>Moyenne</th>
                  <th>Médiane</th>
                  <th>Minimum</th>
                  <th>Maximum</th>
                  <th>Écart-type</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(stats, column) in analysis" :key="column">
                  <td>{{ column }}</td>
                  <td>{{ stats.type === 'numeric' ? 'Numérique' : 'Catégoriel' }}</td>
                  <td>{{ stats.type === 'numeric' ? stats.mean : 'N/A' }}</td>
                  <td>{{ stats.type === 'numeric' ? stats.median : 'N/A' }}</td>
                  <td>{{ stats.type === 'numeric' ? stats.min : 'N/A' }}</td>
                  <td>{{ stats.type === 'numeric' ? stats.max : 'N/A' }}</td>
                  <td>{{ stats.type === 'numeric' ? stats.stddev : 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p v-else>Aucune analyse disponible. Veuillez cliquer sur le bouton pour analyser les colonnes.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ElTable, ElTableColumn } from 'element-plus';

export default {
  components: {
    ElTable,
    ElTableColumn,
  },
  data() {
    return {
      analysis: {},     // Résultats de l'analyse des colonnes
      error: null,      // Erreur si quelque chose ne va pas
      loading: true,    // Indicateur de chargement
    };
  },
  methods: {
    // Fonction pour analyser toutes les colonnes et calculer les statistiques
    async analyzeAllColumns() {
      const fileId = localStorage.getItem("fileId");

      if (!fileId) {
        this.error = "Aucun fichier trouvé dans localStorage.";
        this.loading = false;
        return;
      }

      // Appel à l'API pour analyser les colonnes
      const apiUrl = `http://127.0.0.1:8000/back/files/${fileId}/analyze_columns/`;
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`Erreur HTTP : ${response.status}`);
        }

        const data = await response.json();
        this.analysis = data.analysis;
        this.loading = false;
      } catch (error) {
        this.error = `Erreur lors de l'analyse des colonnes : ${error.message}`;
        this.loading = false;
      }
    },
  },
};
</script>



<style scoped>
.main-container {
  display: flex;
  min-height: 100vh; /* Assure que le contenu prend toute la hauteur de la fenêtre */
}

.menu {
  flex-shrink: 0;
  width: 200px;
  background-color: #ffffff; /* Couleur de fond pour le menu */
}

.dashboard {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.form-container {
  width: 100%;
  max-width: 600px;
}

.form-group {
  background-color: #f0d0d6;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.el-button {
  margin-top: 20px;
  padding: 15px;
  background-color: #d76ba8;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.el-button:hover {
  background-color: #bf5e96;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
}

.stats-table th, .stats-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.stats-table th {
  background-color: #a92a89;
}

.stats-table td {
  background-color: #fff;
}
</style>
