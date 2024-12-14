<script setup lang="js">
import { ref ,reactive,watch} from 'vue';
import steps from './components/steps.vue'
import { ArrowRightBold, ArrowLeftBold } from '@element-plus/icons-vue';
import { useRouter, useRoute, RouterView } from 'vue-router';

import { useStore } from 'vuex';


const nextPage = ref('谈判准备');
const previousPage = ref('查看结果');
const showPrevious = ref(false);
const showFooter = ref(true);
const router = useRouter();
const route = useRoute();
const goToNext = () => {
  if (route.path === '/description') {
    router.push('/preparation');
    showPrevious.value = true;
    nextPage.value = '谈判设定';
    previousPage.value = '欢迎页面';
  }
  else if (route.path === '/preparation') {
    router.push('/preparation/setting');
    showPrevious.value = true;
    nextPage.value = '我方兴趣';
    previousPage.value = '谈判准备';
  }
  else if (route.path === '/preparation/setting') {
    router.push('/preparation/myInterest');
    showPrevious.value = true;
    nextPage.value = '我方议题';
    previousPage.value = '谈判设定';
  }
  else if (route.path === '/preparation/myInterest') {
    router.push('/preparation/myIssue');
    showPrevious.value = true;
    nextPage.value = '对方兴趣';
    previousPage.value = '我方兴趣';
  }
  else if (route.path === '/preparation/myIssue') {
    router.push('/preparation/opponentInterest');
    showPrevious.value = true;
    nextPage.value = '对方议题';
    previousPage.value = '我方议题';
  }
  else if (route.path === '/preparation/opponentInterest') {
    router.push('/preparation/opponentIssue');
    showPrevious.value = true;
    nextPage.value = '数据确认';
    previousPage.value = '对方兴趣';
  }
  else if (route.path === '/preparation/opponentIssue') {
    router.push('/preparation/confirmation');
    showPrevious.value = true;
    nextPage.value = '开始谈判';
    previousPage.value = '对方议题';
  }
  else if (route.path === '/preparation/confirmation') {
    router.push('/negotiation');
    showPrevious.value = true;
    nextPage.value = '查看结果';
    previousPage.value = '谈判准备';
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
  else if (route.path === '/preparation/setting') {
    router.push('/preparation');
    showPrevious.value = true;
    nextPage.value = '谈判设定';
    previousPage.value = '欢迎页面';
  }
  else if (route.path === '/preparation/myInterest') {
    router.push('/preparation/setting');
    showPrevious.value = true;
    nextPage.value = '我方兴趣';
    previousPage.value = '谈判准备';
  }
  else if (route.path === '/preparation/myIssue') {
    router.push('/preparation/myInterest');
    showPrevious.value = true;
    nextPage.value = '我方议题';
    previousPage.value = '谈判设定';
  }
  else if (route.path === '/preparation/opponentInterest') {
    router.push('/preparation/myIssue');
    showPrevious.value = true;
    nextPage.value = '对方兴趣';
    previousPage.value = '我方兴趣';
  }
  else if (route.path === '/preparation/opponentIssue') {
    router.push('/preparation/opponentInterest');
    showPrevious.value = true;
    nextPage.value = '对方议题';
    previousPage.value = '我方议题';
  }
  else if (route.path === '/preparation/confirmation') {
    router.push('/preparation/opponentIssue');
    showPrevious.value = true;
    nextPage.value = '数据确认';
    previousPage.value = '对方兴趣';
  }
  else if (route.path === '/negotiation') {
    router.push('/preparation');
    showPrevious.value = true;
    nextPage.value = '谈判设定';
    previousPage.value = '欢迎页面';
  }
};

// 获取 Vuex store 实例
const store = useStore();

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
    console.log('App.vue中, Nego Settings:', store.state.nego_settings_data);
    console.log('App.vue中, My Interests:', store.state.my_interests_data);
    console.log('App.vue中, My Issues:', store.state.my_issues_data);
    console.log('App.vue中, Op Interests:', store.state.op_interests_data);
    console.log('App.vue中, Op Issues:', store.state.op_issues_data);
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
    <div class="footer" v-if="showFooter">
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
  display: flex;
  width: 100%;
  height: 100%;
  overflow: scroll;
  align-items: center;
  justify-content: space-between
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
