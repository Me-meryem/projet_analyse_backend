<template>
  <div>
    <!-- Bouton pour afficher/masquer le menu -->
    <button 
      class="menu-toggle" 
      @click="toggleMenu"
      style="margin-bottom: 20px; background: none; border: none; cursor: pointer;"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
      </svg>
    </button>

    <!-- Menu -->
    <el-menu
      class="el-menu-vertical-demo menu-colored"
      :collapse="isCollapse"
    >
      <el-menu-item index="1" @click="navigateToSelect">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
        </svg>
        <template #title>Dashboard</template>
      </el-menu-item>

      <el-menu-item index="2" @click="navigateToIndex">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m15.75 15.75-2.489-2.489m0 0a3.375 3.375 0 1 0-4.773-4.773 3.375 3.375 0 0 0 4.774 4.774ZM21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
        </svg>
        <template #title>Indexation</template>
      </el-menu-item>

      <el-menu-item index="3" @click="navigateStati">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 6.878V6a2.25 2.25 0 0 1 2.25-2.25h7.5A2.25 2.25 0 0 1 18 6v.878m-12 0c.235-.083.487-.128.75-.128h10.5c.263 0 .515.045.75.128m-12 0A2.25 2.25 0 0 0 4.5 9v.878m13.5-3A2.25 2.25 0 0 1 19.5 9v.878m0 0a2.246 2.246 0 0 0-.75-.128H5.25c-.263 0-.515.045-.75.128m15 0A2.25 2.25 0 0 1 21 12v6a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 18v-6c0-.98.626-1.813 1.5-2.122" />
        </svg>
        <template #title>Statistiques</template>
      </el-menu-item>

      <el-menu-item index="4" @click="navigateToVisualisation">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
        </svg>
        <template #title>Visualisation</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const isCollapse = ref(true)
const router = useRouter()

// Fonction pour basculer l'état du menu
const toggleMenu = () => {
  isCollapse.value = !isCollapse.value
}

// Fonction pour rediriger vers la page "select"
const navigateToSelect = () => {
  router.push('/select')
}

// Fonction pour rediriger vers la page "index"
const navigateToIndex = () => {
  router.push('/indeex')
}

// Fonction pour rediriger vers la page "index"
const navigateStati = () => {
  router.push('/stati')
}

// Fonction pour rediriger vers la page "index"
const navigateToVisualisation = () => {
  router.push('/visualisation')
}

</script>

<style>
.size-6 {
  width: 24px;
  height: 24px;
}

/* Couleurs personnalisées pour le menu */
.menu-colored {
  background-color: #ffffff; /* Couleur de fond */
  border-radius: 8px;
  padding: 10px;
}

.menu-colored .el-menu-item {
  color: #333; /* Couleur du texte */
}

.menu-colored .el-menu-item:hover {
  background-color: #ffffff; /* Rose plus foncé au survol */
  color: #000; /* Couleur du texte au survol */
}

.menu-colored .el-menu-item.is-active {
  background-color: #ffffff; /* Rose plus foncé pour l'élément actif */
  color: #000; /* Couleur du texte pour l'élément actif */
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
  background-color: #ffffff; /* Fond du menu en rose */
  border-radius: 8px;
}

.el-menu-item {
  border-radius: 4px;
  padding: 10px 15px;
  transition: background-color 0.3s, color 0.3s; /* Animation douce */
}
</style>
