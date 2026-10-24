# 本地运行与恢复 · 0.3.2

本公开仓库不包含游戏本体。当前整理过的电脑保留可运行构建；其他电脑须自行准备有权使用的原始文件。网站仅是介绍页。

## 已有本地构建

在项目目录执行 `./Start-Local.ps1`。启动器使用独立的 `../player-profile`，打开固定地址：

**http://127.0.0.1:8765/local.html**

默认进入充足资源、满级与宽松预算模式。普通模式使用 `local.html?sandbox=0`。不要更换端口、改成 localhost 或直接使用 file://；不同 origin 会使用不同浏览器存储。

也可运行 `python tools/serve_local.py`，它只监听回环地址。按 Ctrl+C 停止前台服务；启动器开启的后台服务须先核对 PID 对应的命令行，再停止，不要批量终止 Python 或浏览器。

## 从公开仓库重建

1. 克隆本项目。准备 Python 3.12 与 Chromium 浏览器；Node 仅用于运行 JavaScript 检查。
2. 将你有权使用的基线构建放在一个单独目录，需包含 `Build/EBS.data`、`EBS.wasm`、`EBS.framework.js`、`EBS.loader.js`（后面三者也在 Build 内）、`TemplateData/style.css` 和 `index.html`。
3. 运行以下导入命令。导入前会核对全部六项 SHA-256，遇到不同版本或不同的已有文件即停止，不覆盖：

```powershell
python tools/import_originals.py --from-directory "你的原始构建目录"
python tools/verify_originals.py
python -m venv ../analysis-env
../analysis-env/Scripts/python.exe -m pip install -r tools/requirements-analysis.txt
```

4. 从 [Noto CJK 官方项目](https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf) 获取字体，存为 `../tool-cache/NotoSansCJKsc-Regular.otf`。SHA-256 必须是 `2c76254f6fc379fddfce0a7e84fb5385bb135d3e399294f6eeb6680d0365b74b`。许可证见 [OFL-Noto.txt](localization/OFL-Noto.txt)。
5. 按顺序生成补丁：

```powershell
../analysis-env/Scripts/python.exe tools/build_local.py
../analysis-env/Scripts/python.exe tools/build_sandbox.py
../analysis-env/Scripts/python.exe tools/build_native_ui.py
./Start-Local.ps1
```

这些步骤验证原件哈希、精确修改指定资源对象，再重新解析结果。原始 .wasm 与 .data 不覆盖。最终运行需要 `EBS.zh-CN.ui.data`、`EBS.sandbox.ui.data` 和 `EBS.local.framework.js`，都在 `local-generated/`。两个不带 `.ui` 的 data 文件只是重建中间产物，可重新生成；本机整理时已回收。

## 资源、等级与存档

- 每次启动前写入 `999999999` 宝石。游戏仍真实扣费；上游自身还可能增加约 50000，所以 HUD 不一定正好等于种子值。这不是严格永不减少的无限资源。
- 37 种兵种设为本构建最高 3 级；8 种史诗兵种仅在独立本地模拟档可用。未修改付款、收据、订阅、VIP 或线上权限。
- 105 个普通关卡与 10 个史诗关卡设置为已完成；普通关卡菜单可能定位到末关，可使用箭头切换。
- 关卡金币为 `999999999`，关卡/自定义/每类兵种配额为 `1000`。地形、碰撞、阵营区域及硬件性能限制仍存在。
- 普通数据库为 `/idbfs`，新版沙盒为 `/idbfs-ebs-local-sandbox-v2`。初始化优先复制有效旧 v1 档，否则复制普通档，否则新建。旧档不覆盖或删除。
- 游戏仍是部分汉化；评分提示、部分商城图片和品牌标识保留英文。当前入口没有顶部模式栏。

## 本机目录

| 目录 | 用途 | 是否上传 |
|---|---|---|
| 项目目录 local-work | 可同步的代码和文档 | 仅 Git 跟踪的文件 |
| Build、TemplateData、index.html | 校验锁定的原始文件 | 否 |
| local-generated | 本地生成包 | 否 |
| output/playwright | 历次截图和日志 | 否 |
| ../player-profile | 个人游戏浏览器配置和存档 | 否 |
| ../original-backup | 六个原始文件独立备份 | 否 |
| ../analysis-env、../tool-cache | 重建环境及 Noto 字体 | 否 |
| ../local-archive | 旧历史恢复包、清理清单 | 否 |

清理没有删除个人存档。专用 QA 配置已回收，重新运行相应 QA 脚本会按需创建新的测试配置。截图证据保留在本机，公开仓库只有文本清单与哈希。

## 复验

无需游戏资产的检查：

```powershell
python tools/check_public.py
node tools/test_prefs.cjs
```

有本地原件与运行环境时：

```powershell
python tools/verify_originals.py
python tools/test_storage.py
python tools/qa_native_ui.py
python tools/qa_native_ui.py mobile
python tools/qa_noads.py
```

浏览器测试需要 Python Playwright 和 Chromium；设置 `EBS_CHROMIUM` 可以指定已有浏览器。测试只操作专用配置或临时上下文，不接管 player-profile。截图须人工复核，脚本退出 0 不等于视觉验收通过。Browser plugin not available，本项目使用 Python Playwright。

历史 `qa_final.py resources` 针对 0.1.0 的非满级档，不能用于当前默认满级入口的消费证明。已经满级时点击升级不能算作实际消费。测试边界见 [AUDIT.md](AUDIT.md)。

## 恢复与回滚

1. 关闭当前战斗并返回菜单。打开同一 origin 的 `local.html?sandbox=0`，使用普通资源与预算，保留中文补丁。数据库不会删除。
2. 需要原始构建时打开 `http://127.0.0.1:8765/index.html`。它仍是原始字节，可能尝试外部服务；严格离线对照须在测试请求拦截环境中进行。
3. 执行 `python tools/verify_originals.py`，核对六个原件和六个备份。若失败，先另存异常文件，不能直接覆盖。
4. 撤销公开代码变更，优先 `git revert <提交>`。不要用会清除未跟踪文件的命令；本地游戏资产正是未跟踪文件。
5. 旧 0.1–0.3.1 Git 历史保存在本机 `../local-archive/pre-public-history.bundle`。它含游戏资产，禁止上传。需要旧版本时：

```powershell
git bundle verify ../local-archive/pre-public-history.bundle
git clone --branch local/zh-buttons-noads ../local-archive/pre-public-history.bundle ../history-recovery
```

恢复在独立目录进行，不替换当前代码或浏览器配置。旧提交：0.1.0 `60192d9`，0.2.0 `669bbe4`，0.3.0 `793eb31`，0.3.1 `62a452e`。新公开历史不包含这些提交；旧的 `git worktree add <旧提交>` 必须在恢复目录中运行。只能有一个本地服务占用 8765。
6. 回收站内容可按系统“还原”恢复，清单见 `../local-archive/cleanup-receipt.json`。旧 .git 不要还原覆盖当前 .git；用上面的 bundle 恢复方法。
7. 停止本地服务并关闭游戏窗口即可停止运行。保留 player-profile 和 original-backup。

## GitHub 同步与网站

公开仓库：`https://github.com/seiya058904/epic-battle-sandbox-cn`。网站只从 `site/` 部署。后续推送前先运行公开文件检查，明确审核暂存清单；不要强制添加被忽略的资产。

```powershell
git status --short
python tools/check_public.py
git fetch origin
git rev-list --left-right --count HEAD...origin/main
```

最后一条输出 `0 0` 才表示当前提交与远端 main 相同。CI 通过与网站部署成功分别核对，不能用本地通过替代线上验证。
