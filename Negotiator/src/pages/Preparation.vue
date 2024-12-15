<script setup lang="js">
import { ref, watch } from 'vue';
import backendData from './specific_contents/backend.json';


const prepare = ref({
  domain: null,
  role: 0,
  first: 0,
  round: 10,
  time: 10,
  my_profile: [0, 0, 0, 0, 0],
  opponent_profile: [0, 0, 0, 0, 0],
  my_interest: [],
  opponent_interest: [],
  my_issue: [],
  opponent_issue: []
});

watch(
  () => prepare.value.domain,
  (newVal, oldVal) => {
    if (newVal) {
      const issue = backendData[newVal].issue;
      const keys = Object.keys(issue);
      const values = Object.values(issue);

      prepare.value.my_interest = keys.map(() => 0);
      prepare.value.opponent_interest = keys.map(() => 0);
      prepare.value.my_issue = values.flat().map(() => 0);
      prepare.value.opponent_issue = values.flat().map(() => 0);
      // prepare.value.opponent_issue = values.map((value) => Array(value.length).fill(0));
    }
  },
  { immediate: true }
);
const marks = {
  '-2': '非常不同意',
  '-1': '',
  '0': '中立',
  '1': '',
  '2': '非常同意'
};


</script>

<template>
  <div class="preparation-domain">
    <div>
      <h3>请选择谈判域</h3>
      <el-radio-group v-model="prepare.domain" size="large">
        <el-radio-button v-for="item in Object.keys(backendData)" :label="item" :value="item" />
      </el-radio-group>
    </div>
  </div>
  <div class="preparation-settings" v-if="prepare.domain">
    <div class="domain-settings">
      <div class="domain-description">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="谈判域">{{ prepare.domain }}</el-descriptions-item>
          <el-descriptions-item label="谈判方">{{ backendData[prepare.domain].players }}</el-descriptions-item>
          <el-descriptions-item label="详情">{{ backendData[prepare.domain].description }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <div class="domain-detail">
        <el-form :model="prepare">
          <el-form-item label="谈判角色">
            <el-radio-group v-model="prepare.role">
              <el-radio-button v-for="(item, idx) in backendData[prepare.domain].role" :value="idx">{{ item
                }}</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="谈判先后">
            <el-radio-group v-model="prepare.first">
              <el-radio-button :value="0">先手</el-radio-button>
              <el-radio-button :value="1">后手</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="谈判轮数" disabled="false">
            <el-input-number v-model="prepare.round" :min="10" :max="1000" show-input>
              <template #suffix><span>轮</span></template>
            </el-input-number>
          </el-form-item>
          <el-form-item label="谈判时间(分钟)" disable="false">
            <el-input-number v-model="prepare.time" :min="10" :max="45" show-input>
              <template #suffix><span>分钟</span></template>
            </el-input-number>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="profile-settings">
      <div class="my-profile">
        <h2>关于我</h2>
        <div class="profile-slider">
          <p class="profile-question">倾向于通过强力手段来压迫对方或争取更好的条件</p>
          <el-slider v-model="prepare.my_profile[0]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
        <div class="profile-slider">
          <p class="profile-question">面对对方提出的条件时，愿意完全妥协</p>
          <el-slider v-model="prepare.my_profile[1]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
        <div class="profile-slider">
          <p class="profile-question">特别关注谈判能否达成协议</p>
          <el-slider v-model="prepare.my_profile[2]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
        <div class="profile-slider">
          <p class="profile-question">通常依赖于过去的经验来做决策</p>
          <el-slider v-model="prepare.my_profile[3]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
        <div class="profile-slider">
          <p class="profile-question">对于风险和不确定性能完全接受</p>
          <el-slider v-model="prepare.my_profile[4]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
      </div>
      <div class="opponent-profile">
        <h2>关于对手</h2>
        <div class="profile-slider">
          <p class="profile-question">倾向于通过强力手段来压迫对方或争取更好的条件</p>
          <el-slider v-model="prepare.opponent_profile[0]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
        <div class="profile-slider">
          <p class="profile-question">面对对方提出的条件时，愿意完全妥协</p>
          <el-slider v-model="prepare.opponent_profile[1]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
        <div class="profile-slider">
          <p class="profile-question">特别关注谈判能否达成协议</p>
          <el-slider v-model="prepare.opponent_profile[2]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
        <div class="profile-slider">
          <p class="profile-question">通常依赖于过去的经验来做决策</p>
          <el-slider v-model="prepare.opponent_profile[3]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
        <div class="profile-slider">
          <p class="profile-question">对于风险和不确定性能完全接受</p>
          <el-slider v-model="prepare.opponent_profile[4]" :min="-2" :max="2" :step="1" :marks="marks"></el-slider>
        </div>
      </div>
    </div>
    <div class="my-interest">
      <div class="slider">
        <h2>我的兴趣</h2>
        <el-form :model="prepare">
          <el-form-item :label="item" v-for="(item, idx) in Object.keys(backendData[prepare.domain].issue)">
            <el-slider v-model="prepare.my_interest[idx]"></el-slider>
          </el-form-item>
        </el-form>
      </div>
      <div class="interest-chart" id="my-interest" style="width: 50%; height: 300px;"></div>
    </div>
    <div class="my-issue">
      <h2>我的议题</h2>
      <template v-for="(item, domain_idx) in Object.keys(backendData[prepare.domain].issue)">
        <div class="slider">
          <h3>{{ item }}</h3>
          <el-form>
            <el-form-item v-for="(key, issue_idx) in backendData[prepare.domain].issue[item]" :label="key">
              <el-slider
                v-model="prepare.my_issue[domain_idx * backendData[prepare.domain].issue[item].length + issue_idx]"></el-slider>
            </el-form-item>
          </el-form>
        </div>
        <div class="interest-chart" :id="'my-issue-' + item" style="width: 50%; height: 300px;"></div>
      </template>
    </div>
    <div class="opponent-interest">
      <div class="slider">
        <h2>对手兴趣</h2>
        <el-form :model="prepare">
          <el-form-item :label="item" v-for="(item, idx) in Object.keys(backendData[prepare.domain].issue)">
            <el-slider v-model="prepare.opponent_interest[idx]"></el-slider>
          </el-form-item>
        </el-form>
      </div>
      <div class="interest-chart" id="opponent-interest" style="width: 50%; height: 300px;"></div>
    </div>
    <div class="opponent-issue">
      <h2>对手议题</h2>
      <template v-for="(item, domain_idx) in Object.keys(backendData[prepare.domain].issue)">
        <div class="slider">
          <h3>{{ item }}</h3>
          <el-form :model="prepare">
            <el-form-item v-for="(key, issue_idx) in backendData[prepare.domain].issue[item]" :label="key">
              <el-slider
                v-model="prepare.opponent_issue[domain_idx * backendData[prepare.domain].issue[item].length + issue_idx]"></el-slider>
            </el-form-item>
          </el-form>
        </div>
        <div class="interest-chart" :id="'opponent-issue-' + item" style="width: 50%; height: 300px;"></div>
      </template>
    </div>
    <div class="confirmation">
      <el-descriptions title="谈判确认" :column="2" border>
        <el-descriptions-item label="谈判域">{{ prepare.domain }}</el-descriptions-item>
        <el-descriptions-item label="谈判角色">{{ prepare.role === 0 ? backendData[prepare.domain].role[0] :backendData[prepare.domain].role[1]  }}</el-descriptions-item>
        <el-descriptions-item label="谈判先后">{{ prepare.first === 0 ? '先手' : '后手' }}</el-descriptions-item>
        <el-descriptions-item label="谈判轮数">{{ prepare.round }}轮</el-descriptions-item>
        <el-descriptions-item label="谈判时间">{{ prepare.time }}分钟</el-descriptions-item>
        <el-descriptions-item label="我的特质">{{ prepare.my_profile }}</el-descriptions-item>
        <el-descriptions-item label="对手特质">{{ prepare.opponent_profile }}</el-descriptions-item>
        <el-descriptions-item label="我的兴趣">{{ prepare.my_interest }}</el-descriptions-item>
        <el-descriptions-item label="我的议题">{{ prepare.my_issue }}</el-descriptions-item>
        <el-descriptions-item label="对手兴趣">{{ prepare.opponent_interest }}</el-descriptions-item>
        <el-descriptions-item label="对手议题">{{ prepare.opponent_issue }}</el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<style scoped>
.preparation-domain {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.domain-settings {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-evenly;
  margin: 20px 0;
}

.domain-description {
  width: 60%;
}

.domain-detail {
  width: 30%;
}

.profile-settings {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-evenly;
  margin: 20px 0;
}

.profile-settings .my-profile,
.profile-settings .opponent-profile {
  width: 40%;
  text-align: center;
}

.profile-slider {
  margin: 20px 5px;
}

.my-interest,
.opponent-interest,
.my-issue,
.opponent-issue {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-evenly;
  margin: 20px 0;
}

.slider {
  width: 40%;
}

.interest-chart {
  width: 50%;
  height: 100%;
  border: 1px solid #000000;
}
</style>
