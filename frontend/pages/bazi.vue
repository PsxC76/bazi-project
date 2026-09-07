<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900 font-serif">八字排盘</h1>
      <p class="text-gray-500 mt-2">输入出生信息，自动计算四柱八字、十神、大运</p>
    </div>

    <!-- Input Form -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8 mb-8">
      <form @submit.prevent="handleCalculate" class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="md:col-span-2 lg:col-span-4">
          <div class="flex items-center gap-4">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="radio" v-model="form.gender" value="男" class="w-4 h-4 text-primary-600">
              <span class="text-sm font-medium text-gray-700">男</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="radio" v-model="form.gender" value="女" class="w-4 h-4 text-primary-600">
              <span class="text-sm font-medium text-gray-700">女</span>
            </label>
          </div>
        </div>

        <div>
          <label class="form-label">出生年份</label>
          <input v-model.number="form.year" type="number" class="form-input" placeholder="如 1990" required min="1900" max="2100">
        </div>

        <div>
          <label class="form-label">月份</label>
          <select v-model.number="form.month" class="form-input" required>
            <option v-for="m in 12" :key="m" :value="m">{{ m }}月</option>
          </select>
        </div>

        <div>
          <label class="form-label">日期</label>
          <select v-model.number="form.day" class="form-input" required>
            <option v-for="d in 31" :key="d" :value="d">{{ d }}日</option>
          </select>
        </div>

        <div>
          <label class="form-label">时辰（选填）</label>
          <select v-model="form.hour" class="form-input">
            <option :value="null">未知</option>
            <option v-for="h in hours" :key="h.value" :value="h.value">{{ h.label }}</option>
          </select>
        </div>

        <div class="md:col-span-2 lg:col-span-4">
          <button type="submit" class="btn-primary px-8 py-3 text-base" :disabled="loading">
            {{ loading ? '计算中...' : '开始排盘' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Result -->
    <div v-if="result" class="space-y-8">
      <!-- Four Pillars -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 font-serif">四柱八字</h2>

        <div class="grid grid-cols-4 gap-4 lg:gap-8 max-w-2xl mx-auto">
          <!-- Year Pillar -->
          <div class="bazi-pillar">
            <div class="text-xs text-gray-400 mb-2">年柱</div>
            <div class="stem text-2xl">{{ result.year_pillar.stem }}</div>
            <div class="branch text-2xl">{{ result.year_pillar.branch }}</div>
            <div class="element">{{ result.year_pillar.stem_element }}{{ result.year_pillar.branch_element }}</div>
            <div class="ten-god">{{ result.ten_gods.year }}</div>
          </div>

          <!-- Month Pillar -->
          <div class="bazi-pillar">
            <div class="text-xs text-gray-400 mb-2">月柱</div>
            <div class="stem text-2xl">{{ result.month_pillar.stem }}</div>
            <div class="branch text-2xl">{{ result.month_pillar.branch }}</div>
            <div class="element">{{ result.month_pillar.stem_element }}{{ result.month_pillar.branch_element }}</div>
            <div class="ten-god">{{ result.ten_gods.month }}</div>
          </div>

          <!-- Day Pillar -->
          <div class="bazi-pillar ring-2 ring-primary-300">
            <div class="text-xs text-primary-600 font-medium mb-2">日柱</div>
            <div class="stem text-2xl text-primary-700">{{ result.day_pillar.stem }}</div>
            <div class="branch text-2xl">{{ result.day_pillar.branch }}</div>
            <div class="element">{{ result.day_pillar.stem_element }}{{ result.day_pillar.branch_element }}</div>
            <div class="ten-god bg-primary-50 text-primary-700">日主</div>
          </div>

          <!-- Hour Pillar -->
          <div class="bazi-pillar" :class="{ 'opacity-50': !result.hour_pillar }">
            <div class="text-xs text-gray-400 mb-2">时柱</div>
            <template v-if="result.hour_pillar">
              <div class="stem text-2xl">{{ result.hour_pillar.stem }}</div>
              <div class="branch text-2xl">{{ result.hour_pillar.branch }}</div>
              <div class="element">{{ result.hour_pillar.stem_element }}{{ result.hour_pillar.branch_element }}</div>
              <div class="ten-god">{{ result.ten_gods.hour }}</div>
            </template>
            <template v-else>
              <div class="text-gray-300 text-4xl">?</div>
              <div class="text-xs text-gray-400 mt-2">未知</div>
            </template>
          </div>
        </div>

        <!-- Day Master Info -->
        <div class="mt-6 text-center">
          <span class="inline-flex items-center gap-2 px-4 py-2 bg-primary-50 rounded-full text-sm text-primary-700">
            日主：<strong class="text-lg">{{ result.day_master }}</strong>（{{ result.day_master_element }}·{{ result.day_master_yinyang }}）
          </span>
        </div>
      </div>

      <!-- Five Elements -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 font-serif">五行统计</h2>

        <div class="grid grid-cols-5 gap-4 max-w-lg mx-auto">
          <div v-for="(count, element) in result.five_elements" :key="element" class="text-center">
            <div class="text-2xl font-bold font-serif" :class="getElementClass(element)">
              {{ element }}
            </div>
            <div class="text-lg font-medium mt-1" :class="getElementClass(element)">{{ count }}</div>
            <div class="w-full bg-gray-100 rounded-full h-2 mt-2">
              <div
                class="h-2 rounded-full transition-all"
                :class="getElementBgClass(element)"
                :style="{ width: `${(count / 8) * 100}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Hidden Stems -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 font-serif">地支藏干</h2>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="(stems, branch) in result.hidden_stems" :key="branch" class="p-4 bg-gray-50 rounded-xl">
            <div class="text-lg font-bold text-gray-900 font-serif mb-2">{{ branch }}</div>
            <div class="flex flex-wrap gap-1">
              <span v-for="stem in stems" :key="stem" class="px-2 py-0.5 bg-white rounded text-sm border border-gray-200">
                {{ stem }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Major Luck -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 font-serif">大运</h2>

        <div class="flex flex-wrap gap-3">
          <div v-for="luck in result.major_luck" :key="luck.pillar" class="flex-shrink-0 p-4 bg-gradient-to-br from-primary-50 to-white rounded-xl border border-primary-100 min-w-[100px] text-center">
            <div class="text-xs text-gray-400 mb-1">{{ luck.start_age }}-{{ luck.end_age }}岁</div>
            <div class="text-xl font-bold font-serif text-primary-800">{{ luck.pillar }}</div>
            <div class="text-xs text-primary-600 mt-1">{{ luck.ten_god }}</div>
          </div>
        </div>
      </div>

      <!-- Save as Case -->
      <div class="text-center">
        <NuxtLink
          :to="`/cases/new?year=${form.year}&month=${form.month}&day=${form.day}&hour=${form.hour || ''}&gender=${form.gender}`"
          class="inline-flex items-center gap-2 btn-primary px-6 py-3"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          保存为案例
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useApi } from '~/utils/api'

useHead({ title: '八字排盘 - 八字命理案例库' })

const api = useApi()
const loading = ref(false)
const result = ref(null)

const form = ref({
  year: 1990,
  month: 1,
  day: 1,
  hour: null,
  gender: '男',
})

const hours = [
  { value: 0, label: '子时 (23:00-01:00)' },
  { value: 1, label: '丑时 (01:00-03:00)' },
  { value: 3, label: '寅时 (03:00-05:00)' },
  { value: 5, label: '卯时 (05:00-07:00)' },
  { value: 7, label: '辰时 (07:00-09:00)' },
  { value: 9, label: '巳时 (09:00-11:00)' },
  { value: 11, label: '午时 (11:00-13:00)' },
  { value: 13, label: '未时 (13:00-15:00)' },
  { value: 15, label: '申时 (15:00-17:00)' },
  { value: 17, label: '酉时 (17:00-19:00)' },
  { value: 19, label: '戌时 (19:00-21:00)' },
  { value: 21, label: '亥时 (21:00-23:00)' },
]

const handleCalculate = async () => {
  loading.value = true
  try {
    result.value = await api.post('/bazi/calculate', form.value)
  } catch (e) {
    alert(e.message || '计算失败')
  } finally {
    loading.value = false
  }
}

const getElementClass = (element) => {
  const map = {
    '木': 'wx-wood',
    '火': 'wx-fire',
    '土': 'wx-earth',
    '金': 'wx-metal',
    '水': 'wx-water',
  }
  return map[element] || ''
}

const getElementBgClass = (element) => {
  const map = {
    '木': 'bg-green-500',
    '火': 'bg-red-500',
    '土': 'bg-yellow-500',
    '金': 'bg-gray-500',
    '水': 'bg-blue-500',
  }
  return map[element] || 'bg-gray-300'
}
</script>
