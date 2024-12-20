<template>
    <div class="container">
        <!-- 左侧部分 -->
        <div class="left-panel">
            <div class='status-bar'>我的出价</div>
            <el-form>
                <el-form-item v-for="key in negotiation.interests" :label="key" :key="key">
                    <el-select v-model="userSelections[key]">
                        <el-option v-for="item, idx in negotiation.issues[key]" :key="idx" :value="item" :label="item">
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
                    <div>
                        <h3>AI推荐出价  <el-icon><StarFilled color="gold" /></el-icon></h3>
                        <!-- <el-icon></el-icon> -->
                    </div>
                    <el-table :data="[agentSuggestion]" class="suggestion-table"
                        :header-cell-style="{ background: '#eef1f6', color: '#000000' }">
                        <!-- <el-table-column > -->
                            <el-table-column v-for="key in Object.keys(agentSuggestion)" :key="key" :label="key"
                                :prop="key">
                                <template #default>
                                    <span>{{ showHints ? agentSuggestion[key] : "?"
                                        }}</span>
                                </template>
                            </el-table-column>
                        <!-- </el-table-column> -->
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
                <div>剩余时间：{{ remainingTime }}</div>
            </div>
            <div class="table-container">
                <el-table :data="reversedBidHistory" class="history-table" stripe>
                    <el-table-column label="轮次" prop="round"></el-table-column>
                    <el-table-column label="出价方" prop="bidder"></el-table-column>
                    <template v-for="key in negotiation.interests" :key="key">
                        <el-table-column :label="key">
                            <template #default="{ row }">
                                <span>{{ row.bidContent[key] }}</span>
                            </template>
                        </el-table-column>
                    </template>
                </el-table>
            </div>
        </div>
    </div>
    <footerComp previous="上一步" previousDetail="谈判准备" :showPrevious=true :showNext=false
        @previous-page="goToPreviousPage" style="width: 100%;" />
</template>

