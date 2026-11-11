import { type BasePaginatorResponse } from "@/models/base";


// 获取自定义 API
export type GetApiToolProvidersWithPageResponse = BasePaginatorResponse<{
    id:string
    name: string
    icon: string
    description: string
    headers: Array<any>
    tools: Array<any>
    created_at: number
}>