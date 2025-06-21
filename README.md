# ArgoSB Python版本

## 简介

这是ArgoSB脚本的Python版本，无需root权限，**完全适用于普通用户**。所有文件安装在用户主目录下的`.agsb`隐藏文件夹中，不会影响系统目录。脚本使用Python 3，**仅使用Python标准库**，无需安装额外依赖。

## 使用方法

### 免费vps免root一键安装hysteria2
```bash
cd ~ && wget https://raw.githubusercontent.com/zhumengkang/agsb/main/nginx-hysteria2.py && python3 nginx-hysteria2.py
然后在运行
cd ~ && python3 nginx-hysteria2.py smart-proxy
```

### 免费vps免root一键安装vmess
```bash
cd ~ && curl -fsSL https://raw.githubusercontent.com/zhumengkang/agsb/main/agsb-v2.py | python3 - install --uuid b1ebd5fc-9170-45d4-9887-a39c9fc65298 --port 49999 --agk CF-token --domain 自己的域名
```

### 固定域名一键安装命令
```bash
cd ~ && curl -fsSL https://raw.githubusercontent.com/zhumengkang/agsb/main/agsb-v2.py | python3 - install --uuid b1ebd5fc-9170-45d4-9887-a39c9fc65298 --port 49999 --agk CF-token --domain 自己的域名
```
或者
```bash
cd ~ && wget https://raw.githubusercontent.com/zhumengkang/agsb/main/agsb.py && python3 agsb.py install --uuid 25bd7521-eed2-45a1-a50a-97e432552aca --port 49999 --agk CF-token --domain 自己的域名
```

### 一键安装命令
```bash
cd ~ && wget https://raw.githubusercontent.com/zhumengkang/agsb/main/agsb.py && python3 agsb.py
```
或者
```bash
cd ~ && curl -fsSL https://raw.githubusercontent.com/zhumengkang/agsb/main/agsb.py | python3 -
```

### 安装
```bash
python3 agsb.py install
```
首次运行会自动安装并配置服务。安装完成后会创建`~/bin/agsb`命令链接，可直接使用`agsb`命令操作。

### 启动服务
```bash
agsb
# 或
python3 agsb.py
```

### 查看服务状态
```bash
agsb status
# 或
python3 agsb.py status
```

### 查看单行节点列表
```bash
agsb cat
# 或
python3 agsb.py cat
```

### 升级脚本
```bash
agsb update
# 或
python3 agsb.py update
```

### 卸载服务
```bash
agsb uninstall
# 或
python3 agsb.py del
```

## 环境变量设置
可以通过环境变量自定义配置：

- `vmpt`: 指定vmess端口
- `uuid`: 指定UUID
- `agn`: 指定Argo固定域名
- `agk`: 指定Argo授权密钥

例如：
```bash
export vmpt=10000
export uuid=your-uuid
python3 agsb.py
```

## 安装目录
所有文件安装在用户主目录下的`.agsb`隐藏文件夹内：
- `~/.agsb/sing-box`: sing-box可执行文件
- `~/.agsb/cloudflared`: cloudflared可执行文件
- `~/.agsb/sb.json`: sing-box配置文件
- `~/.agsb/list.txt`: 节点信息列表
- `~/.agsb/allnodes.txt`: 单行节点列表文件

## 优点
1. **无需root权限**，普通用户即可使用
2. 安装在用户主目录下的隐藏文件夹，不影响系统目录
3. 使用Python 3编写，语法更现代
4. **仅使用标准库**，无需安装任何额外依赖
5. 保留了原shell脚本的所有核心功能
6. 自动创建用户目录下的命令链接，使用更方便
7. 更友好的错误处理和调试信息
8. 提供直接输出节点功能，方便复制使用

## 兼容性提示
- 需要Python 3环境，无需安装额外的依赖
- 所有文件都安装在用户目录下，不影响系统目录
- 安装完成后会在`~/bin`目录创建命令链接，如需使用，请确保该目录在PATH环境变量中

---

# Glitch 网站保活脚本

## 简介

这是一个用于保持 Glitch 项目在线的脚本，通过模拟真人浏览行为定期访问指定网站，防止 Glitch 项目因长时间无访问而休眠。脚本模拟真实用户访问行为，支持多种浏览器和设备的 User-Agent，自动处理缓存和 ETag，减少服务器负担。

## 主要功能

- 模拟真人浏览行为，防止被识别为机器人
- 支持自定义访问间隔时间
- 智能会话管理，模拟真实用户访问模式
- 支持多种浏览器和设备的 User-Agent
- 自动处理缓存和 ETag，减少服务器负担
- 完整的日志记录功能
- 支持通过命令行参数自定义配置

## 安装与使用

### 安装依赖

