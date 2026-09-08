<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white border-b border-gray-100 sticky top-0 z-50 backdrop-blur-sm bg-white/90">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <NuxtLink to="/" class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl flex items-center justify-center text-2xl select-none" style="line-height:1">
              <span>🔮</span>
            </div>
            <div>
              <h1 class="text-lg font-bold text-gray-900">八字命理案例库</h1>
              <p class="text-xs text-gray-400 -mt-1">专业排盘 · 案例管理</p>
            </div>
          </NuxtLink>

          <!-- Navigation -->
          <nav class="hidden md:flex items-center gap-1">
            <NuxtLink
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
              :class="$route.path === item.path ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:text-primary-600 hover:bg-gray-50'"
            >
              {{ item.label }}
            </NuxtLink>
          </nav>

          <!-- User Actions -->
          <div class="flex items-center gap-3">
            <template v-if="userStore.isLoggedIn">
              <NuxtLink to="/cases/new" class="btn-primary text-sm flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                新建案例
              </NuxtLink>

              <!-- User Menu -->
              <div
                class="relative"
                ref="menuRef"
                @mouseenter="handleMouseEnter"
                @mouseleave="handleMouseLeave"
              >
                <button
                  @click="navigateTo('/profile')"
                  class="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white text-sm font-medium">
                    {{ userStore.user?.nickname?.[0] || userStore.user?.username?.[0] || 'U' }}
                  </div>
                  <span class="text-sm text-gray-700 hidden sm:inline">{{ userStore.user?.nickname || userStore.user?.username || '' }}</span>
                </button>

                <Transition name="dropdown">
                  <div
                    v-if="showMenu"
                    class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 z-50"
                    @mouseenter="handleMenuMouseEnter"
                    @mouseleave="handleMenuMouseLeave"
                  >
                    <NuxtLink to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="showMenu = false">
                      个人中心
                    </NuxtLink>
                    <NuxtLink to="/cases" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="showMenu = false">
                      我的案例
                    </NuxtLink>
                    <hr class="my-1 border-gray-100">
                    <button @click="handleLogout" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50">
                      退出登录
                    </button>
                  </div>
                </Transition>
              </div>
            </template>
            <template v-else>
              <NuxtLink to="/login" class="text-sm font-medium text-gray-600 hover:text-primary-600">登录</NuxtLink>
              <NuxtLink to="/register" class="btn-primary text-sm">注册</NuxtLink>
            </template>
          </div>

          <!-- Mobile Menu Button -->
          <button @click="showMobileMenu = !showMobileMenu" class="md:hidden p-2 rounded-lg hover:bg-gray-100">
            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Mobile Menu -->
        <Transition name="slide">
          <div v-if="showMobileMenu" class="md:hidden py-4 border-t border-gray-100">
            <NuxtLink
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              class="block px-4 py-2 rounded-lg text-sm font-medium"
              :class="$route.path === item.path ? 'bg-primary-50 text-primary-700' : 'text-gray-600'"
              @click="showMobileMenu = false"
            >
              {{ item.label }}
            </NuxtLink>
          </div>
        </Transition>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-100 py-8 mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center text-sm text-gray-400">
          <p>八字命理案例库 &copy; {{ new Date().getFullYear() }}</p>
          <p class="mt-1">专业八字排盘与案例管理平台</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '~/stores/user'

const userStore = useUserStore()

const showMenu = ref(false)
const showMobileMenu = ref(false)
const menuRef = ref(null)
let hoverTimer = null

const navItems = [
  { label: '首页', path: '/' },
  { label: '排盘', path: '/bazi' },
  { label: '案例库', path: '/cases' },
  { label: '公开案例', path: '/public' },
]

const handleLogout = () => {
  userStore.logout()
  showMenu.value = false
  navigateTo('/login')
}

// 悬停1秒显示菜单
const handleMouseEnter = () => {
  clearTimeout(hoverTimer)
  hoverTimer = setTimeout(() => {
    showMenu.value = true
  }, 1000)
}

const handleMouseLeave = () => {
  clearTimeout(hoverTimer)
  hoverTimer = setTimeout(() => {
    showMenu.value = false
  }, 300)
}

// 下拉菜单区域的鼠标事件
const handleMenuMouseEnter = () => {
  clearTimeout(hoverTimer)
}

const handleMenuMouseLeave = () => {
  hoverTimer = setTimeout(() => {
    showMenu.value = false
  }, 300)
}

// Close menu when clicking outside
const handleClickOutside = (e) => {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    showMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  clearTimeout(hoverTimer)
})
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.95);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}
</style>
