<template>
    <div class="container">
        <el-descriptions title="谈判信息确认" border>
            <el-descriptions-item label="谈判域">{{prepare.domain}}</el-descriptions-item>
            <el-descriptions-item label="谈判角色(我方)">{{prepare.roles.my}}</el-descriptions-item>
            <el-descriptions-item label="谈判角色(对方)">{{prepare.roles.opponent}}</el-descriptions-item>
            <el-descriptions-item label="谈判先手">{{prepare.first ? '对方' : '我方'}}</el-descriptions-item>
            <el-descriptions-item label="谈判轮数">{{prepare.rounds}}</el-descriptions-item>
            <el-descriptions-item label="谈判时间">{{prepare.time}}</el-descriptions-item>
        </el-descriptions>
        <div class='charts-container'>
            <div id="my-interests" class="chart-item"></div>
            <div id="opponent-interests" class="chart-item"></div>
        </div>
        <footerComp next="下一步" nextDetail="开始谈判" previous="上一步" previousDetail="谈判配置"
            showPrevious="showPrevious" showNext="showNext" @next-page="goToNextPage" @previous-page="goToPreviousPage" />
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

import {ref, onMounted} from 'vue';
const prepare = ref({
    domain: '电子商务',
    roles: {
        my: '买家',
        opponent: '卖家'
    },
    first: false,
    rounds: 3,
    time: 20,
    my_interests: {
        '电子产品': 100,
        '服装': 200
    },
    my_issues: {
        '电子产品': {
            '价格': 50,
            '质量': 50
        },
        '服装': {
            '价格': 100,
            '质量': 100
        }
    },
    opponent_interests: {
        '电子产品': 100,
        '服装': 200
    },
    opponent_issues: {
        '电子产品': {
            '价格': 50,
            '质量': 50
        },
        '服装': {
            '价格': 300,
            '质量': 100
        }
    }
})

import * as echarts from 'echarts/core';
import { SunburstChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import { TitleComponent, TooltipComponent } from 'echarts/components';
echarts.use([SunburstChart, CanvasRenderer, TitleComponent, TooltipComponent]);

const handleMyData = (prepare) => {
    const Data = [];
    for (const key in prepare.my_interests) {
        const children = []
        for (const item in prepare.my_issues[key]) {
            children.push({
                name: item,
                value: prepare.my_issues[key][item]
            });
        }
        Data.push({
            name: key,
            value: prepare.my_interests[key],
            children: children
        });
    }
    return Data;
}

const handleOpponentData = (prepare) => {
    const Data = [];
    for (const key in prepare.opponent_interests) {
        const children = []
        for (const item in prepare.opponent_issues[key]) {
            children.push({
                name: item,
                value: prepare.opponent_issues[key][item]
            });
        }
        Data.push({
            name: key,
            value: prepare.opponent_interests[key],
            children: children
        });
    }
    return Data;
}
const MyData = handleMyData(prepare.value);
const OpponentData = handleOpponentData(prepare.value);
console.log(MyData, OpponentData);

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

window.addEventListener('resize', function () {
    myChart.resize();
    opponentChart.resize();
});
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