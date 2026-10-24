# 本地构建审计与验收 · 游戏补丁 0.3.1 / 文档整理 0.3.2

原验收日期 2026-10-24；上游 `5b6e7f7035a4246fac6f58aca6799d5eaacfcc5d`。以下游戏验证来自本机 0.1–0.3.1 历史。0.3.2 只整理项目、发布补丁源码与介绍网站，不发布游戏资产。旧提交位于本机归档 bundle，当前公开分支为 `main`；恢复方式见 README_LOCAL.md。历史审计在恢复目录可用 `git show 60192d9:AUDIT.md` 查看。

## 结果边界

| 项目 | 状态 | 实际含义 |
|---|---|---|
| 基线运行 | PASS | 初始阶段已完成原始构建单场自动战斗、暂停、结算；原始文件 SHA-256 再核对一致。 |
| 游戏内简体中文 | PARTIAL | 保留既有 Canvas 汉化，新增 33 处原生中文按钮/标题；全游戏仍为部分汉化，商城商品图和 logo 等保留原文。新增逐项证据见 localization/zh-CN.md。 |
| 默认资源模式 | PASS | 无参数 local.html 默认独立试玩；新浏览器直接进入；每次启动写入本地余额 999999999。 |
| 严格无限宝石 | PARTIAL | 实际余额足够，消费仍真实扣减；不是永不减少的无限值。历史三次升级扣费见 validation.json。本版已满级，点击满级按钮不算消费。 |
| 本地兵种开放与等级 | PASS（本构建范围） | 37 个基础等级键、8 个独立 Boss 等级键设为 2；对应 UI 3 级。8 个史诗单位在独立本地模拟档中可用。原生史诗 3 档属性倍率均为 100%，本补丁不另造超强属性。 |
| 金币/布阵限制 | PARTIAL | 105 个普通关卡和 10 个史诗关卡预算为 999999999，关卡/自定义/每类兵种配额为 1000。保留地形、碰撞、区域及引擎限制；不是数学无限兵力。 |
| 原本战斗玩法 | PASS（已测范围） | 本地自定义战斗、暂停、继续、胜负与 +20 奖励实测；不等于所有关卡或满 1000 人压力通过。 |

当前证据清单见 `evidence/sandbox-validation.json`、`evidence/sandbox-patch.json`；历史资源消费证据仍保留在 `evidence/validation.json`。截图只存本机 `output/playwright/v2/`，没有纳入公开产物。

## 默认试玩存档与付费边界

- 正常入口：`http://127.0.0.1:8765/local.html`；普通入口：同地址加 `?sandbox=0`。
- 普通数据库 `/idbfs` 保持独立。新版仅写 `/idbfs-ebs-local-sandbox-v2`；旧 v1 沙盒和普通档不覆盖、不删除。
- 首次启动优先复制有效 v1 沙盒，否则复制普通档。没有存档时创建最小 UnityPrf 文件，由原游戏继续初始化其它默认值。不是要求用户先玩普通档。
- 宝石、满级和关卡进度在加载 Unity 之前设置，读取的是游戏真实 PlayerPrefs；不是修改 HUD。普通 29 种等级与史诗 8 种等级均有三档序列化配置；史诗另读 `*Boss` 键，已单独处理。
- `LevelsCompleted=105`、`EpicLevelsCompleted=10` 用于独立试玩关卡进度。普通关卡菜单默认定位到末关，可用原游戏箭头切换。
- 8 种史诗的本地可用标记（如 `LockedWolf`）仅在模拟档设为 0，`Wolf` 等原本字符串 locked 的本地状态改为整数等级。没有修改付款、收据、账户、订阅或服务器权限。不能将本地模拟当成已购买商品的凭证。
- `HasBoughtIAP`、`HasSubscriptionGoogle` 原值保留，专用测试档均为 0；没调用 CloudSave、付款成功或广告成功接口。
- 上游启动自行增加约 50000 宝石；因此常见实际余额是 1000049999，全新初始化可能另有 250。正常档重启也会增长，这是原构建行为。
- 在菜单中导航至 `local.html?sandbox=0` 切回普通数据包和原数据库。重新打开无参数入口仍默认试玩，不记住关闭选择。

