<script setup lang="js">
import { onMounted, ref } from 'vue';
<<<<<<< HEAD

import rolesData from '../specific_contents/domains_n_roles.json'; 


const sliderValue = ref(10); // 为滑块值创建一个 ref
=======
import { useRouter } from 'vue-router';
import rolesData from '../specific_contents/domains_n_roles.json';
import footerComp from '../../components/footer.vue';
// const router = useRouter();
const nextTitle = ref('下一页')
const nextDetail = ref('我方兴趣')
const previousTitle = ref('上一阶段')
const previousDetail = ref('欢迎页面')
const showPrevious = ref(true)
const showNext = ref(true)
const goToNextPage = () => {
  const dataToSend = {
    BiddingRounds: round.value,
    BiddingTime: timeLimit.value,
    Domain: selectedOption.value.label,
    whoFirst: first.value,
    roles: {
      my: roles.value[role.value],
      op: roles.value[1 - role.value],
    },
    settingValues: {
      my: {
        value1: my_value1.value,
        value2: my_value2.value,
        value3: my_value3.value,
        value4: my_value4.value,
        value5: my_value5.value,
      },
      op: {
        value1: op_value1.value,
        value2: op_value2.value,
        value3: op_value3.value,
        value4: op_value4.value,
        value5: op_value5.value,
      }
    }
  };

  // 使用 $emit 发送数据给父组件
  emit('nextPage', dataToSend);
}
const goToPreviousPage = () => {
  emit('previousPage')
}
const round = ref(10); // 为滑块值创建一个 ref
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
const options = ref([]); // 存储选项
const selectedOption = ref(null); // 存储选中的选项

const timeLimit = ref(10);

<<<<<<< HEAD
const roles = ref([]); 
const radio1 = ref("1");
=======
const roles = ref([]);
const first = ref("1");
const role = ref("0")
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac

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
<<<<<<< HEAD
  return rolesData[domain] ;
=======
  return rolesData[domain];
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
};

// 在选项数据加载后，动态显示角色
const loadRoles = () => {
  if (selectedOption.value) {
    const domain = selectedOption.value.label;
    roles.value = getRolesForDomain(domain);
  }
};




<<<<<<< HEAD
const swapRoles = () => {
    roles.value = [roles.value[1], roles.value[0]];
};
=======
// const swapRoles = () => {
//   roles.value = [roles.value[1], roles.value[0]];
// };
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac



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
<<<<<<< HEAD
    BiddingRounds:sliderValue.value,
    BiddingTime:timeLimit.value,
    Domain:selectedOption.value.label,
    whoFirst:radio1.value,
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
=======
    BiddingRounds: round.value,
    BiddingTime: timeLimit.value,
    Domain: selectedOption.value.label,
    whoFirst: first.value,
    roles: {
      my: roles.value[role.value],
      op: roles.value[1 - role.value],
    },
    settingValues: {
      my: {
        value1: my_value1.value,
        value2: my_value2.value,
        value3: my_value3.value,
        value4: my_value4.value,
        value5: my_value5.value,
      },
      op: {
        value1: op_value1.value,
        value2: op_value2.value,
        value3: op_value3.value,
        value4: op_value4.value,
        value5: op_value5.value,
      }
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
    }
  };

  // 使用 $emit 发送数据给父组件
  emit('submit-data', dataToSend);
};

const handleRandomClick = () => {
<<<<<<< HEAD
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
=======
  const randomIndex = Math.floor(Math.random() * Object.keys(options.value).length); // 获取随机索引
  selectedOption.value = options.value[randomIndex];
  loadRoles();


  if (Math.random() < 0.5) {
    roles.value = [roles.value[1], roles.value[0]]; // 交换 roles 数组的元素
  }

  const randomValue = () => [-2, -1, 0, 1, 2][Math.floor(Math.random() * 5)];

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
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
};

