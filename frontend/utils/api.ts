// 全局 token 存储
let _token: string | null = null

export function setAuthToken(token: string | null) {
  _token = token
  if (import.meta.client) {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }
}

export function getAuthToken(): string | null {
  if (_token) return _token
  if (import.meta.client) {
    _token = localStorage.getItem('token')
  }
  return _token
}

export function useApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string

  const request = async (method: string, path: string, body?: any) => {
    const url = `${baseURL}${path}`
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    const token = getAuthToken()
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const options: RequestInit = { method, headers }
    if (body && method !== 'GET') {
      options.body = JSON.stringify(body)
    }

    let response: Response
    try {
      response = await fetch(url, options)
    } catch (e: any) {
      throw new Error('无法连接到服务器，请确认后端已启动')
    }

    if (!response.ok) {
      let detail = `请求失败 (${response.status})`
      try {
        const err = await response.json()
        if (err.detail) {
          if (typeof err.detail === 'string') {
            detail = err.detail
          } else if (Array.isArray(err.detail)) {
            detail = err.detail.map((d: any) => d.msg || JSON.stringify(d)).join('; ')
          } else {
            detail = JSON.stringify(err.detail)
          }
        }
      } catch { /* ignore */ }
      throw new Error(detail)
    }

    return response.json()
  }

  const upload = async (path: string, formData: FormData) => {
    const url = `${baseURL}${path}`
    const headers: Record<string, string> = {}
    const token = getAuthToken()
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    let response: Response
    try {
      response = await fetch(url, { method: 'POST', headers, body: formData })
    } catch (e: any) {
      throw new Error('无法连接到服务器，请确认后端已启动')
    }

    if (!response.ok) {
      let detail = '上传失败'
      try {
        const err = await response.json()
        if (err.detail) detail = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail)
      } catch { /* ignore */ }
      throw new Error(detail)
    }

    return response.json()
  }

  return {
    get: (path: string) => request('GET', path),
    post: (path: string, body?: any) => request('POST', path, body),
    put: (path: string, body?: any) => request('PUT', path, body),
    delete: (path: string) => request('DELETE', path),
    upload,
  }
}
