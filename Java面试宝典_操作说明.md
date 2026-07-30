# Java 面试宝典 · 操作说明

## 项目概览

| 板块 | 文件 | 题数 |
|------|------|------|
| 总目录 | `Java面试宝典_总目录.html` | — |
| 01 Java 基础 | `Java面试宝典_01_Java基础.html` | 40 |
| 02 集合容器 | `Java面试宝典_02_集合容器.html` | 30 |
| 03 JVM 虚拟机 | `Java面试宝典_03_JVM.html` | 35 |
| 04 并发编程 | `Java面试宝典_04_并发编程.html` | 40 |
| 05 MySQL | `Java面试宝典_05_MySQL.html` | 40 |
| 06 Redis | `Java面试宝典_06_Redis.html` | 35 |
| 07 框架 | `Java面试宝典_07_框架.html` | 40 |
| 08 分布式 & 其他 | `Java面试宝典_08_分布式&其他.html` | 40 |
| **合计** | | **300 题** |

---

## 启动方式

### 步骤一：启动服务

1. 打开 **PowerShell**（Win + X → 终端管理员 运行下面命令以确保权限）
2. 启动 HTTP 服务器：

```powershell
cd D:\AiWordSpace
python -m http.server 9876
```

### 步骤二：放行防火墙（多端访问必须）

以 **管理员身份** 打开 PowerShell，执行：

```powershell
New-NetFirewallRule -DisplayName "Python HTTP Server 9876" -Direction Inbound -Protocol TCP -LocalPort 9876 -Action Allow
```

> 仅执行一次即可，之后无需重复。

### 步骤三：各设备访问地址

| 设备 | 访问地址 |
|------|----------|
| 本机电脑 | http://localhost:9876/Java面试宝典_总目录.html |
| 其他设备（手机/平板/电脑） | http://192.168.5.171:9876/Java面试宝典_总目录.html |

> 所有设备需连接 **同一个 WiFi**。「192.168.5.171」是你当前电脑 IP，如重启路由器后 IP 变了请重新查询。

### 快速查本机 IP

```powershell
ipconfig | findstr "IPv4"
```

### 手机扫码快速访问

将以下 URL 复制到任意二维码生成工具中生成二维码，用手机扫描即可：
```
http://192.168.5.171:9876/Java面试宝典_总目录.html
```

> 端口 9876 被占用时可换其他端口，如 `python -m http.server 8080`，防火墙和访问地址同步更改。

---

## 功能说明

### 查看答案
每个面试题卡片底部有 **「查看答案 ▼」** 按钮，点击展开答案。

### 主题切换
每个页面顶部有主题切换按钮：
- **黑白金**（默认）：黑底白卡，香槟金点缀
- **深绿色**：绿色系沉稳风格
- **深靛紫**：紫色系优雅风格

### 板块导航
每个板块页面顶部有导航链接，可在各板块和总目录之间跳转。

### 标签筛选
每题配有标签（如"高频""基础语法""JVM基础"等），方便快速定位知识点。

---

## 目录结构

```
D:\AiWordSpace\
├── Java面试宝典_总目录.html          # 入口页面
├── Java面试宝典_01_Java基础.html      # 第1板块
├── Java面试宝典_02_集合容器.html      # 第2板块
├── Java面试宝典_03_JVM.html           # 第3板块
├── Java面试宝典_04_并发编程.html      # 第4板块
├── Java面试宝典_05_MySQL.html         # 第5板块
├── Java面试宝典_06_Redis.html         # 第6板块
├── Java面试宝典_07_框架.html          # 第7板块
├── Java面试宝典_08_分布式&其他.html   # 第8板块
├── Java面试宝典_操作说明.md           # 本文件
└── _pdf_text/                         # PDF提取文本（素材来源）
```

---

## 版本管理（Git 本地存档）

项目已初始化 Git 仓库，所有变更都在本地 `.git` 中存档，无需联网。

### 提交新版本

修改完成后，执行以下命令存档：

```powershell
cd D:\AiWordSpace
git add -A
git commit -m "v1.x.x - 变更说明"
```

### 常用操作

| 操作 | 命令 |
|------|------|
| 查看版本历史 | `git log --oneline` |
| 查看某次改了什么 | `git show <版本号>` |
| 回退到之前的版本 | `git checkout <版本号> -- .` |
| 对比两次版本差异 | `git diff v1.0 v1.1` |
| 给版本打标签 | `git tag v1.0.0` |

### 版本记录

详见 `CHANGELOG.md`

---

## 常见问题

**Q: 打开页面看不到样式？**
> 请使用 Python HTTP 服务器方式启动，不要直接双击打开（跨文件引用可能受限）。

**Q: 端口被占用怎么办？**
> 更换端口号即可：`python -m http.server 8888`，然后访问 `http://localhost:8888/...`

**Q: 没有 Python？**
> 从 https://www.python.org/downloads/ 下载安装，或直接用浏览器双击 HTML 文件打开。
