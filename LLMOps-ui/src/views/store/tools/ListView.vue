<template>
  <a-spin :loading="loading" class="block h-full w-full">
    <div class="p-6 flex flex-col">
      <!-- 标题+创建按钮 -->
       <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-2">
            <a-avatar :size="32" class="bg-blue-700">
              <icon-common :size="18"/>
            </a-avatar>
            <div class="text-lg font-medium text-gray-900">
              插件广场
            </div>
          </div>
          <a-button type="primary" class="rounded-lg">
            创建自定义插件
          </a-button>
       </div>
       <!-- 插件分类 + 搜索-->
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-2">
            <a-button 
              class="rounded-lg text-gray-700 px-3"
              :type="category === 'all' ? 'secondary' : 'text'"
              :style="{
                backgroundColor: category === 'all' ? '#e5e6eb' : 'transparent'
              }"
              @click="category = 'all'">全部</a-button>
            <a-button 
              v-for="item in categories"
              :key="item.category" 
              :type="category === item.category ? 'secondary' : 'text'"
              @click="category = item.category"
              :style="{
                backgroundColor: category === item.category ? '#e5e6eb' : 'transparent'
              }"
              class="rounded-lg text-gray-700 px-3">
              {{item.name}}
            </a-button>
          </div>
          <!-- 右侧搜索 -->
           <a-input-search v-model="search_word"  placeholder="请输入插件名称" class="w-[240px] bg-white rounded-lg border-gray-300"></a-input-search>
        </div>
        <!-- 底部插件列表 -->
        <a-row :gutter="[20, 20]" class="flex-1">
          <!-- 有数据 -->
          <a-col :span="6" v-for="(provider, idx) in filterProviders" :key="provider.name">
            <a-card hoverable class="cursor-pointer rounded-lg" @click="showIdx=idx">
              <div class="flex items-center gap-3 mb-3">
                <a-avatar :size="40" shape="square" :style="{backgroundColor: provider.background}">
                  <img :src="`${apiPrefix}/builtin-tools/${provider.name}/icon`" />
                </a-avatar>
                <div class="flex flex-col">
                  <div class="text-base text-gray-900 font-bold">{{provider.label}}</div>
                  <div class="text-xs text-gray-500 line-clamp-1">提供商 {{provider.name}} . {{ provider.tools.length }}</div>
                </div>
              </div>
              <div class="leading-[18px] text-gray-500 h-[72px] line-clamp-4 mb-2">{{ provider.description }}</div>
              <div class="flex items-center gap-1.5">
               <a-avatar :size="18" class="bg-blue-700">
                <icon-user></icon-user>
               </a-avatar>
               <div class="text-xs text-gray-400">发布时间: {{ moment(provider.created_at).format('MM-DD HH:mm') }}</div>
              </div>
            </a-card>
          </a-col>
          <!-- 无数据 -->
          <a-col :span="24" v-if="filterProviders.length === 0">
            <a-empty description="没有可用的内置插件" class="h-[400px] flex flex-col items-center justify-center"/>
          </a-col>
        </a-row>

        <!-- 卡片抽屉 -->
        <a-drawer 

          :visible="showIdx != -1"
          :width="350"
          :footer="false"
          title="工具详情"
          @cancel="showIdx = -1"
          :drawer-style="{background: '#F9FAFB'}">
          <div v-if="showIdx != -1">
            <div class="flex items-center gap-3 mb-3">
              <a-avatar :size="40" shape="square" :style="{backgroundColor: filterProviders[showIdx].background}">
                <img :src="`${apiPrefix}/builtin-tools/${filterProviders[showIdx].name}/icon`" />
              </a-avatar>
              <div class="flex flex-col">
                <div class="text-base text-gray-900 font-bold">{{filterProviders[showIdx].label}}</div>
                <div class="text-xs text-gray-500 line-clamp-1">提供商 {{filterProviders[showIdx].name}} . {{ filterProviders[showIdx].tools.length }}</div>
              </div>
            </div>
            <div class="leading-[18px] text-gray-500 mb-2">{{ filterProviders[showIdx].description }}</div>
            <hr class="my-4 text-gray-300" />
            <div class="flex flex-col">
              <div class="mb-3 text-xs text-gray-500">包含{{filterProviders[showIdx].tools.length}}个工具</div>
              <a-card 
                  class="cursor-pointer flex flex-col rounded-xl" 
                  v-for="tool in filterProviders[showIdx].tools"
                  :key="tool.name">
                <div class="font-bold text-gray-900 mb-2">{{tool.label}}</div>
                <div class="text-gray-500 text-xs">{{tool.description}}</div>
                <div v-if="tool.inputs.length">
                  <div class="flex items-center gap-2 my-4">
                    <div class="text-xs font-bold text-gray-500">参数</div>
                    <hr class="flex-1 text-gray-300" />
                  </div>
                  <div class="flex flex-col gap-4">
                    <div class="flex flex-col gap-2" v-for="input in tool.inputs" :key="input.name">
                      <div class="flex items-center gap-2 text-xs">
                        <div class="font-bold text-gray-900">{{input.name}}</div>
                        <div class="text-gray-500">{{input.type}}</div>
                        <div v-if="input.required" class="text-red-700">必填</div>
                      </div>
                      <div class="text-xs text-gray-500">
                         {{input.description}}
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
import { onMounted, reactive, ref, computed } from 'vue';
import moment from 'moment'
import { getCategories, getBuiltinTools } from '@/services/builtin-tool';
import { apiPrefix } from  '@/config'
const categories = reactive<Array<any>>([])
const providers = reactive<Array<any>>([])
const loading = ref<boolean>(false)
const category = ref<string>('all')
const search_word = ref<string>('')
const showIdx = ref<number>(-1)

const filterProviders = computed(() => {
  
  let providersData = providers.filter((item) => {
    console.log(item, 'item')
    const matchCategory = category.value === 'all' || item.category === category.value

    const matchSearchWord = search_word.value === '' || item.label.toLowerCase().includes(search_word.value.toLowerCase())

    console.log(matchCategory , 'aaa')

    return matchCategory && matchSearchWord
  })
  console.log(providersData, '数据')
  return providersData
})



onMounted(async() => {
  const resp = await getCategories()
  Object.assign(categories, resp.data)
})

onMounted(async() => {
  try {
    loading.value = true
    const resp = await getBuiltinTools()
    Object.assign(providers, resp.data)
  } finally{
    loading.value = false
  }
})
</script>

<style scoped>

</style>
