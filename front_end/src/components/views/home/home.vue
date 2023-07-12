<script setup lang="ts">
import { ref, reactive, watch } from "vue";
import useVideoList from "~/stores/videoList/videoList";
import { queryText } from "~/service/api/query";
import type { UploadFile, UploadRawFile, UploadFiles } from "element-plus";

const videoListStore = reactive(useVideoList());
let fullscreenLoading = ref(false);

// const textarea = ref("");

const fileList: UploadFile[] = reactive([]);

const handleBeforeUpload = function (rawFile: UploadRawFile) {
  console.log("rawFile: ", rawFile);
  fullscreenLoading.value = true;
};

const handleSuccess = async function (
  response: any,
  uploadFile: UploadFile
  // uploadFiles: UploadFiles
) {
  // console.log("response: ", response);
  // console.log("UploadFiles: ", uploadFiles);
  // console.log("UploadFile: ", uploadFile);
  const { name, size } = uploadFile;
  const videoSize = typeof size === "number" ? size : undefined;
  videoListStore.addVideo(name, response, videoSize);
  // videoListStore.addVideo(name, response, size);
  // textarea.value = uploadFile;
  fullscreenLoading.value = false;
  // 防止访问太快
  setTimeout(async () => {
    const { data } = await queryText(response);
    videoListStore.updateLyric(response, data);
  }, 300);
};

const handleError = function () {
  console.log("upload error");
};

// const handleChange = (a: any) => {
//   console.log("change", a);
// };

// watch(fileList, (newValue, oldValue) => {
//   console.log("filelist: newValue, oldValue: ", newValue, oldValue);
// });
</script>

<template>
  <div class="home">
    <el-upload
      class="upload-demo"
      drag
      action="api/upload"
      name="video"
      :before-upload="handleBeforeUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
      :file-list="fileList"
    >
      <svg
        t="1688786819959"
        class="icon"
        viewBox="0 0 1264 1024"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        p-id="2573"
        id="mx_n_1688786819960"
        width="200"
        height="200"
      >
        <path
          d="M992.171444 312.62966C975.189616 137.155482 827.415189 0 647.529412 0 469.849434 0 323.616239 133.860922 303.679205 306.210218 131.598564 333.839271 0 482.688318 0 662.588235c0 199.596576 161.815189 361.411765 361.411765 361.411765h184.014581V692.705882H294.530793l337.939795-361.411764 337.939796 361.411764H726.132229v331.294118H933.647059v-1.555371c185.470975-15.299199 331.294118-170.426291 331.294117-359.856394 0-168.969898-116.101408-310.367302-272.769732-349.958575z"
          p-id="2574"
          fill="#919191"
        ></path>
      </svg>
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
        <div class="el-upload__tip">ogg/webm/mp4 files</div>
      </div>
    </el-upload>
  </div>
</template>

<style scoped lang="scss">
.home {
  margin-top: 10rem;
  padding: 0 20rem 0 20rem;
}
</style>
