<script setup>

const props = defineProps({
  activate: Number
})

</script>

<template>
  <el-steps :active="activate" align-center finish-status="success">
    <el-step title="Introduction"  />
    <el-step title="Preparation"  />
    <el-step title="Negotiation"  />
    <el-step title="Finish"  />
  </el-steps>
</template>