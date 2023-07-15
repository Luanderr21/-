import service from "../request/index";

function queryText(orderId: string) {
  return service({
    url: "/query",
    method: "post",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    data: {
      orderId,
    },
  });
}

export { queryText };
