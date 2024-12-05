<script setup>
  import { defineProps } from 'vue';
  
  // 接收从父组件传递的参数
  const props = defineProps({
    nego_settings_data: Object,
    my_interests_data: Object,
    my_issues_data: Object,
    op_interests_data: Object,
    op_issues_data: Object
  });
  </script>
  
<template>
    <div>
      <h2>确认页面数据</h2>
      
      <!-- 显示 nego_settings_data -->
      <div>
        <h3>Negotiation Settings (nego_settings_data):</h3>
        <pre>{{ nego_settings_data }}</pre>
      </div>
      
      <!-- 显示 my_interests_data -->
      <div>
        <h3>My Interests (my_interests_data):</h3>
        <pre>{{ my_interests_data }}</pre>
      </div>
      
      <!-- 显示 my_issues_data -->
      <div>
        <h3>My Issues (my_issues_data):</h3>
        <pre>{{ my_issues_data }}</pre>
      </div>
      
      <!-- 显示 op_interests_data -->
      <div>
        <h3>Opponent Interests (op_interests_data):</h3>
        <pre>{{ op_interests_data }}</pre>
      </div>
      
      <!-- 显示 op_issues_data -->
      <div>
        <h3>Opponent Issues (op_issues_data):</h3>
        <pre>{{ op_issues_data }}</pre>
      </div>
    </div>
  </template>
  
  
  
  <style scoped>
  h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  h3 {
    font-size: 18px;
    margin-top: 10px;
  }
  
  pre {
    background-color: #f4f4f4;
    padding: 10px;
    border-radius: 5px;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
  </style>
  