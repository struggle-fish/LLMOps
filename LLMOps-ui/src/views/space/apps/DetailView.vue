<template>
  <!-- 最外层容器，高度撑满屏幕 -->
  <div class="min-h-screen">
    <!-- 顶部导航 -->
    <header class="flex h-[74px] items-center border-b border-gray-200 bg-gray-100 px-4">
      顶部导航
    </header>

    <!-- 底部内容区域 -->
    <div class="flex h-[calc(100vh-74px)] flex-row">
      <!-- 左侧 -->
      <div class="h-full w-2/3 bg-gray-50">
        <header class="flex h-16 items-center border-b border-gray-200 px-7 text-xl text-gray-700">
          应用编排
        </header>
        <div class="flex h-[calc(100%-64px)] flex-row">
          <div class="flex-1 border-r border-gray-200 p-6">人设与回复逻辑</div>
          <div class="flex-1 p-6">应用能力</div>
        </div>
      </div>
      <!-- 右侧 -->
      <div class="flex h-full w-1/3 flex-col bg-white">
        <header
          class="flex h-16 shrink-0 items-center border-b border-gray-200 bg-white px-4 text-xl shadow-sm"
        >
          调试与预览
        </header>
        <!-- 对话界面 -->
        <div class="scrollbar-w-none h-full min-h-0 overflow-x-hidden overflow-y-scroll px-6 py-7">
          <!-- 人类消息 -->
          <div
            class="mb-6 flex flex-row gap-2"
            v-for="message in messages"
            :key="message.content"
          >
            <a-avatar
              :style="{ backgroundColor: '#3370ff' }"
              class="shrink-0"
              :size="30"
              v-if="message.role === 'human'"
            >
              <IconUser />
            </a-avatar>
            <a-avatar
              class="shrink-0"
              :style="{ backgroundColor: '#14a9f8' }"
              :size="30"
              v-else
            >
              <icon-github />
            </a-avatar>
            <div class="flex flex-col gap-2">
              <div class="font-semibold text-gray-700">
                {{ message.role === 'human' ? '小铜钱' : 'ChatGPT聊天机器人' }}
              </div>
              <div
                v-if="message.role === 'human'"
                class="max-w-max rounded-2xl border border-blue-800 bg-blue-700 px-4 py-3 leading-5 text-white"
              >
                {{ message.content }}
              </div>

              <div
                v-else
                class="max-w-max rounded-2xl border border-gray-200 bg-gray-100 px-4 py-3 leading-5 text-gray-900"
              >
                {{ message.content }}
              </div>
            </div>
          </div>
          <!-- 无数据的时候 -->
          <div
            v-if="!messages.length"
            class="mt-50 flex flex-col items-center justify-center gap-2"
          >
            <a-avatar
              :size="70"
              shape="square"
              :style="{ backgroundColor: '#00d0b6' }"
            >
              <icon-apps></icon-apps>
            </a-avatar>
            <div class="text-2xl font-semibold text-gray-900">ChatGPT聊天机器人</div>
          </div>
          <!-- AI加载状态 -->
          <div
            class="mb-6 flex flex-row gap-2"
            v-if="isLoading"
          >
            <a-avatar
              class="shrink-0"
              :style="{ backgroundColor: '#14a9f8' }"
              :size="30"
            >
              <icon-github />
            </a-avatar>
            <div class="flex flex-col gap-2">
              <div class="font-semibold text-gray-700">ChatGPT聊天机器人</div>
              <div
                class="max-w-max rounded-2xl border border-gray-200 bg-gray-100 px-4 py-3 leading-5 text-gray-900"
              >
                <icon-loading></icon-loading>
              </div>
            </div>
          </div>
        </div>
        <!-- 对话输入框 -->
        <div class="flex w-full shrink-0 flex-col">
          <div class="flex items-center gap-4 px-6">
            <a-button
              class="shrink-0"
              type="text"
              shape="circle"
            >
              <template #icon>
                <icon-empty :style="{ color: '#374151' }"></icon-empty>
              </template>
            </a-button>
            <!-- 输入框 -->
            <div
              class="flex h-12.5 flex-1 items-center gap-2 rounded-full border border-gray-200 px-4"
            >
              <input
                type="text"
                class="flex-1 outline-0"
                @keyup.enter="send"
                v-model="query"
              />
              <a-button
                shape="circle"
                type="text"
                @click="clearMessages"
              >
                <template #icon>
                  <icon-plus-circle
                    size="16"
                    :style="{ color: '#374151' }"
                  ></icon-plus-circle>
                </template>
              </a-button>
              <a-button
                shape="circle"
                type="text"
                @click="send"
              >
                <template #icon>
                  <icon-send
                    size="16"
                    :style="{ color: '#1d4ed8' }"
                  ></icon-send>
                </template>
              </a-button>
            </div>
          </div>
          <div class="py-4 text-center text-xs text-gray-500">
            内容由AI生成，无法确保真实准确，仅供参考。
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
  import { debugApp } from '@/services/apps'
  import type { BaseResponse } from '@/models/base'
  import { Message } from '@arco-design/web-vue'
  import { ref } from 'vue'

  interface ChatMessage {
    role: string
    content: string
  }

  // 交互所需的数据
  const query = ref('')
  const messages = ref<ChatMessage[]>([])
  const isLoading = ref(false)

  const clearMessages = () => {
    messages.value = []
  }
  const send = async () => {
    if (!query.value) {
      Message.error('用户提问不能为空')
      return
    }
    if (isLoading.value) {
      Message.warning('上一次回复还没有结束，请稍等')
    }

    try {
      const humanQuery = query.value
      messages.value.push({
        role: 'human',
        content: humanQuery,
      })

      query.value = ''
      // 发起请求
      isLoading.value = true
      const response = await debugApp('550e8400-e29b-41d4-a716-446655440000', humanQuery)
      const { content } = response.data
      messages.value.push({
        role: 'ai',
        content: content,
      })
    } catch (error) {
      console.log(error)
      if (error && typeof error === 'object' && 'message' in error) {
        const err = error as BaseResponse<unknown>
        Message.error(err.message)
      } else {
        Message.error('请求异常，请检查网络')
      }
    } finally {
      isLoading.value = false
    }
  }
</script>
