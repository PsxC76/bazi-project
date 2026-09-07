<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- 未登录提示 -->
    <div v-if="needLogin" class="text-center py-16">
      <div class="text-6xl mb-4">🔐</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">请先登录</h2>
      <p class="text-gray-500 mb-6">创建案例需要登录账号</p>
      <div class="flex justify-center gap-4">
        <NuxtLink to="/login" class="btn-primary">去登录</NuxtLink>
        <NuxtLink to="/register" class="btn-secondary">去注册</NuxtLink>
      </div>
    </div>

    <template v-else>
      <div class="mb-8">
        <NuxtLink to="/cases" class="text-sm text-gray-500 hover:text-primary-600 flex items-center gap-1 mb-4">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          返回案例列表
        </NuxtLink>
        <h1 class="text-3xl font-bold text-gray-900 font-serif">新建案例</h1>
        <p class="text-gray-500 mt-1">填写命主信息，系统将自动计算八字</p>
      </div>

    <form @submit.prevent="handleSubmit" class="space-y-8">
      <!-- Basic Info -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-lg font-bold text-gray-900 mb-6">基本信息</h2>

        <div class="grid md:grid-cols-2 gap-6">
          <div>
            <label class="form-label">姓名 <span class="text-red-500">*</span></label>
            <input v-model="form.name" type="text" class="form-input" placeholder="命主姓名" required>
          </div>

          <div>
            <label class="form-label">性别 <span class="text-red-500">*</span></label>
            <div class="flex gap-4 mt-1">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="form.gender" value="男" class="w-4 h-4 text-primary-600">
                <span>男</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="form.gender" value="女" class="w-4 h-4 text-primary-600">
                <span>女</span>
              </label>
            </div>
          </div>

          <div>
            <label class="form-label">出生地点</label>
            <input v-model="form.birth_place" type="text" class="form-input" placeholder="选填">
          </div>

          <div>
            <label class="form-label">是否公开</label>
            <label class="flex items-center gap-2 cursor-pointer mt-1">
              <input type="checkbox" v-model="form.is_public" class="w-4 h-4 text-primary-600 rounded">
              <span class="text-sm text-gray-600">公开此案例（所有人可见）</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Birth Date -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-lg font-bold text-gray-900 mb-6">出生时间</h2>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div>
            <label class="form-label">年份 <span class="text-red-500">*</span></label>
            <input v-model.number="form.birth_year" type="number" class="form-input" placeholder="1990" required min="1900" max="2100">
          </div>

          <div>
            <label class="form-label">月份 <span class="text-red-500">*</span></label>
            <select v-model.number="form.birth_month" class="form-input" required>
              <option v-for="m in 12" :key="m" :value="m">{{ m }}月</option>
            </select>
          </div>

          <div>
            <label class="form-label">日期 <span class="text-red-500">*</span></label>
            <select v-model.number="form.birth_day" class="form-input" required>
              <option v-for="d in 31" :key="d" :value="d">{{ d }}日</option>
            </select>
          </div>

          <div>
            <label class="form-label">时辰</label>
            <select v-model="form.birth_hour" class="form-input">
              <option :value="null">未知</option>
              <option v-for="h in hours" :key="h.value" :value="h.value">{{ h.label }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Tags -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-gray-900">标签</h2>
          <button type="button" @click="addTag" class="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            添加标签
          </button>
        </div>

        <div class="space-y-4">
          <div v-for="(tag, index) in form.tags" :key="index" class="flex items-center gap-3">
            <select v-model="tag.name" class="form-input w-40">
              <option value="">选择标签</option>
              <option v-for="name in tagNames" :key="name" :value="name">{{ name }}</option>
              <option value="__custom">自定义...</option>
            </select>

            <input
              v-if="tag.name === '__custom'"
              v-model="tag.customName"
              type="text"
              class="form-input w-40"
              placeholder="自定义标签名"
            >

            <input v-model="tag.value" type="text" class="form-input flex-1" placeholder="标签值">

            <button type="button" @click="removeTag(index)" class="p-2 text-gray-400 hover:text-red-500">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>

          <div v-if="form.tags.length === 0" class="text-sm text-gray-400 text-center py-4">
            暂无标签，点击"添加标签"来添加
          </div>
        </div>
      </div>

      <!-- Verdict & Notes -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-lg font-bold text-gray-900 mb-6">断语与备注</h2>

        <div class="space-y-6">
          <div>
            <label class="form-label">断语</label>
            <textarea v-model="form.verdict" class="form-input" rows="3" placeholder="对该命例的判断..."></textarea>
          </div>

          <div>
            <label class="form-label">备注</label>
            <textarea v-model="form.notes" class="form-input" rows="3" placeholder="其他备注信息..."></textarea>
          </div>
        </div>
      </div>

      <!-- Preview -->
      <div v-if="baziPreview" class="bg-gradient-to-br from-primary-50 to-white rounded-2xl border border-primary-100 p-6 lg:p-8">
        <h2 class="text-lg font-bold text-primary-900 mb-6">八字预览</h2>

        <div class="grid grid-cols-4 gap-4 max-w-md mx-auto">
          <div v-for="(pillar, key) in baziPreview" :key="key" class="text-center">
            <div class="text-xs text-gray-400 mb-1">{{ pillarLabels[key] }}</div>
            <div class="text-xl font-bold font-serif text-primary-800">{{ pillar.stem }}{{ pillar.branch }}</div>
            <div class="text-xs text-primary-600">{{ pillar.ten_god }}</div>
          </div>
        </div>
      </div>

      <!-- Submit -->
      <div class="flex justify-end gap-4">
        <NuxtLink to="/cases" class="btn-secondary">取消</NuxtLink>
        <button type="submit" class="btn-primary px-8" :disabled="submitting">
          {{ submitting ? '保存中...' : '保存案例' }}
        </button>
      </div>
    </form>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useApi } from '~/utils/api'
