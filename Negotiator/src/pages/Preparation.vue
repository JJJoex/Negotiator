<template>
    <div class="container">
        <div class="domain-select">
            <h2>谈判域选择</h2>
            <div class="domain-content">
                <div class="option-group" v-if="options.length > 0">
                    <button v-for="option in options" :key="option.label"
                        :class="['option-item', { selected: selectedOption === option }]"
                        @click="handleOptionClick(option)">
                        {{ option.label }}
                    </button>
                </div>

                <!-- 显示选中项的描述 -->
                <div class="domain-description" v-if="selectedOption">
                    <h3>谈判域：{{ selectedOption.label }}</h3>
                    <p>{{ selectedOption.description }}</p>
                </div>
            </div>
        </div>
        <div class="domain-settings">
            <h2>谈判设置</h2>
            <el-form :inline="true" label-width="220px">
                <el-form-item label="我的角色">
                    <el-radio-group v-model="myRole" size="large">
                        <el-radio-button value="0" :label="roles[0]"/>
                        <el-radio-button value="1" :label="roles[1]"/>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="谈判轮数(我方出价轮数)">
                    <el-slider v-model="rounds" :min="10" :max="1000" show-input />
                </el-form-item>
                <el-form-item label="谈判先手" size="large">
                    <el-radio-group v-model="first">
                        <el-radio-button value="1" label="我方" />
                        <el-radio-button value="2" label="对方" />
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="谈判时间(分钟)">
                    <el-slider v-model="timeLimit" :min="10" :max="45" show-input />
                </el-form-item>
            </el-form>
        </div>
        <div class="profiles">
            <div class="profile-section">
                <h2>我方画像</h2>
                <div class="profiles-item-block">
                    <span>你是否倾向于通过强力手段来压迫对方或争取更好的条件？</span>
                    <el-slider v-model="my_value1" :min="-2" :max="2" :step="1" show-stops :marks="marks_1" />
                </div>
                <div class="profiles-item-block">
                    <span>当面对对方提出的条件时，你愿意在什么程度上做出让步？</span>
                    <el-slider v-model="my_value2" :min="-2" :max="2" :step="1" show-stops :marks="marks_2" />
                </div>
                <div class="profiles-item-block">
                    <span>你是否特别关注达成协议，还是倾向于仅仅在自己能接受的条件下才同意协议？</span>
                    <el-slider v-model="my_value3" :min="-2" :max="2" :step="1" show-stops :marks="marks_3" />
                </div>
                <div class="profiles-item-block">
                    <span>你通常依赖于过去的经验来做决策，还是依赖直觉或随机选择？</span>
                    <el-slider v-model="my_value4" :min="-2" :max="2" :step="1" show-stops :marks="marks_4" />
                </div>
                <div class="profiles-item-block">
                    <span>你如何看待风险和不确定性？</span>
                    <el-slider v-model="my_value5" :min="-2" :max="2" :step="1" show-stops :marks="marks_5" />
                </div>
            </div>
            <div class="profile-section">
                <h2>对方画像</h2>
                <div class="profiles-item-block">
                    <span>你是否倾向于通过强力手段来压迫对方或争取更好的条件？</span>
                    <el-slider v-model="op_value1" :min="-2" :max="2" :step="1" show-stops :marks="marks_1" />
                </div>
                <div class="profiles-item-block">
                    <span>当面对对方提出的条件时，你愿意在什么程度上做出让步？</span>
                    <el-slider v-model="op_value2" :min="-2" :max="2" :step="1" show-stops :marks="marks_2" />
                </div>
                <div class="profiles-item-block">
                    <span>你是否特别关注达成协议，还是倾向于仅仅在自己能接受的条件下才同意协议？</span>
                    <el-slider v-model="op_value3" :min="-2" :max="2" :step="1" show-stops :marks="marks_3" />
                </div>
                <div class="profiles-item-block">
                    <span>你通常依赖于过去的经验来做决策，还是依赖直觉或随机选择？</span>
                    <el-slider v-model="op_value4" :min="-2" :max="2" :step="1" show-stops :marks="marks_4" />
                </div>
                <div class="profiles-item-block">
                    <span>你如何看待风险和不确定性？</span>
                    <el-slider v-model="op_value5" :min="-2" :max="2" :step="1" show-stops :marks="marks_5" />
                </div>
            </div>
        </div>
        <div class="interest-issue-setting">
            <div>
                <h2>我方兴趣和议题偏好</h2>
                <div class="interest-setting">
                    <div class="interest-issue-sliders">
                        <el-collapse accordion>
                            <template v-for="(key, idx) in Object.keys(my_interests_slider)">
                                <el-collapse-item :name="idx">
                                    <template #title>
                                        <div
                                            style="display: flex; width: 80%; justify-content: space-between; align-items: center;">
                                            <div style="width:100px">{{ key }}</div>
                                            <el-slider v-model="my_interests_slider[key]" :min="0" :max="100" :step="1"
                                                @click.stop.native @input="() => updateInterestIssues()" />
                                        </div>
                                    </template>
                                    <template v-for="issue, idx in Object.keys(my_issues_slider[key])"
                                        style="display:flex; justify-content: space-between; align-items: center;">
                                        <div
                                            style="display: flex; width: 60%; justify-content: space-between; align-items: center; margin-left: 50px;">
                                            <div style="width: 100px;">{{ issue }}</div>
                                            <el-slider v-model="my_issues_slider[key][issue]" :min="0" :max="100"
                                                :step="1" @input="() => updateInterestIssues()" />
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
                        <el-collapse accordion>
                            <template v-for="(key, idx) in Object.keys(op_interests_slider)">
                                <el-collapse-item :name="idx">
                                    <template #title>
                                        <div
                                            style="display: flex; width: 80%; justify-content: space-between; align-items: center;">
                                            <div style="width:100px">{{ key }}</div>
                                            <el-slider v-model="op_interests_slider[key]" :min="0" :max="100" :step="1"
                                                @click.stop.native @input="() => updateInterestIssues()" />
                                        </div>
                                    </template>
                                    <template v-for="issue, idx in Object.keys(op_issues_slider[key])"
                                        style="display:flex; justify-content: space-between; align-items: center;">
                                        <div
                                            style="display: flex; width: 60%; justify-content: space-between; align-items: center; margin-left: 50px;">
                                            <div style="width: 100px;">{{ issue }}</div>
                                            <el-slider v-model="op_issues_slider[key][issue]" :min="0" :max="100"
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
import footerComp from '../components/footer.vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const goToNextPage = () => {
    updateDataToStore();
    router.push('/confirmation');
}
const goToPreviousPage = () => {
    router.push('/description');
}

