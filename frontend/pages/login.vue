<template>
  <div class="min-h-[80vh] flex items-center justify-center py-12 px-4" style="background: #FAF4E3;">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-14 h-14 rounded-xl flex items-center justify-center mx-auto mb-4" style="background: linear-gradient(135deg, #C83C23, #E08D7E);">
          <span class="text-white text-2xl font-bold font-serif">命</span>
        </div>
        <h1 class="text-2xl font-bold" style="color: #191928;">登录账号</h1>
        <p class="mt-1" style="color: #888888;">欢迎回来</p>
      </div>

      <form @submit.prevent="handleLogin" class="p-8 rounded-xl" style="background: #FEFCF8; border: 1px solid #E0E0E0; box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
        <div class="space-y-5">
          <div>
            <label class="form-label">账号</label>
            <input v-model="form.username" type="text" class="form-input" placeholder="请输入账号" required />
          </div>
          <div>
            <label class="form-label">密码</label>
            <input v-model="form.password" type="password" class="form-input" placeholder="请输入密码" required />
          </div>
          <div v-if="error" class="text-sm p-3 rounded-lg" style="color: #C83C23; background: #FDF2F0;">{{ error }}</div>
          <button type="submit" class="w-full btn-primary py-3 text-base" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>
        <div class="mt-6 text-center text-sm" style="color: #888888;">
          还没有账号？<NuxtLink to="/register" class="font-medium" style="color: #C83C23;">立即注册</NuxtLink>
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
  if (!form.value.username || !form.value.password) { error.value = '请输入账号和密码'; return }
  loading.value = true
  try {
    await userStore.login(form.value.username, form.value.password)
    navigateTo('/cases')
  } catch (e) { error.value = e.message || '登录失败' }
  finally { loading.value = false }
}
</script>
