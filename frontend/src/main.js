import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import "./plugins/vue-axios";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");

// import { createApp } from "vue";
// import App from "./App.vue";
// import router from "./router";
//
// const app = createApp(App);
// app.config.globalProperties.$redirect = (page) => {
//   router.push(page);
// };
// app.use(router).mount("#app");
