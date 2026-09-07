<template>
  <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-2xl font-bold font-serif mb-6" style="color: #191928;">个人中心</h1>

    <!-- 未登录 -->
    <div v-if="!userStore.isLoggedIn" class="text-center py-16">
      <div class="text-5xl mb-4">🔐</div>
      <h2 class="text-xl font-bold mb-2" style="color: #191928;">请先登录</h2>
      <div class="flex justify-center gap-4 mt-4">
        <NuxtLink to="/login" class="btn-primary">去登录</NuxtLink>
        <NuxtLink to="/register" class="btn-secondary">去注册</NuxtLink>
      </div>
    </div>

    <template v-else>
      <!-- Avatar -->
      <div class="p-6 rounded-xl mb-6" style="background: #FEFCF8; border: 1px solid #E0E0E0;">
        <h2 class="text-base font-bold mb-4" style="color: #191928;">头像</h2>
        <div class="flex items-center gap-6">
          <div class="w-16 h-16 rounded-full flex items-center justify-center text-white text-2xl font-bold overflow-hidden" style="background: linear-gradient(135deg, #C83C23, #E08D7E);">
            <img v-if="userStore.user?.avatar" :src="userStore.user.avatar" class="w-full h-full object-cover" alt="">
            <span v-else>{{ (userStore.user?.nickname || 'U')[0].toUpperCase() }}</span>
          </div>
          <div>
            <label class="btn-secondary cursor-pointer text-sm">
              上传头像
              <input type="file" accept="image/jpeg,image/png,image/gif,image/webp" class="hidden" @change="handleAvatarUpload">
            </label>
            <p class="text-xs mt-2" style="color: #888888;">支持 JPG / PNG / GIF / WebP，最大 2MB</p>
            <p v-if="avatarError" class="text-xs mt-1" style="color: #C83C23;">{{ avatarError }}</p>
          </div>
        </div>
      </div>

      <!-- Email -->
      <div class="p-6 rounded-xl mb-6" style="background: #FEFCF8; border: 1px solid #E0E0E0;">
        <h2 class="text-base font-bold mb-4" style="color: #191928;">邮箱绑定</h2>
        <div v-if="userStore.user?.email && userStore.user?.email_verified" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full flex items-center justify-center" style="background: #EFF8F3;">
            <svg class="w-4 h-4" style="color: #2E8B57;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium" style="color: #333333;">{{ userStore.user.email }}</p>
            <p class="text-xs" style="color: #2E8B57;">已验证</p>
          </div>
        </div>
        <div v-else>
          <p class="text-sm mb-3" style="color: #666666;">绑定邮箱可接收通知和找回密码</p>
          <div v-if="emailStep === 1" class="space-y-3">
            <input v-model="emailForm.email" type="email" class="form-input" placeholder="请输入邮箱地址" />
            <button @click="handleSendCode" class="btn-primary text-sm" :disabled="emailSending">
              {{ emailSending ? '发送中...' : '发送验证码' }}
            </button>
            <p v-if="emailError" class="text-sm" style="color: #C83C23;">{{ emailError }}</p>
          </div>
          <div v-if="emailStep === 2" class="space-y-3">
            <p class="text-sm" style="color: #666666;">验证码已发送至 <strong>{{ emailForm.email }}</strong></p>
            <input v-model="emailForm.code" type="text" class="form-input text-center text-xl tracking-widest" maxlength="6" placeholder="000000" />
            <div class="flex gap-3">
              <button @click="handleVerifyCode" class="btn-primary text-sm" :disabled="emailVerifying">
                {{ emailVerifying ? '验证中...' : '验证并绑定' }}
              </button>
              <button @click="emailStep = 1" class="btn-secondary text-sm">返回</button>
            </div>
            <p v-if="emailError" class="text-sm" style="color: #C83C23;">{{ emailError }}</p>
            <p v-if="emailSuccess" class="text-sm" style="color: #2E8B57;">{{ emailSuccess }}</p>
          </div>
        </div>
      </div>

      <!-- Profile -->
      <div class="p-6 rounded-xl mb-6" style="background: #FEFCF8; border: 1px solid #E0E0E0;">
        <h2 class="text-base font-bold mb-4" style="color: #191928;">基本信息</h2>
        <form @submit.prevent="handleUpdateProfile" class="space-y-4">
          <div>
            <label class="form-label">账号</label>
            <input :value="userStore.user?.username" type="text" class="form-input" style="background: #F0F0F0;" disabled />
          </div>
          <div>
            <label class="form-label">UID</label>
            <input :value="userStore.user?.nickname" type="text" class="form-input" style="background: #F0F0F0;" disabled />
            <p class="text-xs mt-1" style="color: #888888;">注册时自动生成的唯一标识</p>
          </div>
          <div>
            <label class="form-label">昵称</label>
            <input v-model="profileForm.nickname" type="text" class="form-input" placeholder="选填" />
          </div>
          <div>
            <label class="form-label">个人简介</label>
            <textarea v-model="profileForm.bio" class="form-input" rows="3" placeholder="选填"></textarea>
          </div>
          <button type="submit" class="btn-primary" :disabled="profileSaving">{{ profileSaving ? '保存中...' : '保存修改' }}</button>
        </form>
      </div>

      <!-- Password -->
      <div class="p-6 rounded-xl" style="background: #FEFCF8; border: 1px solid #E0E0E0;">
        <h2 class="text-base font-bold mb-4" style="color: #191928;">修改密码</h2>
        <form @submit.prevent="handleChangePassword" class="space-y-4">
          <div><label class="form-label">原密码</label><input v-model="passwordForm.oldPassword" type="password" class="form-input" required /></div>
          <div><label class="form-label">新密码</label><input v-model="passwordForm.newPassword" type="password" class="form-input" placeholder="8位以上" required /></div>
          <div><label class="form-label">确认新密码</label><input v-model="passwordForm.confirmPassword" type="password" class="form-input" required /></div>
          <p v-if="passwordError" class="text-sm" style="color: #C83C23;">{{ passwordError }}</p>
          <p v-if="passwordSuccess" class="text-sm" style="color: #2E8B57;">{{ passwordSuccess }}</p>
          <button type="submit" class="btn-primary" :disabled="passwordSaving">{{ passwordSaving ? '修改中...' : '修改密码' }}</button>
        </form>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '~/stores/user'

