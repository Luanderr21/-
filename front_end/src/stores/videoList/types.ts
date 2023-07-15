export type VideoItem = {
  name: string;
  lyric: LyricItem[] | [];
  playingIndex: number; // 用于确定现在正在显示的那句话
  status: "uploaded" | "waiting" | "received" | "failed";
  orderId: string;
  index: string;
  size: number | undefined;
  startIndex: number;
  endIndex: number;
  fileName: string;
};

export type LyricItem = {
  bg: string;
  ed: string;
  line: string;
};
