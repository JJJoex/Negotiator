<template>
  <el-steps :active="activeStep" align-center finish-status="success">
    <el-step title="欢迎页面"/>
    <el-step title="准备阶段"/>
    <el-step title="谈判阶段"/>
    <el-step title="查看结果"/>
  </el-steps>
</template>

<script>
export default {
  name: 'Steps',
  computed: {
    // 根据当前路径动态计算激活的步骤
    activeStep() {
      const stepMap = {
        '/description': 0,
        '/preparation': 1,
        '/negotiation': 2,
        '/finish': 4,
      };
      return stepMap[this.$route.path] || 0;
    },
  },
};
</script>

<style scoped>
el-steps {
  width: 100%;
  height: 100%;
}
el-step {
  font-weight: bold;
}
</style>