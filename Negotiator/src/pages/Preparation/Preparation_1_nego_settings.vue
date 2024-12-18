<script setup lang="js">
import { onMounted, ref } from 'vue';
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
const options = ref([]); // 存储选项
const selectedOption = ref(null); // 存储选中的选项

const timeLimit = ref(10);

const roles = ref([]);
const first = ref("1");
const role = ref("0")

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
  return rolesData[domain];
};

// 在选项数据加载后，动态显示角色
const loadRoles = () => {
  if (selectedOption.value) {
    const domain = selectedOption.value.label;
    roles.value = getRolesForDomain(domain);
  }
};




// const swapRoles = () => {
//   roles.value = [roles.value[1], roles.value[0]];
// };



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
  emit('submit-data', dataToSend);
};

const handleRandomClick = () => {
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
};

const marks_1 = {
  "-2": "完全不倾向竞争",
  "-1": "",
  "0": "中立/无明显倾向",
  "1": "",
  "2": "非常倾向竞争"
};
const marks_2 = {
  "-2": "完全不愿意妥协",
  "-1": "",
  "0": "中立/无明显倾向",
  "1": "",
  "2": "非常愿意妥协"
};
const marks_3 = {
  "-2": "完全不关心达成协议",
  "-1": "",
  "0": "不太重视达成协议",
  "1": "",
  "2": "非常重视达成协议"
};
const marks_4 = {
  "-2": "非常依赖随机与直觉",
  "-1": "",
  "0": "无明显依赖",
  "1": "",
  "2": "非常依赖经验"
};
const marks_5 = {
  "-2": "完全避免任何风险",
  "-1": "",
  "0": "追求较为保守的选择",
  "1": "",
  "2": "完全愿意承担风险"
};
</script>

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
        <p>{{ selectedOption.description }}</p>
      </div>
    </div>

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
}

.option-item:hover {
  background-color: #f5f5f5;
}

.option-item.selected {
  background-color: #409eff;
  color: #fff;
  border-color: #409eff;
}

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
