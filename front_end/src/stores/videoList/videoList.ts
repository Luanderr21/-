import { defineStore } from "pinia";
import { LyricItem, VideoItem } from "./types";

export default defineStore("videoList", {
  state: () => {
    return {
      count: 0,
      videos: [] as VideoItem[],
    };
  },
  actions: {
    addVideo(name: string, orderId: string, size: number) {
      this.videos.push({
        name,
        lyric: null,
        status: "waiting",
        orderId,
        size,
        index: "2-" + this.count.toString(),
      });
    },
    updateLyric(orderId: string, text: LyricItem) {
      const indexNow = this.videos.findIndex((item) => {
        console.log("tem.orderId === orderId: ", item.orderId, orderId);
        return item.orderId === orderId;
      });
      console.log(indexNow);
      this.videos[indexNow].lyric = text;
      this.videos[indexNow].status = "received";
    },
  },
});
