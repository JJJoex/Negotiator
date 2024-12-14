<script setup lang="js">
import { ref, reactive, onMounted, computed, watch, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';

// 初始倒计时
const countdown = ref(null);
const remainingRounds = ref(0);
const agentSuggestionDisplay = ref(true);
const bid = ref({});

// 商品分类数据
const groceryStore = ref({
    "面包类": ["法棍", "饼干", "羊角面包", "普通面包"],
    "水果类": ["苹果", "香蕉", "樱桃", "葡萄", "梨", "瓜", "草莓"],
    "零食类": ["巧克力棒", "甜甜圈", "玉米片", "爆米花", "薯片", "糖果", "饼干"],
    "酱料类": ["奶酪", "果酱", "花生酱", "三明治酱", "巧克力酱", "火腿", "萨拉米香肠", "蛋沙拉"],
    "蔬菜类": ["豆子", "西兰花", "韭菜", "土豆", "菠菜", "胡萝卜", "西红柿"],
    "饮料类": ["能量饮料", "牛奶", "茶", "咖啡", "果汁", "可乐", "芬达", "啤酒", "葡萄酒"]
});
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
])
const agentSuggestion = ref({
    "面包类": "饼干",
    "水果类": "苹果",
    "零食类": "巧克力棒",
    "酱料类": "奶酪",
    "蔬菜类": "西兰花",
    "饮料类": "能量饮料"
});

const formatHistory = (bidHistory, groceryStore) => {
    const categories = Object.keys(groceryStore.value);
    return bidHistory.value.reverse().map(({ round, bidder, bidContent }) => {
        // Build the formatted entry for each bid
        const formattedEntry = {
            '轮次': round,
            '出价方': bidder,
        };
        bidContent.forEach((contentIdx, idx) => {
            const category = categories[idx];
            formattedEntry[category] = groceryStore.value[category][contentIdx];
        });
        return formattedEntry;
    });
};

const formatBidHistory = formatHistory(bidHistory, groceryStore)

const formattedCountdown = computed(() => {
  const minutes = Math.floor(countdown.value / 60); // 计算分钟
  const seconds = countdown.value % 60; // 计算剩余秒数
  return `${minutes}分${seconds}秒`; // 返回格式化后的字符串
});

const route = useRoute();

</script>

<template>
    <div class="bidding-input">
        <div class="ending">
            <p>剩余轮数: {{ remainingRounds }} 轮</p>
            <p>倒计时: {{ formattedCountdown }}</p>
        </div>
        <el-form>
            <el-form-item v-for="(items, category) in groceryStore" :label="category" >
                <el-select v-model="bid[category]">
                    <el-option v-for="item in items" :key="item" :value="item" :label="item"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button>测试</el-button>
                <el-button type="info">重置</el-button>
                <el-button type="primary">出价</el-button>
                <el-button type="success">接受</el-button>
                <el-button type="danger">结束</el-button>
                <el-button type="primary">查看推荐出价</el-button>
            </el-form-item>
            <el-form-item v-if="agentSuggestionDisplay">
                <el-table :data="[agentSuggestion]" style="margin: 0 0 10px; width: 100%;" :header-cell-style="{background:'#eef1f6',color:'#000000'}">
                    <el-table-column label="智能体推荐报价">
                        <el-table-column v-for="(category, idx) in Object.keys(agentSuggestion)" :key="idx"
                            :label="category" :prop="category"></el-table-column>
                    </el-table-column>
                </el-table>
                <el-button>隐藏推荐出价</el-button>
                <el-button type="primary">导入推荐出价</el-button>
            </el-form-item>
        </el-form>
    </div>
    <div class="display">
        <div class="bidding-history">
            <el-table :data="formatBidHistory" stripe height="500" :header-cell-style="{background:'#eef1f6',color:'#000000'}">
                <el-table-column v-for="(label, key) in Object.keys(formatBidHistory[0] || {})" :key="key" :prop="label"
                    :label="label">
                </el-table-column>
            </el-table>
        </div>
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

</style>
