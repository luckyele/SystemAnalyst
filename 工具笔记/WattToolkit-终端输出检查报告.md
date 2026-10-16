# Watt Toolkit（Steam++）终端输出检查报告

检查时间：2026-10-16 20:22-20:35
检查对象：/home/lucky/Steam_v3.1.0_linux_x64/nohup.out（1066 行，81834 字节）
检查方式：日志分析 + 配置比对 + 端口实测 + 证书链验证

---

## 一、结论

加速器主进程当前存活，系统代理已生效。
但有 1 个正在影响使用的问题，另有 4 类需要整改的问题。

最严重的问题：系统代理正在拦截全部 HTTPS 流量，而 SteamTools 根证书没有装进系统证书库。
结果：curl、git、pip、apt、wget 等命令行工具现在全部报证书错误。

---

## 二、现场还原

### 运行方式

- 程序：Watt Toolkit v3.1.2025.0（Steam++ Linux x64）
- 目录：/home/lucky/Steam_v3.1.0_linux_x64
- 启动链：Steam++.sh → 内置 dotnet → Steam++.dll（Avalonia GUI）
- 终端输出：nohup.out，最后写入 2026-09-21 23:42
- 配置目录：/home/lucky/.local/share/Steam++/

### 日志构成（1066 行）

| 类型 | 行数 |
|---|---|
| info 级日志 | 527 |
| Request finished | 208 |
| Received response | 104 |
| Proxying | 104 |
| warn 级 | 4 |
| 域名告警 | 4 |

### 时间线

- 08-04：程序解压安装
- 09-21 20:05 至 23:42：从图形终端 nohup 启动，跑了一晚 GitHub 加速
- 09-21 23:42：X 会话结束，GUI 实例死亡
- 10-15 23:16：用户修改代理设置（脚本加速被关掉）
- 10-16 20:14：数据库文件被再次写入（当前实例活动证据）

---

## 三、问题清单

### P0-1 系统代理拦截全部 HTTPS，命令行工具证书错误

证据：

- GNOME 系统代理为 manual 模式，指向 127.0.0.1:26561
- 实测 curl 走代理访问 https://www.gstatic.com/generate_204，退出码 60
- MITM 证书签发者为 CN=SteamTools Certificate; O=BeyondDimension; C=CN
- 该根证书不在 /etc/ssl/certs/ca-certificates.crt 中
- 系统库里只有另一个工具 fastgithub.crt
- SteamTools CA 只装进了 NSS 库（~/.pki/nssdb/cert9.db 已确认存在）

影响：

- curl、git、pip、apt、wget、node、python requests 全部失败
- 浏览器正常（走 NSS 库）
- 被拦截的不只是 Steam 和 GitHub，gstatic.com 同样被拦截
- 带证书固定的应用会直接拒绝连接

改进（二选一）：

- 方案 A：把证书装进系统库，让命令行工具恢复
  ```bash
  sudo cp ~/.local/share/Steam++/Plugins/Accelerator/SteamTools.Certificate.cer \
      /usr/local/share/ca-certificates/SteamTools.crt
  sudo update-ca-certificates
  ```
- 方案 B：只在玩游戏时开系统代理，用完就在 Watt Toolkit 里关掉
- 不建议长期开着系统代理

### P0-2 旧实例已死，当前实例不写日志

证据：

- nohup.out 最后一行：X connection to :0 broken (explicit kill or server shutdown)
- 但 application.dbf-shm 在 10-16 20:14 仍被写入
- Steam 目录下没有其它日志文件

结论：

- 09-21 X 会话结束时，GUI 实例随之死亡
- 现在运行的是另一个实例，stdout 没有落到任何文件
- 出问题时无日志可查

改进：改用 systemd 用户服务托管，日志进 journal。配置见第六节。

### P1-1 nohup.out 无轮换，日志量失控

证据：

- 单个文件 81 KB，无任何轮换机制
- 每条 HTTP 请求产生 4 到 5 行日志
- 527 行 info 里，304 行是 github.githubassets.com 的静态资源
- 16 行是 api.github.com/_private/browser/stats 的遥测上报
- 按此速率估算，重度使用一天可产生数千行（此为估算，非实测）

改进：

- 继续用 nohup：加 logrotate（配置见第六节）
- 改用 systemd：journal 自动轮换，无需额外配置

### P1-2 代理监听 0.0.0.0:26561，等于局域网开放代理

证据：

- ss 显示 0.0.0.0:26561 处于 LISTEN 状态
- GNOME 配置指向 127.0.0.1:26561
- ProxySettings.json 中 SystemProxyIp 也是 127.0.0.1
- 实际监听地址却是全网卡

影响：

