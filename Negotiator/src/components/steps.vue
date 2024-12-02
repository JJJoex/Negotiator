<template>
  <div>
    <!-- 步骤条 -->
    <el-steps :active="activeStep" align-center>
      <el-step title="Description" @click="goToStep('/description')" />
      <el-step title="Preparation" @click="goToStep('/preparation')" />
      <el-step title="Negotiation" @click="goToStep('/negotiation')" />
      <el-step title="Finish" @click="goToStep('/finish')" />
    </el-steps>

    <!-- 渲染当前路由对应的组件 -->
    <div style="margin-top: 20px;">
      <router-view />
    </div>
  </div>
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
        '/finish': 3,
      };
      return stepMap[this.$route.path] || 0;
    },
  },
  methods: {
    // 跳转到指定步骤的路由
    goToStep(path) {
      this.$router.push(path);
    },
  },
};
</script>