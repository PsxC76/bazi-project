<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900 font-serif">公开案例</h1>
      <p class="text-gray-500 mt-1">浏览所有用户公开分享的八字案例</p>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
      <div class="grid md:grid-cols-3 gap-4">
        <input v-model="filters.keyword" type="text" class="form-input" placeholder="搜索姓名或断语..." @input="debouncedSearch">
        <select v-model="filters.gender" class="form-input" @change="fetchCases">
          <option value="">全部性别</option>
          <option value="男">男</option>
          <option value="女">女</option>
        </select>
        <button @click="fetchCases" class="btn-primary">搜索</button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
    </div>

    <div v-else-if="cases.length === 0" class="text-center py-16 bg-white rounded-2xl border border-gray-100">
      <div class="text-6xl mb-4">🌍</div>
      <h3 class="text-xl font-bold text-gray-900 mb-2">暂无公开案例</h3>
      <p class="text-gray-500">还没有用户公开分享案例</p>
    </div>

    <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="c in cases" :key="c.id" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 card-hover">
        <div class="flex items-center gap-3 mb-3">
          <h3 class="text-lg font-bold text-gray-900">{{ c.name }}</h3>
          <span class="px-2 py-0.5 text-xs rounded-full" :class="c.gender === '男' ? 'bg-blue-50 text-blue-600' : 'bg-pink-50 text-pink-600'">{{ c.gender }}</span>
        </div>

        <div class="text-sm text-gray-500 mb-3">
          {{ c.birth_year }}年{{ c.birth_month }}月{{ c.birth_day }}日
          <template v-if="c.birth_hour !== null"> {{ c.birth_hour }}时</template>
        </div>

        <div v-if="c.bazi_result" class="flex gap-2 mb-3">
          <div v-for="key in ['year_pillar', 'month_pillar', 'day_pillar', 'hour_pillar']" :key="key" v-if="c.bazi_result[key]" class="px-2 py-1 bg-primary-50 rounded text-center">
            <div class="font-bold text-primary-800 font-serif text-sm">{{ c.bazi_result[key].stem }}{{ c.bazi_result[key].branch }}</div>
          </div>
        </div>

        <div v-if="c.verdict" class="text-sm text-gray-600 line-clamp-2 mb-3">{{ c.verdict }}</div>

        <div v-if="c.tags.length" class="flex flex-wrap gap-1">
          <span v-for="tag in c.tags" :key="tag.id" class="tag-item text-xs">{{ tag.name }}: {{ tag.value }}</span>
        </div>
      </div>
    </div>

    <div v-if="total > pageSize" class="flex justify-center gap-2 mt-8">
      <button v-for="p in totalPages" :key="p" @click="page = p; fetchCases()" class="w-10 h-10 rounded-lg text-sm font-medium" :class="p === page ? 'bg-primary-600 text-white' : 'bg-white text-gray-600 border border-gray-200'">{{ p }}</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/utils/api'

useHead({ title: '公开案例 - 八字命理案例库' })
const api = useApi()
const loading = ref(true)
const cases = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 12
const filters = ref({ keyword: '', gender: '' })
const totalPages = computed(() => Math.ceil(total.value / pageSize))

const fetchCases = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.set('page', page.value)
    params.set('page_size', pageSize)
    params.set('is_public', 'true')
    if (filters.value.keyword) params.set('keyword', filters.value.keyword)
    if (filters.value.gender) params.set('gender', filters.value.gender)
    const data = await api.get(`/cases?${params.toString()}`)
    cases.value = data.items
    total.value = data.total
  } catch (e) { console.error(e) } finally { loading.value = false }
}

let timer = null
const debouncedSearch = () => { clearTimeout(timer); timer = setTimeout(() => { page.value = 1; fetchCases() }, 300) }

onMounted(fetchCases)
</script>
