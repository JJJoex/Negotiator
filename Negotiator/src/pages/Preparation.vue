<template>
    <div class="container">
        <div class="domain-select">
            <h2>选择谈判领域</h2>
            <div class="domain-content">
                <el-radio-group v-model="prepare.domain">
                    <el-radio-button v-for="item in domains" :label="item" :value="item"></el-radio-button>
                </el-radio-group>
            </div>
            <div v-if="prepare.domain" class="domain-description">
                <h3>谈判域：{{ prepare.domain }}</h3>
                <p>{{ backendData[prepare.domain].description }}</p>
            </div>
        </div>
        <div class="domain-settings">
            <h2>谈判设置</h2>
            <el-form :inline="true" :column="2" label-width="120px">
                <el-form-item label="我方角色">
                    <el-radio-group v-model="prepare.roles.my" size="large">
                        <el-radio-button value="0" :label="backendData[prepare.domain].role[0]" />
                        <el-radio-button value="1" :label="backendData[prepare.domain].role[1]" />
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="谈判轮数(我方出价轮数)">
                    <el-slider v-model="prepare.rounds" :min="10" :max="1000" show-input />
                </el-form-item>
                <el-form-item label="谈判先手" size="large">
                    <el-radio-group v-model="prepare.first">
                        <el-radio-button value="false" label="我方" />
                        <el-radio-button value="true" label="对方" />
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="谈判时间(分钟)">
                    <el-slider v-model="prepare.time" :min="10" :max="45" show-input />
                </el-form-item>
            </el-form>
        </div>
        <div class="profiles">
            <div class="profile-section">
                <h2>我方</h2>
                <div class="profiles-item-block">
                    <span>你是否倾向于通过强力手段来压迫对方或争取更好的条件？</span>
                    <el-slider v-model="prepare.my_profile[0]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_1" />
                </div>
                <div class="profiles-item-block">
                    <span>当面对对方提出的条件时，你愿意在什么程度上做出让步？</span>
                    <el-slider v-model="prepare.my_profile[1]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_2" />
                </div>
                <div class="profiles-item-block">
                    <span>你是否特别关注达成协议，还是倾向于仅仅在自己能接受的条件下才同意协议？</span>
                    <el-slider v-model="prepare.my_profile[2]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_3" />
                </div>
                <div class="profiles-item-block">
                    <span>你通常依赖于过去的经验来做决策，还是依赖直觉或随机选择？</span>
                    <el-slider v-model="prepare.my_profile[3]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_4" />
                </div>
                <div class="profiles-item-block">
                    <span>你如何看待风险和不确定性？</span>
                    <el-slider v-model="prepare.my_profile[4]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_5" />
                </div>
            </div>
            <div class="profile-section">
                <h2>对方</h2>
                <div class="profiles-item-block">
                    <span>你是否倾向于通过强力手段来压迫对方或争取更好的条件？</span>
                    <el-slider v-model="prepare.opponent_profile[0]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_1" />
                </div>
                <div class="profiles-item-block">
                    <span>当面对对方提出的条件时，你愿意在什么程度上做出让步？</span>
                    <el-slider v-model="prepare.opponent_profile[1]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_2" />
                </div>
                <div class="profiles-item-block">
                    <span>你是否特别关注达成协议，还是倾向于仅仅在自己能接受的条件下才同意协议？</span>
                    <el-slider v-model="prepare.opponent_profile[2]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_3" />
                </div>
                <div class="profiles-item-block">
                    <span>你通常依赖于过去的经验来做决策，还是依赖直觉或随机选择？</span>
                    <el-slider v-model="prepare.opponent_profile[3]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_4" />
                </div>
                <div class="profiles-item-block">
                    <span>你如何看待风险和不确定性？</span>
                    <el-slider v-model="prepare.opponent_profile[4]" :min="-2" :max="2" :step="1" show-stops
                        :marks="marks_5" />
                </div>
            </div>
        </div>
        <div class="interest-issue-setting">
            <div>
                <h2>我方兴趣和议题偏好</h2>
                <!-- <pre>{{ prepare.my_issues }}</pre> -->
                <div class="interest-setting">
                    <div class="interest-issue-sliders">
                        <el-collapse accordion>
                            <template v-for="(key, idx) in Object.keys(my_interests)">
                                <el-collapse-item :name="idx">
                                    <template #title>
                                        <div
                                            style="display: flex; width: 80%; justify-content: space-between; align-items: center;">
                                            <div style="width:100px">{{ key }}</div>
                                            <el-slider v-model="my_interests[key]" :min="0" :max="100"
                                                :step="1" @click.stop.native @input="() => updateInterestIssues()" />
                                        </div>
                                    </template>
                                    <template v-if="my_interests[key]"
                                        v-for="issue, idx in Object.keys(my_issues[key])"
                                        style="display:flex; justify-content: space-between; align-items: center;">
                                        <div
                                            style="display: flex; width: 60%; justify-content: space-between; align-items: center; margin-left: 50px;">
                                            <div style="width: 100px;">{{ issue }}</div>
                                            <el-slider v-model="my_issues[key][issue]" :min="0" :max="100"
                                                :step="1"  @input="() => updateInterestIssues()" />
                                        </div>
                                    </template>
                                </el-collapse-item>
                            </template>
                        </el-collapse>
                    </div>
                    <div id="myChart" class="interest-issue-chart" style="width: 50%; height: 700px;"></div>
                </div>
            </div>
            <div>
                <h2>对方兴趣和议题偏好</h2>
                <div class="interest-setting">
                    <div class="interest-issue-sliders">
                        <el-collapse  accordion>
                            <template v-for="(key, idx) in Object.keys(opponent_interests)">
                                <el-collapse-item :name="idx">
                                    <template #title>
                                        <div
                                            style="display: flex; width: 80%; justify-content: space-between; align-items: center;">
                                            <div style="width:100px">{{ key }}</div>
                                            <el-slider v-model="opponent_interests[key]" :min="0" :max="100"
                                                :step="1" @click.stop.native @input="() => updateInterestIssues()"/>
                                        </div>
                                    </template>
                                    <template v-if="opponent_interests[key]"
                                        v-for="issue, idx in Object.keys(opponent_issues[key])"
                                        style="display:flex; justify-content: space-between; align-items: center;">
                                        <div
                                            style="display: flex; width: 60%; justify-content: space-between; align-items: center; margin-left: 50px;">
                                            <div style="width: 100px;">{{ issue }}</div>
                                            <el-slider v-model="opponent_issues[key][issue]" :min="0" :max="100"
                                                :step="1" @input="() => updateInterestIssues()" />
                                        </div>
                                    </template>
                                </el-collapse-item>
                            </template>
                        </el-collapse>
                    </div>
                    <div id="opponentChart" class="interest-issue-chart" style="width: 50%; height: 700px;"></div>
                </div>
            </div>
        </div>
        <footerComp next="下一步" nextDetail="配置确认" previous="上一步" previousDetail="回到主页" :showPrevious=true :showNext=true
            @next-page="goToNextPage" @previous-page="goToPreviousPage" />
    </div>
