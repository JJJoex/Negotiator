<script setup lang="js">
import { ref, watch, onMounted, nextTick } from 'vue';
import issuesData from '../specific_contents/interests_issues.json';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';

const { nego_settings_data } = defineProps({
    nego_settings_data: Object,
});
const domain = ref('');
const my_role = ref('');
const op_role = ref('');

// 滑块数据初始化
const sliders = ref({}); // 存储滑块的值

watch(
    () => nego_settings_data,
    (newValue) => {
        if (newValue) {
            domain.value = nego_settings_data.Domain || '';
            my_role.value = nego_settings_data.roles?.my || '';
            op_role.value = nego_settings_data.roles?.op || '';

            // 初始化滑块值
            const issueNames = issuesData[domain.value] || []; // 获取滑块名称

            sliders.value = Object.fromEntries(
                Object.keys(issueNames).map((category) => [category, 50]) // 默认值为 50
            );
        }
    },
    { immediate: true }
);

const chart = ref(null); // 存储饼形图容器的引用

// 初始化饼图
const updatepieChart_op = () => {
    if (chart.value) {
        const pieData = Object.keys(sliders.value).map(key => ({
            name: key,
            value: sliders.value[key],
        }));

        const option = {
            title: {
                text: '兴趣权重（实时更新）',
                // subtext: '',
                left: 'center',
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b}: {c} ({d}%)',
            },
            series: [
                {
                    name: '权重',
                    type: 'pie',
                    radius: '55%',
                    data: pieData,
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)',
                        },
                    },
                },
            ],
        };

        // 清除现有的图表选项并重新设置
        chart.value.setOption(option, true); // 第二个参数为 `true`，会强制覆盖所有的选项
    }
};

onMounted(() => {
    // 等待 DOM 渲染完成
    nextTick(() => {
        chart.value = echarts.init(document.getElementById('pieChart_op'));
        updatepieChart_op();
    });
});

// 监听滑块值变化并更新图表
watch(sliders, () => {
    nextTick(() => {
        updatepieChart_op(); // 直接调用 updatepieChart_op 更新图表
    });
}, { deep: true });  // 使用 deep:true 监听对象内部变化











// 按钮点击事件的占位方法
const presetClick = () => {
    // 预设按钮的点击事件
    ElMessage.warning('兴趣的预设权重尚未开发！');
};

const randomClick = () => {

    // 随机设置 sliders 的值
    const newSliders = {};
    Object.keys(sliders.value).forEach((key) => {
        newSliders[key] = Math.floor(Math.random() * 101); // 随机值在 0 到 100 之间
    });
    sliders.value = newSliders; // 更新 sliders 的值
};

// 定义发出事件
const emit = defineEmits();

// 点击按钮时将数据传递回父组件
const handleSubmit = () => {
  
  const dataToSend = {};
  const total=Object.values(sliders.value).reduce((sum, value) => sum + value, 0);


  for (const [key, value] of Object.entries(sliders.value)) {
    dataToSend[key] = total > 0 ? value / total : 0; 
  }


  // 使用 $emit 发送数据给父组件
  emit('submit-data', dataToSend);
};






</script>


<template>
  <div class="container">
      <!-- 大标题 -->
      <!-- <h1 class="title">这是大标题</h1> -->

      <!-- 文本框区域 -->
      <el-row class="input-container">
          <el-col :span="8" class="fill-space">
              <div class="custom-box">
                  <div class="box-title">谈判域</div>
                  <div class="box-content">{{ domain }}</div>
              </div>
          </el-col>
          <el-col :span="8" class="fill-space">
              <div class="custom-box">
                  <div class="box-title">我的角色</div>
                  <div class="box-content">{{ my_role }}</div>
              </div>
          </el-col>
          <el-col :span="8" class="fill-space">
              <div class="custom-box">
                  <div class="box-title">对手角色</div>
                  <div class="box-content">{{ op_role }}</div>
              </div>
          </el-col>
      </el-row>

      <h1 class="title2">对手的兴趣</h1>

      <!-- 滑块区域和饼图容器并排显示 -->
      <div class="sliders-and-chart">
          <!-- 滑块区域 -->
          <div class="sliders">
              <h2 class="slider-title">兴趣权重</h2>
              <div v-for="(value, name) in sliders" :key="name" class="slider-box">
                  <span class="slider-label">{{ name }}</span>
                  <el-slider v-model="sliders[name]" :min="0" :max="100"></el-slider>
                  <span class="slider-value">{{ sliders[name] }}</span>
              </div>
          </div>

          <!-- 饼形图容器 -->
          <div id="pieChart_op" class="pie-chart"></div>
      </div>


      <div class="button-container">
          <el-button class="button preset" @click="presetClick">预设</el-button>
          <el-button class="button random" @click="randomClick">随机！</el-button>
          <el-button class="button next-step" @click="handleSubmit">下一步</el-button>
      </div>
  </div>
</template>




















