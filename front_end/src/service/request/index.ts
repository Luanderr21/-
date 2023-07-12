import axios from "axios";
import { BASE_URL, TIMEOUT } from "./config";

// class AxiosRequest {
//   constructor(baseURL: string, timeout = 10000) {
//     // 构造函数
//     this.instance = axios.create({
//       baseURL,
//       timeout,
//     });
//     // // 请求拦截器
//     // this.instance.interceptors.request.use(
//     //   (config) => {
//     //     mainStore.isLoading = true;
//     //     // console.log("is loading");
//     //     return config;
//     //   },
//     //   (err) => {
//     //     return err;
//     //   }
//     // );

//     // // 响应拦截器
//     // this.instance.interceptors.response.use(
//     //   (res) => {
//     //     mainStore.isLoading = false;
//     //     // console.log("loading end");
//     //     return res;
//     //   },
//     //   (err) => {
//     //     mainStore.isLoading = false;
//     //     return err;
//     //   }
//     // );
//   }

//   request(config) {
//     // mainStore.isLoading = true
//     return new Promise((resolve, reject) => {
//       this.instance
//         .request(config)
//         .then((res) => {
//           resolve(res.data);
//           // mainStore.isLoading = false
//         })
//         .catch((err) => {
//           reject(err);
//           // mainStore.isLoading = false
//         });
//     });
//   }

//   get(config) {
//     return this.request({ ...config, method: "get" });
//   }

//   post(config) {
//     return this.request({ ...config, method: "post" });
//   }
// }
// export default new AxiosRequest(BASE_URL, TIMEOUT);

const service = axios.create({ baseURL: BASE_URL, timeout: TIMEOUT });

export default service;
