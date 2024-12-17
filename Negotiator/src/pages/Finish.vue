<script setup lang="js">
import { RouterLink } from 'vue-router';
import { ArrowRightBold } from '@element-plus/icons-vue';
</script>

<template>
    <div>
        <div>
            谈判结束！
        </div>
        <!-- 图片和图注 -->
        <figure style="text-align: center; margin-top: 20px;">
            <img 
                
                src="@/python/output_dir/figures/bidding_history_travel_domain_mOlD_AgentB_vs_AgentA.png"
                alt="谈判结果分析" 
                style="max-width: 100%; height: auto;" 
            />
            <figcaption style="font-size: 14px; color: gray; margin-top: 10px;">
                谈判结果分析
            </figcaption>
        </figure>
    </div>
</template>
