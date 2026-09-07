<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <NuxtLink :to="`/cases/${route.params.id}`" class="text-sm text-gray-500 hover:text-primary-600 flex items-center gap-1 mb-6">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      返回案例详情
    </NuxtLink>

    <h1 class="text-3xl font-bold text-gray-900 font-serif mb-8">编辑案例</h1>

    <div v-if="loading" class="text-center py-16">
      <div class="inline-block w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
    </div>

    <form v-else @submit.prevent="handleSubmit" class="space-y-8">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-lg font-bold text-gray-900 mb-6">基本信息</h2>
        <div class="grid md:grid-cols-2 gap-6">
          <div>
            <label class="form-label">姓名</label>
            <input v-model="form.name" type="text" class="form-input" required>
          </div>
          <div>
            <label class="form-label">性别</label>
            <div class="flex gap-4 mt-1">
              <label class="flex items-center gap-2"><input type="radio" v-model="form.gender" value="男"> 男</label>
              <label class="flex items-center gap-2"><input type="radio" v-model="form.gender" value="女"> 女</label>
            </div>
          </div>
          <div>
            <label class="form-label">出生地点</label>
            <input v-model="form.birth_place" type="text" class="form-input">
          </div>
          <div>
            <label class="form-label">是否公开</label>
            <label class="flex items-center gap-2 mt-1">
              <input type="checkbox" v-model="form.is_public" class="w-4 h-4 text-primary-600 rounded">
              <span class="text-sm">公开此案例</span>
            </label>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-lg font-bold text-gray-900 mb-6">出生时间</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div><label class="form-label">年</label><input v-model.number="form.birth_year" type="number" class="form-input" required></div>
          <div><label class="form-label">月</label><select v-model.number="form.birth_month" class="form-input" required><option v-for="m in 12" :key="m" :value="m">{{ m }}</option></select></div>
          <div><label class="form-label">日</label><select v-model.number="form.birth_day" class="form-input" required><option v-for="d in 31" :key="d" :value="d">{{ d }}</option></select></div>
          <div><label class="form-label">时</label><select v-model="form.birth_hour" class="form-input"><option :value="null">未知</option><option v-for="h in hours" :key="h.value" :value="h.value">{{ h.label }}</option></select></div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-gray-900">标签</h2>
          <button type="button" @click="addTag" class="text-sm text-primary-600">+ 添加标签</button>
        </div>
        <div class="space-y-4">
          <div v-for="(tag, index) in form.tags" :key="index" class="flex items-center gap-3">
            <select v-model="tag.name" class="form-input w-40">
              <option value="">选择</option>
              <option v-for="n in tagNames" :key="n" :value="n">{{ n }}</option>
              <option value="__custom">自定义</option>
            </select>
            <input v-if="tag.name === '__custom'" v-model="tag.customName" class="form-input w-40" placeholder="标签名">
            <input v-model="tag.value" class="form-input flex-1" placeholder="值">
            <button type="button" @click="form.tags.splice(index, 1)" class="text-red-400 hover:text-red-600">✕</button>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-lg font-bold text-gray-900 mb-6">断语与备注</h2>
        <div class="space-y-6">
          <div><label class="form-label">断语</label><textarea v-model="form.verdict" class="form-input" rows="3"></textarea></div>
          <div><label class="form-label">备注</label><textarea v-model="form.notes" class="form-input" rows="3"></textarea></div>
        </div>
      </div>

      <div class="flex justify-end gap-4">
        <NuxtLink :to="`/cases/${route.params.id}`" class="btn-secondary">取消</NuxtLink>
        <button type="submit" class="btn-primary px-8" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/utils/api'

useHead({ title: '编辑案例 - 八字命理案例库' })
const route = useRoute()
const api = useApi()
const loading = ref(true)
const submitting = ref(false)
const tagNames = ['职业', '学历', '婚姻', '财富', '寿夭', '健康', '性格', '其他']
const hours = [
  { value: 0, label: '子时' }, { value: 1, label: '丑时' }, { value: 3, label: '寅时' },
  { value: 5, label: '卯时' }, { value: 7, label: '辰时' }, { value: 9, label: '巳时' },
  { value: 11, label: '午时' }, { value: 13, label: '未时' }, { value: 15, label: '申时' },
  { value: 17, label: '酉时' }, { value: 19, label: '戌时' }, { value: 21, label: '亥时' },
]

const form = ref({
  name: '', gender: '男', birth_place: '', birth_year: 1990, birth_month: 1, birth_day: 1,
  birth_hour: null, is_public: false, verdict: '', notes: '', tags: [],
})

const addTag = () => form.value.tags.push({ name: '', customName: '', value: '' })

onMounted(async () => {
  try {
    const data = await api.get(`/cases/${route.params.id}`)
    form.value = {
      name: data.name, gender: data.gender, birth_place: data.birth_place || '',
      birth_year: data.birth_year, birth_month: data.birth_month, birth_day: data.birth_day,
      birth_hour: data.birth_hour, is_public: data.is_public, verdict: data.verdict || '',
      notes: data.notes || '',
      tags: data.tags.map(t => ({ name: t.name, customName: '', value: t.value })),
    }
  } catch (e) {
    alert('加载失败'); navigateTo('/cases')
  } finally {
    loading.value = false
  }
})

const handleSubmit = async () => {
  submitting.value = true
  try {
    const tags = form.value.tags.filter(t => t.value && (t.name || t.customName)).map(t => ({
      name: t.name === '__custom' ? t.customName : t.name, value: t.value,
    }))
    await api.put(`/cases/${route.params.id}`, { ...form.value, tags })
    navigateTo(`/cases/${route.params.id}`)
  } catch (e) { alert(e.message || '保存失败') } finally { submitting.value = false }
}
</script>
