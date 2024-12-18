<template>
    <div class="introduction">
        <div class="content">
            <h1>这是主页面内容</h1>
        </div>
        <footerComp :next="nextTitle" :nextDetail="nextDetail" :previous="previousTitle"
            :previousDetail="previousDetail" :showPrevious="showPrevious" :showNext="showNext" @next-page="goToNextPage"
            @previous-page="goToPreviousPage" />
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref } from "vue";
import footerComp from "../components/footer.vue";

const nextTitle = ref("下一阶段");
const nextDetail = ref("谈判准备");
const showPrevious = ref(false);
const showNext = ref(true);

const router = useRouter();
const goToNextPage = () => {
    router.push("/preparation");
};
</script>

<style>
.introduction {
    display: flex;
    flex-direction: column;
    min-height: 100%;
}

.content {
    flex: 1;
    padding: 20px;
}

.footerComp {
  position: fixed;
  bottom: 0;
  width: 100%;
  background-color: white; /* 你可以根据需求设置背景色 */
  text-align: center;
  padding: 10px;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}
</style>