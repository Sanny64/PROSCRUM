import {ref} from "vue";
import type { User } from '../types/types.ts'




export function setToken(token: string) {
    localStorage.setItem("activeToken", JSON.stringify(token))
    console.log("3: Token gesetzt")
}

export function getToken() {
  if(localStorage.getItem("activeToken") == null){
    return "INVALID"
  }else{
    return JSON.parse(localStorage.getItem("activeToken" ) || "{}")
  }

}




