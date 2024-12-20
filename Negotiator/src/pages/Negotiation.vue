<template>
    <div v-bind="$attrs" class="container">
        <!-- 左侧部分 -->
        <div class="left-panel">
            <div class='status-bar'>我的出价</div>
            <el-form>
                <el-form-item v-for="(items, category) in groceryStore" :label="category" :key="category">
                    <el-select v-model="userSelections[category]">
                        <el-option v-for="(item, idx) in items" :key="item" :value="idx" :label="item">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleBidClick">出价</el-button>
                    <el-button type="success" @click="handleAcceptClick">接受</el-button>
                    <el-button type="danger" @click="handleRejectClick">结束</el-button>
                    <el-button color="#626aef" @click="handleShowSuggestions">
                        {{ showHints ? '隐藏AI推荐' : '查看AI推荐' }}
                    </el-button>
                </el-form-item>
                <el-form-item v-show="showHints">
                    <h3>AI推荐出价 <el-icon>
                            <StarFilled color="gold" />
                        </el-icon></h3>
                    <el-table :data="[agentSuggestion]" class="suggestion-table"
                        :header-cell-style="{ background: '#eef1f6', color: '#000000' }">
                        <!-- <el-table-column > -->
                        <el-table-column v-for="(category, index) in Object.keys(agentSuggestion)" :key="index"
                            :label="category" :prop="category">
                            <template #default>
                                <span>{{ showHints ? domain_data_content[category][agentSuggestion[category]] : "?"
                                    }}</span>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-form-item>
                <el-form-item v-show="showHints">
                    <el-button type="primary" @click="handleBidSuggestionClick">导入推荐出价</el-button>
                </el-form-item>
            </el-form>
        </div>

        <!-- 右侧部分 -->
        <div class="right-panel">
            <div class="status-bar">
                <div>剩余轮数：{{ remainingRounds }}</div>
                <div>剩余时间：{{ formattedCountdown }}</div>
            </div>
            <div class="table-container">
                <el-table :data="reversedBidHistory" class="history-table" stripe>
                    <el-table-column label="轮次" prop="round"></el-table-column>
                    <el-table-column label="出价方" prop="bidder"></el-table-column>
                    <template v-for="(items, category) in groceryStore">
                        <el-table-column :label="category">
                            <template #default="{ row }">
                                <span>{{
                                    getIssue(category ,row.bidContent[category])
                                }}</span>
                            </template>
                        </el-table-column>
                    </template>
                </el-table>
            </div>
        </div>
    </div>
    <footerComp previous="上一步" previousDetail="谈判设置" :showPrevious=true :showNext=false
        @previous-page="goToPreviousPage" style="width: 100%;" />
</template>


<script setup lang="js">
import footerComp from '../components/footer.vue';
import { useRoute, useRouter } from 'vue-router';
import { ref, onMounted, computed, watch, onBeforeUnmount } from 'vue';
import { ElMessage } from 'element-plus';  // 引入 ElMessage 用于 Toast 提示
import issuesData from './specific_contents/interests_issues.json';
import { useStore } from 'vuex';
import { sendJson } from './SendMessage';
import { StarFilled } from '@element-plus/icons-vue';

const router = useRouter();
const goToPreviousPage = () => {
    router.push('/preparation');
}

const countdown = ref(null);
const remainingRounds = ref(null);
const groceryStore = ref({});
const bidHistory = ref([]);
const agentSuggestion = ref({});
const totalRounds = ref(null);
const userSelections = ref({});

let timerId = null;

const store = useStore();
const negoSettingsData = ref(null);
const myInterestsData = ref(null);
const myIssuesData = ref(null);
const opInterestsData = ref(null);
const opIssuesData = ref(null);
const domain_data_content = ref(null);

onMounted(() => {
    negoSettingsData.value = store.state.nego_settings_data;
    myInterestsData.value = store.state.my_interests_data;
    myIssuesData.value = store.state.my_issues_data;
    opInterestsData.value = store.state.op_interests_data;
    opIssuesData.value = store.state.op_issues_data;

    countdown.value = negoSettingsData.value["BiddingTime"] * 60;
    remainingRounds.value = negoSettingsData.value["BiddingRounds"];
    totalRounds.value = negoSettingsData.value["BiddingRounds"] * 2;
    const domain = negoSettingsData.value["Domain"];

    domain_data_content.value = issuesData[domain];

    if (negoSettingsData.value["whoFirst"] === 2) {
        // 对方先手
        do_bidding(getRandomIndexVector(), '对方');
    }

    Object.keys(domain_data_content.value).forEach(key => {
        groceryStore.value[key] = domain_data_content.value[key];
    });

    Object.keys(domain_data_content.value).forEach(key => {
        agentSuggestion.value[key] = getRandomInterger(0, domain_data_content.value[key].length - 1);
        userSelections.value[key] = getRandomInterger(0, domain_data_content.value[key].length - 1);
    });
});

const getRandomInterger = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

const ChangeNegoState = (state_str) => {
    store.commit('setCurrNegoState', state_str);
    router.push('/finish');
};

