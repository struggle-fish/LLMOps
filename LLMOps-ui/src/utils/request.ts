// 1.接口超时 100s
// 2.不需要写api 前缀
// 3.经常使用get和post,需要对两个方法进行封装
// 4.每次获取数据都使用response.json()才可以获取数据

import { apiPrefix } from "@/config"

const TIME_OUT = 100000

const baseFetchOptions = {
  method: 'GET',
  mode: 'cors',
  credentials: 'include',
  headers: new Headers({
    'Content-Type': 'application/json'
  }),
  redirect: 'follow'
}

type FetchOptionType = Omit<RequestInit, 'body'> & {
  params?: Record<string, unknown>
  body?: BodyInit | Record<string, unknown> | null
}

const baseFetch = <T>(url: string, fetchOptions: FetchOptionType): Promise<T> => {
  // 将所有的配置信息合并起来
  const options: typeof baseFetchOptions & FetchOptionType = Object.assign({},
    baseFetchOptions,
    fetchOptions
  )

  // 组装url
  let urlWithPrefix = `${apiPrefix}${url.startsWith('/') ? url : `/${url}`}`

  // 结构出对应的请求参数，params ,body参数
  const { method, params, body } = options
  // 如果请求是GET ，并且传递了params
  if (method === 'GET' && params) {
    const paramsArray: string[] = []
    Object.entries(params).forEach(([key, value]) => {
      // key=value&key2=value2
      if (value !== undefined && value !== null) {
        paramsArray.push(`${key}=${encodeURIComponent(String(value))}`)
      }
    })
    if (urlWithPrefix.search(/\?/) === -1) {
      urlWithPrefix += `?${paramsArray.join('&')}`
    } else {
      urlWithPrefix += `&${paramsArray.join('&')}`
    }

    delete options.params
  }

  if (body) {
    options.body = JSON.stringify(body)
  }
  console.log(urlWithPrefix, options)
  return Promise.race([
    // 使用定时器来检测是否超时
    new Promise((resolve, reject) => {
      setTimeout(() => {
        reject('接口已超时')
      }, TIME_OUT)
    }),
    // 发起一个正常请求
    new Promise((resolve, reject) => {
      globalThis.fetch(urlWithPrefix, options as RequestInit).then((res) => {
        resolve(res.json())
      }).catch((error) => {
        reject(error)
      })
    })
  ]) as Promise<T>

}


export const request = <T>(url: string, options = {}) => {
  console.log(url, '啊哈哈')
  return baseFetch<T>(url, options)
}

export const get = <T>(url: string, options = {}) => {
  return request<T>(url, Object.assign({}, options, {method: 'GET'}))
}

export const post = <T>(url: string, options = {}) => {
  return request<T>(url, Object.assign({}, options, {method: 'POST'}))
}
