<template>
    <div class="introduction">
        <div class="content">
            <h1>这是主页面内容</h1>
        </div>
        <footerComp next="下一步" nextDetail="谈判设置" :showPrevious=false :showNext=true @next-page="goToNextPage" />
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import footerComp from "../components/footer.vue";

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