脚本仅依赖 Python 标准库和 `requests` 库：

```bash
pip install requests
```

### 使用 curl 一键安装并运行

```bash
# 下载并运行（默认URL）
curl -fsSL https://raw.githubusercontent.com/zhumengkang/agsb/main/cron-glitch.py | python3 -

# 下载并指定URL运行
curl -fsSL https://raw.githubusercontent.com/zhumengkang/agsb/main/cron-glitch.py | python3 - -u https://your-project-name.glitch.me

# 下载并指定URL和访问间隔
curl -fsSL https://raw.githubusercontent.com/zhumengkang/agsb/main/cron-glitch.py | python3 - --url https://your-project-name.glitch.me --interval 30-180

# 一键下载并在后台运行（默认URL）- 使用脚本内置后台功能
curl -fsSL https://raw.githubusercontent.com/zhumengkang/agsb/main/cron-glitch.py -o glitch.py && python3 glitch.py -b

# 一键下载并在后台运行（指定URL）- 使用脚本内置后台功能
curl -fsSL https://raw.githubusercontent.com/zhumengkang/agsb/main/cron-glitch.py -o glitch.py && python3 glitch.py -b -u https://your-project-name.glitch.me

# 查看日志
tail -f glitch.log
```

### 使用 wget 下载并运行

```bash
# 下载脚本
wget https://raw.githubusercontent.com/zhumengkang/agsb/main/cron-glitch.py -O glitch.py

# 运行脚本（默认URL）
python3 glitch.py

# 指定URL运行
python3 glitch.py -u https://your-project-name.glitch.me

# 指定URL和访问间隔
python3 glitch.py --url https://your-project-name.glitch.me --interval 30-180

# 一键下载并在后台运行（默认URL）- 使用脚本内置后台功能
wget https://raw.githubusercontent.com/zhumengkang/agsb/main/cron-glitch.py -O glitch.py && python3 glitch.py -b

# 一键下载并在后台运行（指定URL）- 使用脚本内置后台功能
wget https://raw.githubusercontent.com/zhumengkang/agsb/main/cron-glitch.py -O glitch.py && python3 glitch.py -b -u https://your-project-name.glitch.me

# 查看日志
tail -f glitch.log
```

### 基本用法

```bash
python glitch.py
```

这将使用默认设置（访问 https://seemly-organized-thing.glitch.me/ 网站，每 1-4 分钟访问一次）。

### 指定目标 URL

```bash
python glitch.py -u https://your-project-name.glitch.me
```

或者

```bash
python glitch.py --url https://your-project-name.glitch.me
```

### 自定义访问间隔

```bash
python glitch.py -i 30-180
```

这会将访问间隔设置为 30-180 秒（格式为"最小值-最大值"）。

### 删除特定 URL 的会话记录

```bash
python glitch.py -u https://your-project-name.glitch.me -d
```

或者

```bash
python glitch.py --url https://your-project-name.glitch.me --delete
```

### 清除所有会话记录

```bash
python glitch.py -c
```

或者

```bash
python glitch.py --clear-all
```

### 显示详细日志

```bash
python glitch.py -v
```

或者

```bash
python glitch.py --verbose
```

## 参数说明

| 参数 | 长参数 | 描述 |
|------|--------|------|
| `-u URL` | `--url URL` | 要访问的目标 URL（默认: https://seemly-organized-thing.glitch.me/） |
| `-i INTERVAL` | `--interval INTERVAL` | 请求间隔范围(秒)，格式为"最小值-最大值"（默认: "60-240"） |
| `-v` | `--verbose` | 显示详细日志 |
| `-d` | `--delete` | 删除指定 URL 的会话记录和 Cookie |
| `-c` | `--clear-all` | 清除所有会话记录和 Cookie |

## 工作原理

1. 脚本会在指定的时间间隔内随机选择一个时间点发送请求
2. 每次请求都会使用不同的浏览器指纹信息，模拟真实用户
3. 会话管理系统会保持 Cookie 和会话状态，模拟用户持续访问
4. 支持 ETag 缓存机制，减少服务器负担
5. 模拟人类浏览行为，如滚动、点击等

## 注意事项

- 脚本会在当前目录创建 `cookies` 文件夹存储会话信息
- 日志会同时输出到控制台和 `requests.log` 文件
- 为避免 Glitch 项目休眠，建议将访问间隔设置在 5 分钟以内
- 使用 Ctrl+C 可以随时中断脚本运行

## 在后台运行

脚本提供了内置的后台运行功能，可以让脚本在终端关闭后继续运行。**不依赖外部的nohup命令**，在各种环境下都能正常工作，包括Glitch平台。

### 使用内置后台功能

