# cf-speed-tester

用于对 cloudflare CDN 测速

cf_ips.txt: 从 BGP/ASN 数据网站生成的 Cloudflare 官方 IP，每个 C 段保留 1 个地址

server_checker.py: 检测在指定延迟内，能否连接到目标服务器的指定端口

cf_checker.py: 检测服务器能否作为 AnyCast CDN 使用



## 用法：

默认检查 cloudflare 官方 IP。

假定 cf_ips.txt 内 IP 的所属段均合法。
server_checker.py 默认检测连接至 443 端口，将延迟 <100ms 的结果记录到 valid.txt。
约 5,000 个官方 IP，通常可在半分钟内完成。

连用 cf_checker.py，默认进一步从 valid.txt 中筛选到达指定网页延迟 <100ms 的 IP。
默认检测页面为 Cloudflare 官网，部分段限定高级账户可用，可修改 url 至对应的网站。
检测速度约 25 IPs/s。

注意：
- 运营商到 CDN 节点的优化各不相同，以电信为例，延迟可能需要调整到更大数值，如 150ms，才能出现结果。
- cf_checker.py 不判断 IP 是否支持 websocket。如果 IP 量较大且检测对象为非官方 IP，即 Cloudflare proxy，可使用其他工具检测 websocket 连通性，如 nadoo/glider。
