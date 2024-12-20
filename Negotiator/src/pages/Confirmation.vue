
<template>
    <div class="container">
        <h2>谈判信息确认</h2>
        <el-descriptions border>
            <el-descriptions-item label="谈判域">{{negotiation_settings["Domain"]}}</el-descriptions-item>
            <el-descriptions-item label="谈判角色(我方)">{{negotiation_settings["roles"]["my"]}}</el-descriptions-item>
            <el-descriptions-item label="谈判角色(对方)">{{negotiation_settings["roles"]["op"]}}</el-descriptions-item>
            <el-descriptions-item label="谈判先手">{{negotiation_settings["whoFirst"] === 1 ? '对方' : '我方'}}</el-descriptions-item>
            <el-descriptions-item label="谈判轮数">{{negotiation_settings["BiddingRounds"]}}轮</el-descriptions-item>
            <el-descriptions-item label="谈判时间">{{negotiation_settings["BiddingTime"]}}分钟</el-descriptions-item>
        </el-descriptions>
        <div class='charts-container'>
            <div id="my-interests" class="chart-item"></div>
            <div id="opponent-interests" class="chart-item"></div>
        </div>
        <footerComp next="下一步" nextDetail="开始谈判" previous="上一步" previousDetail="谈判配置"
            :showPrevious=true :showNext=true @next-page="goToNextPage" @previous-page="goToPreviousPage" />
    </div>
</template>

<script setup lang="js">
import footerComp from '../components/footer.vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const goToNextPage = () => {
    router.push('/negotiation');
}
const goToPreviousPage = () => {
    router.push('/preparation');
}

import {ref, onMounted, computed} from 'vue';

import { useStore } from 'vuex';

const store = useStore();
const negotiation_settings = computed(() => store.state.nego_settings_data);
const my_interests = computed(() => store.state.my_interests_data);
const my_issues = computed(() => store.state.my_issues_data);
const opponent_interests = computed(() => store.state.op_interests_data);
const opponent_issues = computed(() => store.state.op_issues_data);

import * as echarts from 'echarts/core';
import { SunburstChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import { TitleComponent, TooltipComponent } from 'echarts/components';
echarts.use([SunburstChart, CanvasRenderer, TitleComponent, TooltipComponent]);

const handleMyData = () => {
    const Data = [];
    for (const key in my_interests.value) {
        const children = []
        for (const item in my_issues.value[key]) {
            children.push({
                name: item,
                value: my_issues.value[key][item]
            });
        }
        Data.push({
            name: key,
            value: my_interests.value[key],
            children: children
        });
    }
    return Data;
}

const handleOpponentData = () => {
    const Data = [];
    for (const key in opponent_interests.value) {
        const children = []
        for (const item in opponent_issues.value[key]) {
            children.push({
                name: item,
                value: opponent_issues.value[key][item]
            });
        }
        Data.push({
            name: key,
            value: opponent_interests.value[key],
            children: children
        });
    }
    return Data;
}
const MyData = handleMyData();
const OpponentData = handleOpponentData();
onMounted(() => {
    const myChart = echarts.init(document.getElementById('my-interests'));
    const opponentChart = echarts.init(document.getElementById('opponent-interests'));

    const myOption = {
        title: {
            text: '我方兴趣与议题',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: '项：{b}<br/>值：{c}'
        },
        series: {
            type: 'sunburst',
            data: MyData,
            radius: [0, '80%'],
            label: {
                rotate: 'radial'
            }
        }
    };
    
    const opponentOption = {
        title: {
            text: '对方兴趣与议题',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: '项：{b}<br/>值：{c}'
        },
        series: {
            type: 'sunburst',
            data: OpponentData,
            radius: [0, '80%'],
            label: {
                rotate: 'radial'
            }
        }
    };
    
    myChart.setOption(myOption);
    opponentChart.setOption(opponentOption);
})

</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.el-descriptions {
  margin-top: 20px;
  margin-bottom: 30px;
}

.charts-container {
  display: flex;
  justify-content: space-between;
  flex: 1; /* Take up remaining space */
  /* margin-bottom: 20px; */
}

.chart-item {
  width: 48%; /* Adjust width to make charts appear side by side */
  height: 700px; /* Fixed height for charts */
}

footer-comp {
  margin-top: auto; /* Push footer to the bottom */
  /* padding: 20px; */
}
</style>