## 资源结构与可回滚补丁

Il2CppDumper v6.7.46 的 WASM 自动识别返回 CodeRegistration=0 / MetadataRegistration=0，不能当作成功。后续只读解析原始 WASM 的 18568 个初始化数据段和 metadata v31，唯一匹配的 MetadataRegistration 为 3902828，类型定义数量 8845，恢复了字段类型与公开序列化顺序。工具与类型布局参考官方 Perfare/Il2CppDumper，不使用来源不明的破解工具。

`tools/inspect_sandbox_schema.py` 可复现只读字段分析；`evidence/sandbox-field-schema.json` 是受控字段表。实际生成器先校验原始 .data、已验收中文包 SHA-256 和字段初值，再沿字符串/数组结构逐字段解析，不依赖汉化前的固定偏移进行盲改。

`tools/build_sandbox.py` 只修改中文包中 `level1 / pathID 8170 / Level_Manager` 的 268 个整数字段：115 个关卡金币、115 个关卡人数、37 个兵种配额、1 个自定义人数。其它 29183 个对象逐字节不变；修改对象也逐字节与白名单构造结果核对。生成 `local-generated/EBS.sandbox.data`，原中文普通包保留，原 .data/.wasm 永不覆盖。字段原值/新值/偏移、输入输出 SHA-256 在 sandbox-patch.json。

实际第 105 关放置 15 名斯巴达兵，支出 10500，余额从 999999999 降到 999989499，超过原关卡 6000 预算；自定义模式放置 163 名 3 级步兵，总成本 3260，超过原 120 人限制。8 个史诗单位逐个单场实测，火龙放置 2 个，其余每类 3 个，均有模型与计数证据。

预算由原游戏逻辑实际扣除；人物数量由实际单位对象计数。不会把展示数字替换为无穷符号，也不会自动把大量单位灌入场景。

## 这是什么构建

- 仓库仅有 6 个编译产物/网页文件，没有 Unity 源工程、README 或授权许可证；不能称为开源游戏。
- 页面标注 `companyName=madkidgames.com`、`productVersion=1.11.4`，资源中的 PlayerSettings 也标注 madkidgames.com。
- 引擎实际为 `2022.3.62f2`；运行时 Analytics 本地记录的应用版本为 `1.4.30`，与网页版本字符串不一致。
- UI 是带 LEVELS/CUSTOM/EPIC LEVELS、近战/远程/骑兵/重型/特殊/史诗兵种的 3D 战斗游戏。资源含 Rappid Studios、`com.rappidstudios.simulatorbattlephysics`、GooglePlay BillingMode、移动端商城和第三方 SDK 痕迹。
- 以上说明它含相关游戏资源，**不能据此证明 CoreScripts 发布得到 Rappid Studios 授权，也不能确认它与任何当前官方手机版逐项相同**。上游已含域名批准循环、直接广告奖励成功回调，以及每次启动约 +50000 宝石的可观察行为；这不是可信的“未修改官方基线”。

## 二进制处理与汉化

使用隔离 venv 的 UnityPy 1.24.2 成功读取 UnityWebData1.0、嵌套 UnityFS 和 IL2CPP metadata v31。官方 UnityDataTools 文档也列出 WebGL `.data` 读取支持，但本次实际执行的是 UnityPy，不声称运行过 AssetRipper 或 UnityDataTools。

