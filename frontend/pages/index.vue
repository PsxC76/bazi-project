<template>
  <div>
    <!-- Hero -->
    <section class="relative overflow-hidden" style="background: linear-gradient(135deg, #191928 0%, #2A2A40 50%, #191928 100%);">
      <div class="absolute inset-0 opacity-5">
        <div class="absolute top-10 left-10 w-64 h-64 rounded-full" style="background: #C83C23; filter: blur(80px);"></div>
        <div class="absolute bottom-10 right-10 w-80 h-80 rounded-full" style="background: #2E8B57; filter: blur(80px);"></div>
      </div>
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28">
        <div class="text-center max-w-2xl mx-auto">
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm mb-6" style="background: rgba(200,60,35,0.15); color: #E08D7E;">
            <span class="w-2 h-2 rounded-full animate-pulse" style="background: #C83C23;"></span>
            专业八字命理平台
          </div>
          <h1 class="text-4xl lg:text-5xl font-bold font-serif mb-6 leading-tight text-white">
            八字命理<span style="color: #E08D7E;">案例库</span>
          </h1>
          <p class="text-lg leading-relaxed mb-8" style="color: #999999;">
            专业的八字排盘与案例管理系统，支持四柱八字、十神、大运分析，帮助您系统化管理命理案例
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <NuxtLink to="/bazi" class="btn-primary px-8 py-3 text-base text-center">
              开始排盘
            </NuxtLink>
            <NuxtLink to="/cases" class="px-8 py-3 rounded-lg font-medium text-center transition-all text-white" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);">
              案例库
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-16" style="background: #FAF4E3;">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-2xl font-bold font-serif" style="color: #191928;">核心功能</h2>
          <p class="mt-2" style="color: #666666;">集成八字排盘、案例管理、条件筛选等功能</p>
        </div>
        <div class="grid md:grid-cols-3 gap-6">
          <div v-for="f in features" :key="f.title" class="card-hover p-6" style="background: #FEFCF8; border: 1px solid #E0E0E0;">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center text-xl mb-4" style="background: #FDF2F0;">
              {{ f.icon }}
            </div>
            <h3 class="text-lg font-bold mb-2" style="color: #191928;">{{ f.title }}</h3>
            <p style="color: #666666; line-height: 1.8;">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
useHead({ title: '八字命理案例库 - 专业排盘与案例管理平台' })

const features = [
  { icon: '🔮', title: '智能排盘', desc: '自动计算四柱八字、十神、大运、流年，准确高效' },
  { icon: '📚', title: '案例管理', desc: '系统化管理命理案例，支持标签、断语、备注' },
  { icon: '🔍', title: '条件筛选', desc: '按姓名、性别、职业、学历等多维度筛选' },
]
</script>
