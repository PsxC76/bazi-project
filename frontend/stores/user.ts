import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '~/utils/api'

interface User {
  id: number
  username: string
  email: string
  nickname: string | null
  avatar: string | null
  bio: string | null
  is_admin: boolean
  created_at: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const api = useApi()

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin || false)

  // Initialize from localStorage
  const init = () => {
    if (import.meta.client) {
      const savedToken = localStorage.getItem('token')
      const savedUser = localStorage.getItem('user')
      if (savedToken) {
        token.value = savedToken
      }
      if (savedUser) {
        try {
          user.value = JSON.parse(savedUser)
        } catch (e) {
          // ignore
        }
      }
    }
  }

  const login = async (username: string, password: string) => {
    const data = await api.post('/users/login', { username, password })
    token.value = data.access_token
    user.value = data.user
    if (import.meta.client) {
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
    }
    return data
  }

  const register = async (username: string, password: string) => {
    const data = await api.post('/users/register', { username, password })
    token.value = data.access_token
    user.value = data.user
    if (import.meta.client) {
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
    }
    return data
  }

  const logout = () => {
    token.value = null
    user.value = null
    if (import.meta.client) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  const fetchProfile = async () => {
    if (!token.value) return
    try {
      const data = await api.get('/users/me')
      user.value = data
      if (import.meta.client) {
        localStorage.setItem('user', JSON.stringify(data))
      }
    } catch (e) {
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
    // 刷新用户信息
    await fetchProfile()
    return result
  }

  // Init on store creation
  init()

  return {
    user,
    token,
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
