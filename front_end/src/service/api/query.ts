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
// DKHJQ202307121643284626EEq7id5eNmjLYin
// DKHJQ202307121643284626EEq7id5eNmjLYin
export { queryText };