- 精确修改 162 个序列化文本字段、74 个兵种显示名称位置、17 个 metadata 显示字符串。共 111 个不同原文；不同原文数量不是视觉验收覆盖率。
- 仅修改 TMP UI 真正引用的 Avalon Bold SDF 和 ARIAL SDF。全部 534 个 TMP UI 引用已解析；没有全局替换字体名称或套用浏览器翻译。
- 新增中文来自 Noto Sans CJK SC，生成 SDF 字形，保留原有拉丁字符和图集像素。两张图集分别为 4096×4096、4096×2048，Alpha8，总计约 24 MiB 未压缩图集数据。所有翻译所需码点通过字体 cmap 检查；不承诺任意用户输入字符都有字形。
- 字体渲染在 Canvas 内完成，没有网页字幕层。网页顶部仅是模式切换控件，明确排除在游戏内汉化统计之外。
- `.wasm` 完全未修改。metadata 只重定向允许清单中的字符串索引；IL2CPP 类型、方法、字段名及存档键未翻译。
- 单位名称来自 `Level_Manager` 显示数组；Army 枚举和 `PlayerPrefs` 键保持英文。汉化后长矛兵升级及原键存档已验证。
- 对 29184 个 Unity 序列化对象逐个比较：176 个已列明对象改变，29008 个原始字节完全一致，未列明改动为 0。见 `evidence/object-verification.json`。
- 0.1.0 中文 `.data` 为 42467663 字节（原始 40460936 字节）；0.3.0 字体扩展后的中间包大小及最终 UI 包 SHA-256 以当前 generated-manifest/native-ui-patch 清单为准。新增数据包只留本机、被 Git 忽略。完整 SHA-256 见生成清单。

现有 5 个 TextAsset 是视频模板、BillingMode 和换行字符表，没有发现现成中文语言表。设置页面没有语言选择。不能用其他平台语言支持替代本构建验证。

**0.3.0 按钮处理**：没有在网页盖字幕，也没有在贴图上画字。将 33 处含英文的 Image 引用换为构建已有的无文字圆角背景，为原按钮增加真实 TextMeshProUGUI 子节点。文字跟随原按钮/场景/遮罩显示，关闭标签自身的射线检测，不拦截父按钮点击。原 Button 回调、单位数据、战斗脚本和存档字段未改。结算按钮运行时会切换 Sprite，已只改 Ui_Manager 中两个经验证的 Sprite 引用，避免英文重新出现。

每个中文普通/沙盒包只改变 69 个已有对象，新增 132 个 UI 对象；所有其它已有对象保持字节一致。启动场景中独立的 H5AutoAds 对象及 H5InterstitialAutoCaller 组件停用，原配置为首次 5 秒、间隔 300 秒、倒计时 3 秒、广告间歇 7 秒；不将间隔改成超大值，也不改购买免广告状态。基线截图 before/8.png 实际复现 “Showing Ads in 2”。当前生成与验证记录在 evidence/native-ui-patch.json 和 evidence/native-ui-validation.json。

剩余英文包括游戏品牌 logo、商店商品图的兵种/宝石/组合标题、部分评分/隐私与订阅图文。对这些不宣称全汉化；真钱商品未点击。

汉化逐条表、页面证据和未解决状态见 [localization/zh-CN.md](localization/zh-CN.md)。

## 网络、广告、付款与授权

基线在浏览器阻止所有非回环请求的情况下仍能进入和完成单人战斗。实测尝试访问的域包括 Google Fonts、madkidgames.com 主页/whitelisted.json、Unity config/analytics。资源另含排行榜、账户、广告、IAP 代码和远端主机引用；仅作为静态证据，未调用或攻击。

本地入口通过 CSP 限制 connect-src 为 self，禁止外部 frame/object，并拒绝 `window.open` 外部导航。测试另外在浏览器路由层拦截一切外部流量。浏览器其它导航途径/扩展并非系统级防火墙，要求绝对物理断网时仍可断开网络使用本地服务。

- 删除了上游 framework 中两处 `OnRewardedAdCompleted` 虚假奖励成功回调，仅保留关闭回调；未添加或调用任何付款成功回调。
- `adConfig` 改为空函数修复上游“adConfig is not a function”，没有模拟广告观看或付费结果。
- 切换模式先停止上游域名消息定时器再退出 Unity，避免对已释放实例 SendMessage。
- 保留的 H5_OnDomainApproved 是上游原有本地页面行为，未扩展至服务器认证，不能解释为授权证明。
- 在线账户、排行榜、订阅、VIP、真钱商品、IAP 收据校验：**OUT OF SCOPE，未消费/未更改授权状态**。不把客户端残留配置当成服务端控制已验证。商城仅查看，未点击真钱商品。
- 未上传原始或生成二进制、图集、字体或提取资源；所有资产权利仍归相应权利人。本补丁的个人本地用途声明不是版权授权。

