<script setup lang="js">
import { RouterLink, RouterView } from 'vue-router'
import steps from './components/steps.vue'
import { ref } from 'vue'

const step = ref(1)

const next = () => {
  step.value += 1;
  if (step.value > 4) {
    step.value = 1;
  }
};

const previous = () => {
  step.value -= 1;
  if (step.value < 0) {
    step.value = 0;
  }
};

</script>

<template>
  <el-container>
    <el-header>
      <div></div>
      <div class="steps">
        <steps :activate="step"/>
      </div>
    </el-header>
    <el-main>
      <RouterView @previous-page="previous" @next-page="next" />
    </el-main>
  </el-container>
</template>

<style scoped>

</style>
