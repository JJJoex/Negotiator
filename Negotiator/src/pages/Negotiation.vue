<script setup lang="js">
import { ref, reactive, onMounted , computed  } from 'vue';
import { ElMessage } from 'element-plus';  // 引入 ElMessage 用于 Toast 提示

// 初始倒计时设置为 100 秒
const countdown = ref(100);

// 定义计时器 ID，确保唯一性
let timerId = null;

// 倒计时结束的逻辑
const onCountdownEnd = () => {
    alert('倒计时结束！触发逻辑。');
};

// 开始倒计时
const startCountdown = () => {
    timerId = setInterval(() => {
        if (countdown.value > 0) {
            countdown.value--;
        } else {
            clearInterval(timerId); // 停止计时器
            onCountdownEnd(); // 调用倒计时结束逻辑
        }
    }, 1000); // 每秒减少 1
};

// 启动倒计时
onMounted(() => startCountdown());

// 子页面数据定义
const subPages = ref([
    { title: '我的出价', content: '' },
    { title: '我方Agent建议出价', content: '' },
    { title: '子页面3', content: '这里是子页面3的内容' },
    { title: '子页面4', content: '这里是子页面4的内容' },
]);

// 商品分类数据
const groceryStore = reactive({
    "面包类": ["法棍", "饼干", "羊角面包", "普通面包"],
    "水果类": ["苹果", "香蕉", "樱桃", "葡萄", "梨", "瓜", "草莓"],
    "零食类": ["巧克力棒", "甜甜圈", "玉米片", "爆米花", "薯片", "糖果", "饼干"],
    "酱料类": ["奶酪", "果酱", "花生酱", "三明治酱", "巧克力酱", "火腿", "萨拉米香肠", "蛋沙拉"],
    "蔬菜类": ["豆子", "西兰花", "韭菜", "土豆", "菠菜", "胡萝卜", "西红柿"],
    "饮料类": ["能量饮料", "牛奶", "茶", "咖啡", "果汁", "可乐", "芬达", "啤酒", "葡萄酒"]
});

// 出价历史数据，包含轮次、出价方和出价内容（索引数组）
const bidHistory = ref([
    { round: 1, bidder: "我方", bidContent: [0, 1, 3, 0, 4, 5] },
    { round: 2, bidder: "对方", bidContent: [2, 3, 1, 0, 5, 2] },
    { round: 3, bidder: "我方", bidContent: [0, 1, 3, 0, 4, 5] },
    { round: 4, bidder: "对方", bidContent: [2, 3, 1, 0, 5, 2] },
    { round: 5, bidder: "我方", bidContent: [0, 1, 3, 0, 4, 5] },
    { round: 6, bidder: "对方", bidContent: [2, 3, 1, 0, 5, 2] },
    { round: 7, bidder: "我方", bidContent: [0, 1, 3, 0, 4, 5] },
    { round: 8, bidder: "对方", bidContent: [2, 3, 1, 0, 5, 2] },
    { round: 9, bidder: "我方", bidContent: [0, 1, 3, 0, 4, 5] },
    { round: 10, bidder: "对方", bidContent: [2, 3, 1, 0, 5, 2] },
    { round: 11, bidder: "我方", bidContent: [3, 0, 2, 1, 3, 4] }
]);

// 计算属性：倒序排列出价历史
const reversedBidHistory = computed(() => {
  return [...bidHistory.value].reverse(); // 使用 reverse 返回倒序数组
});

