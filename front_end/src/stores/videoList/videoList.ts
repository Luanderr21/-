import { defineStore } from "pinia";
import { LyricItem, VideoItem } from "./types";

export default defineStore("videoList", {
  state: () => {
    return {
      count: 1,
      videos: [
        {
          name: "course001.mp4",
          lyric: [],
          playingIndex: 0,
          status: "waiting",
          orderId: "DKHJQ20230714102427553LWq8DLmgBamJ8csl",
          size: 0,
          index: "2-1",
          startIndex: -1,
          endIndex: -1,
          fileName: "",
        },
      ] as VideoItem[],
    };
  },
  actions: {
    addVideo(name: string, orderId: string, size: number | undefined) {
      this.videos.push({
        name,
        lyric: [],
        playingIndex: 0,
        status: "waiting",
        orderId,
        size,
        index: "2-" + this.count.toString(),
        startIndex: -1,
        endIndex: -1,
        fileName: "",
      });
    },
    updateLyric(orderId: string, text: LyricItem[]) {
      const indexNow = this.videos.findIndex((item) => {
        console.log("item.orderId === orderId: ", item.orderId, orderId);
        return item.orderId === orderId;
      });
      console.log(indexNow);
      this.videos[indexNow].lyric = text;
      this.videos[indexNow].status = "received";
    },
    findVideoIndex(orderId: string) {
      return this.videos.findIndex((item) => item.orderId === orderId);
    },
    updateLyricIndex(start: number, end: number, videoIndex: number) {
      this.videos[videoIndex].startIndex = start;
      this.videos[videoIndex].endIndex = end;
    },
  },
});
