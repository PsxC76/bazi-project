import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi, setAuthToken, getAuthToken } from '~/utils/api'

interface User {
  id: number
  username: string
  email: string | null
  nickname: string | null
  avatar: string | null
  bio: string | null
  is_admin: boolean
  created_at: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const api = useApi()

  const isLoggedIn = computed(() => !!getAuthToken())
  const isAdmin = computed(() => user.value?.is_admin || false)

  // 初始化：从 localStorage 恢复用户信息
  const init = () => {
    if (import.meta.client) {
      const savedUser = localStorage.getItem('user')
      if (savedUser) {
        try { user.value = JSON.parse(savedUser) } catch { /* ignore */ }
      }
      // token 由 api.ts 自动从 localStorage 读取
    }
  }

  const login = async (username: string, password: string) => {
    const data = await api.post('/users/login', { username, password })
    setAuthToken(data.access_token)
    user.value = data.user
    if (import.meta.client) {
      localStorage.setItem('user', JSON.stringify(data.user))
    }
    return data
  }

  const register = async (username: string, password: string) => {
    const data = await api.post('/users/register', { username, password })
    setAuthToken(data.access_token)
    user.value = data.user
    if (import.meta.client) {
      localStorage.setItem('user', JSON.stringify(data.user))
    }
    return data
  }

  const logout = () => {
    setAuthToken(null)
    user.value = null
    if (import.meta.client) {
      localStorage.removeItem('user')
    }
  }

  const fetchProfile = async () => {
    if (!getAuthToken()) return
    try {
      const data = await api.get('/users/me')
      user.value = data
      if (import.meta.client) {
        localStorage.setItem('user', JSON.stringify(data))
      }
    } catch {
      logout()
    }
  }

  const updateProfile = async (data: { nickname?: string; bio?: string }) => {
    const result = await api.put('/users/me', data)
    user.value = result
    if (import.meta.client) {
      localStorage.setItem('user', JSON.stringify(result))
    }
    return result
  }

  const changePassword = async (oldPassword: string, newPassword: string) => {
    return await api.post('/users/me/password', {
      old_password: oldPassword,
      new_password: newPassword,
    })
  }

  const uploadAvatar = async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    const result = await api.upload('/users/me/avatar', formData)
    user.value = result
    if (import.meta.client) {
      localStorage.setItem('user', JSON.stringify(result))
    }
    return result
  }

  const sendEmailCode = async (email: string) => {
    return await api.post('/users/me/email/send-code', { email })
  }

  const verifyEmail = async (email: string, code: string) => {
    const result = await api.post('/users/me/email/verify', { email, code })
    await fetchProfile()
    return result
  }

  // 初始化
  init()

  return {
    user,
    isLoggedIn,
    isAdmin,
    login,
    register,
    logout,
    fetchProfile,
    updateProfile,
    changePassword,
    uploadAvatar,
    sendEmailCode,
    verifyEmail,
  }
})