const marks_1 = {
  "-2": "完全不倾向竞争",
<<<<<<< HEAD
  "-1": "不太倾向竞争",
  "0": "中立/无明显倾向",
  "1": "较倾向竞争",
=======
  "-1": "",
  "0": "中立/无明显倾向",
  "1": "",
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
  "2": "非常倾向竞争"
};
const marks_2 = {
  "-2": "完全不愿意妥协",
<<<<<<< HEAD
  "-1": "不太愿意妥协",
  "0": "中立/无明显倾向",
  "1": "较愿意妥协",
=======
  "-1": "",
  "0": "中立/无明显倾向",
  "1": "",
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
  "2": "非常愿意妥协"
};
const marks_3 = {
  "-2": "完全不关心达成协议",
<<<<<<< HEAD
  "-1": "比较不关心达成协议",
  "0": "不太重视达成协议",
  "1": "较重视达成协议",
=======
  "-1": "",
  "0": "不太重视达成协议",
  "1": "",
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
  "2": "非常重视达成协议"
};
const marks_4 = {
  "-2": "非常依赖随机与直觉",
<<<<<<< HEAD
  "-1": "较依赖随机与直觉",
  "0": "无明显依赖",
  "1": "较依赖经验",
=======
  "-1": "",
  "0": "无明显依赖",
  "1": "",
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
  "2": "非常依赖经验"
};
const marks_5 = {
  "-2": "完全避免任何风险",
<<<<<<< HEAD
  "-1": "不愿意承担风险",
  "0": "追求较为保守的选择",
  "1": "愿意承担一定风险",
=======
  "-1": "",
  "0": "追求较为保守的选择",
  "1": "",
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
  "2": "完全愿意承担风险"
};
</script>

<<<<<<< HEAD

<template>
  <div>
    <div class="container">
    <div class="scrollable-content">

    <!-- Slider Block -->
    <div class="slider-demo-block">
      <span class="slider-label">谈判轮数（我方出价轮数）</span>
      <el-slider v-model="sliderValue" :min="10" :max="1000" show-input />
    </div>

    <div class="slider-demo-block">
      <span class="slider-label">我方每轮出价限时（秒）</span>
      <el-slider v-model="timeLimit" :min="60" :max="300" show-input />
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
=======
<template>
  <div class="container">
    <!-- 谈判域选择 -->
    <div class="domain-select">
      <div class="option-group" v-if="options.length > 0">
        <button v-for="option in options" :key="option.label"
          :class="['option-item', { selected: selectedOption === option }]" @click="handleOptionClick(option)">
          {{ option.label }}
        </button>
      </div>
      <div class="domain-description" v-if="selectedOption">
        <h3>谈判域：{{ selectedOption.label }}</h3>
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
        <p>{{ selectedOption.description }}</p>
      </div>
    </div>

<<<<<<< HEAD
    <!-- 角色切换 -->
    <div class="role-selection" v-if="roles.length > 0"  style="text-align: center;">
        <span>我的角色<br>{{ roles[0] }}</span>
        <button @click="swapRoles">互换</button>
        <span>对手角色<br>{{ roles[1] }}</span>
    </div>

    <div class="who-first">
    <el-radio-group v-model="radio1">
      <el-radio value="1" size="large">我方先手</el-radio>
      <el-radio value="2" size="large">对方先手</el-radio>
    </el-radio-group>
  </div>


    <div style="display: flex; align-items: flex-start;">
        
        <!-- 我方的五个滑块 -->
        <div class="role-setting-sliderpacks">
            <span style="text-align: center;font-size: 30px;">我...</span>
            <div class="role-setting-slider">
                <span class="demonstration">你是否倾向于通过强力手段来压迫对方或争取更好的条件？</span>
                <el-slider v-model="my_value1" :min="-2" :max="2" :step="1" show-stops :marks="marks_1">
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">当面对对方提出的条件时，你愿意在什么程度上做出让步？</span>
                <el-slider v-model="my_value2" :min="-2" :max="2" :step="1" show-stops :marks="marks_2">
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">你是否特别关注达成协议，还是倾向于仅仅在自己能接受的条件下才同意协议？</span>
                <el-slider v-model="my_value3" :min="-2" :max="2" :step="1" show-stops :marks="marks_3">
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">你通常依赖于过去的经验来做决策，还是依赖直觉或随机选择？</span>

                <el-slider v-model="my_value4" :min="-2" :max="2" :step="1" show-stops :marks="marks_4">
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">你如何看待风险和不确定性？</span>
                <el-slider v-model="my_value5" :min="-2" :max="2" :step="1" show-stops :marks="marks_5">
                </el-slider>
            </div>
        </div>

        <!-- 对方的五个滑块 -->
        <div class="role-setting-sliderpacks">
            <span style="text-align: center;font-size: 30px;">对手...</span>
            <div class="role-setting-slider">
                <span class="demonstration">你是否倾向于通过强力手段来压迫对方或争取更好的条件？</span>
                <el-slider v-model="op_value1" :min="-2" :max="2" :step="1" show-stops :marks="marks_1">
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">当面对对方提出的条件时，你愿意在什么程度上做出让步？</span>
                <el-slider v-model="op_value2" :min="-2" :max="2" :step="1" show-stops :marks="marks_2">
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">你是否特别关注达成协议，还是倾向于仅仅在自己能接受的条件下才同意协议？</span>
                <el-slider v-model="op_value3" :min="-2" :max="2" :step="1" show-stops :marks="marks_3">
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">你通常依赖于过去的经验来做决策，还是依赖直觉或随机选择？</span>

                <el-slider v-model="op_value4" :min="-2" :max="2" :step="1" show-stops :marks="marks_4">
                </el-slider>
            </div>

            <div class="role-setting-slider">
                <span class="demonstration">你如何看待风险和不确定性？</span>
                <el-slider v-model="op_value5" :min="-2" :max="2" :step="1" show-stops :marks="marks_5">
                </el-slider>
            </div>
        </div>

        
    </div>

  </div>

  
    


  </div>


  
    

  </div>
  

  <div class="fixed-buttons">
        <el-button type="primary" round size="large" @click="handleRandomClick" >随机！</el-button>
        <el-button type="primary" round size="large" @click="handleSubmit" >下一步</el-button>
    </div>
