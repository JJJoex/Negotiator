<script setup lang="js">
import { ref, reactive, watch } from 'vue';
import steps from './components/steps.vue'
import { useRouter, useRoute, RouterView } from 'vue-router';

import { useStore } from 'vuex';

import { sendJson } from './pages/SendMessage';

const router = useRouter();
const route = useRoute();


// 自动获取最大的小数位数
const getPrecision = (num) => {
  const str = num.toString();
  const dotIndex = str.indexOf('.');
  return dotIndex === -1 ? 0 : str.length - dotIndex - 1;
};



// 获取 Vuex store 实例
const store = useStore();


const goToNext = () => {
  if (route.path === '/description') {
    router.push('/preparation');
    showPrevious.value = true;
    nextPage.value = '开始谈判';
    previousPage.value = '欢迎页面';
  }
  else if (route.path === '/preparation') {
    router.push('/negotiation');
    showPrevious.value = true;
    nextPage.value = '查看结果';
    previousPage.value = '准备阶段';

    // 用函数传参
    console.log('App.vue中, Nego Settings:', store.state.nego_settings_data);
    console.log('App.vue中, My Interests:', store.state.my_interests_data);
    console.log('App.vue中, My Issues:', store.state.my_issues_data);
    console.log('App.vue中, Op Interests:', store.state.op_interests_data);
    console.log('App.vue中, Op Issues:', store.state.op_issues_data);
    // console.log(store.state.nego_settings_data['whoFirst'],store.state.nego_settings_data['whoFirst']==="1");



    const my_intr = Object.values(store.state.my_interests_data).map(value => {
      const precision = getPrecision(value);
      return parseFloat(value.toFixed(precision)); // 保留原始精度
    });

    const op_intr = Object.values(store.state.op_interests_data).map(value => {
      const precision = getPrecision(value);
      return parseFloat(value.toFixed(precision)); // 保留原始精度
    });

    console.log(my_intr, op_intr);


    const my_issues = Object.values(store.state.my_issues_data).map(category => Object.values(category));
    const op_issues = Object.values(store.state.op_issues_data).map(category => Object.values(category));

    console.log(my_issues, op_issues);






    const data_to_send = {
      Domain: store.state.nego_settings_data["Domain"],
      Rounds: store.state.nego_settings_data["BiddingRounds"],
      Times: store.state.nego_settings_data["BiddingTime"],
      First: store.state.nego_settings_data['whoFirst'] === "1" ? true : false,
      Profile: {
        my: [
          store.state.nego_settings_data['settingValues']['my']["value1"],
          store.state.nego_settings_data['settingValues']['my']["value2"],
          store.state.nego_settings_data['settingValues']['my']["value3"],
          store.state.nego_settings_data['settingValues']['my']["value4"],
          store.state.nego_settings_data['settingValues']['my']["value5"]
        ],
        op: [
          store.state.nego_settings_data['settingValues']['op']["value1"],
          store.state.nego_settings_data['settingValues']['op']["value2"],
          store.state.nego_settings_data['settingValues']['op']["value3"],
          store.state.nego_settings_data['settingValues']['op']["value4"],
          store.state.nego_settings_data['settingValues']['op']["value5"]
        ]
      },
      Role: store.state.nego_settings_data['roles']['my'],

      MyInterests: my_intr,
      MyIssues: my_issues,
      OpInterests: op_intr,
      OpIssues: op_issues



    }

    console.log('App.vue中, data_to_send:', data_to_send);

    // const return_data=sendJson(1,data_to_send);
    // console.log("App.vue中, 后端返回的data：",return_data);

    // // 把后端python的一些初始返回值存到state里面
    // // const store = useStore();
    // store.commit('setNegoInitialData', return_data.value);

    sendJson(1, data_to_send).then((return_data) => {
      console.log("App.vue中, 后端返回的data：", return_data);

      // 把后端返回值存到state里面
      store.commit('setNegoInitialData', return_data);
    }).catch((error) => {
      console.error("App.vue中, 处理后端返回值时出错：", error);
    });

  }
  else if (route.path === '/negotiation') {
    router.push('/finish');
    showPrevious.value = false;
    nextPage.value = '欢迎页面';
    previousPage.value = '';
  }
  else if (route.path === '/finish') {
    router.push('/description');
    showPrevious.value = false;
    nextPage.value = '谈判准备';
    previousPage.value = '';
  }
}
const goToPrevious = () => {
  if (route.path === '/preparation') {
    router.push('/description');
    showPrevious.value = false;
    nextPage.value = '谈判准备';
    previousPage.value = '';
  }
  else if (route.path === '/negotiation') {
    router.push('/preparation');
    showPrevious.value = true;
    nextPage.value = '谈判设定';
    previousPage.value = '欢迎页面';
  }
};


// 获取 Vuex 数据
const nego_settings_data = store.state.nego_settings_data;
const my_interests_data = store.state.my_interests_data;
const my_issues_data = store.state.my_issues_data;
const op_interests_data = store.state.op_interests_data;
const op_issues_data = store.state.op_issues_data;

// 监听 Vuex 数据变化
watch(
  [
    () => store.state.nego_settings_data,
    () => store.state.my_interests_data,
    () => store.state.my_issues_data,
    () => store.state.op_interests_data,
    () => store.state.op_issues_data
  ],
  () => {
    // 打印所有相关的数据
    // console.log('App.vue中, Nego Settings:', store.state.nego_settings_data);
    // console.log('App.vue中, My Interests:', store.state.my_interests_data);
    // console.log('App.vue中, My Issues:', store.state.my_issues_data);
    // console.log('App.vue中, Op Interests:', store.state.op_interests_data);
    // console.log('App.vue中, Op Issues:', store.state.op_issues_data);
  },
  { deep: true }
);

</script>

<template>
  <div id="app">
    <!-- 固定标题 -->
    <div class="header">
      <div id="title" class="header-title">自动谈判平台</div>
      <div id="steps" class="steps-navigator">
        <steps />
      </div>
    </div>

    <!-- 主体内容 -->
    <div class="body">
      <RouterView style="width: 100%;" />
    </div>
  </div>
</template>

<style scoped>
* {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background-color: #f8f9fa;
  /* 浅灰背景提升内容区域对比度 */
  /* font-family: "Times New Roman", "宋体"; */
}

.body {
  flex: 1;
  overflow-y: auto;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* 标题和导航条分别靠左和靠右 */
  width: 100%;
  height: 60px;
  /* 固定高度，可根据需求调整 */
  padding: 0 20px;
  /* 内边距，保持内容与边界间距 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 添加阴影效果 */
  background-color: #ffffff;
  /* 背景色，可根据需求调整 */
  box-sizing: border-box;
}

.header-title {
  font-size: 24px;
  font-weight: bold;
  color: #333333;
  /* 标题文字颜色 */
}

.steps-navigator {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  /* 右对齐 */
  flex: 1;
  /* 占据剩余空间 */
}

.steps-navigator>* {
  max-width: 1500px;
  /* 导航条最大宽度 */
  min-width: 300px;
  /* 导航条最小宽度 */
  width: 100%;
  /* 根据父元素适配 */
}
</style>