- 同一局域网内任何人都能把你的机器当代理使用
- 你的出口 IP 与流量内容对局域网暴露

改进：

- 在 Watt Toolkit 设置里查找监听地址选项，改为 127.0.0.1
- 若无此选项，用防火墙默认拒绝入站：
  ```bash
  sudo ufw default deny incoming
  ```
- 本环境无权限读取宿主机 iptables 规则，需你在宿主机上确认

### P2-1 avatars.githubusercontent.com 污染告警

证据：

- warn 出现 4 次，全部指向同一域名
- 告警原文：域名可能已经被 DNS 污染，如果域名为本机域名，请解析为非回环 IP
- 该域名请求实际返回 200，功能未损坏

原因：

- 当时的脚本加速把该域名 hosts 到回环地址
- YARP 代理路由表未覆盖该域名
- 两边配置不同步

现状：

- 当前 IsEnableScript 为 false
- /etc/hosts 干净，无残留映射
- 此问题当前不存在，重新开启脚本加速时会复现

### P2-2 GitHub 反代曾监听 0.0.0.0:80 与 0.0.0.0:443

证据：

- 日志头部有 Listened https://0.0.0.0:443 与 http://0.0.0.0:80
- 当前 80/443 未监听，YARP 插件目录已空，此服务已停

影响：

- 占用两个通用端口，易与本机其它 HTTPS 服务冲突
- 全网卡监听等于开放代理

改进：保持关闭；如再用，仅本机使用时应绑定 127.0.0.1。

### P2-3 家目录残留 0 字节文件

证据：

- /home/lucky/WattToolkit/WattToolkit.tar.gz，0 字节
- /home/lucky/WattToolkit/WattToolkit.tgz，0 字节
- 失败下载的残留

改进：确认无用后删除。我不主动删除你的文件，需你确认。

### P2-4 WattToolkit.sh 自启脚本有缺陷，不要直接运行

缺陷 1：ProtectHome=true，且 ReadWritePaths 只含 $WATT_PATH

- 程序需要写 ~/.local/share/Steam++/（数据库、插件、设置）
- 服务化后必然写盘失败

缺陷 2：用 system 级服务运行 GUI 应用

- unit 中没有 DISPLAY、WAYLAND_DISPLAY、DBUS_SESSION_BUS_ADDRESS
- Avalonia 界面起不来

缺陷 3：Restart=on-failure 覆盖不足

- GUI 崩溃场景建议 Restart=always

另注意：Steam++.sh 权限为 700，需在宿主机确认属主是否为当前用户。

### P3-1 日志含隐私信息

证据：

- nohup.out 中含 GitHub 用户名 luckyele
- 含用户 ID 20064094
- 文件权限为 644

改进：排查结束后清空该文件，或将权限改为 600。

### P3-2 HTTP 请求被 302 跳转到 HTTPS

证据：

- curl 走代理访问 http://www.gstatic.com/generate_204
- 返回 302，Location 指向 https 同地址
- 对应配置 EnableHttpProxyToHttps: true

影响：部分程序做 HTTP 连通性检测时会误判。

### P3-3 开机自启可能未生效

证据：

- GeneralSettings.json 中 AutoRunOnStartup 为 true
- ~/.config/autostart/ 下只有 ibus 和 fcitx5，没有 Watt Toolkit 条目

改进：如需开机自启，按第六节配置 systemd 用户服务。

---

## 四、改进优先级

1. 立刻：确定证书方案（装进系统库，或随用随关）
2. 本周：改用 systemd 用户服务，日志进 journal
3. 本周：处理 0.0.0.0 监听问题
4. 顺手：清理 0 字节文件；重写 WattToolkit.sh

---

## 五、systemd 用户服务配置（推荐）

存为 ~/.config/systemd/user/watt-toolkit.service：

```ini
[Unit]
Description=Watt Toolkit (Steam++)
After=graphical-session.target
PartOf=graphical-session.target

[Service]
Type=simple
WorkingDirectory=/home/lucky/Steam_v3.1.0_linux_x64
ExecStart=/bin/bash /home/lucky/Steam_v3.1.0_linux_x64/Steam++.sh
Restart=always
RestartSec=10
Environment=DISPLAY=:0
Environment=DOTNET_CLI_TELEMETRY_OPTOUT=1

[Install]
WantedBy=graphical-session.target
```

启用命令：

```bash
systemctl --user daemon-reload
systemctl --user enable --now watt-toolkit.service
journalctl --user -u watt-toolkit -f
```

要点：

- 用 --user 服务，不需要 sudo，自动继承图形会话环境
- 日志进 journal，自带轮换，nohup.out 无限增长问题消失
- X 会话重启后服务能自恢复
- 不碰 ProtectHome，不存在写盘失败问题

