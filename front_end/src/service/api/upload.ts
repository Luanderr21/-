import service from "../request/index"

function uploadFile(){
  return service({
    method: "post",
    url: "api/upload"
  })
}

export { uploadFile }