const getIssue = (category, index) => {
    return domain_data_content.value[category][index];
};
// 初始化谈判的
// watch(
//     [
//         () => store.state.nego_initial_data
//     ],
//     () => {
//         const recommend = store.state.nego_initial_data.negotiation_obj.recommend;

//         Object.keys(agentSuggestion.value).forEach((key, index) => {
//             if (index < recommend.length) {
//                 agentSuggestion.value[key] = recommend[index];
//             }
//         });
//     },
//     { deep: true }
// );

const load_csv_and_png = (csv_path, png_path) => {
    store.commit("setFigurePath", png_path);
    store.commit("setCsvPath", csv_path);

};

// 倒计时结束的逻辑
const onCountdownEnd = () => {
    ElMessage({
        message: `您已超时！谈判结束...`,
        type: 'error',  // 提示类型
    });
    setTimeout(() => {
        ChangeNegoState("超时");
    }, 3000);
    // do_bidding(getRandomIndexVector());
};

const onRoundsEnd = () => {
    ElMessage({
        message: `谈判轮数用完！未达成协议，即将跳转至“查看结果”阶段...`,
        type: 'error',  // 提示类型
    });
    setTimeout(() => {
        ChangeNegoState("超出最大谈判轮数");
    }, 3000);
};

const stopCountdown = () => {
    if (timerId !== null) {
        clearInterval(timerId);
        timerId = null;
    }
};

const startCountdown = () => {
    stopCountdown();
    timerId = setInterval(() => {
        if (countdown.value > 0) {
            countdown.value--;
        } else {
            stopCountdown();
            onCountdownEnd();
        }
    }, 1000);
};

const formattedCountdown = computed(() => {
    const minutes = Math.floor(countdown.value / 60); // 计算分钟
    const seconds = countdown.value % 60; // 计算剩余秒数
    return `${minutes}分${seconds}秒`; // 返回格式化后的字符串
});

// 在组件销毁前停止计时器
onBeforeUnmount(() => stopCountdown());

// 启动倒计时
onMounted(() => startCountdown());

const route = useRoute();

watch(
    () => route.path, // 监听路由路径
    (newPath, oldPath) => {
        if (newPath === '/negotiation') {
            startCountdown(); // 如果是当前页面，启动倒计时
        } else {
            stopCountdown(); // 如果离开页面，停止倒计时
        }
    },
    { immediate: true } // 初始化时立即触发一次
);

// 计算属性：倒序排列出价历史
const reversedBidHistory = computed(() => {
    return [...bidHistory.value].reverse(); // 使用 reverse 返回倒序数组
});

// 控制提示显示状态的开关
const showHints = ref(false); // 默认不显示提示

// const getBidItemsByCategory = (bidContent) => {
//     return Object.keys(groceryStore.value).map((category, index) => {
//         const itemIndex = bidContent[index];
//         return groceryStore.value[category][itemIndex]; // 根据类别和索引获取商品
//     });
// };



const addBidHistory = (user, bid) => {
    const lastRound = bidHistory.value.at(-1)?.round || 0; // 获取最后一轮的 round 值
    const newEntry = {
        round: lastRound + 1,
        bidder: user,
        bidContent: bid
    };
    // 添加新数据到 bidHistory
    bidHistory.value.push(newEntry);
};


const do_bidding = (bid, bidder) => {
    // 重置时间
    if (bidder === '我方'){
        countdown.value = negoSettingsData.value["BiddingTime"];
        startCountdown();
    
        // const to_send = {
        //     user_offer: bid
        // }
    
        addBidHistory(bidder, bid);
        remainingRounds.value--;
        let op_bid = {};
        setTimeout(() => {
            Object.keys(domain_data_content.value).forEach(key => {
                op_bid[key] = getRandomInterger(0, domain_data_content.value[key].length - 1);
            });
            addBidHistory("对方", op_bid);
        }, 1000);
    }else{
        let op_bid = {};
        Object.keys(domain_data_content.value).forEach(key => {
            op_bid[key] = getRandomInterger(0, domain_data_content.value[key].length - 1);
        });
        addBidHistory("对方", op_bid);
    }
};

// 我方给出报价
// sendJson(4, to_send).then((return_data) => {
//     if (return_data.type === 1 && remainingRounds.value !== 0) {
//         // 继续谈判
//         addBidHistory("对方", return_data.op_next_offer);
//         Object.keys(agentSuggestion.value).forEach((key, index) => {
//             if (index < return_data.recommend.recommend.length) {
//                 agentSuggestion[key] = return_data.recommend.recommend[index];
//             }
//         });


//         ElMessage({
//             message: `对手已做出回应，并更新我方Agent给出的建议！`,
//             type: 'info',  // 提示类型
//         });
//     }
//     else if (return_data.type === 1 && remainingRounds.value === 0) {
//         // 谈判轮数用光
//         addBidHistory("对方", return_data.op_next_offer);
//         Object.keys(agentSuggestion.value).forEach((key, index) => {
//             if (index < return_data.recommend.recommend.length) {
//                 agentSuggestion.value[key] = return_data.recommend.recommend[index];
//             }
//         });

