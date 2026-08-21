import { ref } from 'vue'
import { defineStore } from 'pinia'


// 初始值
const initAccount = {
  name: '小铜钱',
  email: '8888@qq.com',
  avatar: ''
}


export const useAccountStore = defineStore('account', () => {
  // 定义数据
  const account = ref({ ...initAccount })

  // 计算属性
  function update(params: any) {
    Object.assign(account.value, params)
  }

  function clear() {
    account.value = {...initAccount}
  }

  return {
    account,
    clear,
    update
  }
})
