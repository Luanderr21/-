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
        },
        (err) => {
          console.error("结束录音出错：" + err);
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
      const fatherNode = document.getElementById("left");
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
      fatherNode?.appendChild(audio);
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
          const data = await this.upload(this.recBlob);
          videos.value[videoIndex].lyric = [];
          videos.value[videoIndex].fileName = data;
          ElMessage({
            message: "成功上传",
            type: "success",
          });
        }
        // this.dialogVisible = true;
        // console.dir(ElMessageBox);
        // ElMessageBox.confirm(
        //   "这将会上传您录的语音并对视频进行修改",
        //   "Warning",
        //   {
        //     confirmButtonText: "好",
        //     cancelButtonText: "取消",
        //     type: "warning",
        //   }
        // )
        //   .then(async () => {
        //     console.log("then");
        //     ElMessage({
        //       type: "success",
        //       message: "成功上传",
        //     });
        //   })
        //   .catch(() => {
        //     ElMessage({
        //       type: "info",
        //       message: "您取消了上传",
        //     });
        //   });
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
  <div>
    <div>
      <!-- 按钮 -->
      <button @click="recOpen">打开录音,请求权限</button>
      | <button @click="recStart">开始录音</button>
      <button @click="recStop">结束录音</button>
      | <button @click="recPlay">本地试听</button> |
      <el-button type="primary" @click.stop="handleUploadClick"
        >上传修改的内容</el-button
      >
    </div>
    <div style="padding-top: 5px">
      <!-- 波形绘制区域 -->
      <div
        style="
          border: 1px solid #ccc;
          display: inline-block;
          vertical-align: bottom;
        "
      >
        <div style="height: 100px; width: 300px" ref="recwave"></div>
      </div>
    </div>
  </div>
</template>
