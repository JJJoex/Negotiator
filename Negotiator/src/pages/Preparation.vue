<script setup lang="js">
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import { ArrowLeftBold, ArrowRightBold } from '@element-plus/icons-vue';
const activeName = ref('first');

</script>

<template>
  <div style='border: 1px solid black'>
    <el-tabs v-model="activeName" class="demo-tabs">
      <el-tab-pane label="Negotiation Settings" name="first">Negotiation Settings</el-tab-pane>
      <el-tab-pane label="My Interests" name="second">My Interests</el-tab-pane>
      <el-tab-pane label="My Issues" name="third">My Issues</el-tab-pane>
      <el-tab-pane label="Opponent's Interests" name="fourth">Opponent's Interests</el-tab-pane>
      <el-tab-pane label="Opponent's Issues" name="fifth">Opponent's Issues</el-tab-pane>
    </el-tabs>
  </div>
  <div style='border: 1px solid black'>
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

<style>
.demo-tabs>.el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.demo-tabs .custom-tabs-label .el-icon {
  vertical-align: middle;
}

.demo-tabs .custom-tabs-label span {
  vertical-align: middle;
  margin-left: 4px;
}
</style>