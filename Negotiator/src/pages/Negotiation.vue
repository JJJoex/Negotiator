<script setup lang="js">
import { RouterLink } from 'vue-router';

</script>

<template>
    <el-container>hello</el-container>
    <RouterLink to="/preparation" @click="$emit('lastPage')"><el-button >Back to Preparation</el-button></RouterLink>
    <RouterLink to="/finish" @click="$emit('nextPage')"><el-button >Get the Result</el-button></RouterLink>
</template>