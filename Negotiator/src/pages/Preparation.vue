<script setup lang="js">
import { RouterLink } from 'vue-router';
import { onMounted, ref } from 'vue';
import { ArrowLeftBold, ArrowRightBold } from '@element-plus/icons-vue';
import domainsData from './specific_contents/domains_n_descriptions.json';

import Preparation1NegoSettings from './Preparation_1_nego_settings.vue'; 
import Preparation2MyInterests from './Preparation_2_my_interests.vue'; 

const activeName = ref('first');


// 用来接收子组件的数据
const nego_settings_data = ref(null);

// 处理子组件传回的数据
const handleDataFromNegoSettings = (data) => {
  nego_settings_data.value = data;
  console.log('Received data from page nego_settings:', nego_settings_data.value);
  activeName.value='second';
};


</script>

<template>
  <div style="border: 1px solid black; display: flex; align-items: flex-start;">
    <el-tabs v-model="activeName" class="demo-tabs">
      <el-tab-pane label="谈判设置" name="first">
        <Preparation1NegoSettings :domainsData="domainsData" @submit-data="handleDataFromNegoSettings" /> 
      </el-tab-pane>

      <el-tab-pane label="我的兴趣" name="second">
        <Preparation2MyInterests :nego_settings_data="nego_settings_data" /> 
      </el-tab-pane>
      <el-tab-pane label="我的议题" name="third">My Issues</el-tab-pane>
      <el-tab-pane label="对手的兴趣" name="fourth">Opponent's Interests</el-tab-pane>
      <el-tab-pane label="对手的议题" name="fifth">Opponent's Issues</el-tab-pane>
    </el-tabs>
  </div>

  <div style="border: 1px solid black">
    <RouterLink to="/description" @click="$emit('previousPage')">
      <el-icon>
        <ArrowLeftBold />
      </el-icon>
      <span>Back to Introduction</span>
    </RouterLink>

    <!-- 控制 "Start Negotiation" 链接的禁用状态 -->
    <RouterLink 
      v-if="activeName === 'fifth'" 
      to="/negotiation" 
      @click="$emit('nextPage')"
      :class="{ 'disabled-link': activeName !== 'fifth' }"
    >
      <el-icon>
        <ArrowRightBold />
      </el-icon>
      <span>Start Negotiation</span>
    </RouterLink>
  </div>
</template>

<style scoped>
/* 禁用链接的样式 */
.disabled-link {
  pointer-events: none; /* 禁止点击 */
  opacity: 1; /* 调低透明度 */
}
</style>
