export function useApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string

  const getHeaders = () => {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }
    if (import.meta.client) {
      const token = localStorage.getItem('token')
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
    }
    return headers
  }

  const request = async (method: string, path: string, body?: any) => {
    const url = `${baseURL}${path}`
    const options: RequestInit = {
      method,
      headers: getHeaders(),
    }

    if (body && method !== 'GET') {
      options.body = JSON.stringify(body)
    }

    const response = await fetch(url, options)

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: '请求失败' }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
  }

  const upload = async (path: string, formData: FormData) => {
    const url = `${baseURL}${path}`
    const headers: Record<string, string> = {}
    if (import.meta.client) {
      const token = localStorage.getItem('token')
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: '上传失败' }))
      throw new Error(error.detail || `HTTP ${response.status}`)
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