<script setup lang="js">
import footerComp from '../components/footer.vue';
import { ref, onMounted, computed, watch, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { sendJson } from './SendMessage';
import { ElMessage } from 'element-plus';
import { StarFilled } from '@element-plus/icons-vue';
const router = useRouter();
const goToPreviousPage = () => {
    router.push('/preparation');
}
// 获取 Vuex store 实例
const store = useStore();
const prepare = computed(() => store.state.prepare);
const negotiation = ref({
    domain: prepare.value.domain,
    roles: {
        my: prepare.value.roles.my,
        opponent: prepare.value.roles.opponent
    },
    first: prepare.value.first,
    rounds: prepare.value.rounds,
    time: prepare.value.time,
    interests: Object.keys(prepare.value.my_interests),
    issues: Object.fromEntries(
        Object.entries(prepare.value.my_interests).map(([key, value]) => [key, Object.keys(prepare.value.my_issues[key])])
    )
})


const remainingRounds = ref(null);
const agentSuggestion = ref({});
// 定义计时器 ID，确保唯一性
let timerId = null;
// 初始倒计时
const countdown = ref(null);

// 格式化倒计时为 "xxx分xxx秒" 格式
const remainingTime = computed(() => {
    const minutes = Math.floor(countdown.value / 60); // 计算分钟
    const seconds = countdown.value % 60; // 计算剩余秒数
    return `${minutes}分${seconds}秒`; // 返回格式化后的字符串
});

onMounted(() => {
    remainingRounds.value = negotiation.value.rounds;
    countdown.value = negotiation.value.time;
    negotiation.value.interests.forEach(key => {
        agentSuggestion.value[key] = negotiation.value.issues[key][0];
    });
});

// 倒计时结束的逻辑
// const onCountdownEnd = () => {
//     ElMessage({
//         message: `您已超时！谈判结束...`,
//         type: 'warning',  // 提示类型
//     });
//     sendJson(7, {});
// };

// const stopCountdown = () => {
//     if (timerId !== null) {
//         clearInterval(timerId);
//         timerId = null;
//     }
// };


// // 修改 startCountdown 函数
// const startCountdown = () => {
//     stopCountdown();
//     timerId = setInterval(() => {
//         if (countdown.value > 0) {
//             countdown.value--;
//         } else {
//             stopCountdown();
//             onCountdownEnd();
//         }
//     }, 1000);
// };

const userSelections = ref({});


const bidHistory = ref([]);
const reversedBidHistory = computed(() => bidHistory.value.slice().reverse());


const ChangeNegoState = (state_str) => {
    store.commit('setCurrNegoState', state_str);
};



const load_csv_and_png = (csv_path, png_path) => {
    store.commit("setFigurePath", png_path);
    store.commit("setCsvPath", csv_path);

};

const showHints = ref(false); // 默认不显示提示


const addBidHistory = (user, bid) => {
    const lastRound = bidHistory.value.at(-1)?.round || 0; // 获取最后一轮的 round 值
    const newEntry = {
        round: lastRound + 1,
        bidder: user,
        bidContent: bid
    };

    // bid是向量

    // 添加新数据到 bidHistory
    bidHistory.value.push(newEntry);
};

const do_bidding = (my_bid) => {
    // 重置时间
    countdown.value = negoSettingsData.value["BiddingTime"];
    // startCountdown();

    const to_send = {
        user_offer: my_bid
    }

    addBidHistory("我方", my_bid);
    remainingRounds.value--;

    // 我方给出报价
    sendJson(4, to_send).then((return_data) => {
        if (return_data.type === 1 && remainingRounds.value !== 0) {
            // 继续谈判
            addBidHistory("对方", return_data.op_next_offer);
            Object.keys(agentSuggestion).forEach((key, index) => {
                if (index < return_data.recommend.recommend.length) {
                    agentSuggestion[key] = return_data.recommend.recommend[index];
                }
            });


            ElMessage({
                message: `对手已做出回应，并更新我方Agent给出的建议！`,
                type: 'info',  // 提示类型
            });
        }
        else if (return_data.type === 1 && remainingRounds.value === 0) {
            // 谈判轮数用光
            addBidHistory("对方", return_data.op_next_offer);
            Object.keys(agentSuggestion).forEach((key, index) => {
                if (index < return_data.recommend.recommend.length) {
                    agentSuggestion[key] = return_data.recommend.recommend[index];
                }
            });

            load_csv_and_png(
                return_data.final_results.csv,
                return_data.final_results.png
            );

            ElMessage({
                message: `谈判轮数用完！未达成协议，即将跳转至“查看结果”阶段...`,
                type: 'error',  // 提示类型
            });
            setTimeout(() => {

                ChangeNegoState("roundmax");
            }, 3000);

        }
        else if (return_data.type === 0) {
            // 达成协议
            load_csv_and_png(
                return_data.final_results.csv,
                return_data.final_results.png
            );
            ElMessage({
                message: `对手同意我方的提议！即将跳转至“查看结果”阶段...`,
                type: 'success',  // 提示类型
            });
            setTimeout(() => {

                ChangeNegoState("succeed");
            }, 3000);

        }
        else if (return_data.type === 2) {
            // 对方拒绝
            load_csv_and_png(
                return_data.final_results.csv,
                return_data.final_results.png
            );
            ElMessage({
                message: `对手拒绝我方的提议！即将跳转至“查看结果”阶段...`,
                type: 'error',  // 提示类型
            });
            setTimeout(() => {

                ChangeNegoState("op_fail");
            }, 3000);

        }
        else if (return_data.type === -1) {
            // 超时
            load_csv_and_png(
                return_data.final_results.csv,
                return_data.final_results.png
            );
            ElMessage({
                message: `已达到谈判轮次上限！即将跳转至“查看结果”阶段...`,
                type: 'error',  // 提示类型
            });
            setTimeout(() => {

                ChangeNegoState("roundmax");
            }, 3000);


        }
        else {

        }



    }).catch((error) => {
        console.error("Error ", error);
    });
};

const handleShowSuggestions = () => {
    showHints.value = !showHints.value;
};

const bidder = ref(true); // true 代表我方出价，false 代表对方出价

// 处理出价按钮点击事件
const handleBidClick = () => {
    console.log("userSelections", userSelections.value);
    bidHistory.value.push({
        round: bidHistory.value.length + 1,
        bidder: bidder.value ? "对方" : "我方",
        bidContent: {...userSelections.value}
    })
    bidder.value = !bidder.value;

    // const selectionIndices = Object.keys(userSelections).map(category => {
    //     const selectedItem = userSelections[category];
    //     const items = negotiation.value.issues[category];
    //     const index = items.indexOf(selectedItem); // 获取每个选项在列表中的索引
    //     return index; // 返回该类别选项的索引
    // });
    // console.log(selectionIndices, 'selectionIndices');
};

const handleAcceptClick = () => {
    // 我方同意
    sendJson(5, {}).then((return_data) => {
        load_csv_and_png(
            return_data.final_results.csv,
            return_data.final_results.png
        );
        ElMessage({
            message: `我方同意对手的提议！即将跳转至“查看结果”阶段...`,
            type: 'success',  // 提示类型
        });
        setTimeout(() => {
            ChangeNegoState("succeed");
        }, 3000);
    });
};

const handleRejectClick = () => {
    sendJson(6, {}).then((return_data) => {
        load_csv_and_png(
            return_data.final_results.csv,
            return_data.final_results.png
        );
        ElMessage({
            message: `我方拒绝对手的提议！即将跳转至“查看结果”阶段...`,
            type: 'error',  // 提示类型
        });
        setTimeout(() => {
            ChangeNegoState("my_fail");
        }, 3000);
    });

};

const handleBidSuggestionClick = () => {
    // 浅拷贝 避免引用同一个对象
    userSelections.value = { ...agentSuggestion.value };
}

// const finish = ref({
//     result: '',
//     last_player: '',
//     last_bid: ''
// })


</script>



<style scoped>
body {
    margin: 0;
    overflow: hidden;
    /* 禁止页面滚动 */
}

.container {
    display: flex;
    height: 85vh;
    box-sizing: border-box;
    overflow: hidden;
}

.left-panel {
    width: 40%;
    padding: 20px;
    box-sizing: border-box;
    overflow: hidden;
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