</template>


<script setup lang="js">
import { nextTick, onMounted, reactive, ref, watch } from 'vue';
import footerComp from '../components/footer.vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const goToNextPage = () => {
    updatePrepare(prepare.value);
    router.push('/ensurement');
}
const goToPreviousPage = () => {
    router.push('/introduction');
}

import { useStore } from 'vuex';
const store = useStore();

import backendData from './specific_contents/backend.json';
const domains = Object.keys(backendData);
const prepare = ref({
    domain: domains[0],
    roles: {
        my: backendData[domains[0]].role[0],
        opponent: backendData[domains[0]].role[1]
    },
    first: false,
    rounds: 10,
    time: 10,
    my_profile: [0, 0, 0, 0, 0],
    opponent_profile: [0, 0, 0, 0, 0],
    my_interests: {},
    my_issues: {},
    opponent_interests: {},
    opponent_issues: {}
})

const my_interests = ref({});
const my_issues = ref({});
const opponent_interests = ref({});
const opponent_issues = ref({});

const initInterestIssues = (domain) => {
    prepare.value.my_interests = {};
    prepare.value.my_issues = {};
    prepare.value.opponent_interests = {};
    prepare.value.opponent_issues = {};

    my_interests.value = {};
    my_issues.value = {};
    opponent_interests.value = {};
    opponent_issues.value = {};

    const interest_count = Object.keys(backendData[domain].issue).length;
    Object.entries(backendData[domain].issue).forEach(([key, issues]) => {
        prepare.value.my_interests[key] = 1 / interest_count;
        prepare.value.my_issues[key] = {};
        prepare.value.opponent_interests[key] = 1 / interest_count;
        prepare.value.opponent_issues[key] = {};

        my_interests.value[key] = 50;
        opponent_interests.value[key] = 50;
        my_issues.value[key] = {};
        opponent_issues.value[key] = {};

        const issueCount = issues.length;

        issues.forEach(issue => {
            prepare.value.my_issues[key][issue] = 1 / issueCount * prepare.value.my_interests[key];
            prepare.value.opponent_issues[key][issue] = 1 / issueCount * prepare.value.opponent_interests[key];
            
            my_issues.value[key][issue] = 50;
            opponent_issues.value[key][issue] = 50;
        });
    });
    initChart();
}



