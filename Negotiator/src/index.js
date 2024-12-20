import { createStore } from 'vuex';

const store = createStore({
  state: {
    nego_settings_data: null,
    my_interests_data: null,
    my_issues_data: null,
    op_interests_data: null,
    op_issues_data: null,
    nego_initial_data: null,
    curr_nego_state:"negotiating",
    figure_path:null,
    csv_path:null,
    prepare: {
      domain: '',
      roles: {
        my: '',
        opponent: ''
      },
      first: false,
      rounds: 10,
      time: 10,
      my_profile: [0, 0, 0, 0, 0],
      opponent_profile: [0, 0, 0, 0, 0],
      my_interests: {},
      opponent_interests: {},
      my_issues: {},
      opponent_issues: {},
    },
    finish: {
      result: '',
      last_player: '',
      last_bid: [],
    }
  },
  mutations: {
    updatePrepare(state, data) {
      state.prepare = data;
    },
    setMyInterestsData(state, data) {
      state.my_interests_data = data;
    },
    setMyIssuesData(state, data) {
      state.my_issues_data = data;
    },
    setOpInterestsData(state, data) {
      state.op_interests_data = data;
    },
    setOpIssuesData(state, data) {
      state.op_issues_data = data;
    },
    setNegoInitialData(state, data) {
      state.nego_initial_data = data;
    },
    setCurrNegoState(state, curr_state) {
      // negotiating / succeed / fail / timeout / roundmax
      // 正在谈判 / 成功 / 失败（单方破裂） / 超时 / 到达最大轮数
      state.curr_nego_state = curr_state;
    },
    setFigurePath(state, path) {
      state.figure_path = path;
    },
    setCsvPath(state, path) {
      state.csv_path = path;
    },

    setFinish(state, data) {
      state.finish = data;
    }
  }
});

export default store;
