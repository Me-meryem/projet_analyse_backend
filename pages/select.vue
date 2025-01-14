<template>
  <div>
    <Headerr />
  </div>

  <div class="file-upload">
    <p>Sélectionne un fichier</p>
    <label for="file-input" class="custom-file-label">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 0 0-1.883 2.542l.857 6a2.25 2.25 0 0 0 2.227 1.932H19.05a2.25 2.25 0 0 0 2.227-1.932l.857-6a2.25 2.25 0 0 0-1.883-2.542m-16.5 0V6A2.25 2.25 0 0 1 6 3.75h3.879a1.5 1.5 0 0 1 1.06.44l2.122 2.12a1.5 1.5 0 0 0 1.06.44H18A2.25 2.25 0 0 1 20.25 9v.776" />
      </svg>
      Choisir un fichier
    </label>
    <input type="file" id="file-input" @change="handleFileSelection" accept=".csv" />

    <h2 v-if="selectedFile">
      Fichier sélectionné : <strong>{{ selectedFile.name }}</strong>
    </h2>

    <button @click="analyzeData" :disabled="!selectedFile">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
      </svg>
      Télécharger
    </button>
  </div>
</template>

<script>
import { ElNotification } from 'element-plus';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      selectedFile: null,
      csvData: [], // Données extraites du fichier
      previewData: [], // Aperçu des premières lignes
      csvHeaders: [], // En-têtes du fichier CSV
      loading: false,
      showNavigateButton: false,
    };
  },
  methods: {
    handleFileSelection(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
      }
    },

    analyzeData() {
      if (this.selectedFile) {
        this.loading = true;
        const formData = new FormData();
        formData.append('file', this.selectedFile);

        fetch('http://localhost:8000/back/files/', {
          method: 'POST',
          body: formData,
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Erreur lors de l'envoi du fichier");
            }
            return response.json();
          })
          .then((data) => {
            // Sauvegarder l'ID du fichier dans le localStorage
            localStorage.setItem('fileId', data.id);

            // Notification de succès
            ElNotification({
              title: 'Succès',
              message: 'Le fichier a été téléchargé avec succès !',
              type: 'success',
            });

            // Charger l'aperçu des données
            this.fetchPreview(data.id);

            // Stocker les données dans les propriétés de l'instance
            this.csvHeaders = data.headers;
            this.csvData = data.rows;

            // Redirection vers la page affichage
            this.$router.push({
              name: 'affich',
              params: {
                headers: this.csvHeaders,
                rows: this.csvData,
              },
            });

            // Afficher le bouton pour la navigation
            this.showNavigateButton = true;
          })
          .catch((error) => {
            console.error('Erreur:', error);
            ElNotification({
              title: 'Erreur',
              message: "Une erreur est survenue lors du téléchargement du fichier.",
              type: 'error',
            });
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        ElNotification({
          title: 'Erreur',
          message: 'Veuillez sélectionner un fichier avant de lancer l’analyse.',
          type: 'error',
        });
      }
    },

    fetchPreview(fileId) {
      fetch(`http://localhost:8000/back/files/${fileId}/preview/`, {
        method: 'GET',
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Erreur lors de la récupération de l'aperçu des données");
          }
          return response.json();
        })
        .then((data) => {
          // Mise à jour des données de prévisualisation
          this.previewData = data.preview;

          ElNotification({
            title: 'Aperçu prêt',
            message: 'Les données du fichier ont été prévisualisées avec succès !',
            type: 'success',
          });
        })
        .catch((error) => {
          console.error('Erreur:', error);
          ElNotification({
            title: 'Erreur',
            message: "Une erreur est survenue lors de la récupération de l'aperçu des données.",
            type: 'error',
          });
        });
    },

    navigateToAnalysis() {
      this.$router.push('/analyse'); // Redirection vers la page d'analyse
    },
  },
};
</script>



<style scoped>
body {
  background-color: #f3d4db;
  font-family: 'Poppins', sans-serif;
  color: #fff;
  margin: 0;
  padding: 0;
}

.file-upload {
  max-width: 600px;
  margin: 50px auto;
  text-align: center;
  background-color: rgba(247, 150, 165, 0.8);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

p {
  color: #141212;
  font-size: 1.9em;
  margin: 10px 0;
  font-family: 'Poppins';
}

h2 {
  color: #141212;
  font-size: 1em;
  margin: 10px 0;
  font-family: 'Poppins';
}

input[type="file"] {
  display: none;
}

.custom-file-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #ff70a6;
  color: #080808;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.2s ease;
  display: inline-block;
  margin-top: 10px;
  font-family: 'Poppins';
  text-align: center;
}

button,
.custom-file-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  font-size: 1.1em;
  font-weight: bold;
  font-family: 'Poppins';
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  text-align: center;
}

.custom-file-label {
  background-color: #ff70a6;
  color: #080808;
  margin-top: 10px;
}

button {
  background-color: #f8a9c2;
  color: #7f0a0a;
  border: none;
  margin-top: 20px;
}

button:hover,
.custom-file-label:hover {
  background-color: #d76ba8;
  transform: scale(1.05);
}

button:disabled {
  background-color: #f0d0d6;
  cursor: not-allowed;
}

button svg,
.custom-file-label svg {
  width: 20px;
  height: 20px;
}

button:hover {
  background-color: #d76ba8;
  transform: scale(1.05);
}

button:disabled {
  background-color: #f0d0d6;
  cursor: not-allowed;
}

.analysis-results {
  margin-top: 20px;
  text-align: left;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

table th,
table td {
  border: 1px solid #d76ba8;
  padding: 8px;
  text-align: left;
}

.el-notification__content {
  font-size: 10px;
}
</style>
