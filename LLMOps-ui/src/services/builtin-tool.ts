 import {get} from '@/utils/request'

 import { type GetCateGoriesResponse, type GetBuiltinToolsResponse } from '@/models/builtin-tool'


//  获取内置分类列表
export const getCategories = () => {
    return get<GetCateGoriesResponse>('/builtin-tools/categories')
}


export const getBuiltinTools = () => {
    return get<GetBuiltinToolsResponse>('/builtin-tools')
}

