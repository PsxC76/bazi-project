# 部署指南

## 本地运行（推荐先用这种方式看效果）

### 前置要求
1. 安装 Docker Desktop: https://www.docker.com/products/docker-desktop/
2. 安装 Python 3.10+: https://www.python.org/downloads/
3. 安装 Node.js 18+: https://nodejs.org/

### 步骤

#### 1. 启动数据库和Redis
```bash
cd bazi-project
docker-compose up -d db redis
```

#### 2. 启动后端
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

启动后访问 http://localhost:8000/docs 查看API文档

#### 3. 启动前端（新终端）
```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

### 创建管理员账号

注册第一个账号后，手动在数据库中将其设为管理员：

```bash
# 进入PostgreSQL容器
docker exec -it bazi-db psql -U bazi -d bazi_db

# 设置第一个用户为管理员
UPDATE users SET is_admin = true WHERE id = 1;
```

---

## 服务器部署

### 推荐服务器配置
- **入门**: 2核4G内存，50G硬盘（约¥100-200/月）
- **推荐**: 4核8G内存，100G硬盘（约¥300-500/月）

### 推荐云服务商
1. **阿里云ECS**: https://www.aliyun.com/product/ecs
2. **腾讯云轻量**: https://cloud.tencent.com/product/lighthouse
3. **华为云**: https://www.huaweicloud.com/product/ecs.html

### Docker一键部署

```bash
# 1. 安装Docker
curl -fsSL https://get.docker.com | sh

# 2. 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. 上传项目文件到服务器
scp -r bazi-project user@server:/opt/

# 4. 修改配置
cd /opt/bazi-project
# 编辑 .env 文件，修改 SECRET_KEY
# 编辑 docker-compose.yml，修改数据库密码

# 5. 启动
docker-compose up -d

# 6. 查看状态
docker-compose ps
docker-compose logs -f
```

### Nginx反向代理（已有域名时）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### HTTPS配置（推荐）

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com
```

---

## 企业资质与支付接入

### 注册企业流程（简要）
1. **核名**: 到工商局或网上核名
2. **提交材料**: 身份证、租赁合同、章程等
3. **领取执照**: 约3-5个工作日
4. **刻章**: 公章、财务章、法人章
5. **银行开户**: 开对公账户
6. **税务登记**: 到税务局登记

**个体工商户**更简单，几百块即可办理。

### 接入支付
- **微信支付**: https://pay.weixin.qq.com/ (需企业资质)
- **支付宝**: https://open.alipay.com/ (需企业资质)
- **第三方聚合支付**: Payjs、虎皮椒等（门槛较低）

建议先免费运营，积累用户后再办理企业资质接入支付。

---

## 域名购买

推荐域名注册商：
- 阿里云万网: https://wanwang.aliyun.com/
- 腾讯云DNSPod: https://cloud.tencent.com/product/dns
- Namesilo: https://www.namesilo.com/ (国外，便宜)

`.com` 域名约 ¥55-75/年
