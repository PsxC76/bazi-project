import type { Config } from 'tailwindcss'

export default {
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      colors: {
        // 基础色 (60%)
        cream: {
          50: '#FEFCF8',
          100: '#FAF4E3',
          200: '#F5EACC',
          300: '#EDE0B5',
        },
        // 辅助色 (30%)
        ink: {
          50: '#F0F0F0',
          100: '#E0E0E0',
          200: '#CCCCCC',
          300: '#888888',
          400: '#666666',
          500: '#333333',
          600: '#191928',
          700: '#111122',
          800: '#0A0A15',
        },
        // 强调色 (10%)
        vermillion: {
          50: '#FDF2F0',
          100: '#F9DDD8',
          200: '#F0B5AB',
          300: '#E08D7E',
          400: '#D46551',
          500: '#C83C23',
          600: '#A0301C',
          700: '#782415',
          800: '#50180E',
        },
        jade: {
          50: '#EFF8F3',
          100: '#D0EDDB',
          200: '#A1DBB7',
          300: '#72C993',
          400: '#43B76F',
          500: '#2E8B57',
          600: '#256F46',
          700: '#1C5335',
          800: '#133723',
        },
        // 保留主色兼容
        primary: {
          50: '#EFF8F3',
          100: '#D0EDDB',
          200: '#A1DBB7',
          300: '#72C993',
          400: '#43B76F',
          500: '#2E8B57',
          600: '#256F46',
          700: '#1C5335',
          800: '#133723',
          900: '#0A1F14',
        },
      },
      fontFamily: {
        sans: ['"PingFang SC"', '"Noto Sans SC"', '"Microsoft YaHei"', 'sans-serif'],
        serif: ['"Noto Serif SC"', '"Source Han Serif SC"', '"SimSun"', 'serif'],
        mono: ['"Consolas"', '"Menlo"', '"Monaco"', 'monospace'],
      },
    },
  },
  plugins: [],
} satisfies Config
