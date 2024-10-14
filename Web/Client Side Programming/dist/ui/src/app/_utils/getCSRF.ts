
export function getCSRF(){
    return fetch("/api/").then((res)=>res.text())
}
