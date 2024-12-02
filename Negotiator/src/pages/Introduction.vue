<script setup lang="js">
import { RouterLink } from 'vue-router';
</script>

<template>
    Introduction: Welcome to BotNegotiation Platform
    <RouterLink to="/preparation" @click="$emit('nextPage')"><el-button >Preparation Now</el-button></RouterLink>
</template>