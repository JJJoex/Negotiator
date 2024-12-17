import { createStore } from 'vuex';

const store = createStore({
  state: {
    nego_settings_data: null,
    my_interests_data: null,
    my_issues_data: null,
    op_interests_data: null,
    op_issues_data: null,
    nego_initial_data: null
  },
  mutations: {
    setNegoSettingsData(state, data) {
      state.nego_settings_data = data;
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
    }

  }
});

export default store;
