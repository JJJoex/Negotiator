<<<<<<< HEAD
<script setup lang="js">
import { useStore } from 'vuex';
import { ref, watch, onMounted } from 'vue';
import Papa from 'papaparse';
import rolesData from './specific_contents/domains_n_roles.json';  
import issuesData from './specific_contents/interests_issues.json';
import { sendJson } from './SendMessage';

const store = useStore();

const figure_path = ref(null);
const csv_path = ref(null);
const csvData = ref([]);  // 用于存储解析后的 CSV 数据
const transposedData = ref([]);  // 用于存储转置后的 CSV 数据
const negoSettingsData = ref({});
const roles_data_content = ref([]);
const domain_data_content = ref([]);
const agreementValue = ref("");  // 存储协议内容

// 字段翻译映射表
const translationMap = {
  "self_agent": "我方代理",
  "opp_agent": "对方代理",
  "agreement": "协议",
  "self_ufun_agreement": "我方效用协议",
  "opp_ufun_agreement": "对方效用协议",
  "number_of_steps": "步骤数",
  "total_social_welfare": "社会福利总值",
  "pareto_distance": "帕累托距离",
  "nash_distance": "纳什距离"
};

// 监听 store 中 figure_path 和 csv_path 的变化
watch(
  [
    () => store.state.figure_path,
    () => store.state.csv_path,
  ],
  () => {
    figure_path.value = store.state.figure_path;
    csv_path.value = store.state.csv_path;
  },
  { deep: true }
);

// 在组件挂载时初始化 figure_path 和 csv_path
onMounted(() => {
  figure_path.value = store.state.figure_path;
  csv_path.value = store.state.csv_path;

  // 当 csv_path 存在时，读取并解析 CSV 文件
  if (csv_path.value) {
    loadCSV(csv_path.value);
  }

  negoSettingsData.value = store.state.nego_settings_data;

  const domain = negoSettingsData.value["Domain"];
  roles_data_content.value = rolesData[domain] || [];
  domain_data_content.value = issuesData[domain];
});

// 读取并解析 CSV 文件
function loadCSV(path) {
  fetch(path)
    .then((response) => response.text())
    .then((data) => {
      Papa.parse(data, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: function (result) {
          csvData.value = result.data;
          transposeData();  // 转置数据并翻译
        },
        error: function (error) {
          console.error("CSV 解析出错", error);
        }
      });
    })
    .catch((error) => {
      console.error("获取 CSV 文件出错", error);
    });
}

// 转置数据（n行2列）并翻译字段和代理角色
async function transposeData() {
  const transposed = [];
  const promises = [];

  csvData.value.forEach(row => {
    const rowData = [];  // 用来存储当前行的转置数据，保持顺序不变

    for (const key in row) {
      let translatedKey = translationMap[key] || key;
      let value = row[key];

      if (key === 'self_agent' || key === 'opp_agent') {
        const selfAgent = row["self_agent"];
        const oppAgent = row["opp_agent"];

        if (selfAgent && oppAgent && roles_data_content.value.length === 2) {
          if (selfAgent === "AgentA" && oppAgent === "AgentB") {
            value = (key === 'self_agent') 
              ? roles_data_content.value[0] // 中文名1
              : roles_data_content.value[1]; // 中文名2
          } else if (selfAgent === "AgentB" && oppAgent === "AgentA") {
            value = (key === 'self_agent') 
              ? roles_data_content.value[1] // 中文名2
              : roles_data_content.value[0]; // 中文名1
          }
        }
        rowData.push([translatedKey, value]);
      }

      // 处理协议字段的异步翻译
      else if (key === 'agreement' && value !==null) {
        const promise = sendJson(99, { to_translate: value }).then((return_data) => {
          value = mapReturnDataToItems(domain_data_content, return_data.arr);
          agreementValue.value = value.join(", "); // 更新协议内容
          rowData.push([translatedKey, value]);
        });

        promises.push(promise);
      }else if (key === 'agreement' && value ===null) {
        if(store.state.curr_nego_state==="my_fail")  {
            value="未达成协议（我方拒绝）";
        }
        else if(store.state.curr_nego_state==="op_fail")  {
            value="未达成协议（对方拒绝）";
        }
        else if(store.state.curr_nego_state==="roundmax")  {
            value="未达成协议（达到最大轮数）";
        }
        else  {
            value="未达成协议";
        }

        
        agreementValue.value=value;
        rowData.push([translatedKey, value]);


        
      } else {
        rowData.push([translatedKey, value]);
      }
    }

    promises.push(Promise.resolve().then(() => {
      transposed.push(...rowData);
    }));
  });

  await Promise.all(promises);
  transposedData.value = transposed;
}

// 根据返回的数据映射成具体的物品
function mapReturnDataToItems(domainDataContent, returnData) {
  const mappedItems = [];
  const categories = Object.keys(domainDataContent._value);
  const items = domainDataContent._value;

  returnData.forEach((index, i) => {
    const category = categories[i];
    const categoryItems = items[category];

    if (categoryItems && categoryItems[index] !== undefined) {
      mappedItems.push(categoryItems[index]);
    } else {
      mappedItems.push(null);
    }
  });

  return mappedItems;
}
</script>

<template>
  <div>
    <!-- 在页面顶部展示协议 -->
    <div v-if="agreementValue.length > 0" style="text-align: center; margin-top: 20px;">
      <h3>达成的协议:</h3>
      <p>{{ agreementValue }}</p>
=======
<template>
    <div>
        <el-descriptions>
            <el-descriptions-item label="谈判结果">{{ display.result }}</el-descriptions-item>
            <el-descriptions-item label="最后一方">{{ display.last_player }}</el-descriptions-item>
            <el-descriptions-item label="最后一次出价">{{ display.last_bid }}</el-descriptions-item>
        </el-descriptions>
        <!-- 图片和图注 -->
        <figure style="text-align: center; margin-top: 20px;">
            <img src="@/python/output_dir/figures/bidding_history_travel_domain_mOlD_AgentB_vs_AgentA.png" alt="谈判结果分析"
                style="max-width: 100%; height: auto;" />
            <figcaption style="font-size: 14px; color: gray; margin-top: 10px;">
                谈判结果分析
            </figcaption>
        </figure>
        <footerComp nextDetail="回到首页" :showPrevious=false :showNext=true @next-page="goToNextPage" />
>>>>>>> f7d0d8306821e864c930f9a6bd131998a8cecaac
    </div>

    <!-- CSV 数据表格 -->
    <div v-if="transposedData.length > 0" style="margin-top: 20px; text-align: center;">
      <table border="1" style="width: 80%; margin: 0 auto; border-collapse: collapse; text-align: center;">
        <thead>
          <tr>
            <th>字段名</th>
            <th>值</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in transposedData" :key="index">
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 图片和图注 -->
    <figure style="text-align: center; margin-top: 20px;">
      <img v-if="figure_path" :src="figure_path" alt="谈判结果分析" style="max-width: 100%; height: auto;" />
      <figcaption style="font-size: 14px; color: gray; margin-top: 10px;">谈判结果分析</figcaption>
    </figure>
  </div>
</template>

<script setup lang="js">
import footerComp from "../components/footer.vue";
import { useRouter } from 'vue-router';
const router = useRouter();
const goToNextPage = () => {
    router.push('/introduction');
}

import { useStore } from "vuex";
import { ref, computed } from "vue";
const store = useStore();
const finish = computed(() => store.state.finish);
console.log(finish.value, 'finish');

const display = ref({
    result: finish.value.result,
    last_player: finish.value.last_player,
    last_bid: finish.value.last_bid
})

</script>