// 假设 agent 提供了一个出价建议
const agentSuggestion = reactive({
    "面包类": "饼干",  // agent 提供的建议
    "水果类": "苹果",
    "零食类": "巧克力棒",
    "酱料类": "奶酪",
    "蔬菜类": "西兰花",
    "饮料类": "能量饮料"
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


const handleTest = () =>{
    // 测试，加入一组随机
    ElMessage({
        message: `这是一个测试按钮，模拟向history中增加信息`,
        type: 'info',  // 提示类型
    });

    const lastRound = bidHistory.value.at(-1)?.round || 0; // 获取最后一轮的 round 值
    const newEntry = {
        round: lastRound + 1,
        bidder: Math.random() > 0.5 ? "我方" : "对方", // 随机选择 bidder
        bidContent: [0,1,2,0,3,1] // 随机生成出价内容
    };

    // 添加新数据到 bidHistory
    bidHistory.value.push(newEntry);
};

// 处理出价按钮点击事件
const handleBidClick = () => {
    const selectionIndices = Object.keys(userSelections).map(category => {
        const selectedItem = userSelections[category];
        const items = groceryStore[category];
        const index = items.indexOf(selectedItem); // 获取每个选项在列表中的索引
        return index; // 返回该类别选项的索引
    });

    // 使用 ElMessage 显示用户选择的索引数组
    ElMessage({
        message: `选择的选项索引: [${selectionIndices.join(', ')}]`,
        type: 'info',  // 提示类型
    });
};
</script>

<template>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 10px; border: 1px solid black; position: relative;">
        <!-- 倒计时显示 -->
        <div class="countdown-timer">
            倒计时: {{ countdown }} 秒
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
                        {{ showHints ? agentSuggestion[category] : "?" }}
                    </span>
                    </template>
                </el-table-column>
                </el-table>
            </div>


            <!-- <div v-if="index === 2">
                <el-table :data="bidHistory" style="width: 100%">
                    <el-table-column label="轮次" prop="round"></el-table-column>
                    <el-table-column label="出价方" prop="bidder"></el-table-column>

                    
                    <template v-for="(items, category) in groceryStore" :key="category">
                        <el-table-column :label="category">
                            <template #default="{ row }">
                                <span>{{ getBidItemsByCategory(row.bidContent)[Object.keys(groceryStore).indexOf(category)] }}</span>
                            </template>
                        </el-table-column>
                    </template>
                </el-table>
            </div> -->

            <div v-if="index === 2" class="scrollable-table">
                <el-table :data="reversedBidHistory" style="width: 100%">
                <el-table-column label="轮次" prop="round"></el-table-column>
                <el-table-column label="出价方" prop="bidder"></el-table-column>

                <!-- 遍历 groceryStore 中的所有商品类别 -->
                <template v-for="(items, category) in groceryStore" :key="category">
                    <el-table-column :label="category">
                    <template #default="{ row }">
                        <span>{{ getBidItemsByCategory(row.bidContent)[Object.keys(groceryStore).indexOf(category)] }}</span>
                    </template>
                    </el-table-column>
                </template>
                </el-table>
            </div>

            <div v-if="index === 3" class="image-display">
                <img src="@/assets/3.jpg" alt="展示图片" style="max-width: 100%; height: auto;">
            </div>


        </div>
    </div>

    <!-- 底部按钮 -->
    <div style="margin-top: 20px; text-align: center;">
        <el-button type="primary" @click="handleTest">测试</el-button>
        <el-button type="primary" @click="handleBidClick">出价</el-button>
        <el-button type="primary" @click="handleBidSuggestionClick">按照代理建议出价</el-button>
        <el-button type="success" @click="handleAcceptClick">接受</el-button>
        <el-button type="danger" @click="handleRejectClick">拒绝</el-button>
    </div>
</template>

<style>
/* 样式调整 */
div {
    box-sizing: border-box;
}

/* 倒计时组件的独立样式 */
.countdown-timer {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 18px;
    font-weight: bold;
    color: #333; /* 默认字体颜色 */
    margin-bottom: 20px; /* 增加与子页面的间距 */
}

/* 子页面样式 */
.subpage {
    border: 1px solid gray;
    padding: 10px;
}

/* 横向排列样式 */
.horizontal-options {
    display: flex;
    gap: 20px; /* 控制类别之间的水平间隔 */
    flex-wrap: wrap; /* 自动换行 */
}

.option-group {
    display: flex;
    flex-direction: column; /* 让类别和选项垂直排列 */
    align-items: center;
    text-align: center;
    width: 150px; /* 设置固定宽度 */
    box-sizing: border-box; /* 确保宽度包含内边距和边框 */
}

.option-group label {
    margin-bottom: 5px;
    font-weight: bold;
}


.scrollable-table {
  width: 100%;
  max-height: 400px;  /* 设置最大宽度为1000px */
  overflow-x: auto;   /* 使表格内容可以水平滚动 */
  margin: 20px 0;     /* 增加表格和其他内容之间的间距 */
}



/* 出价历史样式 */
.bid-history-item {
    margin-top: 10px;
}

.bid-history-item ul {
    list-style-type: none;
    padding: 0;
}

.bid-history-item li {
    margin: 5px 0;
    font-size: 14px;
}


.agent-suggestion {
    display: flex;
    flex-direction: column; /* 设置竖直排列 */
    gap: 10px; /* 每个类别之间的间隔 */
}

</style>
