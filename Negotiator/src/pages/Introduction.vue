<script setup lang="js">
import { RouterLink } from 'vue-router';
import { ArrowRightBold } from '@element-plus/icons-vue';
</script>

<template>
    <div style="border: 1px black solid;">
        Introduction: Welcome to BotNegotiation Platform
    </div>
    <div style="border: 1px solid black;">
    <RouterLink to="/preparation" @click="$emit('nextPage')">
        <el-icon><ArrowRightBold /></el-icon>
        <span>Preparation Now</span>
    </RouterLink>
    </div>
</template>