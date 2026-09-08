// 全局token管理
let authToken = null

export function setAuthToken(token) {
  authToken = token
  if (import.meta.client) {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }
}

export function getAuthToken() {
  if (authToken) return authToken
  if (import.meta.client) {
    authToken = localStorage.getItem('token')
  }
  return authToken
}

export function useApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  const getHeaders = () => {
    const headers = {
      'Content-Type': 'application/json',
    }
    const token = getAuthToken()
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    return headers
  }

  const request = async (method, path, body) => {
    const url = `${baseURL}${path}`
    const options = {
      method,
      headers: getHeaders(),
    }

    if (body && method !== 'GET') {
      options.body = JSON.stringify(body)
    }

    let response
    try {
      response = await fetch(url, options)
    } catch (e) {
      throw new Error('无法连接到服务器，请确认后端已启动 (localhost:8000)')
    }

    if (!response.ok) {
      let detail = `请求失败 (${response.status})`
      try {
        const err = await response.json()
        if (err.detail) {
          if (typeof err.detail === 'string') {
            detail = err.detail
          } else if (Array.isArray(err.detail)) {
            detail = err.detail.map((d) => d.msg || JSON.stringify(d)).join('; ')
          } else {
            detail = JSON.stringify(err.detail)
          }
        }
      } catch {
        // ignore json parse error
      }
      throw new Error(detail)
    }

    return response.json()
  }

  const upload = async (path, formData) => {
    const url = `${baseURL}${path}`
    const headers = {}
    const token = getAuthToken()
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    let response
    try {
      response = await fetch(url, {
        method: 'POST',
        headers,
        body: formData,
      })
    } catch (e) {
      throw new Error('无法连接到服务器，请确认后端已启动 (localhost:8000)')
    }

    if (!response.ok) {
      let detail = '上传失败'
      try {
        const err = await response.json()
        if (err.detail) {
          detail = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail)
        }
      } catch {
        // ignore
      }
      throw new Error(detail)
    }

    return response.json()
  }

  return {
    get: (path) => request('GET', path),
    post: (path, body) => request('POST', path, body),
    put: (path, body) => request('PUT', path, body),
    delete: (path) => request('DELETE', path),
    upload,
  }
}
