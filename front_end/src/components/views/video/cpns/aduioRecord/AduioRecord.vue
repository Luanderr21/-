<script lang="ts">
//必须引入的核心
import Recorder from "recorder-core";
//引入mp3格式支持文件；如果需要多个格式支持，把这些格式的编码引擎js文件放到后面统统引入进来即可
import "recorder-core/src/engine/mp3";
import "recorder-core/src/engine/mp3-engine";
//录制wav格式的用这一句就行
//import 'recorder-core/src/engine/wav'

//可选的插件支持项，这个是波形可视化插件
import "recorder-core/src/extensions/wavesurfer.view";

//ts import 提示：npm包内已自带了.d.ts声明文件（不过是any类型）

import { replaceFile } from "~/service/api/upload";
import { useRoute } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import { storeToRefs } from "pinia";
import "element-plus/es/components/message-box/style/css";
import "element-plus/es/components/message/style/css";
import useVideoListStore from "~/stores/videoList/videoList";
import { durationFormat } from "~/utils/datatime";

export default {
  data: () => {
    return {
      rec: {},
      wave: {},
      revBlob: {},
      // dialogVisible: false,
      duration: 0,
      orderId: "",
      bg: 0,
      ed: 0,
      isRecording: false,
    };
  },
  methods: {
    recOpen() {
      //创建录音对象
      this.rec = Recorder({
        type: "mp3", //录音格式，可以换成wav等其他格式
        sampleRate: 16000, //录音的采样率，越大细节越丰富越细腻
        bitRate: 16, //录音的比特率，越大音质越好
        onProcess: (
          buffers,
          powerLevel,
          bufferDuration,
          bufferSampleRate,
          newBufferIdx,
          asyncEnd
        ) => {
          //录音实时回调，大约1秒调用12次本回调
          //可实时绘制波形，实时上传（发送）数据
          if (this.wave)
            this.wave.input(
              buffers[buffers.length - 1],
              powerLevel,
              bufferSampleRate
            );
        },
      });

      //打开录音，获得权限
      this.rec.open(
        () => {
          console.log("录音已打开");
          ElMessage({
            message: "按下开始录音即可录音",
            type: "success",
          });
          if (this.$refs.recwave) {
            //创建音频可视化图形绘制对象
            this.wave = Recorder.WaveSurferView({ elem: this.$refs.recwave });
          }
        },
        (msg, isUserNotAllow) => {
          //用户拒绝了录音权限，或者浏览器不支持录音
          console.log(
            (isUserNotAllow ? "UserNotAllow，" : "") + "无法录音:" + msg
          );
        }
      );
    },
    recStart() {
      if (!this.rec) {
        console.error("未打开录音");
        return;
      }
      this.rec.start();
      this.isRecording = true;
      console.log("已开始录音");
    },

    recStop() {
      if (!this.rec) {
        console.error("未打开录音");
        return;
      }
      this.rec.stop(
        (blob, duration) => {
          //blob就是我们要的录音文件对象，可以上传，或者本地播放
          this.recBlob = blob;
          //简单利用URL生成本地文件地址，此地址只能本地使用，比如赋值给audio.src进行播放，赋值给a.href然后a.click()进行下载（a需提供download="xxx.mp3"属性）
          this.duration = duration;
          var localUrl = (window.URL || webkitURL).createObjectURL(blob);
          console.log("录音成功", blob, localUrl, "时长:" + duration + "ms");

          // this.upload(blob); //把blob文件上传到服务器

          this.rec.close(); //关闭录音，释放录音资源，当然可以不释放，后面可以连续调用start
          this.rec = null;
          this.isRecording = false;
        },
        (err) => {
          console.error("结束录音出错：" + err);
          this.isRecording = false;
          this.rec.close(); //关闭录音，释放录音资源，当然可以不释放，后面可以连续调用start
          this.rec = null;
        }
      );
    },
    async upload(blob: any) {
      // KNOW: 文件上传知识
      //使用FormData用multipart/form-data表单上传文件
      //或者将blob文件用FileReader转成base64纯文本编码，使用普通application/x-www-form-urlencoded表单上传
      /**
       *
       * @param audio
       * @param orderID
       * @param bg
       * @param ed
       */
      var form = new FormData();
      form.append("audio", blob, "recorder.mp3"); //和普通form表单并无二致，后端接收到upfile参数的文件，文件名为recorder.mp3
      form.append("orderId", this.orderId);
      // TODO: 通过 pinia 获取
      form.append("bg", this.bg.toString());
      form.append("ed", this.ed.toString());

      const { data } = await replaceFile(form);
      // console.log("data", data);
      return data;
      // var xhr = new XMLHttpRequest();
      // xhr.open("POST", "/upload/xxxx");
      // xhr.onreadystatechange = () => {
      //   if (xhr.readyState == 4) {
      //     if (xhr.status == 200) {
      //       console.log("上传成功");
      //     } else {
      //       console.error("上传失败" + xhr.status);
      //     }
      //   }
      // };
      // xhr.send(form);
    },

    recPlay() {
      const fatherNode = document.querySelector("#audio-container");
      const nextNode = document.querySelector(".wave-container");
      // 清除 原先存在的节点
      if (document.getElementById("record-audio")) {
        fatherNode?.removeChild(
          document.getElementById("record-audio") as Node
        );
      }
      //本地播放录音试听，可以直接用URL把blob转换成本地播放地址，用audio进行播放
      var localUrl = URL.createObjectURL(this.recBlob);
      var audio = document.createElement("audio");
      audio.controls = true;
      audio.id = "record-audio";
      fatherNode?.insertBefore(audio, nextNode);
      audio.src = localUrl;
      audio.play(); //这样就能播放了

      //注意不用了时需要revokeObjectURL，否则霸占内存
      setTimeout(function () {
        URL.revokeObjectURL(audio.src);
      }, 5000);
    },
    handleClose(done: () => void) {
      ElMessageBox.confirm("Are you sure to close this dialog?")
        .then(() => {
          done();
        })
        .catch(() => {
          // catch error
        });
    },
    async handleUploadClick() {
      const videoListStore = useVideoListStore();
      const { videos } = storeToRefs(videoListStore);
      const videoIndex = videoListStore.findVideoIndex(this.orderId);
      this.bg = Number(
        videos.value[videoIndex].lyric[videos.value[videoIndex].startIndex - 1]
          ?.bg
      );
      this.ed = Number(
        videos.value[videoIndex].lyric[videos.value[videoIndex].startIndex - 1]
          ?.ed
      );
      const selectedDuration = this.ed - this.bg;
      console.log("this.ed - this.bg: ", this.ed, this.bg);
      console.log(`录音时间过长 ${this.duration} > ${selectedDuration}`);

      if (this.duration !== 0 && selectedDuration >= this.duration) {
        console.log(
          "我进来了，",
          this.duration !== 0 && selectedDuration >= this.duration
        );
        if (window.confirm("你是否确定上传更改的音频")) {
          console.log("确定");
          videos.value[videoIndex].status = "waiting";
          const data = await this.upload(this.recBlob);
          // videos.value[videoIndex].lyric = [];
          videos.value[videoIndex].fileName = data;
          ElMessage({
            message: "成功上传",
            type: "success",
          });
          videos.value[videoIndex].status = "received";
        }
        console.log("first");
      } else {
        ElMessage({
          message: `没有录音或录音时间过长 ${durationFormat(
            this.duration
          )} > ${durationFormat(selectedDuration)}`,
          type: "error",
          duration: 5000,
        });
      }
    },
  },
  created() {
    this.orderId = useRoute().fullPath.slice(7); //根据路由获取orderId
  },
};
</script>

