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
              <div
                class="text-base font-bold text-gray-900"
              >
                {{ provider.name }}
              </div>
              <div
                class="line-clamp-1 text-xs text-gray-500"
              >
                提供商 {{ provider.name }} .
                {{ provider.tools.length }}
              </div>
            </div>
          </div>
          <div
            class="mb-2 line-clamp-4 h-[72px] leading-[18px] text-gray-500"
          >
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
              编辑时间:
              {{
                moment(provider.created_at).format(
                  'MM-DD HH:mm',
                )
              }}
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
        v-if="
          paginator.current_page <= paginator.total_page
        "
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
            <div class="text-base font-bold text-gray-900">
              {{ providers[showIdx].name }}
            </div>
            <div class="line-clamp-1 text-xs text-gray-500">
              提供商 {{ providers[showIdx].name }} .
              {{ providers[showIdx].tools.length }}
            </div>
          </div>
        </div>
        <div class="mb-2 leading-[18px] text-gray-500">
          {{ providers[showIdx].description }}
        </div>

        <a-button
          type="dashed"
          long
          class="mb-2 rounded-lg"
          @click="handleUpdate"
          :loading="showUpdateModelLoading"
        >
          <template #icon>
            <icon-settings></icon-settings>
          </template>
          编辑工具
        </a-button>

        <hr class="my-4 text-gray-300" />
        <div class="flex flex-col gap-2">
          <div class="text-xs text-gray-500">
            包含{{ providers[showIdx].tools.length }}个工具
          </div>
          <a-card
            class="flex cursor-pointer flex-col rounded-xl"
            v-for="tool in providers[showIdx].tools"
            :key="tool.name"
          >
            <div class="mb-2 font-bold text-gray-900">
              {{ tool.name }}
            </div>
            <div class="text-xs text-gray-500">
              {{ tool.description }}
            </div>
            <div v-if="tool.inputs.length">
              <div class="my-4 flex items-center gap-2">
                <div
                  class="text-xs font-bold text-gray-500"
                >
                  参数
                </div>
                <hr class="flex-1 text-gray-300" />
              </div>
              <div class="flex flex-col gap-4">
                <div
                  class="flex flex-col gap-2"
                  v-for="input in tool.inputs"
                  :key="input.name"
                >
                  <div
                    class="flex items-center gap-2 text-xs"
                  >
                    <div class="font-bold text-gray-900">
                      {{ input.name }}
                    </div>
                    <div class="text-gray-500">
                      {{ typeMap[input.type] }}
                    </div>
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
      :visible="
        props.createType === 'tool' || showUpdateModel
      "
      hide-title
      :footer="false"
      modal-class="rounded-xl"
      @cancel="handleCancel"
    >
      <div class="flex items-center justify-between">
        <div class="text-lg font-bold text-gray-700">
          {{
            props.createType === 'tool' ? '新建' : '更新'
          }}插件
        </div>
        <a-button
          type="text"
          class="text-gray-700"
          size="samll"
          @click="handleCancel"
        >
          <template #icon>
            <icon-close></icon-close>
          </template>
        </a-button>
      </div>
      <!-- 中间表单 -->
      <a-spin
        :loading="showUpdateModelLoading"
        class="block pt-6"
      >
        <a-form
          layout="vertical"
          ref="formRef"
          :model="form"
          @submit="handleSubmit"
        >
          <a-form-item
            field="icon"
            hide-label
            :rules="[
              {
                required: true,
                message: '插件图标不能为空',
              },
            ]"
          >
            <a-upload
              :limit="1"
              v-model="form.icon"
              list-type="picture-card"
              accept="image/png, image/jpeg"
              class="mx-auto w-auto"
            >
            </a-upload>
          </a-form-item>
          <a-form-item
            field="name"
            label="插件名称"
            asterisk-position="end"
            :rules="[
              {
                required: true,
                message: '插件名称不能为空',
              },
            ]"
          >
            <a-input
              v-model="form.name"
              placeholder="请输出插件名称,确保名称含义清晰"
              show-word-limit
              :max-length="60"
            ></a-input>
          </a-form-item>
          <a-form-item
            field="openapi_schema"
            label="OpenAPI Schema"
            asterisk-position="end"
            :rules="[
              {
                required: true,
                message: 'OpenAPI Schema 不能为空',
              },
            ]"
          >
            <a-textarea
              v-model="form.openapi_schema"
              :auto-size="{ minRows: 4, maxRows: 6 }"
              placeholder="在此处输入您的 OpenAPI Schema"
              @blur="handleSchemaBlur"
            ></a-textarea>
          </a-form-item>
          <a-form-item label="可用工具">
            <div
              class="w-full overflow-x-auto rounded-lg border border-gray-200"
            >
              <table
                class="w-full text-xs leading-[18px] font-normal text-gray-700"
              >
                <thead class="text-gray-500">
                  <tr class="border-b border-gray-200">
                    <th class="p-2 pl-3 font-medium">
                      名称
                    </th>
                    <th
                      class="w-[236px] p-2 pl-3 font-medium"
                    >
                      描述
                    </th>
                    <th class="p-2 pl-3 font-medium">
                      方法
                    </th>
                    <th class="p-2 pl-3 font-medium">
                      路径
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    class="border-b border-r-gray-200 text-gray-700 last:border-0"
                    v-for="(tool, idx) in tools"
                    :key="idx"
                  >
                    <td class="p-2 pl-3">
                      {{ tool.name }}
                    </td>
                    <td class="w-[236px] p-2 pl-3">
                      {{ tool.description }}
                    </td>
                    <td class="p-2 pl-3">
                      {{ tool.method }}
                    </td>
                    <td class="w-[62px] p-2 pl-3">
                      {{ tool.path }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </a-form-item>
          <a-form-item label="Headers">
            <div
              class="w-full overflow-x-auto rounded-lg border border-gray-200"
            >
              <table
                class="mb-3 w-full text-xs leading-[18px] font-normal text-gray-200"
              >
                <thead class="text-gray-500">
                  <tr class="border-b border-gray-500">
                    <th class="p-2 pl-3 font-medium">
                      Key
                    </th>
                    <th class="p-2 pl-3 font-medium">
                      Value
                    </th>
                    <th
                      class="w-[50px] p-2 pl-3 font-medium"
                    >
                      操作
                    </th>
                  </tr>
                </thead>
                <tbody
                  v-if="form.headers.length > 0"
                  class="border-b border-gray-200"
                >
                  <tr
                    class="border-b border-gray-200 last:border-0"
                    v-for="(header, idx) in form.headers"
                    :key="idx"
                  >
                    <td class="p-2 pl-3">
                      <a-form-item
                        hide-label
                        class="m-0"
                        :field="`headers[${idx}].key`"
                      >
                        <a-input
                          v-model="header.key"
                          placeholder="请输入请求头建名"
                        ></a-input>
                      </a-form-item>
                    </td>
                    <td class="p-2 pl-3">
                      <a-form-item
                        hide-label
                        class="m-0"
                        :field="`headers[${idx}].value`"
                      >
                        <a-input
                          v-model="header.value"
                          placeholder="请输入请求头建值内容"
                        ></a-input>
                      </a-form-item>
                    </td>
                    <td class="p-2 pl-3">
                      <a-button
                        size="small"
                        type="text"
                        class="text-gray-700"
                        @click="form.headers.splice(idx, 1)"
                      >
                        <template #icon>
                          <icon-delete></icon-delete>
                        </template>
                      </a-button>
                    </td>
                  </tr>
                </tbody>
              </table>

              <a-button
                size="mini"
                class="mb-3 ml-3 rounded text-gray-700"
                @click="
                  form.headers.push({ key: '', value: '' })
                "
              >
                <template #icon>
                  <icon-plus></icon-plus>
                </template>
                增加参数
              </a-button>
            </div>
          </a-form-item>

          <!-- 底部按钮 -->
          <div class="flex items-center justify-between">
            <div>
              <a-button
                v-if="showUpdateModel"
                class="rounded-lg text-red-700"
                @click="handleDelete"
                >删除</a-button
              >
            </div>
            <a-space :size="6">
              <a-button
                class="rounded-lg"
                @click="handleCancel"
                >取消</a-button
              >
              <a-button
                class="rounded-lg"
                html-type="submit"
                type="primary"
                :loading="submitLoading"
                >保存</a-button
              >
            </a-space>
          </div>
        </a-form>
      </a-spin>
    </a-modal>
  </a-spin>
</template>

<script setup lang="ts">
  import {
    onMounted,
    reactive,
    ref,
    watch,
    computed,
  } from 'vue'
  import { useRoute } from 'vue-router'
  import { Message, Modal } from '@arco-design/web-vue'
  import {
    getApiToolProvidersWithPage,
    validateOpenAPISchema,
    getApiToolProvider,
    createApiToolProvider,
    updateApiToolProvider,
    deleteApiToolProvider,
  } from '@/services/api-tool'
  import moment from 'moment'
  import { typeMap } from '@/config'

  const props = defineProps({
    createType: {
      type: String,
      required: true,
    },
  })

  const emits = defineEmits(['update-create-type'])

  const form = reactive({
    icon: 'https://picsum.photos/200',
    name: '',
    openapi_schema: '',
    headers: [],
  })

  const formRef = ref(null)

  // 兼容直接粘贴完整工具提供者JSON的情况，自动提取名称、schema和headers
  const handleSchemaBlur = async () => {
    try {
      const data = JSON.parse(form.openapi_schema)
      if (data && typeof data.openapi_schema === 'string') {
        if (typeof data.name === 'string') {
          form.name = data.name
        }
        if (Array.isArray(data.headers)) {
          form.headers = data.headers
        }
        form.openapi_schema = data.openapi_schema
      }
    } catch {
      // 非JSON数据交给后端校验并提示
    }
    if (form.openapi_schema.trim() === '') {
      return
    }
    const resp = await validateOpenAPISchema(form.openapi_schema)
    if (resp.code !== 'success') {
      Message.error(resp.msg || 'OpenAPI Schema 校验失败')
    }
  }

  const tools = computed(() => {
    try {
      const available_tools = []
      const openapi_schema = JSON.parse(form.openapi_schema)
      if ('paths' in openapi_schema) {
        for (const path in openapi_schema['paths']) {
          for (const method in openapi_schema['paths'][
            path
          ]) {
            if (['get', 'post'].includes(method)) {
              const tool =
                openapi_schema['paths'][path][method]
              if (
                'operationId' in tool &&
                'description' in tool
              ) {
                available_tools.push({
                  name: tool?.operationId,
                  description: tool?.description,
                  method: method,
                  path: path,
                })
              }
            }
          }
        }
      }
      return available_tools
    } catch (e) {
      console.log('解析 openapi_schema失败')
    }
    return []
  })

  const providers = reactive<Array<any>>([])
  const loading = ref(false)
  const showIdx = ref(-1)
  const showUpdateModel = ref(false)
  const showUpdateModelLoading = ref(false)
  const submitLoading = ref(false)
  const route = useRoute()

  const initData = async () => {
    paginator.current_page = 1
    paginator.page_size = 20
    paginator.total_page = 0
    paginator.total_record = 0

    loadMoreData(true)
  }
  const handleDelete = () => {
    Modal.warning({
      title: '删除这个工具?',
      content:
        '删除工具是不可逆的,AI 应用将无法访问您的工具',
      hideCancel: false,
      onOk: async () => {
        try {
          const provider_id = providers[showIdx.value]['id']
          const resp =
            await deleteApiToolProvider(provider_id)
          Message.success(resp.msg || '删除成功')
        } finally {
          handleCancel()
          showIdx.value = -1
          await initData()
        }
      },
    })
  }

  const handleSubmit = async ({ values, errors }) => {
    if (errors) {
      return
    }

    try {
      submitLoading.value = true
      if (props.createType === 'tool') {
        const resp = await createApiToolProvider(values)
        if (resp.code !== 'success') {
          Message.error(resp.msg || '保存失败')
          return
        }
        Message.success(resp.msg || '保存成功')
      } else if (showUpdateModel.value) {
        const resp = await updateApiToolProvider(
          providers[showIdx.value]['id'],
          values,
        )
        if (resp.code !== 'success') {
          Message.error(resp.msg || '保存失败')
          return
        }
        Message.success(resp.msg || '保存成功')
      }

      handleCancel()
      showIdx.value = -1
    } finally {
      submitLoading.value = false
    }
    await initData()
  }

  const handleCancel = () => {
    // 重置表单数据
    formRef.value.resetFields()
    emits('update-create-type', '')
    showUpdateModel.value = false
  }
  const handleUpdate = async () => {
    showUpdateModel.value = true
    showUpdateModelLoading.value = true
    try {
      const provider_id = providers[showIdx.value]['id']
      const resp = await getApiToolProvider(provider_id)
      const data = resp.data
      formRef.value.resetFields()
      form.icon = data.icon
      form.name = data.name
      form.openapi_schema = data.openapi_schema
      form.headers = data.headers
    } catch {
      Message.error('获取插件详情失败，请稍后重试')
      showUpdateModel.value = false
    } finally {
      showUpdateModelLoading.value = false
    }
  }

  // 分页参数
  const paginator = reactive({
    current_page: 1,
    page_size: 20,
    total_page: 0,
    total_record: 0,
  })

  const handleScroll = (event: UIEvent) => {
    const { scrollTop, scrollHeight, clientHeight } =
      event.target as HTMLElement
    if (scrollTop + clientHeight >= scrollHeight - 10) {
      if (loading.value) {
        return
      }
      loadMoreData()
    }
  }

  const loadMoreData = async (init: boolean = false) => {
    if (
      !init &&
      paginator.current_page > paginator.total_page
    ) {
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
      initData()
    },
  )
</script>

<style scoped></style>
