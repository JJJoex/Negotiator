<template>
    <div class="container">
        <h2>谈判结果</h2>
        <el-descriptions>
            <el-descriptions-item label="谈判结果">
                <el-tag>{{ final_state === '达成一致' ? '达成一致' : '谈判失败' }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="我方代理">{{ negotiation_settings.roles.my }}</el-descriptions-item>
            <el-descriptions-item label="对方代理">{{ negotiation_settings.roles.op }}</el-descriptions-item>
            <!-- <el-descriptions-item label="谈判步数">{{ }}</el-descriptions-item>
            <el-descriptions-item label="谈判时间">{{ }}</el-descriptions-item> -->
            <el-descriptions-item label="我方收益">{{ my_utility }}</el-descriptions-item>
            <el-descriptions-item label="对方收益">{{ op_utility }}</el-descriptions-item>
            <el-descriptions-item label="帕累托距离">{{ pareto_distance }}</el-descriptions-item>
            <el-descriptions-item label="纳什均衡距离">{{ ne_distance }}</el-descriptions-item>
        </el-descriptions>

        <el-table :data="contrastData" style="width: 100%;">
            <el-table-column prop="name" label="对比方"></el-table-column>
            <el-table-column prop="收益" label="收益"></el-table-column>
            <el-table-column prop="帕累托距离" label="帕累托距离"></el-table-column>
            <el-table-column prop="纳什均衡距离" label="纳什均衡距离"></el-table-column>
        </el-table>

        <div v-if="final_state === '达成一致'" class="img-div">
            <img src="../assets/2.png" />
        </div>
        <div v-else class="img-div" >
            <img src="../assets/1.png" />
        </div>
        <footerComp next="下一步" nextDetail="回到首页" :showPrevious=false :showNext=true @next-page="goToNextPage" />
    </div>
</template>

<script setup lang="js">
import { computed, ref } from 'vue';
import { useStore } from 'vuex';
import footerComp from '../components/footer.vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const goToNextPage = () => {
    router.push('/description');
}
const store = useStore();
const negotiation_settings = computed(() => store.state.nego_settings_data);
const final_state = computed(() => store.state.curr_nego_state);
const my_utility = ref(0.23380132);
const op_utility = ref(0.6544942);
const pareto_distance = ref(0.23123);
const ne_distance = ref(0.47876);

const contrastData = ref([
    { name: '我方', 收益: my_utility.value, 帕累托距离: pareto_distance.value, 纳什均衡距离: ne_distance.value },
    { name: 'AI', 收益: '0.3849', 帕累托距离: '0.184902', 纳什均衡距离: '0.279401' }
]);
</script>

<style scoped>
.container {
    margin: 20px;
    height: 100%;
    width: 100%;
    display: block;
    margin: 20px;
    /* justify-self: unset; */
}
.img-div {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
}
</style>
