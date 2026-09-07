<template>
  <div class="min-h-[80vh] flex items-center justify-center py-12 px-4" style="background: #FAF4E3;">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-14 h-14 rounded-xl flex items-center justify-center mx-auto mb-4" style="background: linear-gradient(135deg, #C83C23, #E08D7E);">
          <span class="text-white text-2xl font-bold font-serif">命</span>
        </div>
        <h1 class="text-2xl font-bold" style="color: #191928;">注册账号</h1>
        <p class="mt-1" style="color: #888888;">创建您的账号</p>
      </div>

      <form @submit.prevent="handleRegister" class="p-8 rounded-xl" style="background: #FEFCF8; border: 1px solid #E0E0E0; box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
        <div class="space-y-5">
          <div>
            <label class="form-label">账号</label>
            <input v-model="form.username" type="text" class="form-input" :class="{ 'border-red-400': errors.username }" placeholder="不少于6位，字母、数字或下划线" @input="validateUsername" />
            <p v-if="errors.username" class="text-xs mt-1" style="color: #C83C23;">{{ errors.username }}</p>
            <p v-else class="text-xs mt-1" style="color: #888888;">6-50位，字母、数字、下划线</p>
          </div>
          <div>
            <label class="form-label">密码</label>
            <input v-model="form.password" type="password" class="form-input" :class="{ 'border-red-400': errors.password }" placeholder="不少于8位，字母、数字或下划线" @input="validatePassword" />
            <p v-if="errors.password" class="text-xs mt-1" style="color: #C83C23;">{{ errors.password }}</p>
            <p v-else class="text-xs mt-1" style="color: #888888;">8位以上，字母、数字、下划线</p>
          </div>
          <div>
            <label class="form-label">确认密码</label>
            <input v-model="form.confirmPassword" type="password" class="form-input" :class="{ 'border-red-400': errors.confirmPassword }" placeholder="请再次输入密码" @input="validateConfirmPassword" />
            <p v-if="errors.confirmPassword" class="text-xs mt-1" style="color: #C83C23;">{{ errors.confirmPassword }}</p>
          </div>
          <div v-if="error" class="text-sm p-3 rounded-lg" style="color: #C83C23; background: #FDF2F0;">{{ error }}</div>
          <button type="submit" class="w-full btn-primary py-3 text-base" :disabled="loading">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>
        <div class="mt-6 text-center text-sm" style="color: #888888;">
          已有账号？<NuxtLink to="/login" class="font-medium" style="color: #C83C23;">立即登录</NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '~/stores/user'

useHead({ title: '注册 - 八字命理案例库' })
const userStore = useUserStore()
const form = ref({ username: '', password: '', confirmPassword: '' })
const errors = reactive({ username: '', password: '', confirmPassword: '' })
const error = ref('')
const loading = ref(false)

const validateUsername = () => {
  const v = form.value.username
  if (!v) { errors.username = ''; return }
  if (!/^[a-zA-Z0-9_]+$/.test(v)) { errors.username = '请按照格式要求创建您的账号'; return }
  if (v.length < 6) { errors.username = '账号长度不能少于6位'; return }
  errors.username = ''
}
const validatePassword = () => {
  const v = form.value.password
  if (!v) { errors.password = ''; return }
  if (!/^[a-zA-Z0-9_]+$/.test(v)) { errors.password = '密码只能包含字母、数字、下划线'; return }
  if (v.length < 8) { errors.password = '密码长度不能少于8位'; return }
  errors.password = ''
  if (form.value.confirmPassword) validateConfirmPassword()
}
const validateConfirmPassword = () => {
  if (!form.value.confirmPassword) { errors.confirmPassword = ''; return }
  if (form.value.confirmPassword !== form.value.password) { errors.confirmPassword = '两次输入的密码不一致'; return }
  errors.confirmPassword = ''
}

const handleRegister = async () => {
  error.value = ''
  validateUsername(); validatePassword(); validateConfirmPassword()
  if (errors.username || errors.password || errors.confirmPassword) return
  if (!form.value.username || !form.value.password || !form.value.confirmPassword) return
  loading.value = true
  try {
    await userStore.register(form.value.username, form.value.password)
    navigateTo('/cases')
  } catch (e) { error.value = e.message || '注册失败' }
  finally { loading.value = false }
}
</script>
