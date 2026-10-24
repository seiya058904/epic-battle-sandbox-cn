# 简体中文对照与验收

0.1.0 基础汉化统计（保留历史证据）：已写入 111 个不同原文；逐项截图确认 29 项（占已映射项 26.1%，不是全游戏文案完成率）。全游戏文案总数未知。
抽查主页、模式分类、兵种信息、升级、商店、关卡、设置、暂停、结算 9 类界面；7 类有已验证中文，当时 0/9 达到全页中文；0.3.0 新按钮统计另列下表。字母枪械型号 M16、AK47 保留。原始品牌标识未改写。

显示数据、字体和图集修改均进入 Unity Canvas；网页外壳不计入以上统计。未目视条目明确标出，不因文件写入成功而计为已验证。

| 原文 | 中文 | 页面/位置 | 修复方式 | 证据/状态 |
|---|---|---|---|---|
| ` (MAX)` | （满级） | 升级卡 | metadata 字符串索引 | [已验证](../output/playwright/final/resources-spend-3.png) |
| ` Wins The Battle!` | 赢得战斗！ | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `ARMY: 0/35` | 兵力：0/35 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Add Some Troops First!` | 请先放置兵种！ | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `Archer` | 弓箭手 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Axe` | 斧兵 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Bear Rider` | 熊骑兵 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Berserker` | 狂战士 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Blue Team Has No Troops!` | 蓝方尚未布阵！ | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `Blue Team Won The Battle!` | 蓝方赢得战斗！ | 战斗结算 | metadata 字符串索引 | [已验证](../output/playwright/final/mobile-result-dismissed.png) |
| `Bomb` | 炸弹兵 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `By choosing Accept, I agree with the Privacy Policy.` | 选择接受，即表示同意隐私政策。 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Camel` | 骆驼骑兵 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Cannon` | 火炮 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Catapult` | 投石车 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Catapult ` | 投石车 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Catapult - LVL 2` | 投石车 - 2级 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Cavalry` | 骑兵 | 自定义模式分类 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-custom.png) |
| `Chariot` | 战车 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Complete All Previous Levels` | 请先完成前面的所有关卡 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Crossbow` | 弩兵 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Daily Reward` | 每日奖励 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Defeats :` | 失败： | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Drag to place your army.` | 拖动以布置部队。 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Drag two fingers to zoom.` | 双指拖动以缩放。 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Enemy Army` | 敌方部队 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Epic` | 史诗 | 自定义模式分类 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-custom.png) |
| `Epic Level ` | 史诗关卡  | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `Every in app purchase will remove pop up ads!` | 任意应用内购买将移除弹出广告！ | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Fight !` | 战斗！ | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Fire Dragon` | 火龙 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `First Time Win Reward - ` | 首次胜利奖励 -  | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `First Win All Previous Epic Levels` | 请先通关前面的所有史诗关卡 | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `First Win All Previous Levels` | 请先通关前面的所有关卡 | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `Free look` | 自由视角 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `GOLD: 1000` | 金币：1000 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Get 5 Wins` | 取得5场胜利 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Giant` | 巨人 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Gladiator` | 角斗士 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Guard` | 卫兵 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Guardian` | 守护者 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Heavy` | 重型 | 自定义模式分类 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-custom.png) |
| `Hwacha` | 火箭车 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Important` | 重要提示 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Knight` | 骑士 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `LOADING...` | 加载中… | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `LVL ` | 等级  | 升级卡 | metadata 字符串索引 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `LVL 2` | 2级 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Leaderboard` | 排行榜 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Level ` | 关卡  | 普通关卡 | metadata 字符串索引 | [已验证](../output/playwright/final/menus-levels.png) |
| `Level 1` | 第1关 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Level 5 Passed` | 第5关已通过 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Level Stats` | 关卡统计 | 设置 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-settings.png) |
| `Loading` | 加载中 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `MAX` | 满级 | 升级卡 | metadata 字符串索引 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Mage` | 法师 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Mage Tower` | 法师塔 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Man` | 步兵 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Melee` | 近战 | 自定义模式分类 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-custom.png) |
| `Minigun` | 转管机枪 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Move` | 移动 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Music & SFX` | 音乐与音效 | 设置 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-settings.png) |
| `Musketeer` | 火枪手 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `My Army` | 我方部队 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Nickname` | 昵称 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Ninja` | 忍者 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Opponent` | 对手 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Opponent Disconnected` | 对手已断开连接 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Organ Gun` | 排炮 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Password` | 密码 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Paused` | 已暂停 | 暂停 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-pause.png) |
| `Pirate` | 海盗 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Place Army` | 布置部队 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Play Tutorial ` | 开始教程 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Privacy Policy` | 隐私政策 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Ranged` | 远程 | 自定义模式分类 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-custom.png) |
| `Red Team Has No Troops!` | 红方尚未布阵！ | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `Red Team Won The Battle!` | 红方赢得战斗！ | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `Regular Win Reward - ` | 胜利奖励 -  | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `Rhino` | 犀牛 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `SEARCHING FOR OPPONENT...` | 正在寻找对手… | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Samurai` | 武士 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Sentinel` | 哨卫 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Settings` | 设置 | 设置 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-settings.png) |
| `Shield` | 盾兵 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Social` | 社交 | 设置 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-settings.png) |
| `Spartan` | 斯巴达勇士 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组、序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Spear` | 长矛兵 | 升级卡 | Level_Manager 显示数组 | [已验证](../output/playwright/final/resources-spend-3.png) |
| `Special` | 特殊 | 自定义模式分类 | 序列化 UI 文本 | [已验证](../output/playwright/final/mobile-custom.png) |
| `Surrender` | 认输 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Tap "GO!" to start the battle.` | 点击“GO!”开始战斗。 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Terms of Use` | 使用条款 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Trebuchet` | 配重投石机 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Tutorial is completed !!` | 教程完成！ | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Unlock "Spartan", "Sentinel", "Samurai", "Minigun", "Fire Dragon" and "Rhino" !!` | 解锁斯巴达勇士、哨卫、武士、转管机枪、火龙和犀牛！ | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Unlock Six Epic Units! ` | 解锁六种史诗兵种！ | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Upgrade Required` | 需要升级 | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `Use the arrows and drag to move around` | 使用方向键并拖动以移动视角 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Use the arrows to move` | 使用方向键移动 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Use the joystick and drag to move around` | 使用摇杆并拖动以移动视角 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Use the joystick to move` | 使用摇杆移动 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Use the mouse wheel to zoom.` | 滚动鼠标滚轮以缩放。 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Username` | 用户名 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `War Elephant` | 战象 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `Well done` | 做得好 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Wins :` | 胜利： | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Wolf` | 狼骑兵 | 资源中存在；页面待逐项确认 | Level_Manager 显示数组 | 已映射，未逐项目视验证 |
| `You need more gems` | 宝石不足 | 资源中存在；页面待逐项确认 | metadata 字符串索引 | 已映射，未逐项目视验证 |
| `Your Army has not been set` | 尚未布置部队 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Your account:` | 你的账户： | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |
| `Zoom` | 缩放 | 资源中存在；页面待逐项确认 | 序列化 UI 文本 | 已映射，未逐项目视验证 |

