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
          <!-- 账号 -->
          <div>
            <label class="form-label">账号</label>
            <input
              v-model="form.username"
              type="text"
              class="form-input"
              :class="{ 'border-red-400': errors.username }"
              placeholder="不少于6位，字母、数字或下划线"
              @input="validateUsername"
            />
            <p v-if="errors.username" class="text-red-500 text-xs mt-1">{{ errors.username }}</p>
            <p v-else class="text-gray-400 text-xs mt-1">6-50个字符，只能包含字母、数字、下划线</p>
          </div>

          <!-- 密码 -->
          <div>
            <label class="form-label">密码</label>
            <input
              v-model="form.password"
              type="password"
              class="form-input"
              :class="{ 'border-red-400': errors.password }"
              placeholder="不少于8位，字母、数字或下划线"
              @input="validatePassword"
            />
            <p v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</p>
            <p v-else class="text-gray-400 text-xs mt-1">8位以上，只能包含字母、数字、下划线</p>
          </div>

          <!-- 确认密码 -->
          <div>
            <label class="form-label">确认密码</label>
            <input
              v-model="form.confirmPassword"
              type="password"
              class="form-input"
              :class="{ 'border-red-400': errors.confirmPassword }"
              placeholder="请再次输入密码"
              @input="validateConfirmPassword"
            />
            <p v-if="errors.confirmPassword" class="text-red-500 text-xs mt-1">{{ errors.confirmPassword }}</p>
          </div>

          <!-- 全局错误 -->
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
import { ref, reactive } from 'vue'
import { useUserStore } from '~/stores/user'

useHead({ title: '注册 - 八字命理案例库' })

const userStore = useUserStore()
const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
})
const errors = reactive({
  username: '',
  password: '',
  confirmPassword: '',
})
const error = ref('')
const loading = ref(false)

const validateUsername = () => {
  const v = form.value.username
  if (!v) {
    errors.username = ''
    return
  }
  if (!/^[a-zA-Z0-9_]+$/.test(v)) {
    errors.username = '账号只能包含字母、数字、下划线'
    return
  }
  if (v.length < 6) {
    errors.username = '账号长度不能少于6位'
    return
  }
  errors.username = ''
}

const validatePassword = () => {
  const v = form.value.password
  if (!v) {
    errors.password = ''
    return
  }
  if (!/^[a-zA-Z0-9_]+$/.test(v)) {
    errors.password = '密码只能包含字母、数字、下划线'
    return
  }
  if (v.length < 8) {
    errors.password = '密码长度不能少于8位'
    return
  }
  errors.password = ''
  // 如果确认密码已填写，重新校验
  if (form.value.confirmPassword) {
    validateConfirmPassword()
  }
}

const validateConfirmPassword = () => {
  if (!form.value.confirmPassword) {
    errors.confirmPassword = ''
    return
  }
  if (form.value.confirmPassword !== form.value.password) {
    errors.confirmPassword = '两次输入的密码不一致'
    return
  }
  errors.confirmPassword = ''
}

const handleRegister = async () => {
  error.value = ''

  // 全面校验
  validateUsername()
  validatePassword()
  validateConfirmPassword()

  if (errors.username || errors.password || errors.confirmPassword) {
    return
  }

  if (!form.value.username) {
    errors.username = '请输入账号'
    return
  }
  if (!form.value.password) {
    errors.password = '请输入密码'
    return
  }
  if (!form.value.confirmPassword) {
    errors.confirmPassword = '请确认密码'
    return
  }

  loading.value = true
  try {
    await userStore.register(form.value.username, form.value.password)
    navigateTo('/cases')
  } catch (e) {
    error.value = e.message || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>
