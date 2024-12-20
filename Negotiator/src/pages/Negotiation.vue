<<<<<<< HEAD
<script setup lang="js">
import { ref, reactive, onMounted, computed, watch, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';

import { useRoute } from 'vue-router';

import { useStore } from 'vuex'; 
import { sendJson } from './SendMessage';



// 初始倒计时
const countdown = ref(null);
const remainingRounds=ref(null);

// 子页面数据定义
const subPages = ref([
    { title: '我的出价', content: '' },
    { title: '我方Agent建议出价', content: '' },
    { title: '出价历史', content: '' },
    // { title: '实时图片', content: '边界' },
]);
const remainingRounds = ref(0);
const agentSuggestionDisplay = ref(true);
const bid = ref({});

// 商品分类数据
const groceryStore = reactive({});

// 出价历史数据，包含轮次、出价方和出价内容（索引数组）
const bidHistory = ref([]);

// 假设 agent 提供了一个出价建议
const agentSuggestion=reactive({});




// 获取 Vuex store 实例
const store = useStore();

// 定义响应式变量，用于存储 Vuex 数据
const negoSettingsData = ref(null);
const myInterestsData = ref(null);
const myIssuesData = ref(null);
const opInterestsData = ref(null);
const opIssuesData = ref(null);

const domain_data_content=ref(null);

// 在组件挂载时从 Vuex 获取数据
onMounted(() => {
  negoSettingsData.value = store.state.nego_settings_data;
  myInterestsData.value = store.state.my_interests_data;
  myIssuesData.value = store.state.my_issues_data;
  opInterestsData.value = store.state.op_interests_data;
  opIssuesData.value = store.state.op_issues_data;

  // 打印加载的 Vuex 数据
//   console.log('加载的 Nego Settings:', negoSettingsData.value);
//   console.log('加载的 My Interests:', myInterestsData.value);
//   console.log('加载的 My Issues:', myIssuesData.value);
//   console.log('加载的 Op Interests:', opInterestsData.value);
//   console.log('加载的 Op Issues:', opIssuesData.value);

    countdown.value=negoSettingsData.value["BiddingTime"];
    // countdown.value=negoSettingsData.value["BiddingTime"]*60;
    remainingRounds.value=negoSettingsData.value["BiddingRounds"];
    
    const domain= negoSettingsData.value["Domain"];

    
    domain_data_content.value=issuesData[domain];

    // console.log("aaa",issuesData[domain],domain_data_content.value);


    Object.keys(domain_data_content.value).forEach(key => {
        // console.log("bbb",key);
        groceryStore[key] = domain_data_content.value[key] || [];
        userSelections[key] = groceryStore[key][0];
    });

    // console.log("ffffffffff",groceryStore);

    // 初始化agentSuggestion，每个都选第一个，测试用
    Object.keys(domain_data_content.value).forEach(key => {
        // agentSuggestion[key] = domain_data_content.value[key][0] || [];
        agentSuggestion[key] = 0;
    });
    

});

const ChangeNegoState = (state_str) => {
    store.commit('setCurrNegoState', state_str);

};


// 初始化谈判的
watch(
  [
    () => store.state.nego_initial_data
  ],
  () => {
    console.log('谈判中，store.state.nego_initial_data：', store.state.nego_initial_data);
    const  recommend=store.state.nego_initial_data.negotiation_obj.recommend;

    console.log(recommend);
    

    Object.keys(agentSuggestion).forEach((key, index) => {
        if (index < recommend.length) {
            agentSuggestion[key] = recommend[index];
        }
    });

    console.log(agentSuggestion);
    ElMessage({
        message: `已更新我方Agent给出的建议！`,
        type: 'info',  // 提示类型
    });



  },
  { deep: true }
);

const load_csv_and_png=(csv_path,png_path)=>{
    store.commit("setFigurePath",png_path);
    store.commit("setCsvPath",csv_path);

};



// 定义计时器 ID，确保唯一性
let timerId = null;


const getRandomIndexVector=() => {
    const indexVector = [];

    // 遍历 groceryStore 对象
    for (const category in groceryStore) {
        // 获取当前类别的项
        const items = groceryStore[category];

        // 随机选择一个元素的索引
        const randomIndex = Math.floor(Math.random() * items.length);
        
        // 将选中的索引添加到向量中
        indexVector.push(randomIndex);
    }

    return indexVector;
}


// 倒计时结束的逻辑
const onCountdownEnd = () => {
    // alert('倒计时结束！触发逻辑。');
    // 超时 结束
    ElMessage({
        message: `您已超时！已为您随机挑选一个出价...`,
        type: 'warning',  // 提示类型
    });
    // getRandomIndexVector();
    do_bidding( getRandomIndexVector());
    sendJson(7,{});
};

const stopCountdown = () => {
    if (timerId !== null) {
        clearInterval(timerId);
        timerId = null;
    }
};

// 修改 startCountdown 函数
const startCountdown = () => {
    stopCountdown(); // 确保之前的计时器被清除
    timerId = setInterval(() => {
        if (countdown.value > 0) {
            countdown.value--;
        } else {
            stopCountdown();
            onCountdownEnd();
        }
    }, 1000);
};

// 格式化倒计时为 "xxx分xxx秒" 格式
const formattedCountdown = computed(() => {
  const minutes = Math.floor(countdown.value / 60); // 计算分钟
  const seconds = countdown.value % 60; // 计算剩余秒数
  return `${minutes}分${seconds}秒`; // 返回格式化后的字符串
});

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


const getBidItemsByCategory = (bidContent) => {
    return Object.keys(groceryStore).map((category, index) => {
        const itemIndex = bidContent[index];
        return groceryStore[category][itemIndex]; // 根据类别和索引获取商品
    });
};

// 用户选择结果
const userSelections = reactive(
    Object.fromEntries(Object.keys(groceryStore).map(category => [category, groceryStore[category][0]]))
);


const addBidHistory = (user, bid)=>{
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


const do_bidding = (my_bid)=>{
    // 重置时间
    countdown.value=negoSettingsData.value["BiddingTime"];
    startCountdown();

    const to_send={
        user_offer: my_bid
    }

    addBidHistory("我方",my_bid);
    remainingRounds.value --;

    // 我方给出报价
    sendJson(4,to_send).then((return_data) => {
        if (return_data.type === 1 && remainingRounds.value!==0){
            // 继续谈判
            addBidHistory("对方",return_data.op_next_offer);
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
        else if (return_data.type === 1 && remainingRounds.value===0){
            // 谈判轮数用光
            addBidHistory("对方",return_data.op_next_offer);
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
        else if(return_data.type === 0){
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
        else if(return_data.type === 2){
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
        else if(return_data.type === -1){
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
        else{

        }



    }).catch((error) => {
      console.error("Error ", error);
    });
};


// const handleTest = () =>{
//     // 测试，加入一组随机
//     ElMessage({
//         message: `这是一个测试按钮，模拟向history中增加信息`,
//         type: 'info',  // 提示类型
//     });

//     const lastRound = bidHistory.value.at(-1)?.round || 0; // 获取最后一轮的 round 值
//     const newEntry = {
//         round: lastRound + 1,
//         bidder: Math.random() > 0.5 ? "我方" : "对方", // 随机选择 bidder
//         bidContent: [0,1,2,0,3,1] // 随机生成出价内容
//     };

//     // 添加新数据到 bidHistory
//     bidHistory.value.push(newEntry);
// };

// 处理出价按钮点击事件
const handleBidClick = () => {
    const selectionIndices = Object.keys(userSelections).map(category => {
        const selectedItem = userSelections[category];
        const items = groceryStore[category];
        const index = items.indexOf(selectedItem); // 获取每个选项在列表中的索引
        return index; // 返回该类别选项的索引
    });

    do_bidding(selectionIndices);
};

const handleBidSuggestionClick = () => {
    const selectionIndices = Object.values(agentSuggestion);
    do_bidding(selectionIndices);
};

const handleAcceptClick = () => {
    // 我方同意
    sendJson(5,{}).then((return_data)=>{
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
    // 我方拒绝
    sendJson(6,{}).then((return_data)=>{
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





</script>


<script lang="js">
export default {
    methods: {
        setRowClass(row) {
            


            const x = row.row.bidder === '我方' ? 'white-row' : 'gray-row';
            console.log("eeeee",row,  row.row.bidder,x);
            return x;
        }
    }
};
</script>


=======
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
<template>
    <div class="container">
        <!-- 左侧部分 -->
        <div class="left-panel">
            <div class='status-bar'>我的出价</div>
            <el-form>
                <el-form-item v-for="key in negotiation.interests" :label="key" :key="key">
                    <el-select v-model="userSelections[key]">
                        <el-option v-for="item in negotiation.issues[key]" :key="item" :value="item"
                            :label="item"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleBidClick">出价</el-button>
                    <el-button type="success" @click="handleAcceptClick">接受</el-button>
                    <el-button type="danger" @click="handleRejectClick">结束</el-button>
                    <el-button @click="handleShowSuggestions">
                        {{ showHints ? '隐藏AI推荐' : '查看AI推荐' }}
                    </el-button>
                </el-form-item>
                <el-form-item v-show="showHints">
                    <el-table :data="[agentSuggestion]" class="suggestion-table"
                        :header-cell-style="{ background: '#eef1f6', color: '#000000' }">
                        <el-table-column label="AI推荐出价">
                            <el-table-column v-for="key in Object.keys(agentSuggestion)" :key="key" :label="key"
                                :prop="key">
                                <template #default>
                                    <span>{{ showHints ? agentSuggestion[key] : "?"
                                        }}</span>
                                </template>
                            </el-table-column>
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
                <div>剩余时间：{{ remainingTime }}</div>
            </div>
            <div class="table-container">
                <el-table :data="reversedBidHistory" class="history-table">
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
<<<<<<< HEAD



            <!-- <div v-if="index === 3" class="image-display">
                <img src="@/assets/3.png" alt="展示图片" style="max-width: 100%; height: auto;">
            </div> -->


=======
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
        </div>

        <!-- 底部 -->
    </div>
    <footerComp previous="上一步" previousDetail="谈判准备" :showPrevious=true :showNext=false
        @previous-page="goToPreviousPage" style="width: 100%;" />
</template>

<script setup lang="js">
import footerComp from '../components/footer.vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const goToPreviousPage = () => {
    router.push('/preparation');
}

import { ref, computed } from 'vue';
import { useStore } from 'vuex';
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
// 成功获取数据,可以开始谈判

const userSelections = ref(Object.fromEntries(negotiation.value.interests.map(key => [key, ''])));

const showHints = ref(false);

const finish = ref({
    result: '',
    last_player: '',
    last_bid: ''
})

const handleBidClick = () => {
    console.log('出价');
}
const handleAcceptClick = () => {
    finish.value.result = 'accept';
    finish.value.last_player = BidHistory.value[0].bidder;
    finish.value.last_bid = BidHistory.value[0].bidContent;
    store.commit('setFinish', finish.value);
    router.push('/finish');
    console.log('接受');
}
const handleRejectClick = () => {
    finish.value.result = 'reject';
    finish.value.last_player = BidHistory.value[0].bidder;
    finish.value.last_bid = BidHistory.value[0].bidContent;
    store.commit('setFinish', finish.value);
    router.push('/finish');
    console.log('结束');
}

const handleShowSuggestions = () => {
    showHints.value = !showHints.value;
}

const handleBidSuggestionClick = () => {
    userSelections.value = agentSuggestion.value;
    console.log('导入推荐出价');
}

const agentSuggestion = ref(Object.fromEntries(negotiation.value.interests.map(key => [key, negotiation.value.issues[key][0]])));

const remainingRounds = ref(negotiation.value.rounds);
const remainingTime = ref(negotiation.value.time);

const BidHistory = ref([
    { round: 1, bidder: '买家', bidContent: { '技术': '技术一', '商务': '商务二' } }, 
    { round: 2, bidder: '卖家', bidContent: { '电子产品': 150, '服装': 250 } }
]);
const reversedBidHistory = computed(() => BidHistory.value.slice().reverse());

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
</style>
