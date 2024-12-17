<script setup lang="js">
import { ref, reactive, onMounted, computed, watch, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';

import { useRoute } from 'vue-router';

import { useStore } from 'vuex'; 
import { sendJson } from './SendMessage';



// 初始倒计时
const countdown = ref(null);
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

    countdown.value=negoSettingsData.value["BiddingTime"]*60;
    remainingRounds.value=negoSettingsData.value["BiddingRounds"];
    
    const domain= negoSettingsData.value["Domain"];

    
    domain_data_content.value=issuesData[domain];

    // console.log("aaa",issuesData[domain],domain_data_content.value);


    Object.keys(domain_data_content.value).forEach(key => {
        // console.log("bbb",key);
        groceryStore[key] = domain_data_content.value[key] || [];
        userSelections[key] = groceryStore[key][0];
    });

    // 初始化agentSuggestion，每个都选第一个，测试用
    Object.keys(domain_data_content.value).forEach(key => {
        // agentSuggestion[key] = domain_data_content.value[key][0] || [];
        agentSuggestion[key] = 0;
    });
    

});


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





// 定义计时器 ID，确保唯一性
let timerId = null;

// 倒计时结束的逻辑
const onCountdownEnd = () => {
    // alert('倒计时结束！触发逻辑。');
    // 超时 结束
    sendJson(7,{});
};

const formatBidHistory = formatHistory(bidHistory, groceryStore)

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
    const to_send={
        user_offer: my_bid
    }

    addBidHistory("我方",my_bid);

    // 我方给出报价
    sendJson(4,to_send).then((return_data) => {
        addBidHistory("对方",return_data.op_next_offer);
        Object.keys(agentSuggestion).forEach((key, index) => {
            if (index < return_data.recommend.recommend.length) {
                agentSuggestion[key] = return_data.recommend.recommend[index];
            }
        });
        remainingRounds.value--;

        // 检查剩余回合数是否为 0
        if (remainingRounds.value === 0) {
            handleFinalRoundEnd(); 
        }

    }).catch((error) => {
      console.error("Error ", error);
    });
};

const handleFinalRoundEnd = () => {
    ElMessage({
        message: `谈判轮次已用完！`,
        type: 'info',  // 提示类型
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
    sendJson(5,{});

};

const handleRejectClick = () => {

    // 我方终止
    sendJson(6,{});

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


<template>
    <div class="bidding-input">
        <div class="ending">
            <p>剩余轮数: {{ remainingRounds }} 轮</p>
            <p>倒计时: {{ formattedCountdown }}</p>
        </div>
        <!-- 倒计时显示 -->
        <div class="countdown-timer">
            倒计时: {{ formattedCountdown }}
        </div>

        <!-- 四个子页面 -->
        <div v-for="(page, index) in subPages" :key="index" class="subpage">
            <h3>{{ page.title }}</h3>
            <p>{{ page.content }}</p>
            <!-- 仅在第一个子页面显示横向排列的下拉菜单 -->
            <div v-if="index === 0" class="horizontal-options">
                <div v-for="(items, category) in groceryStore" :key="category" class="option-group">
                    <label :for="category">{{ category }}</label>
                    <select :id="category" v-model="userSelections[category]">
                        <option v-for="item in items" :key="item" :value="item">{{ item }}</option>
                    </select>
                </div>
            </div>

            <div v-if="index === 1" class="agent-suggestion">
                <!-- 查看提示复选框 -->
                <div style="margin-bottom: 10px;">
                <label>
                    <input type="checkbox" v-model="showHints" />
                    查看提示
                </label>
                </div>

                <!-- 提示表格 -->
                <el-table :data="[agentSuggestion]" style="width: 100%">
                <el-table-column
                    v-for="(category, index) in Object.keys(agentSuggestion)"
                    :key="index"
                    :label="category"
                    :prop="category"
                >
                    <template #default>
                    <span>
                        <!-- {{ showHints ? agentSuggestion[category] : "?" }} -->
                        {{ showHints ? domain_data_content[category][agentSuggestion[category]] : "?" }}
                        <!-- {{ showHints ? index : "?" }} -->
                        
                    </span>
                    </template>
                </el-table-column>
                </el-table>
            </div>




            <!-- <div v-if="index === 2" class="scrollable-table">
                <el-table :data="reversedBidHistory" style="width: 100%">
                <el-table-column label="轮次" prop="round"></el-table-column>
                <el-table-column label="出价方" prop="bidder"></el-table-column>

                
                <template v-for="(items, category) in groceryStore" :key="category">
                    <el-table-column :label="category">
                    <template #default="{ row }">
                        <span>{{ getBidItemsByCategory(row.bidContent)[Object.keys(groceryStore).indexOf(category)] }}</span>
                    </template>
                    </el-table-column>
                </el-table>
            </div> -->

            <div v-if="index === 2" class="scrollable-table">
                <el-table 
                    :data="reversedBidHistory" 
                    style="width: 100%" 
                    :row-class-name="setRowClass"
                    
                >
                    <el-table-column label="轮次" prop="round"></el-table-column>
                    <el-table-column label="出价方" prop="bidder"></el-table-column>

                    <!-- 遍历 groceryStore 中的所有商品类别 -->
                    <template v-for="(items, category) in groceryStore" :key="category" >
                        <el-table-column :label="category">
                            <template #default="{ row }">
                                <span>{{ getBidItemsByCategory(row.bidContent)[Object.keys(groceryStore).indexOf(category)] }}</span>
                            </template>
                        </el-table-column>
                    </template>
                </el-table>
            </div>



            <div v-if="index === 3" class="image-display">
                <img src="@/assets/3.png" alt="展示图片" style="max-width: 100%; height: auto;">
            </div>


        </div>
    </div>

    <!-- 底部按钮 -->
    <div class="button-container-bidding" style="margin-top: 20px; text-align: center;">
        <!--<el-button type="primary" @click="handleTest">测试</el-button> -->
        <el-button type="primary" @click="handleBidClick">出价</el-button>
        <el-button type="primary" @click="handleBidSuggestionClick">按照代理建议出价</el-button>
        <el-button type="success" @click="handleAcceptClick">接受</el-button>
        <el-button type="danger" @click="handleRejectClick">拒绝</el-button>
    </div>
</template>

<style>
.bidding-input {
    width: 40%;
    height: 100%;
    margin: 10px;
    padding: 10px;
}

.bidding-input .el-select {
    --el-select-width: 200px;
}

.bidding-input .el-form-item__label {
    color:black;
}
.ending {
    display: flex;
    margin: 10px 0;
    font-size: larger;
    justify-content:space-between;
    font-weight: bolder;
}

.display {
    width: 60%;
    height: 100%;
    overflow: scroll;
    text-align: right;
}

.display .el-table tr{
    background-color: rgb(226, 240, 203);
}

.el-table tbody tr{
    pointer-events: none;
}


/* .white-row {
    background-color: #ffffff; 
}
.gray-row {
    background-color: #949494; 
} */


::v-deep(.white-row) tr {
    background-color: #ffffff !important;
}

::v-deep(.gray-row) tr {
    background-color: #f5f5f5 !important;
}
</style>