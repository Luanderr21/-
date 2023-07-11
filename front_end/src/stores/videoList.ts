import { defineStore } from "pinia";

export default defineStore("videoList", {
  state: () => {
    return {
      count: 2,
      videos: [
        {
          name: "asfdddddddddddddddddddddddddddd",
          lenght: 0,
          lyric: {},
          status: "uploaded", //uploaded, waiting, received, failed
          orderId: 0,
          index: "2-1",
        },
        {
          name: "fdasfdasdfafdasdfafasdfasdfasdfasdfasf",
          lenght: 0,
          lyric: {},
          status: "uploaded", //uploaded, waiting, received, failed
          orderId: 1,
          index: "2-2",
        },
      ],
    };
  },
  actions: {
    addVideo(name: string, lenght: Number, lyric: Object, orderId: String) {},
  },
});
