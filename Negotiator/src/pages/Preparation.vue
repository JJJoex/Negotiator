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
                <!-- <p>{{ selectedOption.description }}</p> -->
            </div>
        </div>
        <div class="domain-settings">
            <h2>谈判设置</h2>
            <el-form :inline="true" :column="2" label-width="120px">
                <el-form-item label="我方角色">
                    <el-radio-group v-model="prepare.roles.my" size="large">
                        <el-radio-button value="0" :label="roles[0]" />
                        <el-radio-button value="1" :label="roles[1]" />
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
                <div class="interest-setting">
                    <div class="interest-issue-sliders">
                        <template v-for="key in Object.keys(prepare.my_interests)">
                            <span>{{ key }}</span>
                            <el-slider v-model="prepare.my_interests[key]" :min="0" :max="10" :step="1" />
                            <template v-if="prepare.my_interests[key]"
                                v-for="issue in Object.keys(prepare.my_issues[key])">
                                <span>{{ issue }}</span>
                                <el-slider v-model="prepare.my_issues[key][issue]" :min="0" :max="10" :step="1" />
                            </template>
                        </template>
                    </div>
                    <div id="myChart" class="interest-issue-chart" style="width: 50%; height: 500px;"></div>
                </div>
            </div>
            <div>
                <h2>对方兴趣和议题偏好</h2>
                <div class="interest-setting">
                    <div class="interest-issue-sliders">
                        <template v-for="key in Object.keys(prepare.opponent_interests)">
                            <span>{{ key }}</span>
                            <el-slider v-model="prepare.opponent_interests[key]" :min="0" :max="10" :step="1" />
                            <template v-if="prepare.opponent_interests[key]"
                                v-for="issue in Object.keys(prepare.opponent_issues[key])">
                                <span>{{ issue }}</span>
                                <el-slider v-model="prepare.opponent_issues[key][issue]" :min="0" :max="10" :step="1" />
                            </template>
                        </template>
                    </div>
                    <div id="opponentChart" class="interest-issue-chart" style="width: 50%; height: 500px;"></div>
                </div>
            </div>
        </div>
        <footerComp next="下一步" nextDetail="配置确认" previous="上一步" previousDetail="回到主页" showPrevious="showPrevious"
            showNext="showNext" @next-page="goToNextPage" @previous-page="goToPreviousPage" />
    </div>
</template>

<script setup lang="js">
import { onMounted, ref, watch } from 'vue';
import footerComp from '../components/footer.vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const goToNextPage = () => {
    router.push('/ensurement');
}
const goToPreviousPage = () => {
    router.push('/introduction');
}
const domains = ref(['技术', '商务', '法律', '金融', '其他']);
const roles = ['甲方', '乙方'];

const prepare = ref({
    domain: '技术',
    roles: {
        my: '',
        opponent: ''
    },
    first: false,
    rounds: 10,
    time: 10,
    my_profile: [0, 0, 0, 0, 0],
    opponent_profile: [0, 0, 0, 0, 0],
    my_interests: {
        '技术': 3,
        '商务': 4,
        '法律': 5,
        '金融': 6,
        '其他': 2
    },
    my_issues: {
        '技术': {
            '技术1': 1,
            '技术2': 2,
            '技术3': 0
        },
        '商务': {
            '商务1': 2,
            '商务2': 1,
            '商务3': 1
        },
        '法律': {
            '法律1': 2,
            '法律2': 1,
            '法律3': 2
        },
        '金融': {
            '金融1': 0,
            '金融2': 0,
            '金融3': 0
        },
        '其他': {
            '其他1': 0,
            '其他2': 0,
            '其他3': 0
        }
    },
    opponent_interests: {
        '技术': 0,
        '商务': 0,
        '法律': 0,
        '金融': 0,
        '其他': 0
    },
    opponent_issues: {
        '技术': {
            '技术1': 0,
            '技术2': 0,
            '技术3': 0
        },
        '商务': {
            '商务1': 0,
            '商务2': 0,
            '商务3': 0
        },
        '法律': {
            '法律1': 0,
            '法律2': 0,
            '法律3': 0
        },
        '金融': {
            '金融1': 0,
            '金融2': 0,
            '金融3': 0
        },
        '其他': {
            '其他1': 0,
            '其他2': 0,
            '其他3': 0
        }
    }
})
watch(prepare.value.roles.my, () => {
    prepare.value.roles.opponent = prepare.value.roles.my === '0' ? '1' : '0';
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
const MyData = handleMyData(prepare.value);
const OpponentData = handleOpponentData(prepare.value);

onMounted(() => {
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
})

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