<script setup lang="js">
import { ref, watch, onMounted, nextTick } from 'vue';
import issuesData from './specific_contents/interests_issues.json';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';

const props = defineProps({
  my_interests_data: Object,
  nego_settings_data: Object
});

const { my_interests_data, nego_settings_data } = props;
const domain = ref('');
const my_role = ref('');
const op_role = ref('');

// 每个分类的滑块集合
const sliders = ref({}); 

// 监视 nego_settings_data
watch(
  () => nego_settings_data,
  (newValue) => {
    if (newValue) {
      domain.value = nego_settings_data.Domain || '';
      my_role.value = nego_settings_data.roles?.my || '';
      op_role.value = nego_settings_data.roles?.op || '';

      const categoryData = issuesData[domain.value];

      if (categoryData && typeof categoryData === 'object') {
        // 遍历每个类别
        Object.keys(categoryData).forEach((category) => {
          if (!sliders.value[category]) {
            sliders.value[category] = {};  // 如果没有初始化，先初始化为一个空对象
          }
          const issues = categoryData[category];
          issues.forEach((item) => {
            sliders.value[category][item] = 50; // 设置每个滑块的初始值
          });
        });
      } else {
        console.error(`Invalid data structure for ${domain.value}`);
      }
    }
  },
  { immediate: true }
);

// 监视 my_interests_data
watch(
  () => my_interests_data,
  (newValue) => {
    if (newValue) {
      // 这里可以根据 my_interests_data 做相应的处理

    }
  },
  { immediate: true }
);

// 更新饼图
const updateChart = (category) => {
  const chartData = Object.keys(sliders.value[category]).map((key) => ({
    name: key,
    value: sliders.value[category][key]
  }));

  const chartInstance = echarts.init(document.querySelector(`.pie-chart-op-${category}`)); 
  chartInstance.setOption({
    series: [
      {
        type: 'pie',
        radius: '50%',
        data: chartData
      }
    ]
  });
};

// 初始化 ECharts 饼图
onMounted(() => {
  nextTick(() => {
    Object.keys(sliders.value).forEach((category) => {
      updateChart(category); // 为每个分类初始化饼图
    });
  });
});







// 按钮点击事件的占位方法
const presetClick = () => {
    // 预设按钮的点击事件
    ElMessage.warning('议题的预设权重尚未开发！');
};

const randomClick = () => {
    Object.keys(sliders.value).forEach(category => {
    // 遍历每个分类中的滑块项
    Object.keys(sliders.value[category]).forEach(item => {
      // 为每个滑块项随机生成一个0到100之间的整数
      sliders.value[category][item] = Math.floor(Math.random() * 101);
    });
    
    // 每次更新完滑块值后，更新饼图
    updateChart(category);
  });
};

// 定义发出事件
const emit = defineEmits();

// 点击按钮时将数据传递回父组件
const handleSubmit = () => {
  // 创建一个新的对象来存储归一化后的数据
  const normalizedData = {};

  // 遍历 sliders 中的每个类别
  for (const category in sliders.value) {
    const categoryData = sliders.value[category];
    
    // 计算该类别所有值的总和
    const total = Object.values(categoryData).reduce((sum, value) => sum + value, 0);

    // 对该类别中的每个项进行归一化
    normalizedData[category] = {};
    for (const item in categoryData) {
      // 归一化每个项的值
      normalizedData[category][item] = total > 0 ? categoryData[item] / total : 0; 
    }
  }




  // 使用 $emit 发送归一化后的数据给父组件
  emit('submit-data', normalizedData);
};
</script>



<template>
    <div>
      <div class="domain-section">
        <h2>兴趣-议题设置</h2>
        <div v-if="domain && issuesData[domain]" class="slider-container">
          <!-- 每个分类 -->
          <div
            v-for="(issues, category, index) in issuesData[domain]"
            :key="category"
            :class="['category', { 'alternate-bg': index % 2 === 1 }]"
            >
            <h3>{{ category }}：权重 {{ my_interests_data[category]?.toFixed(4) }}</h3>
            <div class="slider-category">
                <!-- 左侧的 sliders -->
                <div class="slider-items">
                <div v-for="(item, index) in issues" :key="index" class="slider-item">
                    <!-- 左侧文字描述 -->
                    <div class="slider-label">{{ item }}</div>
                    <!-- 滑块 -->
                    <el-slider
                    v-model="sliders[category][item]"
                    :min="0"
                    :max="100"
                    :step="1"
                    :active-color="'#409EFF'"
                    :inactive-color="'#d3d3d3'"
                    @input="() => updateChart(category)"
                    />
                    <!-- 右侧显示当前数值 -->
                    <div class="slider-value">{{ sliders[category][item] }}</div>
                </div>
                </div>
                <!-- 右侧的饼图 -->
                <div ref="pieChart" :class="'pie-chart-op-' + category" class="pie-chart-op"></div>
            </div>
            </div>
        </div>
      </div>

      <div class="button-container">
          <el-button class="button preset" @click="presetClick">预设</el-button>
          <el-button class="button random" @click="randomClick">随机！</el-button>
          <el-button class="button next-step" @click="handleSubmit">下一步</el-button>
      </div>
    </div>
  </template>
  
  <style scoped>
  /* 整体布局 */
  body, html {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
  }
  
  .domain-section {
    display: flex;
    flex-direction: column;
    padding: 20px;
    box-sizing: border-box; /* 确保 padding 不影响整体宽度 */
    width: 100%; /* 使容器填满整个宽度 */
  }
  
  /* 滑块容器 */
  .slider-container {
    margin-top: 20px;
    width: 100%; /* 填满宽度 */
  }
  
/* 每个分类的默认样式 */
.category {
  padding: 20px;
  background-color: transparent; /* 默认无背景色 */
}

/* 隔一个设置浅灰背景 */
.alternate-bg {
  background-color: #f7f7f7; /* 浅灰色 */
}
  
  /* 滑块和饼图的布局 */
  .slider-category {
    display: flex;
    align-items: flex-start; /* 滑块和饼图顶部对齐 */
    justify-content: space-between;
    gap: 20px; /* 滑块和饼图之间的间距 */
    width: 100%; /* 填满宽度 */
  }
  
  /* 左侧的滑块部分 */
  .slider-items {
    display: flex;
    flex-direction: column; /* 使滑块竖直排列 */
    flex: 2; /* 滑块区域占较大的比例 */
    width: 400px;
  }
  
  /* 单个滑块的布局 */
  .slider-item {
    display: flex;
    align-items: center; /* 垂直居中对齐 */
    margin-bottom: 15px; /* 滑块之间的间距 */
  }
  
  /* 固定文字描述宽度 */
  .slider-label {
    width: 100px; /* 固定宽度为 100px */
    text-align: left; /* 左对齐 */
    font-size: 14px; /* 可调整字体大小 */
  }
  
  /* 数值显示 */
  .slider-value {
    margin-left: 10px; /* 与滑块保持间距 */
    width: 50px; /* 固定宽度 */
    text-align: right; /* 右对齐 */
    font-size: 14px; /* 可调整字体大小 */
  }
  
  /* 饼图部分 */
  .pie-chart-op {
    margin-top: -100px;
    flex: 1; /* 饼图区域占剩余空间 */
    min-width: 500px; /* 最小宽度，避免饼图过小 */
    height: 500px; /* 调整饼图高度 */
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
  