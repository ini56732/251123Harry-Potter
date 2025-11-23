# 部署指南

本文档详细说明如何部署"毒舌哲学家"项目。

## 前置要求

- Node.js >= 18.0.0
- pnpm >= 10.4.1
- Git

## 本地开发部署

### 1. 克隆仓库

```bash
git clone https://github.com/danna1013/the-toxic-philosopher.git
cd the-toxic-philosopher
```

### 2. 安装依赖

```bash
pnpm install
```

### 3. 启动开发服务器

```bash
pnpm dev
```

访问 http://localhost:3000

## 生产环境部署

### 方法一：Vercel 部署（推荐）

1. **Fork 仓库**
   - 访问 https://github.com/danna1013/the-toxic-philosopher
   - 点击右上角 "Fork" 按钮

2. **导入到 Vercel**
   - 访问 https://vercel.com
   - 点击 "New Project"
   - 选择刚才 Fork 的仓库
   - 点击 "Import"

3. **配置构建设置**
   - Framework Preset: Vite
   - Build Command: `pnpm build`
   - Output Directory: `dist/public`
   - Install Command: `pnpm install`

4. **配置环境变量（可选）**
   ```
   VITE_AI_API_URL=your_api_url
   VITE_AI_API_KEY=your_api_key
   ```

5. **部署**
   - 点击 "Deploy"
   - 等待构建完成
   - 访问生成的 URL

### 方法二：Netlify 部署

1. **连接仓库**
   - 访问 https://app.netlify.com
   - 点击 "New site from Git"
   - 选择 GitHub 并授权
   - 选择仓库

2. **配置构建设置**
   - Build command: `pnpm build`
   - Publish directory: `dist/public`
   - Base directory: (留空)

3. **部署**
   - 点击 "Deploy site"
   - 等待构建完成

### 方法三：Docker 部署

1. **创建 Dockerfile**

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# 安装 pnpm
RUN npm install -g pnpm@10.4.1

# 复制依赖文件
COPY package.json pnpm-lock.yaml ./

# 安装依赖
RUN pnpm install --frozen-lockfile

# 复制源代码
COPY . .

# 构建项目
RUN pnpm build

# 生产环境镜像
FROM node:18-alpine

WORKDIR /app

RUN npm install -g pnpm@10.4.1

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./
COPY --from=builder /app/pnpm-lock.yaml ./

RUN pnpm install --prod --frozen-lockfile

EXPOSE 3000

CMD ["pnpm", "start"]
```

2. **构建镜像**

```bash
docker build -t toxic-philosopher .
```

3. **运行容器**

```bash
docker run -p 3000:3000 toxic-philosopher
```

### 方法四：传统服务器部署

1. **连接服务器**

```bash
ssh user@your-server.com
```

2. **安装 Node.js 和 pnpm**

```bash
# 安装 Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 pnpm
npm install -g pnpm@10.4.1
```

3. **克隆仓库**

```bash
git clone https://github.com/danna1013/the-toxic-philosopher.git
cd the-toxic-philosopher
```

4. **安装依赖并构建**

```bash
pnpm install
pnpm build
```

5. **使用 PM2 运行（推荐）**

```bash
# 安装 PM2
npm install -g pm2

# 启动应用
pm2 start npm --name "toxic-philosopher" -- start

# 设置开机自启
pm2 startup
pm2 save
```

6. **配置 Nginx 反向代理**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 环境变量配置

### 必需的环境变量

无必需的环境变量，项目可以开箱即用。

### 可选的环境变量

如果需要集成自定义 AI 服务：

```env
VITE_AI_API_URL=https://your-api-url.com
VITE_AI_API_KEY=your_api_key_here
```

## 性能优化建议

### 1. 启用 Gzip 压缩

在 Nginx 配置中添加：

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

### 2. 配置 CDN

将静态资源（图片、字体等）上传到 CDN：

- 使用 Cloudflare CDN
- 或使用 AWS CloudFront
- 或使用阿里云 CDN

### 3. 启用缓存

在 Nginx 配置中添加：

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|webp)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## 监控和日志

### 使用 PM2 查看日志

```bash
# 查看所有日志
pm2 logs

# 查看特定应用日志
pm2 logs toxic-philosopher

# 清空日志
pm2 flush
```

### 使用 PM2 监控

```bash
# 查看应用状态
pm2 status

# 查看详细监控
pm2 monit
```

## 故障排查

### 构建失败

1. 检查 Node.js 版本：`node -v`（应该 >= 18）
2. 检查 pnpm 版本：`pnpm -v`（应该 >= 10.4）
3. 清除缓存：`pnpm store prune && rm -rf node_modules && pnpm install`

### 运行时错误

1. 检查端口占用：`lsof -i :3000`
2. 查看日志：`pm2 logs toxic-philosopher`
3. 重启应用：`pm2 restart toxic-philosopher`

### 图片加载失败

1. 检查 `client/public/` 目录下图片文件是否存在
2. 检查文件权限：`chmod 644 client/public/*.png`
3. 检查 Nginx 配置是否正确代理静态文件

## 更新部署

### Vercel/Netlify

推送到 GitHub 仓库后自动部署：

```bash
git pull origin master
git push origin master
```

### 传统服务器

```bash
cd the-toxic-philosopher
git pull origin master
pnpm install
pnpm build
pm2 restart toxic-philosopher
```

## 回滚部署

### Vercel

在 Vercel Dashboard 中选择之前的部署版本并回滚。

### 传统服务器

```bash
git log  # 查看提交历史
git checkout <commit-hash>
pnpm install
pnpm build
pm2 restart toxic-philosopher
```

## 安全建议

1. **使用 HTTPS**
   - 使用 Let's Encrypt 免费证书
   - 或使用 Cloudflare SSL

2. **配置防火墙**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

3. **定期更新依赖**
   ```bash
   pnpm update
   ```

4. **环境变量保护**
   - 不要将 `.env` 文件提交到 Git
   - 使用环境变量管理工具

## 支持

如有问题，请：
1. 查看 [GitHub Issues](https://github.com/danna1013/the-toxic-philosopher/issues)
2. 提交新的 Issue
3. 查看项目 README.md

---

**祝部署顺利！**