const updateInterestIssues = () => {
    const my_interest_normalized = {};
    const opponent_interest_normalized = {};

    let my_interest_sum = 0;
    let opponent_interest_sum = 0;
    const my_issues_sum = {};
    const opponent_issues_sum = {};
    for (let key in my_interests.value) {
        my_interest_sum += my_interests.value[key];
        prepare.value.my_issues[key] = {};
        let issue_sum = 0;
        for(let issue in my_issues.value[key]) {
            issue_sum += my_issues.value[key][issue];
        }
        my_issues_sum[key] = issue_sum;
    }
    for (let key in opponent_interests.value) {
        opponent_interest_sum += opponent_interests.value[key];
        prepare.value.opponent_issues[key] = {};
        let issue_sum = 0;
        for(let issue in opponent_issues.value[key]) {
            issue_sum += opponent_issues.value[key][issue];
        }
        opponent_issues_sum[key] = issue_sum;
    }
    for (let key in my_interests.value) {
        my_interest_normalized[key] = my_interests.value[key] / my_interest_sum;
        opponent_interest_normalized[key] = opponent_interests.value[key] / opponent_interest_sum;
        prepare.value.my_interests[key] = my_interest_normalized[key];
        prepare.value.opponent_interests[key] = opponent_interest_normalized[key];
    }
    for(let key in my_interests.value) {
        for(let issue in my_issues.value[key]) {
            prepare.value.my_issues[key][issue] = my_issues.value[key][issue] / my_issues_sum[key] * my_interest_normalized[key];
        }
    }
    for(let key in opponent_interests.value) {
        for(let issue in opponent_issues.value[key]) {
            prepare.value.opponent_issues[key][issue] = opponent_issues.value[key][issue] / opponent_issues_sum[key] * opponent_interest_normalized[key];
        }
    }
    updateChart();
}


watch(() => prepare.value.domain, (newVal) => {
    initInterestIssues(newVal);
    initChart();
})

const marks_1 = {
    "-2": "完全不倾向竞争",
    "-1": "",
    "0": "中立/无明显倾向",
    "1": "",
    "2": "非常倾向竞争"
};
const marks_2 = {
    "-2": "完全不愿意妥协",
    "-1": "",
    "0": "中立/无明显倾向",
    "1": "",
    "2": "非常愿意妥协"
};
const marks_3 = {
    "-2": "完全不关心达成协议",
    "-1": "",
    "0": "不太重视达成协议",
    "1": "",
    "2": "非常重视达成协议"
};
const marks_4 = {
    "-2": "非常依赖随机与直觉",
    "-1": "",
    "0": "无明显依赖",
    "1": "",
    "2": "非常依赖经验"
};
const marks_5 = {
    "-2": "完全避免任何风险",
    "-1": "",
    "0": "追求较为保守的选择",
    "1": "",
    "2": "完全愿意承担风险"
};

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

onMounted(() => {
    initInterestIssues(domains[0]);
})

const initChart = () => {
    const MyData = handleMyData(prepare.value);
    const OpponentData = handleOpponentData(prepare.value);
    const myChart = echarts.init(document.getElementById('myChart'));
    const opponentChart = echarts.init(document.getElementById('opponentChart'));

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
}

const updateChart = () => {
    const MyData = handleMyData(prepare.value);
    const OpponentData = handleOpponentData(prepare.value);

    const myChartDom = document.getElementById('myChart');
    const opponentChartDom = document.getElementById('opponentChart');

    let myChart = echarts.getInstanceByDom(myChartDom);
    let opponentChart = echarts.getInstanceByDom(opponentChartDom);

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
}

const updatePrepare = (prepare) => {
    store.commit('updatePrepare', prepare);
}

</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.domain-select,
.domain-settings,
.profiles,
.interest-issue-setting {
    margin-bottom: 30px;
}

.domain-content {
    display: flex;
    justify-content: space-between;
}

.domain-buttons {
    width: 45%;
}

.domain-description {
    width: 45%;
}

.domain-settings .el-form-item {
    width: 40%;
}

.profiles {
    display: flex;
    justify-content: space-between;
}

.profile-section {
    display: flex;
    flex-direction: column;
    width: 50%;
}

.profiles-section p {
    margin-bottom: 18px;
    text-align: center;
}

.profiles-item-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
}

.profiles-item-block .el-slider {
    width: 80%;
}

.interest-setting {
    display: flex;
    width: 100%;
}

.interest-issue-sliders {
    width: 50%;
    margin-bottom: 20px;
}

.interest-issue-chart {
    width: 50%;
    height: 1000px;
}

footer-comp {
    margin-top: auto;
    width: 100%;
}
</style>