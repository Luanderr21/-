import dayjs from "dayjs";
import duration from "dayjs/plugin/duration";
dayjs.extend(duration);
/**
 * 进度格式化
 */
export const durationFormat = (ms: number | string) => {
  if (typeof ms === "string") {
    ms = Number(ms);
  }
  if (!ms) {
    return "00:00";
  }
  if (ms < 1000 * 60 * 60) {
    // 如果小于1小时
    return dayjs.duration(ms).format("mm:ss");
  } else if (ms < 1000 * 60 * 60 * 24) {
    // 如果小于24小时
    return dayjs.duration(ms).format("HH:mm:ss");
  }
};
