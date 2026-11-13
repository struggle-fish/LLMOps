<template>
  <a-spin
    :loading="loading"
    class="block h-full w-full"
  >
    <div class="flex flex-col p-6">
      <!-- 标题+创建按钮 -->
      <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <a-avatar
            :size="32"
            class="bg-blue-700"
          >
            <icon-common :size="18" />
          </a-avatar>
          <div class="text-lg font-medium text-gray-900">插件广场</div>
        </div>
        <a-button
          type="primary"
          class="rounded-lg"
        >
          创建自定义插件
        </a-button>
      </div>
      <!-- 插件分类 + 搜索-->
      <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <a-button
            class="rounded-lg px-3 text-gray-700"
            :type="category === 'all' ? 'secondary' : 'text'"
            :style="{
              backgroundColor: category === 'all' ? '#e5e6eb' : 'transparent',
            }"
            @click="category = 'all'"
            >全部</a-button
          >
          <a-button
            v-for="item in categories"
            :key="item.category"
            :type="category === item.category ? 'secondary' : 'text'"
            @click="category = item.category"
            :style="{
              backgroundColor: category === item.category ? '#e5e6eb' : 'transparent',
            }"
            class="rounded-lg px-3 text-gray-700"
          >
            {{ item.name }}
          </a-button>
        </div>
        <!-- 右侧搜索 -->
        <a-input-search
          v-model="search_word"
          placeholder="请输入插件名称"
          class="w-[240px] rounded-lg border-gray-300 bg-white"
        ></a-input-search>
      </div>
      <!-- 底部插件列表 -->
      <a-row
        :gutter="[20, 20]"
        class="flex-1"
      >
        <!-- 有数据 -->
        <a-col
          :span="6"
          v-for="(provider, idx) in filterProviders"
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
                :style="{ backgroundColor: provider.background }"
              >
                <img :src="`${apiPrefix}/builtin-tools/${provider.name}/icon`" />
              </a-avatar>
              <div class="flex flex-col">
                <div class="text-base font-bold text-gray-900">{{ provider.label }}</div>
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
                发布时间: {{ moment(provider.created_at).format('MM-DD HH:mm') }}
              </div>
            </div>
          </a-card>
        </a-col>
        <!-- 无数据 -->
        <a-col
          :span="24"
          v-if="filterProviders.length === 0"
        >
          <a-empty
            description="没有可用的内置插件"
            class="flex h-[400px] flex-col items-center justify-center"
          />
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
              :style="{ backgroundColor: filterProviders[showIdx].background }"
            >
              <img :src="`${apiPrefix}/builtin-tools/${filterProviders[showIdx].name}/icon`" />
            </a-avatar>
            <div class="flex flex-col">
              <div class="text-base font-bold text-gray-900">
                {{ filterProviders[showIdx].label }}
              </div>
              <div class="line-clamp-1 text-xs text-gray-500">
                提供商 {{ filterProviders[showIdx].name }} .
                {{ filterProviders[showIdx].tools.length }}
              </div>
            </div>
          </div>
          <div class="mb-2 leading-[18px] text-gray-500">
            {{ filterProviders[showIdx].description }}
          </div>
          <hr class="my-4 text-gray-300" />
          <div class="flex flex-col gap-2">
            <div class="text-xs text-gray-500">
              包含{{ filterProviders[showIdx].tools.length }}个工具
            </div>
            <a-card
              class="flex cursor-pointer flex-col rounded-xl"
              v-for="tool in filterProviders[showIdx].tools"
              :key="tool.name"
            >
              <div class="mb-2 font-bold text-gray-900">{{ tool.label }}</div>
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
    </div>
  </a-spin>
</template>

<script setup lang="ts">
  import { onMounted, reactive, ref, computed } from 'vue'
  import moment from 'moment'
  import { getCategories, getBuiltinTools } from '@/services/builtin-tool'
  import { apiPrefix } from '@/config'
  import { typeMap } from '@/config'
  const categories = reactive<Array<any>>([])
  const providers = reactive<Array<any>>([])
  const loading = ref<boolean>(false)
  const category = ref<string>('all')
  const search_word = ref<string>('')
  const showIdx = ref<number>(-1)

  const filterProviders = computed(() => {
    let providersData = providers.filter((item) => {
      const matchCategory = category.value === 'all' || item.category === category.value

      const matchSearchWord =
        search_word.value === '' ||
        item.label.toLowerCase().includes(search_word.value.toLowerCase())

      console.log(matchCategory, 'aaa')

      return matchCategory && matchSearchWord
    })
    console.log(providersData, '数据')
    return providersData
  })

  onMounted(async () => {
    const resp = await getCategories()
    categories.push(...resp.data)
  })

  onMounted(async () => {
    try {
      loading.value = true
      const resp = await getBuiltinTools()
      providers.push(...resp.data)
    } finally {
      loading.value = false
    }
  })
</script>

<style scoped></style>
