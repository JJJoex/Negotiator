<script setup lang="js">
import { RouterLink } from 'vue-router';
import { onMounted, ref } from 'vue';
import { ArrowLeftBold, ArrowRightBold } from '@element-plus/icons-vue';
import domainsData from './specific_contents/domains_n_descriptions.json';

import Preparation1NegoSettings from './Preparation/Preparation_1_nego_settings.vue'; 
import Preparation2MyInterests from './Preparation/Preparation_2_my_interests.vue'; 
import Preparation3MyIssues from './Preparation/Preparation_3_my_issues.vue'; 

import Preparation4OpInterests from './Preparation/Preparation_4_op_interests.vue'; 
import Preparation5OpIssues from './Preparation/Preparation_5_op_issues.vue'; 

import Preparation6Ensure from './Preparation/Preparation_6_ensure.vue'; 

import { useStore } from 'vuex';

const activeName = ref('first');


// 用来接收子组件的数据
const nego_settings_data = ref(null);
const my_interests_data = ref(null);
const my_issues_data = ref(null);

const op_interests_data = ref(null);
const op_issues_data = ref(null);

const handleDataFromNegoSettings = (data) => {
  nego_settings_data.value = data;
  console.log('Received data from page 1 nego_settings:', nego_settings_data.value);
  activeName.value='second';
};

const handleDataFromMyInterests = (data) => {
  my_interests_data.value = data;
  console.log('Received data from page 2 my interests:', my_interests_data.value);
  activeName.value='third';
};

const handleDataFromMyIssues = (data) => {
  my_issues_data.value = data;
  console.log('Received data from page 3 my issues:', my_issues_data.value);
  activeName.value='fourth';
};


const handleDataFromOpInterests = (data) => {
  op_interests_data.value = data;
  console.log('Received data from page 4 op interests:', op_interests_data.value);
  activeName.value='fifth';
};

const handleDataFromOpIssues = (data) => {
  op_issues_data.value = data;
  console.log('Received data from page 5 op issues:', op_issues_data.value);
  activeName.value='sixth';
  updateDataToStore();
  console.log("子页面Preparation.vue 提交数据到App.vue成功");
};


// 获取 Vuex store 实例
const store = useStore();

// 提交数据到 Vuex 的方法
const updateDataToStore = () => {

  console.log('Submitting to Vuex:');
  console.log('Nego Settings:', nego_settings_data.value);
  console.log('My Interests:', my_interests_data.value);
  console.log('My Issues:', my_issues_data.value);
  console.log('Op Interests:', op_interests_data.value);
  console.log('Op Issues:', op_issues_data.value);
  
  store.commit('setNegoSettingsData', nego_settings_data.value);
  store.commit('setMyInterestsData', my_interests_data.value);
  store.commit('setMyIssuesData', my_issues_data.value);
  store.commit('setOpInterestsData', op_interests_data.value);
  store.commit('setOpIssuesData', op_issues_data.value);
};

</script>



<!-- <script>
import { useStore } from 'vuex';

export default {
  data() {
    return {
      nego_settings_data: 'some value',
      my_interests_data: 'some value',
      my_issues_data: 'some value',
      op_interests_data: 'some value',
      op_issues_data: 'some value'
    };
  },
  methods: {
    updateData() {
      const store = useStore();
      store.commit('setNegoSettingsData', this.nego_settings_data);
      store.commit('setMyInterestsData', this.my_interests_data);
      store.commit('setMyIssuesData', this.my_issues_data);
      store.commit('setOpInterestsData', this.op_interests_data);
      store.commit('setOpIssuesData', this.op_issues_data);
    }
  }
};
</script> -->

<template>
  <div style=" display: flex; align-items: flex-start;">
    <el-tabs v-model="activeName" class="demo-tabs">
      <el-tab-pane label="谈判设置" name="first" :disabled="true">
        <Preparation1NegoSettings :domainsData="domainsData" @submit-data="handleDataFromNegoSettings" /> 
      </el-tab-pane>

      <el-tab-pane label="我的兴趣" name="second" :disabled="true">
        <Preparation2MyInterests :nego_settings_data="nego_settings_data" @submit-data="handleDataFromMyInterests"/> 
      </el-tab-pane>
      <el-tab-pane label="我的议题" name="third" :disabled="true">
        <Preparation3MyIssues :my_interests_data="my_interests_data" :nego_settings_data="nego_settings_data" :key="my_interests_data" 
                                                                                              @submit-data="handleDataFromMyIssues" /> 
      </el-tab-pane>
      
      <el-tab-pane label="对手的兴趣" name="fourth" :disabled="true">
        <Preparation4OpInterests :nego_settings_data="nego_settings_data" @submit-data="handleDataFromOpInterests"/> 
      </el-tab-pane>
      <el-tab-pane label="对手的议题" name="fifth" :disabled="true">
        <Preparation5OpIssues :my_interests_data="my_interests_data" :nego_settings_data="nego_settings_data" :op_interests_data="op_interests_data" :key="op_interests_data" 
                                                                                              @submit-data="handleDataFromOpIssues" /> 

      </el-tab-pane>
      <el-tab-pane label="确认" name="sixth" :disabled="true">
        
        <Preparation6Ensure   :nego_settings_data="nego_settings_data" 
                              :my_interests_data="my_interests_data"
                              :my_issues_data="my_issues_data"
                              :op_interests_data="op_interests_data"
                              :op_issues_data="op_issues_data"
        
        /> 
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
/* 禁用链接的样式 */
.disabled-link {
  pointer-events: none; /* 禁止点击 */
  opacity: 1; /* 调低透明度 */
}
</style>
