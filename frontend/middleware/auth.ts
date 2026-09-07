export default defineNuxtRouteMiddleware((to) => {
  if (!import.meta.client) return

  const protectedPaths = ['/cases/new', '/profile']
  const isEditPage = /^\/cases\/\d+\/edit$/.test(to.path)
  const needAuth = protectedPaths.includes(to.path) || isEditPage

  if (needAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      return navigateTo('/login')
    }
  }
})
