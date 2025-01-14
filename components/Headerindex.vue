<template>
    <div class="header flex bg-black w-full items-center px-4">
        <!-- Centered Header Text -->
        <div class="header-title text-white text-xl font-bold mx-auto">
            <h1>Indexation des lignes et colonnes</h1>
        </div>

        <!-- Header Image (Moved to the right) -->
        <div class="header-image">
            <img src="/images/image header.png" alt="Header Image" class="rounded-lg w-24 h-16 object-cover" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const onLogout = (): void => {
    router.push('/login');
};
</script>

<style scoped>
.header {
    width: 100%;
    box-sizing: border-box;
    height: 70px;
    display: flex;
    align-items: center;
    position: relative;
}

.header-title {
    text-align: center;
    flex-grow: 1; /* Allows the text to occupy central space */
}

.header-image {
    position: absolute;
    right: 20px; /* Fixes the image to the far right */
}

.header-image img {
    transition: transform 0.3s ease;
    border-radius: 8px;
}

h1 {
  margin-bottom: 20px;
  font-size: 2.5em;
  font-weight: bold;
  color: #d76ba8;
  font-family: 'Poppins';
}

.header-image img:hover {
    transform: scale(1.05);
}
</style>
