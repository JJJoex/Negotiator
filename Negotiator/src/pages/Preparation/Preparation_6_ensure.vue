<script setup>
import { defineProps, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import footerComp from '../../components/footer.vue';
const nextTitle = ref('下一阶段')
const nextDetail = ref('开始谈判')
const previousTitle = ref('上一页')
const previousDetail = ref('对方议题')
const showPrevious = ref(true)
const showNext = ref(true)
const emit = defineEmits();
const goToNextPage = () => {
  emit('nextPage')
}
const goToPreviousPage = () => {
  emit('previousPage')
}
// 接收从父组件传递的参数
const props = defineProps({
  nego_settings_data: Object,
  my_interests_data: Object,
  my_issues_data: Object,
  op_interests_data: Object,
  op_issues_data: Object
});
</script>

<template>
    <h2>确认页面数据</h2>
    <el-descriptions title="谈判环境设置">
      <el-description-item label="谈判域">{{ nego_settings_data.domain || '' }}</el-description-item>
      <el-description-item label="角色">{{ nego_settings_data.roles.my + nego_settings_data.roles.op }}</el-description-item>
      <el-description-item label="谈判轮数">{{ nego_settings_data.BiddingRounds || '' }}</el-description-item>
      <el-description-item label="谈判时间">{{ nego_settings_data.BiddingTime || '' }}</el-description-item>
      <el-description-item label="兴趣">{{ Object.keys(my_interests_data) }}</el-description-item>

    </el-descriptions>
    <el-descriptions title="我方">
      <el-description-item label="角色">{{ nego_settings_data.roles.my || '' }}</el-description-item>
      <el-description-item label="先手">{{ nego_settings_data.whoFirst ? '对方' : '我方' || ''}}</el-description-item>
    </el-descriptions>
    <el-descriptions title="对方">
      <el-description-item label="角色">{{ nego_settings_data.roles.op || '' }}</el-description-item>
      <el-description-item label="先手">{{ nego_settings_data.whoFirst ? '对方' : '我方' || ''}}</el-description-item>
    </el-descriptions>
    
  <footerComp :next="nextTitle" :nextDetail="nextDetail" :previous="previousTitle" :previousDetail="previousDetail"
    :showPrevious="showPrevious" :showNext="showNext" @next-page="goToNextPage" @previous-page="goToPreviousPage" />
</template>


<style scoped>
h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

h3 {
  font-size: 18px;
  margin-top: 10px;
}

pre {
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: monospace;
  font-size: 14px;
  user-select: text;
  /* 确保文本可选和复制 */
}
</style>