## 0.1.0 历史未完成项（当前状态以文末 0.3.0 为准）

| 原文 | 目标中文 | 所在页面 | 已确认原因 |
|---|---|---|---|
| LEVELS / CUSTOM / EPIC LEVELS | 关卡 / 自定义 / 史诗关卡 | 主菜单 | btn_levels / btn_custom / btn_epic_levels 的图片烘焙文字 |
| UPGRADE / EPIC / SHOP | 升级 / 史诗 / 商店 | 主菜单图标 | 图片文字 |
| Upgrade Troops | 升级兵种 | 升级页标题 | title_upgrade Sprite，已提取确认 |
| CLEAR / HOME / GO! | 清空 / 主页 / 开战 | 布阵 | 图片按钮 |
| RESUME / SURRENDER / MAIN MENU | 继续 / 认输 / 主菜单 | 暂停 | button_resume 等 Sprite，已提取确认 |
| PLAY AGAIN | 再战 | 结算 | 图片按钮 |
| Privacy Policy | 隐私政策 | 设置 | 已翻译同名文本字段，但可见按钮实际使用图片 |
| Do you like this Game? / 评分说明 | 喜欢这款游戏吗？/ 评分说明 | 战后评分弹窗 | 未改写该弹窗的可见内容 |
| Gems Packs / 商品说明与订阅说明 | 宝石礼包 / 商品说明 | 商店 | 图片及部分运行时文案；仅查看，不操作付款 |
| 广告倒计时及平台提示 | 对应中文 | 启动/提示 | 上游桥接残留，未完成汉化 |

