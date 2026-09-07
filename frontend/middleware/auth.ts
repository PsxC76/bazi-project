export default defineNuxtRouteMiddleware((to) => {
  // 需要登录的页面
  const protectedRoutes = ['/cases/new', '/cases/[id]/edit', '/profile']

  const isProtected = protectedRoutes.some((route) => {
    // 支持动态路由匹配，如 /cases/[id]/edit
    const pattern = route.replace(/\[.*?\]/g, '[^/]+')
    const regex = new RegExp(`^${pattern}$`)
    return regex.test(to.path) || to.path.startsWith(route.replace(/\[.*?\]/g, ''))
  })

  // /cases/new 需要登录
  if (to.path === '/cases/new') {
    if (import.meta.client) {
      const token = localStorage.getItem('token')
      if (!token) {
        return navigateTo('/login')
      }
    }
  }

  // /cases/:id/edit 需要登录
  if (to.path.match(/^\/cases\/\d+\/edit$/)) {
    if (import.meta.client) {
      const token = localStorage.getItem('token')
      if (!token) {
        return navigateTo('/login')
      }
    }
  }

  // /profile 需要登录
  if (to.path === '/profile') {
    if (import.meta.client) {
      const token = localStorage.getItem('token')
      if (!token) {
        return navigateTo('/login')
      }
    }
  }
})