</template>

<style scoped>

.who-first{
  margin-left: 30px;
  font-size: 20px;
}
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
=======
    <!-- 谈判设置 -->
    <div class="domain-settings">
      <el-form :inline="true" class="domain-settings" :column="2">
        <el-form-item label="我方角色">
          <el-radio-group v-model="role" size="large">
            <el-radio-button value="0" :label="roles[0]"/>
            <el-radio-button value="1" :label="roles[1]"/>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="谈判轮数(我方出价轮数)">
          <el-slider v-model="round" :min="10" :max="1000" show-input />
        </el-form-item>
        <el-form-item label="谈判先手" size="large">
          <el-radio-group v-model="first">
            <el-radio-button value="1" label="我方" />
            <el-radio-button value="2" label="对方"/>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="谈判时间(分钟)">
          <el-slider v-model="timeLimit" :min="10" :max="45" show-input />
        </el-form-item>
      </el-form>
    </div>

    <!-- 玩家属性 -->
    <div class="profiles" >
      <div class="profile-settings">
        <span class="profile-title">我...</span>
        <div class="role-setting-slider">
          <span class="demonstration">你是否倾向于通过强力手段来压迫对方或争取更好的条件？</span>
          <el-slider v-model="my_value1" :min="-2" :max="2" :step="1" show-stops :marks="marks_1">
          </el-slider>
        </div>
        <div class="role-setting-slider">
          <span class="demonstration">当面对对方提出的条件时，你愿意在什么程度上做出让步？</span>
          <el-slider v-model="my_value2" :min="-2" :max="2" :step="1" show-stops :marks="marks_2">
          </el-slider>
        </div>
        <div class="role-setting-slider">
          <span class="demonstration">你是否特别关注达成协议，还是倾向于仅仅在自己能接受的条件下才同意协议？</span>
          <el-slider v-model="my_value3" :min="-2" :max="2" :step="1" show-stops :marks="marks_3">
          </el-slider>
        </div>
        <div class="role-setting-slider">
          <span class="demonstration">你通常依赖于过去的经验来做决策，还是依赖直觉或随机选择？</span>
          <el-slider v-model="my_value4" :min="-2" :max="2" :step="1" show-stops :marks="marks_4">
          </el-slider>
        </div>
        <div class="role-setting-slider">
          <span class="demonstration">你如何看待风险和不确定性？</span>
          <el-slider v-model="my_value5" :min="-2" :max="2" :step="1" show-stops :marks="marks_5">
          </el-slider>
        </div>
      </div>
      <div class="profile-settings">
        <span class="profile-title">对手...</span>
        <div class="role-setting-slider">
          <span class="demonstration">你是否倾向于通过强力手段来压迫对方或争取更好的条件？</span>
          <el-slider v-model="op_value1" :min="-2" :max="2" :step="1" show-stops :marks="marks_1">
          </el-slider>
        </div>
        <div class="role-setting-slider">
          <span class="demonstration">当面对对方提出的条件时，你愿意在什么程度上做出让步？</span>
          <el-slider v-model="op_value2" :min="-2" :max="2" :step="1" show-stops :marks="marks_2">
          </el-slider>
        </div>
        <div class="role-setting-slider">
          <span class="demonstration">你是否特别关注达成协议，还是倾向于仅仅在自己能接受的条件下才同意协议？</span>
          <el-slider v-model="op_value3" :min="-2" :max="2" :step="1" show-stops :marks="marks_3">
          </el-slider>
        </div>
        <div class="role-setting-slider">
          <span class="demonstration">你通常依赖于过去的经验来做决策，还是依赖直觉或随机选择？</span>
          <el-slider v-model="op_value4" :min="-2" :max="2" :step="1" show-stops :marks="marks_4">
          </el-slider>
        </div>
        <div class="role-setting-slider">
          <span class="demonstration">你如何看待风险和不确定性？</span>
          <el-slider v-model="op_value5" :min="-2" :max="2" :step="1" show-stops :marks="marks_5">
          </el-slider>
        </div>
      </div>
    </div>

    <!-- 页脚组件 -->
    <footerComp :next="nextTitle" :nextDetail="nextDetail" :previous="previousTitle" :previousDetail="previousDetail"
      :showPrevious="showPrevious" :showNext="showNext" @next-page="goToNextPage" @previous-page="goToPreviousPage" />
  </div>
