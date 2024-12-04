<script setup lang="js">
import { onMounted, ref } from 'vue';

import rolesData from './specific_contents/domains_n_roles.json'; 


const sliderValue = ref(10); // 为滑块值创建一个 ref
const options = ref([]); // 存储选项
const selectedOption = ref(null); // 存储选中的选项

const roles = ref([]); 

// 从父组件传递的数据
const { domainsData } = defineProps({
  domainsData: Object,
});

// 加载选项数据
const loadOptions = () => {
  try {
    // 确保 domainsData 是一个对象
    if (typeof domainsData === 'object' && domainsData !== null) {
      // 将 JSON 数据转换为适合的格式，存储为对象数组
      options.value = Object.keys(domainsData).map(key => ({
        label: key, // 使用 key 作为 label
        description: domainsData[key], // 使用 value 作为 description
      }));

      // 默认选中第一个选项
      if (options.value.length > 0) {
        selectedOption.value = options.value[0];
      }
    }
  } catch (error) {
    console.error('加载选项数据失败:', error);
  }
};
// 组件挂载时加载选项
onMounted(() => {
  loadOptions(); // 组件挂载时加载数据
  loadRoles();
});


const handleOptionClick = (option) => {
  selectedOption.value = option;
  loadRoles(); // 更新角色
};



// 根据选中的 domain 获取对应的角色
const getRolesForDomain = (domain) => {
  return rolesData[domain] ;
};

// 在选项数据加载后，动态显示角色
const loadRoles = () => {
  if (selectedOption.value) {
    const domain = selectedOption.value.label;
    roles.value = getRolesForDomain(domain);
  }
};




const swapRoles = () => {
    // console.log("111111")
    roles.value = [roles.value[1], roles.value[0]];
//   if (roles.length === 2) {
//     const temp=roles["0"]
//     roles.value = [roles.value[1], roles.value[0]];
//   }
};



const my_value1 = ref(0)
const my_value2 = ref(0)
const my_value3 = ref(0)
const my_value4 = ref(0)
const my_value5 = ref(0)

const op_value1 = ref(0)
const op_value2 = ref(0)
const op_value3 = ref(0)
const op_value4 = ref(0)
const op_value5 = ref(0)

// 定义发出事件
const emit = defineEmits();

// 点击按钮时将数据传递回父组件
const handleSubmit = () => {
  const dataToSend = {
    BiddingRounds:sliderValue.value,
    Domain:selectedOption.value.label,
    roles:{
        my:roles.value[0],
        op:roles.value[1],
    },
    settingValues:{
        my:{
            value1:my_value1.value,
            value2:my_value2.value,
            value3:my_value3.value,
            value4:my_value4.value,
            value5:my_value5.value,
        },
        op:{
            value1:op_value1.value,
            value2:op_value2.value,
            value3:op_value3.value,
            value4:op_value4.value,
            value5:op_value5.value,
        }
    }
  };

  // 使用 $emit 发送数据给父组件
  emit('submit-data', dataToSend);
};

const handleRandomClick = () => {
    const randomIndex = Math.floor(Math.random() * Object.keys(options.value).length); // 获取随机索引
    selectedOption.value = options.value[randomIndex];
    loadRoles();


    if (Math.random() < 0.5) {
        roles.value = [roles.value[1], roles.value[0]]; // 交换 roles 数组的元素
    }

    const randomValue = () => [-2, -1, 0, 1, 2] [Math.floor(Math.random() * 5)];

    my_value1.value = randomValue();
    my_value2.value = randomValue();
    my_value3.value = randomValue();
    my_value4.value = randomValue();
    my_value5.value = randomValue();

    op_value1.value = randomValue();
    op_value2.value = randomValue();
    op_value3.value = randomValue();
    op_value4.value = randomValue();
    op_value5.value = randomValue();
};

</script>