```bash
# 在后台运行（默认URL）
python glitch.py -b
# 或
python glitch.py --background

# 在后台运行并指定URL
python glitch.py -b -u https://your-project-name.glitch.me
# 或
python glitch.py --background --url https://your-project-name.glitch.me

# 在后台运行并指定URL和访问间隔
python glitch.py -b -u https://your-project-name.glitch.me -i 30-180
```

### 管理后台进程

```bash
# 列出所有正在运行的脚本实例
python glitch.py -l
# 或
python glitch.py --list

# 停止所有正在运行的脚本实例
python glitch.py -s
# 或
python glitch.py --stop
```

### 查看日志

后台运行的脚本日志会保存在 `glitch.log` 文件中，可以使用以下命令查看：

```bash
# 查看完整日志
cat glitch.log

# 实时查看日志更新
tail -f glitch.log
```

---

# Ubuntu Proot 环境安装脚本

在某些环境中，您可能需要一个完整的Ubuntu环境来运行上述ArgoSB脚本。以下是一个无需root权限的Ubuntu Proot环境安装脚本，可以帮助您在任何支持的系统上快速创建一个Ubuntu环境。

## 一键安装命令

```bash
cd ~ && wget https://raw.githubusercontent.com/zhumengkang/agsb/main/root.sh && chmod +x root.sh && ./root.sh
```
## curl一键安装命令Proot
```bash
cd ~ && curl -sSL https://raw.githubusercontent.com/zhumengkang/agsb/main/root.sh -o root.sh && chmod +x root.sh && ./root.sh
```
## 基本命令

```bash
./root.sh          # 安装Ubuntu Proot环境
./root.sh del      # 删除所有配置和文件
./root.sh help     # 显示帮助信息
./start-proot.sh   # 启动Proot环境
```

## 功能特点

- 自动检测系统架构（支持x86_64和aarch64）
- 下载并安装Ubuntu 20.04基础系统
- 自动配置DNS服务器
- 更新软件源为Ubuntu 22.04 (Jammy)
- 自动创建与物理机用户同名的用户目录
- 安装常用开发工具和软件包
- 美观的彩色界面和提示信息
- **无需root权限**，普通用户即可使用
- 支持一键删除所有配置和文件

## 进入和退出Proot环境

### 首次安装

首次安装时，脚本会询问是否立即启动proot环境。如果选择是，将自动进入proot环境，并执行初始化操作（更新软件源、安装软件包等）。

### 再次进入

安装完成后，如果需要再次进入proot环境，可以使用以下命令：

```bash
./start-proot.sh
```

### 退出Proot环境

在proot环境中，输入以下命令即可退出：

```bash
exit
```

### 如何判断是否在Proot环境中

在proot环境中，命令提示符会显示为`proot-ubuntu:/当前目录$`的形式，并且使用`uname -a`命令会显示Ubuntu系统信息。

### 删除Proot环境

如果您想要删除所有配置和文件，可以使用以下命令：

```bash
./root.sh del
```

此命令会删除所有生成的文件，但保留`root.sh`和`README.md`文件，以便您可以重新安装。

## 自动安装的软件包

脚本会自动安装以下软件包：

- curl, wget, git
- vim, nano
- htop, tmux
- python3, python3-pip
- nodejs, npm
- build-essential
- net-tools
- zip, unzip
- sudo
- locales
- tree
- ca-certificates
- gnupg
- lsb-release
- iproute2
- cron
- podman

## 注意事项

- 脚本需要在支持的系统架构上运行（x86_64或aarch64）
- 确保您有足够的磁盘空间
- 需要网络连接以下载必要的文件
- 首次运行时会自动下载并安装所需的软件包，这可能需要一些时间

## 常见问题解决

### 如果proot环境无法正常启动

请检查：
1. 是否有足够的磁盘空间
2. 是否有网络连接
3. 系统架构是否受支持

如果仍有问题，可以尝试删除所有配置后重新安装：
```bash
./root.sh del
./root.sh
```

### 如果在proot环境中无法访问网络

请检查DNS配置是否正确，可以尝试以下命令：
```bash
echo "nameserver 1.1.1.1" > /etc/resolv.conf
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
```

## 作者信息

- 作者: 康康
- GitHub: https://github.com/zhumengkang/
- YouTube: https://www.youtube.com/@康康的V2Ray与Clash
- Telegram: https://t.me/+WibQp7Mww1k5MmZl

## 许可证

本项目基于MIT许可证开源。

## 支持与贡献

如果您喜欢这个项目，请在GitHub上给我一个Star，或在YouTube上关注我的频道！
如有问题或建议，欢迎通过GitHub Issues或Telegram群组联系我。
## 赞助商
[![Powered by DartNode](https://dartnode.com/branding/DN-Open-Source-sm.png)](https://dartnode.com "Powered by DartNode - Free VPS for Open Source")
