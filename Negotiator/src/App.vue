<script setup lang="js">
import { ref ,reactive,watch} from 'vue';
import steps from './components/steps.vue'
import { ArrowRightBold, ArrowLeftBold } from '@element-plus/icons-vue';
import { useRouter, useRoute, RouterView } from 'vue-router';

import { useStore } from 'vuex';

import {sendJson} from './pages/SendMessage';
import { ElMessage } from 'element-plus';


const nextPage = ref('准备阶段');
const previousPage = ref('查看结果');
const showPrevious = ref(false);

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
    nextPage.value = '谈判阶段';
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

    console.log(my_intr,op_intr);


    const my_issues = Object.values(store.state.my_issues_data).map(category => Object.values(category));
    const op_issues = Object.values(store.state.op_issues_data).map(category => Object.values(category));

    console.log(my_issues,op_issues);






    const data_to_send={
      Domain: store.state.nego_settings_data["Domain"],
      Rounds: store.state.nego_settings_data["BiddingRounds"],
      Times: store.state.nego_settings_data["BiddingTime"],
      First: store.state.nego_settings_data['whoFirst']==="1"?true:false,
      Profile: {
        my:[
          store.state.nego_settings_data['settingValues']['my']["value1"],
          store.state.nego_settings_data['settingValues']['my']["value2"],
          store.state.nego_settings_data['settingValues']['my']["value3"],
          store.state.nego_settings_data['settingValues']['my']["value4"],
          store.state.nego_settings_data['settingValues']['my']["value5"]
        ],
        op:[
          store.state.nego_settings_data['settingValues']['op']["value1"],
          store.state.nego_settings_data['settingValues']['op']["value2"],
          store.state.nego_settings_data['settingValues']['op']["value3"],
          store.state.nego_settings_data['settingValues']['op']["value4"],
          store.state.nego_settings_data['settingValues']['op']["value5"]
        ]
      },
      Role:store.state.nego_settings_data['roles']['my'],

      MyInterests:my_intr,
      MyIssues:my_issues,
      OpInterests:op_intr,
      OpIssues:op_issues



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
    nextPage.value = '准备阶段';
    previousPage.value = '';
  }
}
const goToPrevious = () => {
  if (route.path === '/preparation') {
    router.push('/description');
    showPrevious.value = false;
    nextPage.value = '准备阶段';
    previousPage.value = '';
  }
  else if (route.path === '/negotiation') {
    router.push('/preparation');
    showPrevious.value = true;
    nextPage.value = '谈判阶段';
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


// 监听 Vuex 数据变化
watch(
  [
    () => store.state.curr_nego_state
  ],
  () => {
    if (route.path === '/negotiation' && store.state.curr_nego_state!=="negotiating"){
      console.log("App.vue之路由检测到谈判状态改变，准备进入结算阶段...");
      ElMessage({
          message: `App.vue之路由检测到谈判状态改变，准备进入结算阶段...`,
          type: 'info',  
      });
      goToNext();
    }

  },
  { deep: true }
);

</script>






<template>
  <div id="app">
    <div class="header">
      <div id="title">自动谈判平台</div>
      <div id="steps">
        <steps />
      </div>
    </div>
    <div class="body">
      <RouterView style="width: 100%;"/>


    </div>
    <div class="footer">
      <div id="previous" @click="goToPrevious" v-if="showPrevious">
        <div style="font-size: 5px; text-align: right;">
          <ArrowLeftBold style="width: 5em; height: 5em; margin: 20px;" />
        </div>
        <div style="text-align: left;">
          <p>上一步</p>
          <p style="font-size: 25px; font-weight: bolder;">{{ previousPage }}</p>
        </div>
      </div>
      <div id="next" @click="goToNext">
        <div style="text-align: right;">
          <p>下一步</p>
          <p style="font-size: 25px; font-weight: bolder;">{{ nextPage }}</p>
        </div>
        <div style="font-size: 5px; text-align: left;">
          <ArrowRightBold style="width: 5em; height: 5em; margin: 20px;" />
        </div>
      </div>
    </div>
  </div>
</template>

<style>
*{ 
 -webkit-touch-callout:none; 
 -webkit-user-select:none; 
 -khtml-user-select:none; 
 -moz-user-select:none;
 -ms-user-select:none; 
 user-select:none; 
} 

#app {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  font-family: "Times New Roman", "宋体";
}

.header {
  font-weight: bold;
  align-items: center;
  display: flex;
  width: 100%;
  height: 10%;
  background-color: #8fcedac8;
}

.body {
  width: 100%;
  height: 80%;
  overflow: scroll;
}

.footer {
  display: flex;
  width: 100%;
  height: 10%;
  background-color: #8fcedac8;
  justify-content: right;
}

#title {
  display: flex;
  width: 30%;
  height: 100%;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

#steps {
  width: 70%;
  height: 80%;
  padding: 10px 0 0;
}

#previous,
#next {
  display: flex;
  width: 50%;
  height: 100%;
  align-items: center;
  justify-content: center;
}

#previous div,
#next div {
  width: 50%;
  flex-direction: row;
  align-items: center;
}

p {
  margin: 0;
}

#previous:hover,
#next:hover {
  background-color: #77adb7;
}

::-webkit-scrollbar {
  /* display: none; */
  width: 10px;
}
::-webkit-scrollbar-thumb {
  background-color: #c5c5c5;
  /* border-radius: 10px; */
}
</style>
