<script setup lang="js">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router';
import { ArrowRightBold } from '@element-plus/icons-vue';
import footerComp from "../components/footer.vue";

const nextTitle = ref("下一页");
const nextDetail = ref("欢迎页面");
const showPrevious = ref(false);
const showNext = ref(true)
const router = useRouter();
const goToNextPage = () => {
    router.push("/introduction");
};
</script>

<template>
    <div>
        <div style="line-height: 170px;">
            谈判结束！
        </div>
        <!-- 图片和图注 -->
        <figure style="text-align: center; margin-top: 20px;">
            <img src="@/python/output_dir/figures/bidding_history_travel_domain_mOlD_AgentB_vs_AgentA.png" alt="谈判结果分析"
                style="max-width: 100%; height: auto;" />
            <figcaption style="font-size: 14px; color: gray; margin-top: 10px;">
                谈判结果分析
            </figcaption>
        </figure>
        <footerComp :next="nextTitle" :nextDetail="nextDetail" :previous="previousTitle"
            :previousDetail="previousDetail" :showPrevious="showPrevious" :showNext="showNext" @next-page="goToNextPage"
            @previous-page="goToPreviousPage" />
    </div>
</template>
