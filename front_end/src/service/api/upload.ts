import service from "../request/index";

function uploadFile() {
  return service({
    method: "post",
    url: "api/upload",
  });
}

function replaceFile(data: FormData) {
  return service.postForm("replace", data, {});
}

export { uploadFile, replaceFile };