完整对象坐标、资源文件和原文见 [patch-ledger.json](../evidence/patch-ledger.json)。
字体只覆盖本翻译集的汉字、标点；未知用户输入、未访问界面、在线界面不在字形/布局验收内。

## 0.3.0 原生中文按钮与自动广告

新增 33 个原生 TextMeshPro 标签实例。下面按 Sprite/用途列出；资源写入不等于该界面已目视验证。品牌标识、商城商品卡图片及评分弹窗仍有英文，全游戏保持 PARTIAL。

| 原文/原 Sprite | 中文 | 位置 | 修复方式 | 证据/状态 |
|---|---|---|---|---|
| CUSTOM（Image 6835） | 自由布阵 | 主页 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/home.png) |
| Sprite 1440（Image 6855） | 会员 | Title_Img | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| HOME（Image 6861） | 主页 | 布阵 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/custom-empty.png) |
| 教程图标（Image 6879） | 教程 | 主页 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/home.png) |
| Sprite 1397（Image 6946） | 开始 | PlayFirstIncomplete_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| VIP（Image 7014） | 会员 | 主页 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/home.png) |
| UPGRADE TROOPS（Image 7026） | 兵种升级 | 升级 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/upgrades.png) |
| Sprite 1395（Image 7107） | 更多游戏 | CrossPromotion_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| Sprite 1322（Image 7117） | 认输 | SurrenderMulti_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| EPIC LEVELS（Image 7176） | 史诗关卡 | PlayEpicLevelsInfo_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，此独立控件未逐项目视验证 |
| Sprite 1283（Image 7197） | 领取 | DailyReward_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| EPIC COMBOS（Image 7214） | 史诗组合 | 商店 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/shop.png) |
| Sprite 1398（Image 7244） | 确定 | Ok_Button | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| Sprite 1274（Image 7294） | 联机 | PlayMultiplayer_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| EPIC（Image 7297） | 史诗 | 主页 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/home.png) |
| RESUME（Image 7345） | 继续游戏 | 暂停 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/pause.png) |
| SHOP（Image 7373） | 商店 | 主页 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/home.png) |
| Sprite 1303（Image 7440） | 取消 | No_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| Sprite 1319（Image 7458） | 订阅 | Subscription_btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| EPIC LEVELS（Image 7547） | 史诗关卡 | 主页 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/home.png) |
| SURRENDER（Image 7576） | 认输 | 暂停 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/pause.png) |
| Sprite 1330（Image 7587） | 确定 | Yes_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| CLEAR（Image 7654） | 清空 | 布阵 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/clear.png) |
| GO!（Image 7706） | 开战 | 布阵 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/custom-empty.png) |
| UPGRADE（Image 7740） | 升级 | 主页 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/home.png) |
| NEXT LEVEL / PLAY AGAIN（Image 7754） | 继续战斗 | 结算 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/result-after-dismiss.png) |
| Sprite 1311（Image 7837） | 恢复购买 | Restore_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| GEM PACKS（Image 7847） | 宝石商店 | 商店 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/shop.png) |
| Sprite 1435（Image 7862） | 特别优惠 | Title_Image | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| MAIN MENU（Image 7887） | 返回主页 | 暂停 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/pause.png) |
| LEVELS（Image 8033） | 关卡 | 主页 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/home.png) |
| Sprite 1318（Image 8094） | 特惠 | InAppSpecial_Btn | 原 Image 换无字背景，添加原生 TMP 子节点 | 已写入，未逐项目视验证 |
| EPIC TROOPS（Image 8148） | 史诗兵种 | 商店 | 原 Image 换无字背景，添加原生 TMP 子节点 | [已验证](../output/playwright/v3/desktop/shop.png) |

本次目视确认 19/33 个新增标签实例；含相同文字的不同控件，不与旧版 29 个不同原文混算百分比。广告基线 [Showing Ads in 2](../output/playwright/v3/before/8.png) 已复现；本地停用独立 H5AutoAds 对象和自动调用组件，保留存档与真实支付标记不变。长时观测结果见 evidence/native-ui-validation.json。
