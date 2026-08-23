import type { BaseResponse } from "./base";

// 应用预览与调试接口
export type DebugAppResponse = BaseResponse<{
  content: string
}>
