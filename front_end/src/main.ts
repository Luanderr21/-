import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router/index";
import App from "./App.vue";
import "~/styles/index.scss";
import "uno.css";

import "element-plus/theme-chalk/src/message.scss";

const app = createApp(App);
const pinia = createPinia();
// app.use(ElementPlus);
app.use(pinia);
app.use(router);
app.mount("#app");
