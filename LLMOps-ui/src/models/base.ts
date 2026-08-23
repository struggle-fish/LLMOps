// 基础响应格式
export type BaseResponse<T> = {
  code: string
  message: string
  data: T
}



// 分页响应格式
/**
{
  code: string
  message: string
  data: {
    list: Array<T>   // 当前页的数据列表，数组里面每一项是 T 类型
    paginator: {
      total_page: number
      total_record: number
      current_page: number
      page_size: number
    }
  }
}
 */
export type BasePaginatorResponse<T> = BaseResponse<{
  list: Array<T>
  paginator: {
    total_page: number
    total_record: number
    current_page: number
    page_size: number
  }
}>