## 测试与剩余限制

- `python tools/verify_originals.py`：6 个原件和 6 个独立备份 SHA-256 全通过。
- `python tools/test_storage.py`：全新档、空 v1 回退、有效 v1 迁移，以及普通/v1 两个源数据库原字节不变均通过。
- `node tools/test_prefs.cjs`：旧宝石修改、全新档、全部等级键、独立史诗等级、locked 类型转换、原输入不变、幂等、重复/截断拒绝、付款与订阅标记不变。
- 生成沙盒包后重新读取全部对象，对照 268 字段允许清单。
- `tools/qa_sandbox.py`：1280×720 桌面、844×390 触屏模拟，默认入口、升级界面、关卡消费、自定义战斗、暂停/继续、结算、刷新、重开和普通档隔离。截图必须逐张人工核对，不能把脚本退出 0 等同于视觉通过。
- `tools/qa_epic.py`：每个史诗兵种在独立空场重新选取，记录等级及实际放置，避免菜单收起首次点击或碰撞造成误判。
- `tools/qa_capacity.py`：实际关卡消费和超过旧自定义人数限制的放置证据。
- 早期检查发现只设基本键会让史诗仍显示 1 级，已增加独立 Boss 等级设置。最终史诗截图在 epic-full；混合阵容中地形/碰撞导致的个别放置失败不能算该兵种不可用，也不能算已放置。
- 保留 CSP 拒绝 Unity analytics/config 与域名清单请求的日志；这些阻止外连的记录不是未解释的 JS 崩溃。没有将“无 console 错误”作为不实声明。
- 没有测试真实 Android 设备、全部关卡通关、满 1000 人战斗、长期存档泄漏、GPU 峰值或线上功能。基线阶段的无头绘制计数不能当成真实帧率；本版不声称帧率或内存性能无回退。
- 未解锁或模拟真实支付成功、订阅、VIP、排行榜或在线账户；在线内容 OUT OF SCOPE。开放本地模拟兵种不授予游戏资产再分发权。

运行、修改文件清单及逐步回滚见 [README_LOCAL.md](README_LOCAL.md)。全部原始资源保持本地；公开上传原始/生成游戏二进制仍需版权人授权。

0.3.0 使用前端测试技能；Browser plugin not available，沿用项目的 Python Playwright + 现有 Chromium。测试只使用 qa-v3-* 或临时上下文，不接管用户游玩窗口。新增原生 UI 复验覆盖桌面和触屏、主页/设置/升级/商店/关卡/布阵、清空按钮、开战、暂停/继续、结算和关闭沙盒。完整刷新/保存检查沿用相同 v2 数据库，未迁移或删除用户存档。

0.3.0 验收：普通/沙盒共用的自动广告对象已停用；连续观测约 360 秒，8、305、315、360 秒截图均无倒计时或广告覆盖。WASM 导入计数仅作为辅助，不能单凭 0 次判定通过。两种视口完整战斗均显示蓝方获胜和 +20；刷新后满级保留，关闭模式回到普通等级。无 JS pageerror，除既有外连被 CSP 拒绝外无新增未解释的 Console error。19/33 个新增标签实例已逐项截图确认，其余只完成结构修改，未虚报目视通过。

0.3.1：按用户要求移除顶部模式栏和按钮，Canvas 布局不再预留 38 像素。默认沙盒初始化及数据库保持不变，普通模式仍可通过 `local.html?sandbox=0` 回滚访问。

0.3.1 验证：独立临时 Chromium 上下文确认顶部栏与按钮不存在；1280×720 Canvas 占满视口，844×390 触屏视口保持比例并可进入自由布阵；默认 sandbox=true，无 JS pageerror。存档迁移与源数据库保护测试通过。证据：evidence/no-toolbar-validation.json，截图位于 output/playwright/v3/no-toolbar/。本次仅做相关回归，未重复长时广告和完整战斗测试。
