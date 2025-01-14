<template>
    <div>
      <Headerindex />
    </div>
  
    <!-- Conteneur principal -->
    <div class="background">
      <!-- Conteneur Flex -->
      <div class="main-container">
        <!-- Menu -->
        <Menu class="menu" />
        
        <!-- Centrage du formulaire -->
        <div class="form-container">
          <div class="form-group">
            <div class="w-full text-center">
              <div class="flex flex-col gap-6 mt-3">
                <!-- Label centré et style -->
                <div class="form-group flex flex-col items-center bg-[#f0d0d6] p-4 rounded-lg">
                  <label for="indexation" class="font-serif text-3xl mb-4 text-black text-center w-full">
                    Indexation :
                  </label>
                  <!-- Champ de saisie pour l'indexation -->
                  <el-input
                    id="indexation"
                    size="large"
                    v-model="userInput"
                    placeholder="Entrez un index de ligne ou un nom de colonne"
                    class="transparent-input mb-6"
                  />
                  <el-button type="primary" size="large" @click="fetchData" class="button-spacing">
                    Afficher les données
                  </el-button>
                </div>
  
                <!-- Afficher les données ou les messages d'erreur -->
                <div v-if="error" style="color: red; margin-top: 10px;">
                  <p>{{ error }}</p>
                </div>
  
                <!-- Tableau des données -->
                <div v-if="data && !error" class="mt-4">
                  <h3>Données récupérées :</h3>
                  <el-table :data="data" style="width: 100%">
                    <el-table-column
                      v-for="(value, index) in Object.keys(data[0] || {})"
                      :key="index"
                      :label="value"
                      :prop="value"
                    ></el-table-column>
                  </el-table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  
  <script setup>
  import { ref } from 'vue';

  // Références pour l'input utilisateur et les données
  const userInput = ref('');
  const data = ref([]);
  const error = ref('');
  
  // Récupérer l'ID du fichier depuis localStorage
  const fileId = localStorage.getItem("fileId");
  console.log("File ID from localStorage:", fileId); // Log pour débogage

  // Vérifier si l'ID du fichier est disponible
  if (!fileId) {
    error.value = "Aucun fichier trouvé dans localStorage.";
  }
  
  // Fonction pour récupérer les données en fonction de l'index ou du nom de colonne
  const fetchData = async () => {
    // Vérifier si l'utilisateur a entré un numéro d'index ou un nom de colonne
    if (!isNaN(Number(userInput.value))) { // Si l'input est un index de ligne
      try {
        const response = await fetch(`http://127.0.0.1:8000/back/files/${fileId}/get_row/${userInput.value}/`);
        const result = await response.json();
        if (response.ok) {
          data.value = [result.row_data]; // Placer la ligne dans un tableau pour ElTable
          error.value = '';
        } else {
          error.value = result.error;
        }
      } catch (err) {
        error.value = 'Erreur lors de la récupération des données';
      }
    } else { // Si l'input est un nom de colonne
      try {
        const response = await fetch(`http://127.0.0.1:8000/back/files/${fileId}/get_column/${userInput.value}/`);
        const result = await response.json();
        if (response.ok) {
          if (result.error) {
            error.value = result.error;  // Affiche l'erreur si la colonne n'est pas trouvée
          } else {
            data.value = result.column_data.map(value => ({ [userInput.value]: value })); // Formater la colonne pour ElTable
            error.value = '';
          }
        } else {
          error.value = result.error;
        }
      } catch (err) {
        error.value = 'Erreur lors de la récupération des données';
      }
    }
  };
</script>


  

  
  <style scoped>
/* Conteneur principal */
.background {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Prend toute la hauteur de la fenêtre */
  width: 100%;
}

/* Conteneur Flex pour aligner le menu et le formulaire */
.main-container {
  display: flex;
  justify-content: space-between; /* Espacement entre les sections */
  align-items: flex-start; /* Alignement en haut */
  width: 90%;
  max-width: 1400px;
}

/* Menu */
.menu {
  flex: 1; /* Le menu occupe 1 part de l'espace */
  max-width: 250px; /* Largeur maximale */
  margin-right: 20px; /* Espace entre le menu et le formulaire */
}

/* Formulaire */
.form-container {
  flex: 3; /* Le formulaire occupe 3 parts de l'espace */
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

.el-input {
  width: 100%;
  padding: 20px;
  font-size: 20px;
  font-family: 'Times New Roman', Times, serif;
}

.el-button {
  width: 100%;
  padding: 25px;
  background-color: #d76ba8;
  color: white;
  border: none;
  border-radius: 60px;
  font-family: 'Times New Roman', Times, serif;
  font-size: 18px;
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
</style>