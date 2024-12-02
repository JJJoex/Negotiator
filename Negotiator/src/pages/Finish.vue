<script setup lang="js">
import { RouterLink } from 'vue-router';
import { ArrowRightBold } from '@element-plus/icons-vue';
</script>

<template>
    <div style="border: 1px black solid;">
        Congratulations! You have successfully completed the negotiation process.
    </div>
    <div style="border: 1px black solid;">
        <RouterLink to="/" @click="$emit('nextPage')">
            <el-icon>
                <ArrowRightBold />
            </el-icon>
            <span>Back to Start</span>
        </RouterLink>
    </div>
</template>