import { onMounted, ref, watch } from 'vue';

const options = ref([]);
const selectedOption = ref(null);
const myRole = ref("0");
const roles = ref([]);
const first = ref("1");
const rounds = ref(10);
const timeLimit = ref(10);
const my_value1 = ref(0)
const my_value2 = ref(0)
const my_value3 = ref(0)
const my_value4 = ref(0)
const my_value5 = ref(0)
const op_value1 = ref(0)
const op_value2 = ref(0)
const op_value3 = ref(0)
const op_value4 = ref(0)
const op_value5 = ref(0)

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

import domainsData from './specific_contents/domains_n_descriptions.json';

onMounted(() => {
    loadOptions();
    loadRoles();
    // initInterestIssues(selectedOption.value.label);
});

watch(() => selectedOption.value, () => {
    initInterestIssues(selectedOption.value.label);
    initChart();
})

const loadOptions = () => {
    try {
        if (typeof domainsData === 'object' && domainsData !== null) {
            options.value = Object.keys(domainsData).map(key => ({
                label: key,
                description: domainsData[key],
            }));

            if (options.value.length > 0) {
                selectedOption.value = options.value[0];
            }
        }
    } catch (error) {
        console.error('加载选项数据失败:', error);
    }
};

const handleOptionClick = (option) => {
    selectedOption.value = option;
    loadRoles();
};

import rolesData from './specific_contents/domains_n_roles.json';

const getRolesForDomain = (domain) => {
    return rolesData[domain];
};

const loadRoles = () => {
    if (selectedOption.value) {
        const domain = selectedOption.value.label;
        roles.value = getRolesForDomain(domain);
    }
};

import issuesData from './specific_contents/interests_issues.json';

const my_interests_slider = ref({});
const my_issues_slider = ref({});
const op_interests_slider = ref({});
const op_issues_slider = ref({});

const my_interests_data = ref({});
const my_issues_data = ref({});
const op_interests_data = ref({});
const op_issues_data = ref({});

