<template>
    <div class="px-6 flex flex-col overflow-hidden h-full">
        <div class="pt-6 sticky top-0 bg-gray-50">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-2">
                <a-avatar :size="32" class="bg-blue-700">
                    <icon-user :size="18"/>
                </a-avatar>
                <div class="text-lg font-medium text-gray-900">
                    个人空间
                </div>
                </div>
                <a-button v-if="route.path.startsWith('/space/apps')" type="primary" class="rounded-lg">
                    创建 AI 应用
                </a-button>
                <a-button v-if="route.path.startsWith('/space/tools')" type="primary" class="rounded-lg">
                    创建自定义插件
                </a-button>
                <a-button v-if="route.path.startsWith('/space/workflows')" type="primary" class="rounded-lg">
                    创建工作流
                </a-button>
                <a-button v-if="route.path.startsWith('/space/datasets')" type="primary" class="rounded-lg">
                    创建知识库
                </a-button>
            
            </div>
            <!-- 导航按钮 + 搜索-->
            <div class="flex items-center justify-between mb-6">
                <!-- 左侧导航 -->
                <div class="flex items-center gap-2">
                    <router-link 
                        to="/space/apps" 
                        active-class="bg-gray-100"
                        class="rounded-lg text-gray-700 px-3 h-8 leading-8 hover:bg-gray-200 transition-all">
                        AI 应用
                    </router-link>
                    <router-link 
                        to="/space/tools" 
                        active-class="bg-gray-100"
                        class="rounded-lg text-gray-700 px-3 h-8 leading-8 hover:bg-gray-200 transition-all">
                        插件
                    </router-link>
                    <router-link 
                        to="/space/workflows" 
                        active-class="bg-gray-100"
                        class="rounded-lg text-gray-700 px-3 h-8 leading-8 hover:bg-gray-200 transition-all">
                        工作流
                    </router-link>
                    <router-link 
                        to="/space/datasets" 
                        active-class="bg-gray-100"
                        class="rounded-lg text-gray-700 px-3 h-8 leading-8 hover:bg-gray-200 transition-all">
                        知识库
                    </router-link>
                </div>
                <!-- 右侧搜索 -->
                <a-input-search 
                    placeholder="请输入搜索词" 
                    @search="handleSearch"
                    v-model="searchWord"
                    class="w-[240px] bg-white rounded-lg border-gray-300"></a-input-search>
            </div>
        </div>

        <!-- 中间内容 -->
        <router-view></router-view>
    </div>
</template>
<script lang="ts" setup>
import { watch, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router'; 
const route = useRoute()
const router = useRouter()

const searchWord = ref(route.query?.search_word ?? '')

const handleSearch = (value: string) => {
    router.push({
        path: route.path,
        query: {
            search_word: value
        } 
    })
}
watch(() => route.query?.search_word, ()=> {
    searchWord.value = route.query?.search_word ?? ''
})
</script>