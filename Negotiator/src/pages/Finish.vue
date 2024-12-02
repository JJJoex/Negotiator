<script setup lang="js">
import { RouterLink } from 'vue-router';
</script>

<template>
    <div>
        Congratulations! You have successfully completed the negotiation process.
    </div>
    <img />
    <RouterLink to="/" @click="$emit('nextPage')"><el-button >Back to Start</el-button></RouterLink>
</template>