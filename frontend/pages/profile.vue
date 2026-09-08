<template>
  <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-3xl font-bold text-gray-900 font-serif mb-8">个人中心</h1>

    <!-- Avatar -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8 mb-6">
      <h2 class="text-lg font-bold text-gray-900 mb-6">头像</h2>
      <div class="flex items-center gap-6">
        <div class="w-20 h-20 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white text-3xl font-bold overflow-hidden">
          <img v-if="userStore.user?.avatar" :src="userStore.user.avatar" class="w-full h-full object-cover" alt="avatar">
          <span v-else>{{ userStore.user?.nickname?.[0] || 'U' }}</span>
        </div>
        <div>
          <label class="btn-secondary cursor-pointer">
            上传头像
            <input type="file" accept="image/*" class="hidden" @change="handleAvatarUpload">
          </label>
          <p class="text-xs text-gray-400 mt-2">支持 JPG、PNG，最大 2MB</p>
        </div>
      </div>
    </div>

    <!-- Email Binding -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8 mb-6">
      <h2 class="text-lg font-bold text-gray-900 mb-6">邮箱绑定</h2>

      <!-- 已绑定邮箱 -->
      <div v-if="userStore.user?.email && userStore.user?.email_verified">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center">
            <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-900">{{ userStore.user.email }}</p>
            <p class="text-xs text-primary-600">已验证</p>
          </div>
        </div>

        <!-- 解绑邮箱流程 -->
        <div v-if="!unbindMode">
          <button @click="startUnbind" class="text-sm text-red-500 hover:text-red-700 underline">解绑邮箱</button>
        </div>

        <div v-if="unbindMode" class="mt-4 space-y-4 border-t border-gray-100 pt-4">
          <p class="text-sm text-gray-600">解绑邮箱需要验证身份，验证码将发送到 <strong>{{ userStore.user.email }}</strong></p>
          <button
            @click="handleSendUnbindCode"
            class="btn-secondary text-sm"
            :disabled="unbindSending || unbindCooldown > 0"
          >
            {{ unbindCooldown > 0 ? `${unbindCooldown}s后重发` : (unbindSending ? '发送中...' : '发送验证码') }}
          </button>
          <div v-if="unbindStep === 2">
            <label class="form-label">验证码</label>
            <input
              v-model="unbindCode"
              type="text"
              class="form-input text-center text-2xl tracking-[0.5em]"
              maxlength="6"
              placeholder="000000"
              @input="unbindCode = unbindCode.replace(/\D/g, '')"
            />
            <div class="flex gap-3 mt-3">
              <button @click="handleUnbindEmail" class="btn-primary text-sm" :disabled="unbindVerifying">
                {{ unbindVerifying ? '解绑中...' : '确认解绑' }}
              </button>
              <button @click="cancelUnbind" class="btn-secondary text-sm">取消</button>
            </div>
          </div>
          <div v-if="unbindError" class="text-red-500 text-sm bg-red-50 p-3 rounded-lg">{{ unbindError }}</div>
          <div v-if="unbindSuccess" class="text-green-600 text-sm bg-green-50 p-3 rounded-lg">{{ unbindSuccess }}</div>
        </div>
      </div>

      <!-- 未绑定邮箱 -->
      <div v-else>
        <p class="text-sm text-gray-500 mb-4">绑定邮箱后可以接收通知和找回密码</p>

        <!-- Step 1: 输入邮箱 -->
        <div v-if="emailStep === 1" class="space-y-4">
          <div>
            <label class="form-label">邮箱地址</label>
            <input
              v-model="emailForm.email"
              type="email"
              class="form-input"
              :class="{ 'border-red-400': emailErrors.email }"
              placeholder="请输入邮箱地址"
              @input="validateEmailInput"
            />
            <p v-if="emailErrors.email" class="text-red-500 text-xs mt-1">{{ emailErrors.email }}</p>
          </div>
          <button @click="handleSendCode" class="btn-primary" :disabled="emailSending">
            {{ emailSending ? '发送中...' : '发送验证码' }}
          </button>
          <div v-if="emailError" class="text-red-500 text-sm bg-red-50 p-3 rounded-lg">{{ emailError }}</div>
        </div>

        <!-- Step 2: 输入验证码 -->
        <div v-if="emailStep === 2" class="space-y-4">
          <p class="text-sm text-gray-600">
            验证码已发送至 <strong>{{ emailForm.email }}</strong>，请在10分钟内输入
          </p>
          <div>
            <label class="form-label">验证码</label>
            <input
              v-model="emailForm.code"
              type="text"
              class="form-input text-center text-2xl tracking-[0.5em]"
              maxlength="6"
              placeholder="000000"
              @input="emailForm.code = emailForm.code.replace(/\D/g, '')"
            />
          </div>
          <div class="flex gap-3">
            <button @click="handleVerifyCode" class="btn-primary" :disabled="emailVerifying">
              {{ emailVerifying ? '验证中...' : '验证并绑定' }}
            </button>
            <button @click="emailStep = 1; emailError = ''" class="btn-secondary">返回</button>
          </div>
          <div v-if="emailError" class="text-red-500 text-sm bg-red-50 p-3 rounded-lg">{{ emailError }}</div>
          <div v-if="emailSuccess" class="text-green-600 text-sm bg-green-50 p-3 rounded-lg">{{ emailSuccess }}</div>
        </div>
      </div>
    </div>

    <!-- Profile -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8 mb-6">
      <h2 class="text-lg font-bold text-gray-900 mb-6">基本信息</h2>
      <form @submit.prevent="handleUpdateProfile" class="space-y-4">
        <div>
          <label class="form-label">账号</label>
          <input :value="userStore.user?.username" type="text" class="form-input bg-gray-50" disabled>
        </div>
        <div>
          <label class="form-label">昵称</label>
          <input v-model="profileForm.nickname" type="text" class="form-input">
        </div>
        <div>
          <label class="form-label">个人简介</label>
          <textarea v-model="profileForm.bio" class="form-input" rows="3"></textarea>
        </div>
        <button type="submit" class="btn-primary" :disabled="profileSaving">{{ profileSaving ? '保存中...' : '保存修改' }}</button>
      </form>
    </div>

    <!-- Password -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8 mb-6">
      <h2 class="text-lg font-bold text-gray-900 mb-6">修改密码</h2>
      <form @submit.prevent="handleChangePassword" class="space-y-4">
        <div>
          <label class="form-label">原密码</label>
          <input v-model="passwordForm.oldPassword" type="password" class="form-input" required>
        </div>
        <div>
          <label class="form-label">新密码</label>
          <input v-model="passwordForm.newPassword" type="password" class="form-input" placeholder="6位以上，字母、数字或下划线" required>
        </div>
        <div>
          <label class="form-label">确认新密码</label>
          <input v-model="passwordForm.confirmPassword" type="password" class="form-input" required>
        </div>
        <div v-if="passwordError" class="text-red-500 text-sm bg-red-50 p-3 rounded-lg">{{ passwordError }}</div>
        <div v-if="passwordSuccess" class="text-green-600 text-sm bg-green-50 p-3 rounded-lg">{{ passwordSuccess }}</div>
        <button type="submit" class="btn-primary" :disabled="passwordSaving">{{ passwordSaving ? '修改中...' : '修改密码' }}</button>
      </form>
    </div>

    <!-- Logout -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
      <button @click="handleLogout" class="w-full py-3 text-base text-red-600 border border-red-200 rounded-lg hover:bg-red-50 transition-colors font-medium">
        退出登录
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '~/stores/user'