import * as echarts from 'echarts/core';
import { SunburstChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import { TitleComponent, TooltipComponent } from 'echarts/components';
echarts.use([SunburstChart, CanvasRenderer, TitleComponent, TooltipComponent]);


const initInterestIssues = (domain) => {
    const issueNames = issuesData[domain];

    my_interests_data.value = {};
    op_interests_data.value = {};
    my_issues_data.value = {};
    op_issues_data.value = {};

    my_interests_slider.value = {};
    my_issues_slider.value = {};
    op_interests_slider.value = {};
    op_issues_slider.value = {};

    const interest_count = Object.keys(issueNames).length;
    Object.entries(issueNames).forEach(([category, issues]) => {
        my_interests_data.value[category] = 1 / interest_count;
        op_interests_data.value[category] = 1 / interest_count;
        my_issues_data.value[category] = {};
        op_issues_data.value[category] = {};

        my_interests_slider.value[category] = 50;
        op_interests_slider.value[category] = 50;
        my_issues_slider.value[category] = {};
        op_issues_slider.value[category] = {};

        const issueCount = issues.length;
        issues.forEach(item => {
            my_issues_data.value[category][item] = 1 / issueCount * my_interests_data.value[category];
            op_issues_data.value[category][item] = 1 / issueCount * op_interests_data.value[category];

            my_issues_slider.value[category][item] = 50;
            op_issues_slider.value[category][item] = 50;
        });
    });
    initChart();
}

const initChart = () => {
    const myChart = echarts.init(document.getElementById('myChart'));
    const opponentChart = echarts.init(document.getElementById('opponentChart'));
    const MyData = handleMyData(my_interests_data.value, my_issues_data.value);
    const OpData = handleOpData(op_interests_data.value, op_issues_data.value)

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

    const opOption = {
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
            data: OpData,
            radius: [0, '80%'],
            label: {
                rotate: 'radial'
            }
        }
    };

    myChart.setOption(myOption);
    opponentChart.setOption(opOption);
}

const handleMyData = (my_interests_data, my_issues_data) => {
    const myData = [];
    for (const key in my_interests_data) {
        const children = []
        for (const item in my_issues_data[key]) {
            children.push({
                name: item,
                value: my_issues_data[key][item]
            });
        }
        myData.push({
            name: key,
            value: my_interests_data[key],
            children: children
        });
    }

    return myData;
}
const handleOpData = (op_interests_data, op_issues_data) => {
    const opData = [];
    for (const key in op_interests_data) {
        const children = []
        for (const item in op_issues_data[key]) {
            children.push({
                name: item,
                value: op_issues_data[key][item]
            });
        }
        opData.push({
            name: key,
            value: op_interests_data[key],
            children: children
        });
    }
    return opData;
}

const updateInterestIssues = () => {
    const my_interest_normalized = {};
    const opponent_interest_normalized = {};

    let my_interest_sum = 0;
    let opponent_interest_sum = 0;
    const my_issues_sum = {};
    const op_issues_sum = {};
    for (let key in my_interests_slider.value) {
        my_interest_sum += my_interests_slider.value[key];
        my_issues_data.value[key] = {};
        let issue_sum = 0;
        for (let issue in my_issues_slider.value[key]) {
            issue_sum += my_issues_slider.value[key][issue];
        }
        my_issues_sum[key] = issue_sum;
    }
    for (let key in op_interests_slider.value) {
        opponent_interest_sum += op_interests_slider.value[key];
        op_issues_data.value[key] = {};
        let issue_sum = 0;
        for (let issue in op_issues_slider.value[key]) {
            issue_sum += op_issues_slider.value[key][issue];
        }
        op_issues_sum[key] = issue_sum;
    }
    for (let key in my_interests_slider.value) {
        my_interest_normalized[key] = my_interests_slider.value[key] / my_interest_sum;
        opponent_interest_normalized[key] = op_interests_slider.value[key] / opponent_interest_sum;
        my_interests_data.value[key] = my_interest_normalized[key];
        op_interests_data.value[key] = opponent_interest_normalized[key];
    }
    for (let key in my_interests_slider.value) {
        for (let issue in my_issues_slider.value[key]) {
            my_issues_data.value[key][issue] = my_issues_slider.value[key][issue] / my_issues_sum[key] * my_interest_normalized[key];
        }
    }
    for (let key in op_interests_slider.value) {
        for (let issue in op_issues_slider.value[key]) {
            op_issues_data.value[key][issue] = op_issues_slider.value[key][issue] / op_issues_sum[key] * opponent_interest_normalized[key];
        }
    }
    updateChart();
}