</template>

<style scoped>
::v-deep .el-form-item__label{
font-size: 16px;
}

.container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
}

.domain-select {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin: 20px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 200px;
  margin-left: 10px;
}

.option-item {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
}

.option-item:hover {
  background-color: #f5f5f5;
}

.option-item.selected {
  background-color: #409eff;
  color: #fff;
  border-color: #409eff;
}

<<<<<<< HEAD
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
    margin-left: 150px;
    max-width: 1500px; /* 适应父容器 */
    display: flex;
    flex-direction: column; /* 使所有滑块容器竖着排列 */
    width: 600px;
    margin-top: 30px;
    margin-right: 100px;
}

.role-setting-slider {
    display: flex;
    flex-direction: column; /* 让描述和滑块垂直排列 */
    align-items: center; /* 使内容水平居中 */
    margin-bottom: 50px; /* 适当的间距 */
}

.role-setting-slider .el-slider {
    width: 100%; /* 让滑块宽度填满父容器 */
    margin-top: 10px; /* 描述与滑块之间的间距 */
}

.role-setting-slider .demonstration {
    font-size: 16px;
    line-height: 22px;
    color: #000000;
    text-align: center; /* 水平居中 */
    margin-bottom: -5px; /* 描述与滑块之间的间距 */
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


.container {
  display: flex;
  flex-direction: column;
  height: 100%; /* 子页面的高度，继承外部高度 */
  box-sizing: border-box;
}

.scrollable-content {
  height: calc(90% - 60px); /* 设置最大高度为父容器的 90%，减去按钮区域的高度 */
  overflow-y: auto; /* 启用垂直滚动 */
  padding: 16px; /* 内边距 */
  box-sizing: border-box;
  background-color: #f9f9f9; /* 可选背景色 */
}

/* 按钮区域 */
.fixed-buttons {
  position: fixed; /* 固定位置 */
  bottom: 100px; /* 距离底部 20px */
  right: 20px; /* 距离右边 20px */
  z-index: 1000; /* 确保按钮在其他元素之上 */
  display: flex; /* 使用 flexbox 布局 */
  gap: 10px; /* 按钮之间的间距 */
}
</style>

=======
.domain-description {
  flex-grow: 1;
  margin-left: 20px;
}

.domain-description h3 {
  font-size: 24px;
  margin-top: 0;
}

.domain-description p {
  font-size: 18px;
  line-height: 1.6;
  white-space: pre-line;
}
.domain-settings {
  margin-left: 100px;
}

.domain-settings .el-form-item {
  width:40%;
}

.profile-settings {
  display: flex;
  flex-direction: column;
}

.profile-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
}

.role-setting-slider {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.role-setting-slider .el-slider {
  width: 80%;
}

.role-setting-slider .demonstration {
  font-size: 16px;
  text-align: center;
}

.profiles {
  display: flex;
  justify-content: space-evenly;
  align-items: flex-start;
  margin-top: 30px;
}

footerComp {
  position: relative;
  bottom: 0;
  width: 100%;
  background-color: white; /* 你可以根据需求设置背景色 */
  text-align: center;
  /* padding: 10px; */
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}
</style>
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
