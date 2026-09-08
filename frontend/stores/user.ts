import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi, setAuthToken, getAuthToken } from '~/utils/api'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const api = useApi()

  const isLoggedIn = computed(() => !!getAuthToken())
  const isAdmin = computed(() => user.value?.is_admin || false)

  // Initialize from localStorage
  const init = () => {
    if (import.meta.client) {
      const savedUser = localStorage.getItem('user')
      if (savedUser) {
        try {
          user.value = JSON.parse(savedUser)
        } catch (e) {
          // ignore
        }
      }
    }
  }

  const login = async (username, password) => {
    const data = await api.post('/users/login', { username, password })
    setAuthToken(data.access_token)
    user.value = data.user
    if (import.meta.client) {
      localStorage.setItem('user', JSON.stringify(data.user))
    }
    return data
  }

  const register = async (username, password, email) => {
    const data = await api.post('/users/register', { username, password, email })
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
    } catch (e) {
      logout()
    }
  }

  const updateProfile = async (data) => {
    const result = await api.put('/users/me', data)
    user.value = result
    if (import.meta.client) {
      localStorage.setItem('user', JSON.stringify(result))
    }
    return result
  }

  const changePassword = async (oldPassword, newPassword) => {
    return await api.post('/users/me/password', {
      old_password: oldPassword,
      new_password: newPassword,
    })
  }

  const uploadAvatar = async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const result = await api.upload('/users/me/avatar', formData)
    user.value = result
    if (import.meta.client) {
      localStorage.setItem('user', JSON.stringify(result))
    }
    return result
  }

  const sendEmailCode = async (email) => {
    return await api.post('/users/email/send-code', { email })
  }

  const verifyEmail = async (email, code) => {
    return await api.post('/users/email/verify', { email, code })
  }

  const unbindEmail = async () => {
    return await api.post('/users/me/email/unbind')
  }

  // Init on store creation
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
    unbindEmail,
  }
})
