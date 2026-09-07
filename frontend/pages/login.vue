<template>
  <div class="min-h-[80vh] flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <span class="text-white text-3xl font-bold font-serif">命</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900">登录账号</h1>
        <p class="text-gray-500 mt-2">欢迎回来，请输入您的账号信息</p>
      </div>

      <form @submit.prevent="handleLogin" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <div class="space-y-5">
          <div>
            <label class="form-label">账号</label>
            <input
              v-model="form.username"
              type="text"
              class="form-input"
              placeholder="请输入账号"
              required
            />
          </div>

          <div>
            <label class="form-label">密码</label>
            <input
              v-model="form.password"
              type="password"
              class="form-input"
              placeholder="请输入密码"
              required
            />
          </div>

          <div v-if="error" class="text-red-500 text-sm bg-red-50 p-3 rounded-lg">
            {{ error }}
          </div>

          <button
            type="submit"
            class="w-full btn-primary py-3 text-base"
            :disabled="loading"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>

        <div class="mt-6 text-center text-sm text-gray-500">
          还没有账号？
          <NuxtLink to="/register" class="text-primary-600 font-medium hover:text-primary-700">立即注册</NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '~/stores/user'

useHead({ title: '登录 - 八字命理案例库' })

const userStore = useUserStore()
const form = ref({ username: '', password: '' })
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  if (!form.value.username || !form.value.password) {
    error.value = '请输入账号和密码'
    return
  }
  loading.value = true
  try {
    await userStore.login(form.value.username, form.value.password)
    navigateTo('/cases')
  } catch (e) {
    error.value = e.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>
