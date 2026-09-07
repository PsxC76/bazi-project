<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 font-serif">我的案例</h1>
        <p class="text-gray-500 mt-1">管理您的八字命理案例</p>
      </div>
      <NuxtLink to="/cases/new" class="btn-primary flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        新建案例
      </NuxtLink>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
      <div class="grid md:grid-cols-4 gap-4">
        <div>
          <input v-model="filters.keyword" type="text" class="form-input" placeholder="搜索姓名或断语..." @input="debouncedSearch">
        </div>
        <div>
          <select v-model="filters.gender" class="form-input" @change="fetchCases">
            <option value="">全部性别</option>
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>
        <div>
          <input v-model="filters.tagName" type="text" class="form-input" placeholder="标签名称（如：职业）" @input="debouncedSearch">
        </div>
        <div>
          <input v-model="filters.tagValue" type="text" class="form-input" placeholder="标签值（如：教师）" @input="debouncedSearch">
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
      <p class="text-gray-500 mt-3">加载中...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="cases.length === 0" class="text-center py-16 bg-white rounded-2xl border border-gray-100">
      <div class="text-6xl mb-4">📚</div>
      <h3 class="text-xl font-bold text-gray-900 mb-2">暂无案例</h3>
      <p class="text-gray-500 mb-6">点击下方按钮创建您的第一个八字案例</p>
      <NuxtLink to="/cases/new" class="btn-primary">创建案例</NuxtLink>
    </div>

    <!-- Case List -->
    <div v-else class="space-y-4">
      <NuxtLink
        v-for="caseItem in cases"
        :key="caseItem.id"
        :to="`/cases/${caseItem.id}`"
        class="block bg-white rounded-2xl shadow-sm border border-gray-100 p-6 card-hover"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="text-lg font-bold text-gray-900">{{ caseItem.name }}</h3>
              <span class="px-2 py-0.5 text-xs rounded-full" :class="caseItem.gender === '男' ? 'bg-blue-50 text-blue-600' : 'bg-pink-50 text-pink-600'">
                {{ caseItem.gender }}
              </span>
              <span v-if="caseItem.is_public" class="px-2 py-0.5 text-xs rounded-full bg-primary-50 text-primary-600">公开</span>
            </div>

            <div class="text-sm text-gray-500 mb-3">
              出生：{{ caseItem.birth_year }}年{{ caseItem.birth_month }}月{{ caseItem.birth_day }}日
              <template v-if="caseItem.birth_hour !== null"> {{ caseItem.birth_hour }}时</template>
            </div>

            <!-- Bazi Preview -->
            <div v-if="caseItem.bazi_result" class="flex gap-2 mb-3">
              <div v-for="(pillar, key) in getDisplayPillars(caseItem.bazi_result)" :key="key" class="px-3 py-1.5 bg-primary-50 rounded-lg text-center">
                <div class="text-xs text-gray-400">{{ pillarLabels[key] }}</div>
                <div class="font-bold text-primary-800 font-serif">{{ pillar.stem }}{{ pillar.branch }}</div>
              </div>
            </div>

            <div v-if="caseItem.verdict" class="text-sm text-gray-600 line-clamp-2">{{ caseItem.verdict }}</div>

            <!-- Tags -->
            <div v-if="caseItem.tags.length" class="flex flex-wrap gap-2 mt-3">
              <span v-for="tag in caseItem.tags" :key="tag.id" class="tag-item">
                {{ tag.name }}: {{ tag.value }}
              </span>
            </div>
          </div>

          <div class="text-sm text-gray-400">
            {{ formatDate(caseItem.created_at) }}
          </div>
        </div>
      </NuxtLink>

      <!-- Pagination -->
      <div v-if="total > pageSize" class="flex justify-center gap-2 mt-8">
        <button
          v-for="p in totalPages"
          :key="p"
          @click="page = p; fetchCases()"
          class="w-10 h-10 rounded-lg text-sm font-medium transition-colors"
          :class="p === page ? 'bg-primary-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'"
        >
          {{ p }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/utils/api'

useHead({ title: '我的案例 - 八字命理案例库' })

const api = useApi()
const loading = ref(true)
const cases = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20

const filters = ref({
  keyword: '',
  gender: '',
  tagName: '',
  tagValue: '',
})

const totalPages = computed(() => Math.ceil(total.value / pageSize))

const pillarLabels = {
  year_pillar: '年柱',
  month_pillar: '月柱',
  day_pillar: '日柱',
  hour_pillar: '时柱',
}

const getDisplayPillars = (bazi) => {
  const result = {}
  if (bazi.year_pillar) result.year_pillar = bazi.year_pillar
  if (bazi.month_pillar) result.month_pillar = bazi.month_pillar
  if (bazi.day_pillar) result.day_pillar = bazi.day_pillar
  if (bazi.hour_pillar) result.hour_pillar = bazi.hour_pillar
  return result
}

const fetchCases = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.set('page', page.value)
    params.set('page_size', pageSize)
    if (filters.value.keyword) params.set('keyword', filters.value.keyword)
    if (filters.value.gender) params.set('gender', filters.value.gender)
    if (filters.value.tagName) params.set('tag_name', filters.value.tagName)
    if (filters.value.tagValue) params.set('tag_value', filters.value.tagValue)

    const data = await api.get(`/cases?${params.toString()}`)
    cases.value = data.items
    total.value = data.total
  } catch (e) {
    console.error('Failed to fetch cases:', e)
  } finally {
    loading.value = false
  }
}

let searchTimer = null
const debouncedSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    fetchCases()
  }, 300)
}

const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

onMounted(fetchCases)
</script>