import { useUserStore } from '~/stores/user'

useHead({ title: '新建案例 - 八字命理案例库' })

const api = useApi()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const submitting = ref(false)
const baziPreview = ref(null)
const needLogin = ref(false)

// 检查登录状态
onMounted(() => {
  if (!userStore.isLoggedIn) {
    needLogin.value = true
  }
})

const tagNames = ['职业', '学历', '婚姻', '财富', '寿夭', '健康', '性格', '其他']

const hours = [
  { value: 0, label: '子时 (23-1时)' },
  { value: 1, label: '丑时 (1-3时)' },
  { value: 3, label: '寅时 (3-5时)' },
  { value: 5, label: '卯时 (5-7时)' },
  { value: 7, label: '辰时 (7-9时)' },
  { value: 9, label: '巳时 (9-11时)' },
  { value: 11, label: '午时 (11-13时)' },
  { value: 13, label: '未时 (13-15时)' },
  { value: 15, label: '申时 (15-17时)' },
  { value: 17, label: '酉时 (17-19时)' },
  { value: 19, label: '戌时 (19-21时)' },
  { value: 21, label: '亥时 (21-23时)' },
]

const pillarLabels = {
  year_pillar: '年柱',
  month_pillar: '月柱',
  day_pillar: '日柱',
  hour_pillar: '时柱',
}

const form = ref({
  name: '',
  gender: '男',
  birth_place: '',
  birth_year: parseInt(route.query.year) || 1990,
  birth_month: parseInt(route.query.month) || 1,
  birth_day: parseInt(route.query.day) || 1,
  birth_hour: route.query.hour ? parseInt(route.query.hour) : null,
  is_lunar: false,
  verdict: '',
  notes: '',
  is_public: false,
  tags: [],
})

const addTag = () => {
  form.value.tags.push({ name: '', customName: '', value: '' })
}

const removeTag = (index) => {
  form.value.tags.splice(index, 1)
}

// Auto-preview bazi when date changes
let previewTimer = null
watch(
  () => [form.value.birth_year, form.value.birth_month, form.value.birth_day, form.value.birth_hour, form.value.gender],
  () => {
    clearTimeout(previewTimer)
    previewTimer = setTimeout(async () => {
      if (form.value.birth_year && form.value.birth_month && form.value.birth_day) {
        try {
          const result = await api.post('/bazi/calculate', {
            year: form.value.birth_year,
            month: form.value.birth_month,
            day: form.value.birth_day,
            hour: form.value.birth_hour,
            gender: form.value.gender,
          })
          baziPreview.value = {
            year_pillar: result.year_pillar,
            month_pillar: result.month_pillar,
            day_pillar: result.day_pillar,
            hour_pillar: result.hour_pillar,
          }
        } catch (e) {
          // ignore preview errors
        }
      }
    }, 500)
  },
  { immediate: true }
)

const handleSubmit = async () => {
  if (!userStore.isLoggedIn) {
    alert('请先登录')
    navigateTo('/login')
    return
  }
  submitting.value = true
  try {
    const tags = form.value.tags
      .filter(t => t.value && (t.name || t.customName))
      .map(t => ({
        name: t.name === '__custom' ? t.customName : t.name,
        value: t.value,
      }))

    const data = {
      ...form.value,
      tags,
    }
    delete data.tags

    const result = await api.post('/cases', { ...data, tags })
    navigateTo(`/cases/${result.id}`)
  } catch (e) {
    alert(e.message || '保存失败')
  } finally {
    submitting.value = false
  }
}
</script>
