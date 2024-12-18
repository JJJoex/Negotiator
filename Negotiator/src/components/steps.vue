<template>
  <el-steps :active="activeStep" align-center finish-status="success" class="steps-container">
    <el-step title="首页" />
    <el-step title="谈判准备" />
    <el-step title="准备确认" />
    <el-step title="开始谈判" />
    <el-step title="结果详情" />
  </el-steps>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

// 动态获取路由
const route = useRoute();

// 计算激活步骤
const activeStep = computed(() => {
  const stepMap = {
    "/description": 0,
    "/preparation": 1,
    "/ensurement": 2,
    "/negotiation": 3,
    "/finish": 4,
  };
  return stepMap[route.path] || 0;
});
</script>

<style scoped>
.steps-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}

el-step {
  font-weight: bold;
}
</style>