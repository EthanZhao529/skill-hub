# Skill Hub 部署指南(新手版)

目标:让一个云端机器人**每天自动**把 GitHub 全网的公开 skill(star ≥ 2)抓下来,
更新到你的技能库网页里。全程免费。

---

## 一、它怎么运作(先理解,再操作)

```
GitHub Actions(云端,每天定时)
   └─ 运行 update_skills.py
        └─ 用你的令牌搜遍 GitHub 的 SKILL.md → 过滤 star≥2 → 生成 skills.js
             └─ 提交回仓库
                  └─ 网页(curated.js + skills.js)显示最新技能库
```

- `index.html` / `curated.js`:网页本体 + 人工精选的 43 个(永远在)。
- `update_skills.py`:抓取脚本。
- `skills.js`:**自动生成**的全网数据(第一次运行后才出现)。
- `.github/workflows/update-skills.yml`:每日定时任务。

---

## 二、准备一个 GitHub 令牌(必须)

搜遍全网需要登录令牌,免费生成:

1. 没有 GitHub 账号就先去 https://github.com 注册。
2. 打开 https://github.com/settings/tokens → **Generate new token** → **classic**。
3. Note 随便填(如 `skill-hub`),Expiration 选 90 天或 No expiration。
4. 勾选权限:只勾 **`public_repo`** 就够(只读公开仓库)。
5. 点 **Generate token**,复制那串 `ghp_...`。**只显示一次,先存好。**

> ⚠️ 不要把这串令牌发到聊天里或提交进代码,它等于你的钥匙。

---

## 三、把这个文件夹放上 GitHub

最简单(不用命令行):

1. 在 GitHub 点右上角 **+ → New repository**,名字填 `skill-hub`,选 **Public**,**Create**。
2. 新仓库页面点 **uploading an existing file**。
3. 把本文件夹(`D:\ac-ir-controller\skill-hub`)里的所有文件拖进去:
   `index.html`、`curated.js`、`update_skills.py`、`SETUP.md`、以及 `.github` 文件夹。
   - 注意:网页拖拽有时会忽略 `.github` 文件夹。若没传上去,见文末「补传工作流」。
4. **Commit changes**。

> 会用 git / GitHub Desktop 的话,直接把这个文件夹初始化为仓库推上去即可。

---

## 四、把令牌存进仓库密钥

1. 进你的 `skill-hub` 仓库 → **Settings** → 左侧 **Secrets and variables → Actions**。
2. **New repository secret**。
3. Name 必须填:**`SKILLS_TOKEN`**(和工作流里一致)。
4. Secret 粘贴第二步复制的 `ghp_...`,**Add secret**。

---

## 五、第一次手动跑起来

1. 仓库顶部 **Actions** 标签 → 若提示启用就点 **I understand... enable**。
2. 左侧选 **每日更新技能库** → 右侧 **Run workflow** → 绿色按钮。
3. 等几分钟(全网抓取较慢)。跑完后仓库里会多出 `skills.js`,技能数量大涨。
4. 之后每天 UTC 03:00(北京时间约 11:00)会自动重跑,你什么都不用管。

---

## 六、让网页能在线打开(可选,推荐)

1. 仓库 **Settings → Pages**。
2. Source 选 **Deploy from a branch**,Branch 选 **main / (root)**,**Save**。
3. 等一两分钟,页面会给你一个网址:`https://<你的用户名>.github.io/skill-hub/`。
   以后手机/电脑打开这个网址就是最新技能库。

> 不开 Pages 也行:直接双击本地的 `index.html` 一样能用,只是数据是上次同步下来的。

---

## 本地测试(可选,想先看效果)

在你自己的终端里(令牌不会进聊天记录):

PowerShell:
```powershell
cd D:\ac-ir-controller\skill-hub
$env:GITHUB_TOKEN="ghp_你的令牌"
python update_skills.py
```

跑完本地会生成 `skills.js`,双击 `index.html` 即可看到扩充后的库。

---

## 补传工作流(如果 .github 没传上去)

在仓库网页里:**Add file → Create new file**,文件名输入:
```
.github/workflows/update-skills.yml
```
把本地同名文件的内容粘进去,Commit 即可。

---

## 可调参数(在工作流的 env 里改)

- `MIN_STARS`:收录的 star 下限(默认 2,调高更精)。
- `MAX_REPOS`:单次最多处理的仓库数(默认 4000,防跑太久)。