useHead({ title: '个人中心 - 八字命理案例库' })
const userStore = useUserStore()

// Profile
const profileForm = ref({ nickname: '', bio: '' })
const profileSaving = ref(false)

// Email binding
const emailStep = ref(1)
const emailForm = ref({ email: '', code: '' })
const emailErrors = ref({ email: '' })
const emailError = ref('')
const emailSuccess = ref('')
const emailSending = ref(false)
const emailVerifying = ref(false)

// Email unbind
const unbindMode = ref(false)
const unbindStep = ref(1)
const unbindCode = ref('')
const unbindSending = ref(false)
const unbindVerifying = ref(false)
const unbindError = ref('')
const unbindSuccess = ref('')
const unbindCooldown = ref(0)
let unbindCooldownTimer = null

// Password
const passwordForm = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })
const passwordSaving = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

onMounted(() => {
  if (userStore.user) {
    profileForm.value.nickname = userStore.user.nickname || ''
    profileForm.value.bio = userStore.user.bio || ''
  }
})

const validateEmailInput = () => {
  const v = emailForm.value.email
  if (!v) { emailErrors.value.email = ''; return }
  if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(v)) {
    emailErrors.value.email = '请输入正确的邮箱地址'
  } else {
    emailErrors.value.email = ''
  }
}