<template>
  <div>
    <!-- Slider Block -->
    <div class="slider-demo-block">
      <span class="slider-label">谈判轮数</span>
      <el-slider v-model="sliderValue" :min="10" :max="1000" show-input />
    </div>

    <!-- Option Group -->
    <div style="display: flex; align-items: flex-start;">
      <div class="option-group" v-if="options.length > 0">
        <span class="slider-label">谈判域（domains）</span>
        <button
          v-for="option in options"
          :key="option.label"
          :class="['option-item', { selected: selectedOption === option }]"
          @click="handleOptionClick(option)"
        >
          {{ option.label }}
        </button>
      </div>

      <!-- 显示选中项的描述 -->
      <div class="domain-description" v-if="selectedOption">
        <h3>{{ selectedOption.label }}</h3>
        <p>{{ selectedOption.description }}</p>
      </div>
    </div>

    <!-- 角色切换 -->
    <div class="role-selection" v-if="roles.length > 0"  style="text-align: center;">
        <span>我的角色<br>{{ roles[0] }}</span>
        <button @click="swapRoles">互换</button>
        <span>对手角色<br>{{ roles[1] }}</span>
    </div>


    <div style="display: flex; align-items: flex-start;">
        
        <!-- 我方的五个滑块 -->
        <div class="role-setting-sliderpacks">
            <span style="text-align: center;font-size: 30px;">我...</span>
            <div class="role-setting-slider">
                <span class="demonstration">喜欢激烈的竞争</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="my_value1" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">愿意合作</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="my_value2" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">真的需要这次谈判达成协议</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="my_value3" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">谈判经验很丰富</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="my_value4" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">备用</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="my_value5" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>
        </div>

        <!-- 对方的五个滑块 -->
        <div class="role-setting-sliderpacks">
            <span style="text-align: center;font-size: 30px;">对手...</span>
            <div class="role-setting-slider">
                <span class="demonstration">喜欢激烈的竞争</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="op_value1" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">愿意合作</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="op_value2" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">真的需要这次谈判达成协议</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="op_value3" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">谈判经验很丰富</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="op_value4" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">备用</span>
                <div class="slider-labels-bottom">
                    <span class="slider-label-left">否</span>
                    <span class="slider-label-right">是</span>
                </div>
                <el-slider v-model="op_value5" :min="-2" :max="2" :step="1" show-stops>
                </el-slider>
            </div>
        </div>

        <div class="centered-container">
            <el-button type="primary" round size="large" @click="handleRandomClick" >随机！</el-button>
            <el-button type="primary" round size="large" @click="handleSubmit" >下一步</el-button>
        </div>
    </div>
    



    

  </div>
</template>

<style scoped>
.slider-demo-block {
  max-width: 600px;
  display: flex;
  align-items: center;
  margin-top: 16px;
}
.slider-label {
  font-size: 16px;
  color: #333;
  margin-right: 12px;
  white-space: nowrap;
  margin-left: 20px;
}
.slider-demo-block .el-slider {
  flex: 1;
  margin-left: 20px;
}

/* 可选项样式 */
.option-group {
  display: flex;
  flex-direction: column;
  margin-top: 16px;
  margin-left: 20px;
  margin-bottom: 20px;
  gap: 12px;
  width: 200px;
}

.option-item {
  padding: 8px 16px;
  font-size: 14px;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  cursor: pointer;
  transition: background-color 0.3s, border-color 0.3s;
}

.option-item:hover {
  background-color: #f5f5f5;
}

.option-item.selected {
  background-color: #409eff;
  color: #fff;
  border-color: #409eff;
}

.domain-description h3 {
  margin: 20px 20px 20px 20px;
  display: flex;
  font-size: 24px;
  color: #333;
}

.domain-description p {
  margin: 20px 20px 20px 20px;
  display: flex;
  font-size: 18px;
  color: #555;
  line-height: 1.6;
  white-space: pre-line;
}

.role-selection {
  display: flex;
  align-items: center;
  margin-top: 20px;
  margin-left: 30px;
  gap: 16px;
  width: 500px;
  margin-bottom: 30px;
}

.role-selection button {
  padding: 6px 12px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100px;
  
}

.role-selection button:hover {
  background-color: #66b1ff;
}




.role-setting-sliderpacks {
    margin-left: 50px;
    max-width: 1000px; /* 适应父容器 */
    display: flex;
    flex-direction: column; /* 使所有滑块容器竖着排列 */
    width: 400px;
    margin-top: 30px;
}

.role-setting-slider {
    display: flex;
    flex-direction: column; /* 让描述和滑块垂直排列 */
    align-items: center; /* 使内容水平居中 */
    margin-bottom: 20px; /* 适当的间距 */
}

.role-setting-slider .el-slider {
    width: 100%; /* 让滑块宽度填满父容器 */
    margin-top: 10px; /* 描述与滑块之间的间距 */
}

.role-setting-slider .demonstration {
    font-size: 20px;
    line-height: 44px;
    color: #333;
    text-align: center; /* 水平居中 */
    margin-bottom: -25px; /* 描述与滑块之间的间距 */
}


.slider-labels-bottom {
  display: flex;
  justify-content: space-between;
  width: 100%;
  
  top: 1px; /* 调整位置，避免覆盖滑块 */
}

.slider-label-left, .slider-label-right {
  font-size: 14px;
  color: #333;
  margin-bottom: -5px;
}

.el-button {
    width: 110px; /* 设置固定宽度 */
    display: flex; /* 激活 flex 布局 */
    justify-content: center; /* 水平居中 */
    align-items: center; /* 垂直居中 */
}

.centered-container {
    display: flex; /* 激活 flex 布局 */
    flex-direction: column; /* 设置垂直排列 */
    justify-content: center; /* 垂直居中 */
    align-items: center; /* 水平居中 */
    margin-top: 300px; /* 调整顶部间距 */
    gap: 30px; 
    margin-left: 100px;
}


</style>
