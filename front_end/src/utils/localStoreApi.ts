import dayjs from "dayjs";
class localStoreApi {
  set(key: string, val: string) {
    try {
      localStorage.setItem(key, val);
    } catch (e: any) {
      if (e.name === "QuotaExceededError") {
        throw new Error("Out of Memory Limit Localstorage");
      } else {
        throw new Error(e.name);
      }
    }
  }
  get(key: string): string {
    return localStorage.getItem(key) || "";
  }

  remove(key: string): void {
    localStorage.removeItem(key);
  }

  // 有时效的 localStorage
  setExpire(key: string, value: string, expire: number): void {
    const time = dayjs().add(expire, "h").unix();
    return this.set(key, JSON.stringify({ val: value, time }));
  }

  getExpire(key: string): string {
    const val: string = this.get(key);
    const dataObj = val ? JSON.parse(val) : null;
    if (dataObj && dayjs().unix() - dataObj.time < 0) {
      return dataObj.val;
    } else {
      return "";
    }
  }
}

export { localStoreApi };
