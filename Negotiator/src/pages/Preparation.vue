<script setup lang="js">
import { RouterLink } from 'vue-router';
import { onMounted, ref } from 'vue';
import { ArrowLeftBold, ArrowRightBold } from '@element-plus/icons-vue';
import domainsData from './specific_contents/domains_n_descriptions.json';
import Preparation1NegoSettings from './Preparation_1_nego_settings.vue'; // 引入新组件

const activeName = ref('first');
</script>

<template>
  <div style="border: 1px solid black; display: flex; align-items: flex-start;">
    <el-tabs v-model="activeName" class="demo-tabs">
      <el-tab-pane label="谈判设置" name="first">
        <Preparation1NegoSettings :domainsData="domainsData" /> <!-- 使用新组件 -->
      </el-tab-pane>
      <el-tab-pane label="My Interests" name="second">My Interests</el-tab-pane>
      <el-tab-pane label="My Issues" name="third">My Issues</el-tab-pane>
      <el-tab-pane label="Opponent's Interests" name="fourth">Opponent's Interests</el-tab-pane>
      <el-tab-pane label="Opponent's Issues" name="fifth">Opponent's Issues</el-tab-pane>
    </el-tabs>
  </div>

  <div style="border: 1px solid black">
    <RouterLink to="/description" @click="$emit('previousPage')">
      <el-icon>
        <ArrowLeftBold />
      </el-icon>
      <span>Back to Introduction</span>
    </RouterLink>
    <RouterLink to="/negotiation" @click="$emit('nextPage')">
      <el-icon>
        <ArrowRightBold />
      </el-icon>
      <span>Start Negotiation</span>
    </RouterLink>
  </div>
</template>
