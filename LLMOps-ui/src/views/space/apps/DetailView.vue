<template>
  <a-button @click=debug()>发起请求</a-button>
</template>
<script lang="ts" setup>
import { post } from '@/utils/request';
async function debug() {
  const response = await post('/apps/550e8400-e29b-41d4-a716-446655440000/debug', {
      body: {
        query: '你好你是谁'
      }
    })
    console.log(response)
  }
</script>
