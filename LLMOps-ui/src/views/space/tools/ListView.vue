<template>
  <a-spin
    :loading="loading"
    @scroll="handleScroll"
    class="scrollbar-w-none block h-full w-full overflow-scroll"
  >
    <!-- 底部插件列表 -->
    <a-row
      :gutter="[20, 20]"
      class="flex-1"
    >
      <a-col
        :span="6"
        v-for="(provider, idx) in providers"
        :key="provider.name"
      >
        <a-card
          hoverable
          class="cursor-pointer rounded-lg"
          @click="showIdx = idx"
        >
          <div class="mb-3 flex items-center gap-3">
            <a-avatar
              :size="40"
              shape="square"
              :image-url="provider.icon"
            ></a-avatar>
            <div class="flex flex-col">
              <div class="text-base font-bold text-gray-900">{{ provider.name }}</div>
              <div class="line-clamp-1 text-xs text-gray-500">
                提供商 {{ provider.name }} . {{ provider.tools.length }}
              </div>
            </div>
          </div>
          <div class="mb-2 line-clamp-4 h-[72px] leading-[18px] text-gray-500">
            {{ provider.description }}
          </div>
          <div class="flex items-center gap-1.5">
            <a-avatar
              :size="18"
              class="bg-blue-700"
            >
              <icon-user></icon-user>
            </a-avatar>
            <div class="text-xs text-gray-400">
              编辑时间: {{ moment(provider.created_at).format('MM-DD HH:mm') }}
            </div>
          </div>
        </a-card>
      </a-col>
      <!-- 无数据 -->
      <a-col
        :span="24"
        v-if="providers.length === 0"
      >
        <a-empty
          description="没有可用的API插件"
          class="flex h-[400px] flex-col items-center justify-center"
        />
      </a-col>
    </a-row>

    <!-- 加载器 -->
    <a-row v-if="providers.length > 0">
      <a-col
        v-if="paginator.current_page <= paginator.total_page"
        :span="24"
        align="center"
      >
        <a-space class="my-4">
          <a-spin />
          <div class="text-gray-400">加载中</div>
        </a-space>
      </a-col>
      <a-col
        v-else
        :span="24"
        align="center"
      >
        <div class="my-4 text-gray-400">数据已加载完成</div>
      </a-col>
    </a-row>
    <!-- 卡片抽屉 -->
    <a-drawer
      :visible="showIdx != -1"
      :width="350"
      :footer="false"
      title="工具详情"
      @cancel="showIdx = -1"
      :drawer-style="{ background: '#F9FAFB' }"
    >
      <div v-if="showIdx != -1">
        <div class="mb-3 flex items-center gap-3">
          <a-avatar
            :size="40"
            shape="square"
            :image-url="providers[showIdx].icon"
          >
          </a-avatar>
          <div class="flex flex-col">
            <div class="text-base font-bold text-gray-900">{{ providers[showIdx].name }}</div>
            <div class="line-clamp-1 text-xs text-gray-500">
              提供商 {{ providers[showIdx].name }} . {{ providers[showIdx].tools.length }}
            </div>
          </div>
        </div>
        <div class="mb-2 leading-[18px] text-gray-500">{{ providers[showIdx].description }}</div>
        <hr class="my-4 text-gray-300" />
        <div class="flex flex-col gap-2">
          <div class="text-xs text-gray-500">包含{{ providers[showIdx].tools.length }}个工具</div>
          <a-card
            class="flex cursor-pointer flex-col rounded-xl"
            v-for="tool in providers[showIdx].tools"
            :key="tool.name"
          >
            <div class="mb-2 font-bold text-gray-900">{{ tool.name }}</div>
            <div class="text-xs text-gray-500">{{ tool.description }}</div>
            <div v-if="tool.inputs.length">
              <div class="my-4 flex items-center gap-2">
                <div class="text-xs font-bold text-gray-500">参数</div>
                <hr class="flex-1 text-gray-300" />
              </div>
              <div class="flex flex-col gap-4">
                <div
                  class="flex flex-col gap-2"
                  v-for="input in tool.inputs"
                  :key="input.name"
                >
                  <div class="flex items-center gap-2 text-xs">
                    <div class="font-bold text-gray-900">{{ input.name }}</div>
                    <div class="text-gray-500">{{ typeMap[input.type] }}</div>
                    <div
                      v-if="input.required"
                      class="text-red-700"
                    >
                      必填
                    </div>
                  </div>
                  <div class="text-xs text-gray-500">
                    {{ input.description }}
                  </div>
                </div>
              </div>
            </div>
          </a-card>
        </div>
      </div>
    </a-drawer>

    <!-- 新建/修改模态窗 -->
    <a-modal
      :width="630"
      :visible="true"
      hide-title
      :footer="false"
      modal-class="rounded-xl"
    >
      上岛咖啡近段时间
    </a-modal>
  </a-spin>
</template>

<script setup lang="ts">
  import { onMounted, reactive, ref, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import { getApiToolProvidersWithPage } from '@/services/api-tool'
  import moment from 'moment'
  import { typeMap } from '@/config'

  const providers = reactive<Array<any>>([])
  const loading = ref(false)
  const showIdx = ref(-1)

  const route = useRoute()

  // 分页参数
  const paginator = reactive({
    current_page: 1,
    page_size: 20,
    total_page: 0,
    total_record: 0,
  })

  const handleScroll = (event: UIEvent) => {
    const { scrollTop, scrollHeight, clientHeight } = event.target as HTMLElement
    if (scrollTop + clientHeight >= scrollHeight - 10) {
      if (loading.value) {
        return
      }
      loadMoreData()
    }
  }

  const loadMoreData = async (init: boolean = false) => {
    if (!init && paginator.current_page > paginator.total_page) {
      return
    }
    try {
      loading.value = true
      const resp = await getApiToolProvidersWithPage(
        paginator.current_page,
        paginator.page_size,
        String(route.query?.search_word ?? ''),
      )
      const data = resp.data

      paginator.current_page = data.paginator.current_page
      paginator.page_size = data.paginator.page_size
      paginator.total_page = data.paginator.total_page
      paginator.total_record = data.paginator.total_record

      if (paginator.current_page <= paginator.total_page) {
        paginator.current_page += 1
      }

      if (init) {
        providers.splice(0, providers.length, ...data.list)
      } else {
        providers.push(...data.list)
      }
    } finally {
      loading.value = false
    }
  }

  onMounted(async () => {
    await loadMoreData(true)
  })

  watch(
    () => route.query?.search_word ?? '',
    () => {
      paginator.current_page = 1
      paginator.page_size = 20
      paginator.total_page = 0
      paginator.total_record = 0

      loadMoreData(true)
    },
  )
</script>

<style scoped></style>