## 六、logrotate 备选配置

若继续用 nohup 方式，存为 /etc/logrotate.d/watt-toolkit：

```
/home/lucky/Steam_v3.1.0_linux_x64/nohup.out {
    weekly
    rotate 4
    compress
    missingok
    notifempty
    copytruncate
}
```

## 八、GitHub 加速专项（2026-10-16 晚补充实测）

用户目标收窄为：仅关注 GitHub 浏览加速。以下为针对性实测。

### 8.1 直连实测（加速器关闭状态）

| 目标 | 结果 |
|---|---|
| github.com | 时通时断。20:52 三次全 200（TTFB 0.34-1.04s，首页 572KB 下载 13-20s）；20:53 两次即时 SSL 失败；20:57 十连测 0/10 |
| 真实 IP 20.205.243.166 | TCP 79ms 连上，TLS 590ms 完成，之后请求无响应，15s 超时 |
| api.github.com | 200，0.25s，正常 |
| avatars.githubusercontent.com | 200，0.79s，正常 |
| github.githubassets.com | 可达 |
| codeload / objects.githubusercontent.com | 可达 |
| raw.githubusercontent.com | 不通。TCP 能连，TLS 阶段连接被杀 |
| 系统 DNS 对 github.com | 间歇性无应答 |
| 阿里 DNS / Google DNS | 均返回正确 IP 20.205.243.166 |

加速器开启时对比：

| 模式 | github.com | raw |
|---|---|---|
| 系统代理（26561） | 200，TTFB 1.0-2.2s，首页 29s | 不通（20s 超时） |
| YARP 脚本模式（80/443） | 200，TTFB 0.74s，首页 13.3s | 未测 |

两种模式下首页吞吐都在 20-43KB/s 量级，没有质变。

### 8.2 路由追踪

- 路径：192.168.1.1 → 211.138.186.229（移动骨干）→ 221.183.x（电信骨干）→ 223.120.2.x（电信国际出口）→ 51.10.49.101 → GitHub
- 国际出口段（223.120.2.x）ICMP 丢包 80-90%
- 对照组 223.5.5.5（阿里 DNS，国内路径）：0% 丢包，24ms
- 注意：骨干路由器常限流 ICMP，ICMP 丢包不能直接等同 TCP 丢包。但 TCP 层「握手成功、数据卡死」是实测事实。

### 8.3 干扰来源判断

干扰特征：

- TCP/TLS 握手能完成，之后数据被卡死或连接被重置
- 按分钟级时通时断（20:52 三连通，20:57 十连断）
- 按域名选择性打击：raw 全死，api 和 avatars 正常
- 系统 DNS 间歇无应答，公共 DNS 正常

结论：指向国际出口处的针对性干扰，叠加电信国际出口段的高丢包。
不是单纯的运营商拥塞。拥塞不会只封一个域名，也不会在握手成功后杀连接。
但国际出口走的是电信/移动线路，干扰位置与差的链路质量重合。
说「运营商线路掺和其中」成立，说「运营商单方面搞的」不准确。

用户自判方法：

1. 手机开 4G/5G 同时打开 github.com。手机稳定而宽带抖，问题在宽带这条出口。
2. 系统 DNS 换成 223.5.5.5。这只解决解析间歇失败，不解决 TCP 层阻断。
3. 每隔几小时直连测一次，记录通/断比例，摸清阻断的时间规律。

### 8.4 使用建议

1. 加速器值得开，但定位是兜底。直连通的时段不需要它；断的时段它能救命。
2. 两种模式都慢，脚本模式略快（13.3s 对 29s）。差别不大，随用随开即可。
3. raw.githubusercontent.com 两种模式都不通。绕法：用镜像前缀（gh-proxy.com 实测可达，ghfast.top 不通），或等直连窗口期。
4. git 命令行操作需要把 SteamTools CA 装进系统库，一条命令。纯浏览器浏览不需要。
5. 系统 DNS 换 223.5.5.5，减少解析失败。

---

## 九、原问题清单（首次检查，2026-10-16 20:22）

以下为首次全量检查记录。其中与 GitHub 加速无关的条目（P1-1 日志、P2-3 残留文件、P2-4 自启脚本、P3-1 隐私），经用户确认本次不处理。

以下四项在当前环境无法验证，需在宿主机确认：

1. 当前实例由谁启动、以什么身份启动（Steam++.sh 权限为 700）
2. 宿主机防火墙实际规则（本环境无权限读取 iptables）
3. 浏览器信任 SteamTools CA 的具体来源（NSS 库已确认有该证书）
4. GitHub 加速当前是否仍需要（09-21 日志显示代理链路响应 350ms 至 1200ms，建议实测对比直连）
