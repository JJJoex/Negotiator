<template>
    <div>
        <el-descriptions>
            <el-descriptions-item label="谈判结果">{{ display.result }}</el-descriptions-item>
            <el-descriptions-item label="最后一方">{{ display.last_player }}</el-descriptions-item>
            <el-descriptions-item label="最后一次出价">{{ display.last_bid }}</el-descriptions-item>
        </el-descriptions>
        <!-- 图片和图注 -->
        <figure style="text-align: center; margin-top: 20px;">
            <img src="@/python/output_dir/figures/bidding_history_travel_domain_mOlD_AgentB_vs_AgentA.png" alt="谈判结果分析"
                style="max-width: 100%; height: auto;" />
            <figcaption style="font-size: 14px; color: gray; margin-top: 10px;">
                谈判结果分析
            </figcaption>
        </figure>
        <footerComp nextDetail="回到首页" :showPrevious=false :showNext=true @next-page="goToNextPage" />
    </div>
</template>

<script setup lang="js">
import footerComp from "../components/footer.vue";
import { useRouter } from 'vue-router';
const router = useRouter();
const goToNextPage = () => {
    router.push('/introduction');
}

import { useStore } from "vuex";
import { ref, computed } from "vue";
const store = useStore();
const finish = computed(() => store.state.finish);
console.log(finish.value, 'finish');

const display = ref({
    result: finish.value.result,
    last_player: finish.value.last_player,
    last_bid: finish.value.last_bid
})

</script>