const handleAvatarUpload = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  try {
    await userStore.uploadAvatar(file)
    alert('头像更新成功')
  } catch (e) {
    alert(e.message || '上传失败')
  }
}

const handleSendCode = async () => {
  emailError.value = ''
  validateEmailInput()
  if (emailErrors.value.email) return

  emailSending.value = true
  try {
    await userStore.sendEmailCode(emailForm.value.email)
    emailStep.value = 2
  } catch (e) {
    emailError.value = e.message || '发送失败'
  } finally {
    emailSending.value = false
  }
}

const handleVerifyCode = async () => {
  emailError.value = ''
  emailSuccess.value = ''

  if (emailForm.value.code.length !== 6) {
    emailError.value = '请输入6位验证码'
    return
  }

  emailVerifying.value = true
  try {
    await userStore.verifyEmail(emailForm.value.email, emailForm.value.code)
    emailSuccess.value = '邮箱绑定成功！'
    emailStep.value = 1
    emailForm.value = { email: '', code: '' }
    await userStore.fetchProfile()
  } catch (e) {
    emailError.value = e.message || '验证失败'
  } finally {
    emailVerifying.value = false
  }
}

// 解绑邮箱
const startUnbind = () => {
  unbindMode.value = true
  unbindStep.value = 1
  unbindCode.value = ''
  unbindError.value = ''
  unbindSuccess.value = ''
}

const cancelUnbind = () => {
  unbindMode.value = false
  unbindStep.value = 1
  unbindCode.value = ''
  unbindError.value = ''
  unbindSuccess.value = ''
}

const startUnbindCooldown = () => {
  unbindCooldown.value = 60
  unbindCooldownTimer = setInterval(() => {
    unbindCooldown.value--
    if (unbindCooldown.value <= 0) {
      clearInterval(unbindCooldownTimer)
    }
  }, 1000)
}

const handleSendUnbindCode = async () => {
  unbindError.value = ''
  unbindSending.value = true
  try {
    await userStore.unbindEmail()
    unbindStep.value = 2
    startUnbindCooldown()
  } catch (e) {
    unbindError.value = e.message || '发送失败'
  } finally {
    unbindSending.value = false
  }
}

const handleUnbindEmail = async () => {
  unbindError.value = ''
  unbindSuccess.value = ''

  if (unbindCode.value.length !== 6) {
    unbindError.value = '请输入6位验证码'
    return
  }

  unbindVerifying.value = true
  try {
    await userStore.unbindEmail()
    unbindSuccess.value = '邮箱解绑成功！'
    await userStore.fetchProfile()
    setTimeout(() => {
      cancelUnbind()
    }, 2000)
  } catch (e) {
    unbindError.value = e.message || '解绑失败'
  } finally {
    unbindVerifying.value = false
  }
}

const handleUpdateProfile = async () => {
  profileSaving.value = true
  try {
    await userStore.updateProfile(profileForm.value)
    alert('保存成功')
  } catch (e) {
    alert(e.message || '保存失败')
  } finally {
    profileSaving.value = false
  }
}

const handleChangePassword = async () => {
  passwordError.value = ''
  passwordSuccess.value = ''

  if (passwordForm.value.newPassword.length < 6) {
    passwordError.value = '新密码长度不能少于6位'
    return
  }
  if (!/^[a-zA-Z0-9_]+$/.test(passwordForm.value.newPassword)) {
    passwordError.value = '新密码只能包含字母、数字、下划线'
    return
  }
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = '两次输入的密码不一致'
    return
  }

  passwordSaving.value = true
  try {
    await userStore.changePassword(passwordForm.value.oldPassword, passwordForm.value.newPassword)
    passwordSuccess.value = '密码修改成功'
    passwordForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
  } catch (e) {
    passwordError.value = e.message || '修改失败'
  } finally {
    passwordSaving.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
  navigateTo('/login')
}
</script>