const updateChart = () => {
    const MyData = handleMyData(my_interests_data.value, my_issues_data.value);
    const OpponentData = handleOpData(op_interests_data.value, op_issues_data.value);

    let myChart = echarts.getInstanceByDom(document.getElementById('myChart'));
    let opponentChart = echarts.getInstanceByDom(document.getElementById('opponentChart'));

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


import { useStore } from 'vuex';
const store = useStore();

const updateDataToStore = () => {
    const nego_settings_data = {
        BiddingRounds: rounds.value,
        BiddingTime: timeLimit.value,
        Domain: selectedOption.value.label,
        whoFirst: first.value,
        roles: {
            my: myRole.value === 0 ? roles.value[0] : roles.value[1],
            op: myRole.value === 0 ? roles.value[1] : roles.value[0],
        },
        settingValues: {
            my: {
                value1: my_value1.value,
                value2: my_value2.value,
                value3: my_value3.value,
                value4: my_value4.value,
                value5: my_value5.value,
            },
            op: {
                value1: op_value1.value,
                value2: op_value2.value,
                value3: op_value3.value,
                value4: op_value4.value,
                value5: op_value5.value,
            }
        }
    };
    console.log('nego_settings_data:', nego_settings_data);
    store.commit('setNegoSettingsData', nego_settings_data);
    store.commit('setMyInterestsData', my_interests_data.value);
    store.commit('setMyIssuesData', my_issues_data.value);
    store.commit('setOpInterestsData', op_interests_data.value);
    store.commit('setOpIssuesData', op_issues_data.value);
};

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
    margin: 0 50px 30px;
}

.domain-content {
    display: flex;
    justify-content: space-evenly;
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
    margin-bottom: 20px;
    text-align: center;
}

.profiles-item-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 50px;
}

.profiles-item-block .el-slider {
    width: 70%;
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

.option-group {
    display: flex;
    flex-direction: column;
    margin-top: 16px;
    margin-left: 20px;
    margin-bottom: 20px;
    gap: 12px;
    width: 200px;
}

.option-item {
    width: 200px;
    padding: 8px 16px;
    font-size: 14px;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #fff;
    cursor: pointer;
    transition: background-color 0.3s, border-color 0.3s;
}

.option-item:hover {
    background-color: #f5f5f5;
}

.option-item.selected {
    background-color: #409eff;
    color: #fff;
    border-color: #409eff;
}

.domain-description h3 {
    margin: 20px 20px 20px 20px;
    display: flex;
    font-size: 24px;
    color: #333;
}

.domain-description p {
    margin: 20px 20px 20px 20px;
    display: flex;
    font-size: 18px;
    color: #555;
    line-height: 1.6;
    white-space: pre-line;
}

.role-selection {
    display: flex;
    align-items: center;
    margin-top: 20px;
    margin-left: 30px;
    gap: 16px;
    width: 500px;
    margin-bottom: 30px;
}

.role-selection button {
    padding: 6px 12px;
    background-color: #409eff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100px;

}

.role-selection button:hover {
    background-color: #66b1ff;
}




.role-setting-sliderpacks {
    margin-left: 150px;
    max-width: 1500px;
    /* 适应父容器 */
    display: flex;
    flex-direction: column;
    /* 使所有滑块容器竖着排列 */
    width: 600px;
    margin-top: 30px;
    margin-right: 100px;
}

.role-setting-slider {
    display: flex;
    flex-direction: column;
    /* 让描述和滑块垂直排列 */
    align-items: center;
    /* 使内容水平居中 */
    margin-bottom: 50px;
    /* 适当的间距 */
}

.role-setting-slider .el-slider {
    width: 100%;
    /* 让滑块宽度填满父容器 */
    margin-top: 10px;
    /* 描述与滑块之间的间距 */
}

.role-setting-slider .demonstration {
    font-size: 16px;
    line-height: 22px;
    color: #000000;
    text-align: center;
    /* 水平居中 */
    margin-bottom: -5px;
    /* 描述与滑块之间的间距 */
}


.slider-labels-bottom {
    display: flex;
    justify-content: space-between;
    width: 100%;

    top: 1px;
    /* 调整位置，避免覆盖滑块 */
}

.slider-label-left,
.slider-label-right {
    font-size: 14px;
    color: #333;
    margin-bottom: -5px;
}
</style>