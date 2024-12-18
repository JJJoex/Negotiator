<script setup lang="js">
import { ref, watch } from 'vue';
import domainsData from './specific_contents/domains_n_descriptions.json';
import footerComp from '../components/footer.vue'
import Preparation1NegoSettings from './Preparation/Preparation_1_nego_settings.vue';
import Preparation2MyInterests from './Preparation/Preparation_2_my_interests.vue';
import Preparation3MyIssues from './Preparation/Preparation_3_my_issues.vue';
import Preparation4OpInterests from './Preparation/Preparation_4_op_interests.vue';
import Preparation5OpIssues from './Preparation/Preparation_5_op_issues.vue';
import Preparation6Ensure from './Preparation/Preparation_6_ensure.vue';

import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const activeName = ref('first');


// 用来接收子组件的数据
const nego_settings_data = ref(null);
const my_interests_data = ref(null);
const my_issues_data = ref(null);

const op_interests_data = ref(null);
const op_issues_data = ref(null);

const handleDataFromNegoSettings = (data) => {
  nego_settings_data.value = data;
  // console.log('Received data from page 1 nego_settings:', nego_settings_data.value);
  activeName.value = 'second';

};

const handleDataFromMyInterests = (data) => {
  my_interests_data.value = data;
  console.log('Received data from page 2 my interests:', my_interests_data.value);
  activeName.value = 'third';
};

const handleDataFromMyIssues = (data) => {
  my_issues_data.value = data;
  console.log('Received data from page 3 my issues:', my_issues_data.value);
  activeName.value = 'fourth';
};


const handleDataFromOpInterests = (data) => {
  op_interests_data.value = data;
  console.log('Received data from page 4 op interests:', op_interests_data.value);
  activeName.value = 'fifth';
};

const handleDataFromOpIssues = (data) => {
  op_issues_data.value = data;
  console.log('Received data from page 5 op issues:', op_issues_data.value);
  activeName.value = 'sixth';
  updateDataToStore();
  console.log("子页面Preparation.vue 提交数据到App.vue成功");
};


// 获取 Vuex store 实例
const store = useStore();

// 提交数据到 Vuex 的方法
const updateDataToStore = () => {
  store.commit('setNegoSettingsData', nego_settings_data.value);
  store.commit('setMyInterestsData', my_interests_data.value);
  store.commit('setMyIssuesData', my_issues_data.value);
  store.commit('setOpInterestsData', op_interests_data.value);
  store.commit('setOpIssuesData', op_issues_data.value);
};

const router = useRouter();
const goToIntroduction = () => {
  router.push("/introduction")
}
const goToNegotiation = () => {
  router.push("/negotiation")
}
const goToPage1 = () => {activeName.value = 'first'}
const goToPage2 = () => {activeName.value = 'second'}
const goToPage3 = () => {activeName.value = 'third'}
const goToPage4 = () => {activeName.value = 'fourth'}
const goToPage5 = () => {activeName.value = 'fifth'}


</script>

<template>
  <div class='preparation' style=" display: flex; align-items: flex-start;">
    <el-tabs v-model="activeName" class="demo-tabs">
      <el-tab-pane label="谈判设置" name="first" :disabled="true" ref="firstTab">
        <Preparation1NegoSettings :domainsData="domainsData" @nextPage="handleDataFromNegoSettings" @previousPage="goToIntroduction"/>
      </el-tab-pane>

      <el-tab-pane label="我方兴趣" name="second" :disabled="true" ref="secondTab">
        <Preparation2MyInterests :nego_settings_data="nego_settings_data" @nextPage="handleDataFromMyInterests" @previousPage="goToPage1"/>
      </el-tab-pane>
      <el-tab-pane label="我方议题" name="third" :disabled="true" ref="thirdTab">
        <Preparation3MyIssues :my_interests_data="my_interests_data" :nego_settings_data="nego_settings_data"
          :key="my_interests_data" @nextPage="handleDataFromMyIssues" @previousPage="goToPage2" />
      </el-tab-pane>
      <el-tab-pane label="对方兴趣" name="fourth" :disabled="true" ref="fourthTab">
        <Preparation4OpInterests :nego_settings_data="nego_settings_data" @nextPage="handleDataFromOpInterests" @previousPage="goToPage3" />
      </el-tab-pane>
      <el-tab-pane label="对方议题" name="fifth" :disabled="true" ref="fifthTab">
        <Preparation5OpIssues :my_interests_data="my_interests_data" :nego_settings_data="nego_settings_data"
          :op_interests_data="op_interests_data" :key="op_interests_data" @nextPage="handleDataFromOpIssues" @previousPage="goToPage4" />

      </el-tab-pane>
      <!-- <el-tab-pane label="谈判确认" name="sixth" :disabled="true" ref="sixthTab">
        <Preparation6Ensure :nego_settings_data="nego_settings_data" :my_interests_data="my_interests_data"
          :my_issues_data="my_issues_data" :op_interests_data="op_interests_data" :op_issues_data="op_issues_data" @nextPage="goToNegotiation"  @previousPage="goToPage5"/>
      </el-tab-pane> -->
    </el-tabs>

  </div>
</template>

<style scoped>
.demo-tabs {
  width: 100%;
  /* height: 100%; */
  /* overflow: auto; */
}

.demo-tabs .el-tabs__content {
  width: 100%;
  display: flex;
  justify-content: center;
  /* 如果需要垂直居中内容 */
}

.demo-tabs .el-tab-pane {
  width: 100%;
  display: block;
}

.preparation {
  display: flex;
  align-items: flex-start;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

/* 禁用链接的样式 */
.disabled-link {
  pointer-events: none;
  /* 禁止点击 */
  opacity: 1;
  /* 调低透明度 */
}
</style>
