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

    <!-- Profile -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8 mb-6">
      <h2 class="text-lg font-bold text-gray-900 mb-6">基本信息</h2>
      <form @submit.prevent="handleUpdateProfile" class="space-y-4">
        <div>
          <label class="form-label">用户名</label>
          <input :value="userStore.user?.username" type="text" class="form-input bg-gray-50" disabled>
        </div>
        <div>
          <label class="form-label">邮箱</label>
          <input :value="userStore.user?.email" type="email" class="form-input bg-gray-50" disabled>
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
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
      <h2 class="text-lg font-bold text-gray-900 mb-6">修改密码</h2>
      <form @submit.prevent="handleChangePassword" class="space-y-4">
        <div>
          <label class="form-label">原密码</label>
          <input v-model="passwordForm.oldPassword" type="password" class="form-input" required>
        </div>
        <div>
          <label class="form-label">新密码</label>
          <input v-model="passwordForm.newPassword" type="password" class="form-input" required minlength="6">
        </div>
        <div>
          <label class="form-label">确认新密码</label>
          <input v-model="passwordForm.confirmPassword" type="password" class="form-input" required>
        </div>
        <div v-if="passwordError" class="text-red-500 text-sm">{{ passwordError }}</div>
        <div v-if="passwordSuccess" class="text-green-600 text-sm">{{ passwordSuccess }}</div>
        <button type="submit" class="btn-primary" :disabled="passwordSaving">{{ passwordSaving ? '修改中...' : '修改密码' }}</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '~/stores/user'

useHead({ title: '个人中心 - 八字命理案例库' })
const userStore = useUserStore()

const profileForm = ref({ nickname: '', bio: '' })
const profileSaving = ref(false)

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
  const file = e.target.files[0]
  if (!file) return
  try {
    await userStore.uploadAvatar(file)
    alert('头像更新成功')
  } catch (e) {
    alert(e.message || '上传失败')
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
</script>
