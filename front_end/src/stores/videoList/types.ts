export type VideoItem = {
  name: string;
  lyric: LyricItem | null;
  status: "uploaded" | "waiting" | "received" | "failed";
  orderId: string;
  index: string;
  size: number | undefined;
};

export type LyricItem = {
  bg: string;
  ed: string;
  line: string;
};