useHead({ title: '个人中心 - 八字命理案例库' })
const userStore = useUserStore()

const profileForm = ref({ nickname: '', bio: '' })
const profileSaving = ref(false)
const avatarError = ref('')

const emailStep = ref(1)
const emailForm = ref({ email: '', code: '' })
const emailError = ref('')
const emailSuccess = ref('')
const emailSending = ref(false)
const emailVerifying = ref(false)

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

const handleAvatarUpload = async (e) => {
  avatarError.value = ''
  const file = e.target.files[0]
  if (!file) return

  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    avatarError.value = '请上传 JPG、PNG、GIF 或 WebP 格式的图片'
    return
  }
  if (file.size > 2 * 1024 * 1024) {
    avatarError.value = '图片大小不能超过 2MB'
    return
  }

  try {
    await userStore.uploadAvatar(file)
    avatarError.value = ''
    alert('头像更新成功')
  } catch (e) {
    avatarError.value = e.message || '上传失败'
  }
}

const handleSendCode = async () => {
  emailError.value = ''
  if (!emailForm.value.email) { emailError.value = '请输入邮箱地址'; return }
  emailSending.value = true
  try {
    await userStore.sendEmailCode(emailForm.value.email)
    emailStep.value = 2
  } catch (e) { emailError.value = e.message || '发送失败' }
  finally { emailSending.value = false }
}

const handleVerifyCode = async () => {
  emailError.value = ''; emailSuccess.value = ''
  if (emailForm.value.code.length !== 6) { emailError.value = '请输入6位验证码'; return }
  emailVerifying.value = true
  try {
    await userStore.verifyEmail(emailForm.value.email, emailForm.value.code)
    emailSuccess.value = '邮箱绑定成功！'
    emailStep.value = 1
    emailForm.value = { email: '', code: '' }
  } catch (e) { emailError.value = e.message || '验证失败' }
  finally { emailVerifying.value = false }
}

const handleUpdateProfile = async () => {
  profileSaving.value = true
  try { await userStore.updateProfile(profileForm.value); alert('保存成功') }
  catch (e) { alert(e.message || '保存失败') }
  finally { profileSaving.value = false }
}

const handleChangePassword = async () => {
  passwordError.value = ''; passwordSuccess.value = ''
  if (passwordForm.value.newPassword.length < 8) { passwordError.value = '新密码长度不能少于8位'; return }
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) { passwordError.value = '两次输入的密码不一致'; return }
  passwordSaving.value = true
  try {
    await userStore.changePassword(passwordForm.value.oldPassword, passwordForm.value.newPassword)
    passwordSuccess.value = '密码修改成功'
    passwordForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
  } catch (e) { passwordError.value = e.message || '修改失败' }
  finally { passwordSaving.value = false }
}
</script>
