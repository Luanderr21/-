export type VideoState = {
  /** 显示控件 */
  showControl: boolean;
  /** 是否全屏 */
  isFullscreen: boolean;
  /** 是否网页全屏 */
  isPageFull: boolean;
  /** 是否画中画 */
  isPictureInPicture: boolean;
  /** 是否暂停播放中 */
  isPause: boolean;
  /** 音量 */
  volume: number;
  /** 倍速 */
  rate: string;
  /** 已播放时长 */
  currentTime: number;
  /** 总时长 */
  duration: number;
  /** 视频是否播放过 */
  isPlayed: boolean;
};
