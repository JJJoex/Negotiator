import { createStore } from 'vuex';

const store = createStore({
  state: {
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
    setFinish(state, data) {
      state.finish = data;
    }
  }
});

export default store;
