<!-- 
    @author: wrk
-->
<!-- 
    需求：
        page 1: 谈判域，我方角色，对方角色，bidding轮数（正整数）
            选中一个谈判域的时候，要显示相关的介绍
-->

<template>
  <div class="preparation">
    <h2>Preparation Step</h2>
    <!-- 使用 Element Plus 的 Tabs 组件 -->
    <el-tabs type="border-card">
      <el-tab-pane label="page1">
        <p>This is the content of page 1.</p>
      </el-tab-pane>
      <el-tab-pane label="page2">
        <p>This is the content of page 2.</p>
      </el-tab-pane>
      <el-tab-pane label="page3">
        <p>This is the content of page 3.</p>
      </el-tab-pane>
      <el-tab-pane label="page4">
        <p>This is the content of page 4.</p>
      </el-tab-pane>
      <el-tab-pane label="page5">
        <p>This is the content of page 5.</p>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: 'Preparation',
};
</script>

<style scoped>
/* 样式适配 */
.preparation {
  padding: 20px;
}
</style>
