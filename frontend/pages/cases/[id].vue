<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Back -->
    <NuxtLink to="/cases" class="text-sm text-gray-500 hover:text-primary-600 flex items-center gap-1 mb-6">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      返回案例列表
    </NuxtLink>

    <div v-if="loading" class="text-center py-16">
      <div class="inline-block w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
    </div>

    <div v-else-if="caseData" class="space-y-6">
      <!-- Header -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <h1 class="text-3xl font-bold text-gray-900 font-serif">{{ caseData.name }}</h1>
              <span class="px-3 py-1 text-sm rounded-full" :class="caseData.gender === '男' ? 'bg-blue-50 text-blue-600' : 'bg-pink-50 text-pink-600'">
                {{ caseData.gender }}
              </span>
              <span v-if="caseData.is_public" class="px-3 py-1 text-sm rounded-full bg-primary-50 text-primary-600">公开</span>
            </div>
            <div class="text-gray-500">
              出生：{{ caseData.birth_year }}年{{ caseData.birth_month }}月{{ caseData.birth_day }}日
              <template v-if="caseData.birth_hour !== null"> {{ caseData.birth_hour }}时</template>
              <template v-if="caseData.birth_place"> · {{ caseData.birth_place }}</template>
            </div>
          </div>

          <div class="flex gap-2">
            <NuxtLink :to="`/cases/${caseData.id}/edit`" class="btn-secondary text-sm">编辑</NuxtLink>
            <button @click="handleDelete" class="px-4 py-2 text-sm text-red-600 border border-red-200 rounded-lg hover:bg-red-50">删除</button>
          </div>
        </div>

        <!-- Tags -->
        <div v-if="caseData.tags.length" class="flex flex-wrap gap-2 mt-4">
          <span v-for="tag in caseData.tags" :key="tag.id" class="tag-item">
            {{ tag.name }}: {{ tag.value }}
          </span>
        </div>
      </div>

      <!-- Bazi Chart -->
      <div v-if="caseData.bazi_result" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 font-serif">四柱八字</h2>

        <div class="grid grid-cols-4 gap-4 lg:gap-8 max-w-2xl mx-auto">
          <div v-for="(key, idx) in ['year_pillar', 'month_pillar', 'day_pillar', 'hour_pillar']" :key="key" class="bazi-pillar" :class="{ 'ring-2 ring-primary-300': key === 'day_pillar', 'opacity-50': !caseData.bazi_result[key] }">
            <div class="text-xs mb-2" :class="key === 'day_pillar' ? 'text-primary-600 font-medium' : 'text-gray-400'">
              {{ ['年柱', '月柱', '日柱', '时柱'][idx] }}
            </div>
            <template v-if="caseData.bazi_result[key]">
              <div class="stem text-2xl" :class="{ 'text-primary-700': key === 'day_pillar' }">{{ caseData.bazi_result[key].stem }}</div>
              <div class="branch text-2xl">{{ caseData.bazi_result[key].branch }}</div>
              <div class="element">{{ caseData.bazi_result[key].stem_element }}{{ caseData.bazi_result[key].branch_element }}</div>
              <div class="ten-god" :class="{ 'bg-primary-50 text-primary-700': key === 'day_pillar' }">
                {{ caseData.bazi_result.ten_gods[key.replace('_pillar', '')] || '日主' }}
              </div>
            </template>
            <template v-else>
              <div class="text-gray-300 text-4xl">?</div>
            </template>
          </div>
        </div>

        <!-- Day Master -->
        <div class="mt-6 text-center">
          <span class="inline-flex items-center gap-2 px-4 py-2 bg-primary-50 rounded-full text-sm text-primary-700">
            日主：<strong class="text-lg">{{ caseData.bazi_result.day_master }}</strong>
            （{{ caseData.bazi_result.day_master_element }}·{{ caseData.bazi_result.day_master_yinyang }}）
          </span>
        </div>
      </div>

      <!-- Five Elements -->
      <div v-if="caseData.bazi_result" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 font-serif">五行统计</h2>
        <div class="grid grid-cols-5 gap-4 max-w-lg mx-auto">
          <div v-for="(count, element) in caseData.bazi_result.five_elements" :key="element" class="text-center">
            <div class="text-2xl font-bold font-serif" :class="getElementClass(element)">{{ element }}</div>
            <div class="text-lg font-medium mt-1" :class="getElementClass(element)">{{ count }}</div>
            <div class="w-full bg-gray-100 rounded-full h-2 mt-2">
              <div class="h-2 rounded-full transition-all" :class="getElementBgClass(element)" :style="{ width: `${(count / 8) * 100}%` }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Major Luck -->
      <div v-if="caseData.bazi_result?.major_luck" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 font-serif">大运</h2>
        <div class="flex flex-wrap gap-3">
          <div v-for="luck in caseData.bazi_result.major_luck" :key="luck.pillar" class="flex-shrink-0 p-4 bg-gradient-to-br from-primary-50 to-white rounded-xl border border-primary-100 min-w-[100px] text-center">
            <div class="text-xs text-gray-400 mb-1">{{ luck.start_age }}-{{ luck.end_age }}岁</div>
            <div class="text-xl font-bold font-serif text-primary-800">{{ luck.pillar }}</div>
            <div class="text-xs text-primary-600 mt-1">{{ luck.ten_god }}</div>
          </div>
        </div>
      </div>

      <!-- Verdict & Notes -->
      <div v-if="caseData.verdict || caseData.notes" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 font-serif">断语与备注</h2>
        <div v-if="caseData.verdict" class="mb-4">
          <h3 class="text-sm font-medium text-gray-500 mb-2">断语</h3>
          <p class="text-gray-700 whitespace-pre-wrap">{{ caseData.verdict }}</p>
        </div>
        <div v-if="caseData.notes">
          <h3 class="text-sm font-medium text-gray-500 mb-2">备注</h3>
          <p class="text-gray-700 whitespace-pre-wrap">{{ caseData.notes }}</p>
        </div>
      </div>

      <!-- Timestamps -->
      <div class="text-sm text-gray-400 text-center">
        创建时间：{{ formatDate(caseData.created_at) }} · 更新时间：{{ formatDate(caseData.updated_at) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/utils/api'

const route = useRoute()
const api = useApi()
const loading = ref(true)
const caseData = ref(null)

useHead({ title: '案例详情 - 八字命理案例库' })

const fetchCase = async () => {
  try {
    caseData.value = await api.get(`/cases/${route.params.id}`)
  } catch (e) {
    alert(e.message || '加载失败')
    navigateTo('/cases')
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('确定要删除此案例吗？')) return
  try {
    await api.delete(`/cases/${route.params.id}`)
    navigateTo('/cases')
  } catch (e) {
    alert(e.message || '删除失败')
  }
}

const getElementClass = (element) => {
  const map = { '木': 'wx-wood', '火': 'wx-fire', '土': 'wx-earth', '金': 'wx-metal', '水': 'wx-water' }
  return map[element] || ''
}

const getElementBgClass = (element) => {
  const map = { '木': 'bg-green-500', '火': 'bg-red-500', '土': 'bg-yellow-500', '金': 'bg-gray-500', '水': 'bg-blue-500' }
  return map[element] || 'bg-gray-300'
}

const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

onMounted(fetchCase)
</script>