<style scoped>
/* 让容器占满页面宽度 */
.container {
    width: 100vw; /* 视口宽度 */
    padding: 0;
    margin: 0; /* 移除外边距 */
}

/* 大标题样式 */
.title {
    font-size: 36px; /* 大标题字号 */
    font-weight: bold; /* 加粗 */
    text-align: center; /* 居中显示 */
    margin-bottom: 20px; /* 与其他内容的间距 */
}

.title2 {
    font-size: 26px; /* 大标题字号 */
    font-weight: bold; /* 加粗 */
    text-align: center; /* 居中显示 */
    margin-bottom: 20px; /* 与其他内容的间距 */
    margin-top: 60px;
}

/* 调整输入框区域使其充满父容器 */
.input-container {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
    width: 95%; 
}

/* 均分空间 */
.fill-space {
    flex: 1; /* 每个组件均分宽度 */
    margin: 0 50px; /* 组件之间间距 */
}

/* 输入框样式 */
.custom-box {
    border: 1px solid #ccc; /* 边框样式 */
    border-radius: 4px; /* 圆角 */
    padding: 10px;
    text-align: center; /* 内容居中 */
    height: 100%; /* 填满父容器 */
}

/* 标题和内容样式 */
.box-title {
    font-size: 24px; /* 标题字号 */
    font-weight: bold; /* 标题加粗 */
    margin-bottom: 5px; /* 标题和内容之间的间距 */
}

.box-content {
    font-size: 18px; /* 内容字号 */
    color: #555; /* 内容颜色 */
    word-break: break-word; /* 长单词自动换行 */
}


/* 滑块区域和饼图容器并排显示 */
.sliders-and-chart {
    display: flex; /* 使用 Flex 布局 */
    justify-content: space-between; /* 或 justify-content: space-evenly; */
    gap: 30px; /* 控制滑块和饼图之间的间距 */
    margin-top: 30px;
    width: 100%; /* 确保占满父容器的宽度 */
}

/* 滑块区域样式 */
.sliders {
    max-width: 600px; /* 设置滑块区域的最大宽度 */
    flex-grow: 1; /* 允许滑块区域占据剩余空间 */
    padding: 20px; /* 内边距，避免内容紧贴边界 */
    text-align: center; /* 文本居中对齐 */
}

/* 滑块标题样式 */
.slider-title {
    font-size: 24px; /* 滑块标题字号 */
    font-weight: bold; /* 加粗 */
    margin-bottom: 20px; /* 标题与滑块的间距 */
}

/* 每个滑块的盒子 */
.slider-box {
    display: flex; /* 使用 Flex 布局 */
    align-items: center; /* 垂直居中 */
    justify-content: space-between; /* 左右对齐 */
    margin-bottom: 15px; /* 滑块之间的间距 */
    border: 1px solid #ccc; /* 可选：滑块盒子的边框 */
    border-radius: 4px; /* 可选：滑块盒子的圆角 */
    padding: 10px; /* 滑块盒子的内边距 */
}

/* 滑块标签样式 */
.slider-label {
    flex: 0 1 auto; /* 设置 flex 使其自适应宽度 */
    font-size: 16px; /* 标签字号 */
    text-align: left; /* 左对齐 */
    white-space: normal; /* 允许文本换行 */
    word-wrap: break-word; /* 长单词自动换行 */
    margin-right: 10px; /* 标签与滑块之间的间距 */
    min-width: 80px; /* 设置标签的最小宽度 */
}

/* 滑块的容器样式 */
.slider-component {
    flex: 1; /* 滑块占据较多宽度 */
    width: 100px;
    margin: 0 10px; /* 滑块与左右内容的间距 */
}

/* 滑块值显示样式 */
.slider-value {
    flex: 1; /* 滑块值占据一定宽度 */
    font-size: 14px; /* 值的字号 */
    text-align: right; /* 右对齐 */
    color: #555; /* 值的颜色 */
}

/* 饼图容器样式 */
.pie-chart {
    width: 600px;
    height: 600px;
    margin-left: 20px; /* 饼图和滑块之间的间距 */
    flex-shrink: 0; /* 防止饼图被压缩 */
    margin-right: 200px;
}




/* 按钮容器样式 */
.button-container {
    display: flex; /* 水平排列 */
    justify-content: center; /* 居中对齐 */
    margin-top: 0px; /* 按钮与上方内容的间距 */
    margin-bottom: 20px;
}

/* 按钮样式 */
.button {
    margin: 0 15px; /* 每个按钮之间的间距 */
    font-size: 18px; /* 按钮字体大小 */
}


/* 预设按钮样式 - 浅绿色 */
.preset {
    background-color: #cceccc; /* 浅绿色 */
}

/* 随机按钮样式 - 浅红色 */
.random {
    background-color: #ffcccb; /* 浅红色 */
}

/* 下一步按钮样式 - 天蓝色 */
.next-step {
    background-color: #49b9ff; /* 天蓝色 */
    -webkit-text-fill-color: #ffffff;
}
</style>
