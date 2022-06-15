import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    bucket: null,
    video: null,
    gif: null,
    status: null,
  },
  getters: {},
  mutations: {
    setBucket(state, payload) {
      state.isSubmitted = true;
      state.bucket = payload.bucket;
    },
    setVideo(state, payload) {
      state.isSubmitted = true;
      state.video = payload.video;
      state.gif = payload.gif;
    },
    clearBucket(state) {
      state.isSubmitted = false;
      state.bucket = null;
      state.video = null;
      state.gif = null;
    },
    clearVideo(state) {
      state.isSubmitted = false;
      state.video = null;
      state.gif = null;
    },
  },
  actions: {},
  modules: {},
});
