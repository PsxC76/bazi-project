<template>
  <div>
    <!-- Hero Section -->
    <section class="relative overflow-hidden bg-gradient-to-br from-primary-900 via-primary-800 to-primary-950 text-white">
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-20 left-20 w-72 h-72 bg-primary-400 rounded-full filter blur-3xl"></div>
        <div class="absolute bottom-20 right-20 w-96 h-96 bg-accent-400 rounded-full filter blur-3xl"></div>
      </div>

      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
        <div class="text-center max-w-3xl mx-auto">
          <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-white/10 rounded-full text-sm mb-8 backdrop-blur-sm">
            <span class="w-2 h-2 bg-primary-400 rounded-full animate-pulse"></span>
            专业八字命理平台
          </div>

          <h1 class="text-4xl lg:text-6xl font-bold font-serif mb-6 leading-tight">
            八字命理<span class="text-primary-300">案例库</span>
          </h1>

          <p class="text-lg lg:text-xl text-primary-100 mb-10 leading-relaxed">
            专业的八字排盘与案例管理系统，支持四柱八字、十神、大运分析，
            <br class="hidden lg:block">
            帮助您系统化管理命理案例，提升研究效率
          </p>

          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <NuxtLink to="/bazi" class="px-8 py-3.5 bg-white text-primary-700 rounded-xl font-medium hover:bg-primary-50 transition-all shadow-lg shadow-primary-900/30 text-center">
              开始排盘
            </NuxtLink>
            <NuxtLink to="/cases" class="px-8 py-3.5 bg-white/10 text-white rounded-xl font-medium hover:bg-white/20 transition-all backdrop-blur-sm border border-white/20 text-center">
              案例库
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-gray-900 font-serif mb-4">核心功能</h2>
          <p class="text-gray-500 max-w-2xl mx-auto">集成八字排盘、案例管理、条件筛选等功能，为命理研究者提供一站式工具</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div v-for="feature in features" :key="feature.title" class="card-hover p-8 rounded-2xl bg-gradient-to-br from-gray-50 to-white border border-gray-100">
            <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-50 flex items-center justify-center text-2xl mb-6">
              {{ feature.icon }}
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">{{ feature.title }}</h3>
            <p class="text-gray-500 leading-relaxed">{{ feature.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-20 bg-gradient-to-br from-primary-50 to-accent-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-bold text-gray-900 font-serif mb-4">开始使用</h2>
        <p class="text-gray-500 mb-8">注册账号，立即体验专业八字排盘与案例管理功能</p>
        <NuxtLink to="/register" class="inline-block px-8 py-3.5 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-xl font-medium hover:from-primary-700 hover:to-primary-800 transition-all shadow-lg shadow-primary-600/20">
          免费注册
        </NuxtLink>
      </div>
    </section>
  </div>
</template>

<script setup>
useHead({
  title: '八字命理案例库 - 专业排盘与案例管理平台',
})

const features = [
  {
    icon: '🔮',
    title: '智能排盘',
    desc: '自动计算四柱八字、十神、大运、流年，准确高效，省去手动查万年历的繁琐',
  },
  {
    icon: '📚',
    title: '案例管理',
    desc: '系统化管理您的命理案例，支持添加标签、断语、备注，构建个人知识库',
  },
  {
    icon: '🔍',
    title: '条件筛选',
    desc: '按姓名、性别、职业、学历、婚姻等多维度筛选，快速定位目标案例',
  },
]
</script>
