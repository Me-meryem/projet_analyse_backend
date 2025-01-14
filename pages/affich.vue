<template>
  <div>
    <Headerr />
  </div>
  <div class="main-container">
    <!-- Menu -->
    <Menu class="menu" />

    <!-- Contenu principal -->
    <div class="content">

      <div v-if="error" class="error">{{ error }}</div>

      <!-- Tableau des données avec un indicateur de chargement -->
      <el-table
        v-loading="loading"
        :data="previewData"
        style="width: 100%"
        element-loading-text="Chargement des données..."
        class="custom-table"
      >
        <el-table-column
          v-for="(header, index) in Object.keys(previewData[0] || {})"
          :key="index"
          :label="header"
          :prop="header"
        />
      </el-table>
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
      previewData: [], // Données à afficher dans le tableau
      error: null, // Erreur si quelque chose ne va pas
      loading: true, // Indicateur de chargement
    };
  },
  async mounted() {
    // Récupérer l'ID du fichier depuis localStorage
    let fileId = localStorage.getItem("fileId");
    console.log("File ID from localStorage:", fileId); // Log pour débogage

    // Vérifier si un ID de fichier est disponible
    if (!fileId) {
      this.error = "Aucun fichier trouvé dans localStorage.";
      this.loading = false;
      return;
    }

    // Construire l'URL de l'API
    const apiUrl = `http://127.0.0.1:8000/back/files/${fileId}/preview/`;
    console.log("API URL:", apiUrl); // Log pour débogage

    try {
      const response = await fetch(apiUrl);

      // Vérification de la réponse
      if (!response.ok) {
        throw new Error(`Erreur HTTP : ${response.status}`);
      }

      const data = await response.json();

      // Vérifier si les données de prévisualisation sont disponibles
      if (!data.preview || !data.preview.length) {
        this.error = "Aucune donnée à afficher pour ce fichier.";
      } else {
        this.previewData = data.preview;
      }
    } catch (error) {
      this.error = `Erreur lors de la récupération des données : ${error.message}`;
    } finally {
      this.loading = false; // Fin du chargement
    }
  },
};
</script>


<style scoped>
body,
html {
  background-color: #ffffff; /* Fond blanc pour le corps et html */
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

.main-container {
  display: flex;
  min-height: 100vh;
}

.menu {
  flex-shrink: 0;
  width: 200px;
}

.content {
  flex: 1; /* Utilise tout l'espace restant */
  padding: 20px;
}

.error {
  color: red; /* Style pour les messages d'erreur */
  font-size: 1.2em;
}

.custom-table {
  margin-top: 20px;
  background-color: #ffffff; /* Couleur de fond pour toute la table */
}

.el-table__header,
.el-table__body {
  background-color: #ffffff; /* Fond blanc pour l'en-tête et le corps du tableau */
}
</style>
