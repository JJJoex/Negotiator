<script setup>
import steps from './components/steps.vue'
</script>

<template>
  <el-container>
    <el-header>
      <div>Title</div>
      <div class="steps">
        <steps />
      </div>
    </el-header>
    <el-main>
      
    </el-main>
  </el-container>
</template>

<style scoped>
el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
