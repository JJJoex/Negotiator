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
