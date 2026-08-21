<template>
  <p>我是首页</p>
  <p>
    当前登录的账号是{{accountStore.account.name}}
  </p>
  <p>
    当前登录的邮箱是{{accountStore.account.email}}
  </p>
  <a-button @click="updateName">更新名字</a-button>
  <a-button @click="accountStore.clear">重置</a-button>
</template>
<script lang="ts" setup>
import { useAccountStore } from '@/stores/account'
const accountStore = useAccountStore()
function updateName() {
  accountStore.update({
    name: '你好啊'
  })
}
</script>
