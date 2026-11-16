import { type BasePaginatorResponse } from '@/models/base'

// 获取自定义 API
export type GetApiToolProvidersWithPageResponse =
  BasePaginatorResponse<{
    id: string
    name: string
    icon: string
    description: string
    headers: Array<any>
    tools: Array<any>
    created_at: number
  }>

// 新增自定义 API 插件提供者请求结构
export type CreateApiToolProviderRequest = {
  name: string
  icon: string
  openapi_schema: string
  headers: Array<any>
}

// 更新 自定义 API工具提供者请求和响应结构
export type UpdateApiToolProviderRequest = {
  name: string
  icon: string
  openapi_schema: string
  headers: Array<any>
}

// 获取自定义 API 工具体统这响应结构体
export type GetApiToolProviderResponse = {
  id: string
  name: string
  openapi_schema: string
  headers: Array<any>
  created_at: number
}
