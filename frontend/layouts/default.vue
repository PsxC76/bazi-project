<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="sticky top-0 z-50 backdrop-blur-sm" style="background: rgba(25, 25, 40, 0.95);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-14">
          <!-- Logo -->
          <NuxtLink to="/" class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg flex items-center justify-center" style="background: linear-gradient(135deg, #C83C23, #E08D7E);">
              <span class="text-white text-lg font-bold font-serif">命</span>
            </div>
            <div>
              <h1 class="text-base font-bold text-white">八字命理案例库</h1>
            </div>
          </NuxtLink>

          <!-- Navigation -->
          <nav class="hidden md:flex items-center gap-1">
            <NuxtLink
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              class="px-3 py-1.5 rounded text-sm font-medium transition-all"
              :class="$route.path === item.path ? 'bg-white/15 text-white' : 'text-gray-300 hover:text-white hover:bg-white/10'"
            >
              {{ item.label }}
            </NuxtLink>
          </nav>

          <!-- User Actions -->
          <div class="flex items-center gap-3">
            <template v-if="userStore.isLoggedIn">
              <NuxtLink to="/cases/new" class="btn-primary text-sm flex items-center gap-1 py-1.5 px-4">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                新建案例
              </NuxtLink>

              <!-- User Area - 点击跳转个人中心，悬停1s显示菜单 -->
              <div class="relative" ref="menuRef" @mouseenter="startHoverTimer" @mouseleave="cancelHoverTimer">
                <NuxtLink to="/profile" class="flex items-center gap-2 px-2 py-1 rounded transition-colors hover:bg-white/10">
                  <div class="w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-medium overflow-hidden" style="background: linear-gradient(135deg, #C83C23, #E08D7E);">
                    <img v-if="userStore.user?.avatar" :src="userStore.user.avatar" class="w-full h-full object-cover" alt="">
                    <span v-else>{{ avatarLetter }}</span>
                  </div>
                  <span class="text-sm text-gray-200 hidden sm:inline">{{ userStore.user?.nickname || userStore.user?.username || '用户' }}</span>
                </NuxtLink>

                <Transition name="dropdown">
                  <div v-if="showMenu" class="absolute right-0 mt-1 w-48 rounded-lg shadow-lg py-1 z-50" style="background: #FEFCF8; border: 1px solid #E0E0E0;">
                    <NuxtLink to="/profile" class="block px-4 py-2 text-sm hover:bg-gray-50" style="color: #333333;" @click="showMenu = false">
                      个人中心
                    </NuxtLink>
                    <NuxtLink to="/cases" class="block px-4 py-2 text-sm hover:bg-gray-50" style="color: #333333;" @click="showMenu = false">
                      我的案例
                    </NuxtLink>
                    <hr class="my-1" style="border-color: #E0E0E0;">
                    <button @click="handleLogout" class="w-full text-left px-4 py-2 text-sm" style="color: #C83C23;">
                      退出登录
                    </button>
                  </div>
                </Transition>
              </div>
            </template>
            <template v-else>
              <NuxtLink to="/login" class="text-sm font-medium text-gray-300 hover:text-white">登录</NuxtLink>
              <NuxtLink to="/register" class="btn-primary text-sm py-1.5 px-4">注册</NuxtLink>
            </template>
          </div>

          <!-- Mobile Menu -->
          <button @click="showMobileMenu = !showMobileMenu" class="md:hidden p-2 rounded hover:bg-white/10">
            <svg class="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <Transition name="slide">
          <div v-if="showMobileMenu" class="md:hidden py-3 border-t" style="border-color: rgba(255,255,255,0.1);">
            <NuxtLink v-for="item in navItems" :key="item.path" :to="item.path"
              class="block px-3 py-2 rounded text-sm font-medium"
              :class="$route.path === item.path ? 'bg-white/15 text-white' : 'text-gray-300'"
              @click="showMobileMenu = false">
              {{ item.label }}
            </NuxtLink>
          </div>
        </Transition>
      </div>
    </header>

    <!-- Main -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="py-6 mt-auto" style="background: #191928; border-top: 1px solid rgba(255,255,255,0.05);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm" style="color: #666666;">
        <p>八字命理案例库 &copy; {{ new Date().getFullYear() }}</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
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

const avatarLetter = computed(() => {
  const u = userStore.user
  if (!u) return 'U'
  return (u.nickname || u.username || 'U')[0].toUpperCase()
})

// 悬停 1s 后显示下拉菜单
const startHoverTimer = () => {
  hoverTimer = setTimeout(() => { showMenu.value = true }, 1000)
}
const cancelHoverTimer = () => {
  clearTimeout(hoverTimer)
  showMenu.value = false
}

const handleLogout = () => {
  userStore.logout()
  showMenu.value = false
  navigateTo('/login')
}

const handleClickOutside = (e) => {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    showMenu.value = false
  }
}

onMounted(() => { document.addEventListener('click', handleClickOutside) })
onUnmounted(() => { document.removeEventListener('click', handleClickOutside) })
</script>

<style scoped>
.dropdown-enter-active, .dropdown-leave-active { transition: all 0.2s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: translateY(-8px) scale(0.95); }
.slide-enter-active, .slide-leave-active { transition: all 0.3s ease; }
.slide-enter-from, .slide-leave-to { opacity: 0; max-height: 0; overflow: hidden; }
</style>
