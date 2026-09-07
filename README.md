# 八字命理案例库

专业的八字排盘与案例管理系统。

## 功能特性

### 基础功能
- 用户注册、登录、修改密码
- 个人资料管理、头像上传
- 管理员/普通用户权限区分

### 八字排盘
- 四柱八字自动计算（年柱、月柱、日柱、时柱）
- 十神分析
- 大运排列（支持8步大运）
- 五行统计
- 地支藏干

### 案例管理
- 案例的增删改查
- 自定义标签系统（职业、学历、婚姻、财富、寿夭等）
- 多条件筛选搜索
- 公开案例板块（所有人可见）

### UI设计
- 绿色主色调，简洁高级
- 响应式设计，支持移动端
- SSR支持，SEO友好

## 技术栈

| 层面 | 技术 |
|------|------|
| 前端 | Vue 3 + Nuxt 3 + Tailwind CSS |
| 后端 | Python + FastAPI |
| 数据库 | PostgreSQL |
| 缓存 | Redis |
| 部署 | Docker + Nginx |

## 本地开发

### 前置要求
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### 快速启动

```bash
# 1. 克隆项目
cd bazi-project

# 2. 启动数据库
docker-compose up -d db redis

# 3. 安装后端依赖
cd backend
pip install -r requirements.txt

# 4. 启动后端
uvicorn app.main:app --reload --port 8000

# 5. 安装前端依赖（新终端）
cd frontend
npm install

# 6. 启动前端
npm run dev
```

访问 http://localhost:3000

### Docker 一键部署

```bash
docker-compose up -d
```

## API文档

后端启动后访问：http://localhost:8000/docs

## 项目结构

```
bazi-project/
├── backend/                 # Python后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 配置、数据库、安全
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   ├── services/       # 业务逻辑
│   │   └── main.py         # FastAPI入口
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # Vue前端
│   ├── pages/              # 页面
│   ├── components/         # 组件
│   ├── stores/             # Pinia状态
│   ├── layouts/            # 布局
│   ├── utils/              # 工具函数
│   ├── assets/             # 静态资源
│   └── nuxt.config.ts
├── nginx/                   # Nginx配置
├── docker-compose.yml
└── README.md
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| DATABASE_URL | 数据库连接 | postgresql+asyncpg://bazi:bazi123@localhost:5432/bazi_db |
| REDIS_URL | Redis连接 | redis://localhost:6379/0 |
| SECRET_KEY | JWT密钥 | 需要修改 |

## 许可证

私有项目，未经授权禁止使用。