<template>
  <div class="container" id="audio-container">
    <div class="button-container">
      <!-- 按钮 -->
      <el-button @click="recOpen">请求权限</el-button
      ><el-button @click="recPlay">本地试听</el-button
      ><el-button type="primary" @click.stop="handleUploadClick"
        >上传修改</el-button
      >
    </div>
    <div class="wave-container">
      <!-- 波形绘制区域 -->
      <div
        style="
          border: 1px solid #ccc;
          display: inline-block;
          vertical-align: bottom;
          width: 100%;
        "
      >
        <div style="height: 150px; width: 100%" ref="recwave"></div>
      </div>
      <div class="record-button-container">
        <el-button @click="recStart" circle v-if="!isRecording"
          ><svg
            t="1689738622995"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="3282"
            width="16"
            height="16"
          >
            <path
              d="M808.533333 610.133333c-10.666667-4.266667-23.466667 2.133333-27.733333 12.8-38.4 119.466667-147.2 198.4-273.066667 198.4-157.866667 0-285.866667-128-285.866666-285.866666 0-12.8-8.533333-21.333333-21.333334-21.333334s-21.333333 8.533333-21.333333 21.333334c0 174.933333 136.533333 315.733333 307.2 328.533333v78.933333H405.333333c-12.8 0-21.333333 8.533333-21.333333 21.333334s8.533333 21.333333 21.333333 21.333333h204.8c12.8 0 21.333333-8.533333 21.333334-21.333333s-8.533333-21.333333-21.333334-21.333334h-81.066666v-78.933333c134.4-8.533333 249.6-98.133333 292.266666-228.266667 4.266667-10.666667-2.133333-21.333333-12.8-25.6z"
              fill="#666767"
              p-id="3283"
            ></path>
            <path
              d="M507.733333 736c102.4 0 183.466667-83.2 183.466667-183.466667V226.133333c0-102.4-83.2-183.466667-183.466667-183.466666s-183.466667 83.2-183.466666 183.466666v324.266667c0 102.4 83.2 185.6 183.466666 185.6z m-140.8-509.866667c0-78.933333 64-140.8 140.8-140.8 78.933333 0 140.8 64 140.8 140.8v324.266667c0 78.933333-64 140.8-140.8 140.8s-140.8-64-140.8-140.8V226.133333z"
              fill="#666767"
              p-id="3284"
            ></path>
            <path
              d="M819.2 544m-29.866667 0a29.866667 29.866667 0 1 0 59.733334 0 29.866667 29.866667 0 1 0-59.733334 0Z"
              fill="#666767"
              p-id="3285"
            ></path></svg
        ></el-button>
        <el-button @click="recStop" circle v-else>
          <svg
            t="1689738398678"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="2305"
            width="16"
            height="16"
          >
            <path
              d="M785.655172 494.344828a17.655172 17.655172 0 0 0-17.655172 17.655172v105.931034c0 136.297931-110.874483 247.172414-247.172414 247.172414s-247.172414-110.874483-247.172414-247.172414v-105.931034a17.655172 17.655172 0 1 0-35.310344 0v105.931034c0 149.804138 117.300966 272.401655 264.827586 281.582345V988.689655h-88.275862a17.655172 17.655172 0 1 0 0 35.310345h211.862069a17.655172 17.655172 0 1 0 0-35.310345h-88.275862v-89.176276c147.526621-9.18069 264.827586-131.795862 264.827586-281.582345v-105.931034a17.655172 17.655172 0 0 0-17.655173-17.655172z"
              fill=""
              p-id="2306"
            ></path>
            <path
              d="M520.827586 812.137931c107.078621 0 194.206897-87.128276 194.206897-194.206897V194.206897c0-107.078621-87.128276-194.206897-194.206897-194.206897s-194.206897 87.128276-194.206896 194.206897v423.724137c0 107.078621 87.128276 194.206897 194.206896 194.206897z m-158.896552-617.931034c0-87.622621 71.291586-158.896552 158.896552-158.896552s158.896552 71.273931 158.896552 158.896552v423.724137c0 87.622621-71.291586 158.896552-158.896552 158.896552s-158.896552-71.273931-158.896552-158.896552V194.206897zM921.723586 75.793655a17.637517 17.637517 0 0 0-24.964414 0l-158.896551 158.896552a17.637517 17.637517 0 1 0 24.964413 24.964414l158.896552-158.896552a17.637517 17.637517 0 0 0 0-24.964414z"
              fill=""
              p-id="2307"
            ></path>
            <path
              d="M656.896 365.585655a17.637517 17.637517 0 1 0-24.964414-24.964414l-247.172414 247.172414a17.637517 17.637517 0 1 0 24.964414 24.964414l247.172414-247.172414zM225.862621 746.690207l-123.586207 123.586207a17.637517 17.637517 0 1 0 24.964414 24.964414l123.586206-123.586207a17.637517 17.637517 0 1 0-24.964413-24.964414z"
              fill=""
              p-id="2308"
            ></path>
          </svg>
        </el-button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container {
  width: 100%;
  margin-top: 20px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  flex-wrap: warp;
  gap: 10px;
  background-color: var(--el-color-warning-light-7);
  box-sizing: border-box;
  padding: 10px;
  .button-container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    button {
      width: 50px;
    }
    .ep-button + .ep-button {
      margin-left: 0;
    }
  }
  .wave-container {
    width: 40%;
    height: 150px;
    position: relative;
    .record-button-container {
      position: absolute;
      left: 0;
      top: 0;
      button {
        background-color: rgba(255, 255, 255, 0.2);
      }
    }
  }
}
</style>