//         load_csv_and_png(
//             return_data.final_results.csv,
//             return_data.final_results.png
//         );

//         ElMessage({
//             message: `谈判轮数用完！未达成协议，即将跳转至“查看结果”阶段...`,
//             type: 'error',  // 提示类型
//         });
//         setTimeout(() => {

//             ChangeNegoState("roundmax");
//         }, 3000);

//     }
//     else if (return_data.type === 0) {
//         // 达成协议
//         load_csv_and_png(
//             return_data.final_results.csv,
//             return_data.final_results.png
//         );
//         ElMessage({
//             message: `对手同意我方的提议！即将跳转至“查看结果”阶段...`,
//             type: 'success',  // 提示类型
//         });
//         setTimeout(() => {

//             ChangeNegoState("succeed");
//         }, 3000);

//     }
//     else if (return_data.type === 2) {
//         // 对方拒绝
//         load_csv_and_png(
//             return_data.final_results.csv,
//             return_data.final_results.png
//         );
//         ElMessage({
//             message: `对手拒绝我方的提议！即将跳转至“查看结果”阶段...`,
//             type: 'error',  // 提示类型
//         });
//         setTimeout(() => {

//             ChangeNegoState("op_fail");
//         }, 3000);

//     }
//     else if (return_data.type === -1) {
//         // 超时
//         load_csv_and_png(
//             return_data.final_results.csv,
//             return_data.final_results.png
//         );
//         ElMessage({
//             message: `已达到谈判轮次上限！即将跳转至“查看结果”阶段...`,
//             type: 'error',  // 提示类型
//         });
//         setTimeout(() => {

//             ChangeNegoState("roundmax");
//         }, 3000);
//     }
//     else {
//     }
// });

// 处理出价按钮点击事件
const handleBidClick = () => {
    // bidHistory.value.push(({
    //     round: bidHistory.value.length + 1,
    //     bidder: "我方",
    //     bidContent: Object.values(userSelections.value)
    // }))
    do_bidding(userSelections.value, '我方');
};

const handleBidSuggestionClick = () => {
    userSelections.value = { ...agentSuggestion.value };
    Object.keys(domain_data_content.value).forEach(key => {
        agentSuggestion.value[key] = getRandomInterger(0, domain_data_content.value[key].length - 1);
    });
};

const handleAcceptClick = () => {
    ElMessage({
        message: `我方同意对手的提议！即将跳转至“查看结果”阶段...`,
        type: 'success',  // 提示类型
    });
    setTimeout(() => {
        ChangeNegoState("达成一致");
    }, 3000);
    // 我方同意
    // sendJson(5, {}).then((return_data) => {
    //     load_csv_and_png(
    //         return_data.final_results.csv,
    //         return_data.final_results.png
    //     );
    //     ElMessage({
    //         message: `我方同意对手的提议！即将跳转至“查看结果”阶段...`,
    //         type: 'success',  // 提示类型
    //     });
    //     setTimeout(() => {

    //         ChangeNegoState("succeed");
    //     }, 3000);
    // });
};

const handleRejectClick = () => {
    // // 我方拒绝
    // sendJson(6, {}).then((return_data) => {
    //     load_csv_and_png(
    //         return_data.final_results.csv,
    //         return_data.final_results.png
    //     );
    //     ElMessage({
    //         message: `我方拒绝对手的提议！即将跳转至“查看结果”阶段...`,
    //         type: 'error',  // 提示类型
    //     });
    //     setTimeout(() => {

    //         ChangeNegoState("my_fail");
    //     }, 3000);
    // });
    ElMessage({
        message: `我方拒绝对手的提议！即将跳转至“查看结果”阶段...`,
        type: 'error',  // 提示类型
    });
    setTimeout(() => {
        ChangeNegoState("拒绝谈判");
    }, 3000);
};

const handleShowSuggestions = () => {
    showHints.value = !showHints.value;
};



</script>


<script lang="js">
export default {
    methods: {
        setRowClass(row) {



            const x = row.row.bidder === '我方' ? 'white-row' : 'gray-row';
            console.log("eeeee", row, row.row.bidder, x);
            return x;
        }
    }
};
</script>

<style scoped>
body {
    margin: 0;
    /* 禁止页面滚动 */
}

.container {
    display: flex;
    height: 100%;
    box-sizing: border-box;
}

.left-panel {
    width: 40%;
    padding: 20px;
    box-sizing: border-box;
    background-color: #f5f5f5;
}

.right-panel {
    /* flex: 0 0 60%; */
    width: 60%;
    padding: 20px;
    box-sizing: border-box;
    overflow: hidden;
}

.status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    font-size: 20px;
    font-weight: bold;
}

.table-container {
    height: 90%;
    /* 留出顶部状态栏的空间 */
    overflow-y: auto;
}

.history-table {
    width: 100%;
}

.suggestion-table {
    margin: 0 0;
    width: 100%;
}

::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
    background: #e0dfe1;
}
</style>