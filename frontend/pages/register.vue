<template>
  <div class="min-h-[80vh] flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <span class="text-white text-3xl font-bold font-serif">命</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900">注册账号</h1>
        <p class="text-gray-500 mt-2">创建您的账号，开始使用八字命理案例库</p>
      </div>

      <form @submit.prevent="handleRegister" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <div class="space-y-5">
          <div>
            <label class="form-label">用户名</label>
            <input
              v-model="form.username"
              type="text"
              class="form-input"
              placeholder="3-50个字符，字母数字下划线"
              required
            />
          </div>

          <div>
            <label class="form-label">邮箱</label>
            <input
              v-model="form.email"
              type="email"
              class="form-input"
              placeholder="请输入邮箱地址"
              required
            />
          </div>

          <div>
            <label class="form-label">昵称</label>
            <input
              v-model="form.nickname"
              type="text"
              class="form-input"
              placeholder="选填，默认为用户名"
            />
          </div>

          <div>
            <label class="form-label">密码</label>
            <input
              v-model="form.password"
              type="password"
              class="form-input"
              placeholder="至少6个字符"
              required
            />
          </div>

          <div>
            <label class="form-label">确认密码</label>
            <input
              v-model="form.confirmPassword"
              type="password"
              class="form-input"
              placeholder="请再次输入密码"
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
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>

        <div class="mt-6 text-center text-sm text-gray-500">
          已有账号？
          <NuxtLink to="/login" class="text-primary-600 font-medium hover:text-primary-700">立即登录</NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '~/stores/user'

useHead({ title: '注册 - 八字命理案例库' })

const userStore = useUserStore()
const form = ref({
  username: '',
  email: '',
  nickname: '',
  password: '',
  confirmPassword: '',
})
const error = ref('')
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''

  if (form.value.password !== form.value.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }

  loading.value = true
  try {
    await userStore.register(
      form.value.username,
      form.value.email,
      form.value.password,
      form.value.nickname || undefined
    )
    navigateTo('/cases')
  } catch (e) {
    error.value = e.message || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>
