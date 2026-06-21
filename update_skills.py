#!/usr/bin/env python3
"""
Skill Hub 抓取脚本
------------------
用 GitHub 代码搜索找出全网公开的 SKILL.md,按 star 数过滤,读取技能的
name/description,自动分类,生成 skills.js(被网页读取)。

用法:
    设置环境变量 GITHUB_TOKEN(或 GH_TOKEN)后运行:
        python update_skills.py
    本地测试(PowerShell):  $env:GITHUB_TOKEN="ghp_xxx"; python update_skills.py
    本地测试(bash):        GITHUB_TOKEN=ghp_xxx python update_skills.py

令牌:GitHub → Settings → Developer settings → Personal access tokens →
     Tokens (classic) → 勾选 public_repo(只读公开仓库即可)。
"""
import os, re, sys, json, time, datetime, urllib.request, urllib.error, urllib.parse
import concurrent.futures as cf

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
MIN_STARS = int(os.environ.get("MIN_STARS", "2"))   # 质量门槛:star 下限
MAX_REPOS = int(os.environ.get("MAX_REPOS", "4000")) # 单次运行最多处理多少个仓库,防跑太久
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills.js")

VERIFIED = {"anthropics/skills", "obra/superpowers", "cloudflare/skills", "vercel-labs/skills"}
SRC_BY_REPO = {"anthropics/skills":"off", "obra/superpowers":"sp",
               "cloudflare/skills":"cf", "vercel-labs/skills":"vc"}

if not TOKEN:
    sys.exit("错误:未设置 GITHUB_TOKEN,无法调用 GitHub 代码搜索。请先生成令牌并设为环境变量。")

API = "https://api.github.com"
HDR = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
       "User-Agent": "skill-hub-crawler", "X-GitHub-Api-Version": "2022-11-28"}


def api_get(url, headers=None, retries=4):
    """带速率限制退避的 GET。返回 (status, data_or_text)。"""
    h = dict(headers or HDR)
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                ct = r.headers.get("Content-Type", "")
                body = r.read()
                return r.status, (json.loads(body) if "json" in ct else body.decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            # 403/429 = 速率限制,按返回头等待后重试
            if e.code in (403, 429):
                reset = e.headers.get("X-RateLimit-Reset")
                wait = 8 * (attempt + 1)
                if reset:
                    wait = max(wait, int(reset) - int(time.time()) + 2)
                wait = min(wait, 90)
                print(f"  速率限制,等待 {wait}s …", flush=True)
                time.sleep(wait)
                continue
            return e.code, e.read().decode("utf-8", "replace")[:200]
        except Exception as e:
            time.sleep(5)
            if attempt == retries - 1:
                return -1, str(e)
    return -1, "重试耗尽"


def search_code(query, cap=1000):
    """分页拉取代码搜索结果(GitHub 上限 1000/查询)。"""
    items = []
    for page in range(1, 11):  # 100 * 10 = 1000
        url = f"{API}/search/code?q={urllib.parse.quote(query)}&per_page=100&page={page}"
        st, data = api_get(url)
        if st != 200 or not isinstance(data, dict):
            print(f"  搜索失败 [{st}] {query!r}: {str(data)[:120]}", flush=True)
            break
        batch = data.get("items", [])
        items.extend(batch)
        total = data.get("total_count", 0)
        if page == 1:
            print(f"  查询 {query!r} 命中 total={total}", flush=True)
        if len(batch) < 100 or len(items) >= cap:
            break
        time.sleep(2.2)  # 代码搜索 30 次/分钟
    return items


def discover():
    """用多个 size 分桶突破 1000 上限,收集 (repo, path) 唯一集合。"""
    buckets = ["size:<300", "size:300..700", "size:700..1500",
               "size:1500..3500", "size:>3500"]
    found = {}  # (repo, path) -> html_url
    for b in buckets:
        for item in search_code(f"filename:SKILL.md {b}"):
            repo = item.get("repository", {}).get("full_name")
            path = item.get("path")
            if repo and path and path.split("/")[-1].lower() == "skill.md":
                found[(repo, path)] = item.get("html_url", "")
        time.sleep(2.2)
    print(f"代码搜索去重后:{len(found)} 个 SKILL.md", flush=True)
    return found


def repo_meta(repo):
    st, data = api_get(f"{API}/repos/{repo}")
    if st == 200 and isinstance(data, dict):
        return {"stars": data.get("stargazers_count", 0),
                "branch": data.get("default_branch", "main")}
    return {"stars": 0, "branch": "main"}


def raw_text(repo, branch, path):
    # raw 域名不计入 API 速率限制
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/{urllib.parse.quote(path)}"
    st, data = api_get(url, headers={"User-Agent": "skill-hub-crawler"})
    return data if st == 200 and isinstance(data, str) else ""


def parse_frontmatter(text):
    """从 SKILL.md 顶部 --- --- 块里取 name 与 description。"""
    if not text.lstrip().startswith("---"):
        return None, None
    t = text.lstrip()
    end = t.find("\n---", 3)
    block = t[3:end] if end != -1 else t[3:3000]
    name = desc = None
    lines = block.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"\s*name\s*:\s*(.+)", line)
        if m and name is None:
            name = m.group(1).strip().strip("'\"")
        m = re.match(r"\s*description\s*:\s*(.*)", line)
        if m and desc is None:
            val = m.group(1).strip()
            if val in (">", "|", ">-", "|-", ">+", "|+", ""):
                # 折叠/块标量:收集后续缩进行
                buf = []
                for nxt in lines[i + 1:]:
                    if re.match(r"\S", nxt):
                        break
                    buf.append(nxt.strip())
                desc = " ".join(x for x in buf if x)
            else:
                desc = val.strip("'\"")
    if desc:
        desc = re.sub(r"\s+", " ", desc)[:200]
    return name, desc


CAT_RULES = [  # 顺序=优先级,先匹配先归类(具体的放前面)
    ("文档办公", ["docx","pdf","pptx","xlsx","word","excel","powerpoint","document","spreadsheet","slide","resume","invoice","contract","letter","markdown","notion","report","报告","文档","表格","简历","合同","公文"]),
    ("数据·AI", ["data","sql","pandas","analytic","chart","visuali","dashboard","etl","dataset","bigquery","machine learning","ml ","llm","prompt","rag","embedding","openai","anthropic","gpt","model","ai ","neural","数据","分析","可视化","模型"]),
    ("安全", ["security","vulnerab","owasp","pentest","exploit","oauth","encrypt","secret","cve","compliance","threat","audit","firewall","malware","安全","漏洞","加密","合规","审计"]),
    ("设计创意", ["design","brand","theme","art","canvas","color","palette","ui","ux","figma","logo","icon","illustration","animation","设计","配色","艺术","图标","动画"]),
    ("工作流·质量", ["test","debug","review","git","plan","ci/cd","lint","tdd","refactor","commit","changelog","release","issue","pull request"," pr ","workflow","automation","测试","调试","评审","重构","自动化","流程"]),
    ("技能开发", ["skill-creator","writing-skill","skill creator","agent skill","subagent","mcp","创建技能","写技能"]),
    ("开发编程", ["api","sdk","code","deploy","server","backend","frontend","database","cloudflare","react","vue","svelte","next","node","python","golang","rust","java","docker","kubernetes","terraform","aws","gcp","azure","cli","部署","开发","编程","后端","前端"]),
]
def classify(name, desc):
    hay = f"{name} {desc}".lower()
    for cat, kws in CAT_RULES:
        if any(k in hay for k in kws):
            return cat
    return "其他"


def make_kw(name, repo):
    parts = re.split(r"[-_/ ]+", name.lower())
    owner = repo.split("/")[0].lower()
    kw = [p for p in parts if p][:4]
    if owner not in kw:
        kw.append(owner)
    return kw[:5]


def build_entry(repo, branch, path, html, verified, stars):
    text = raw_text(repo, branch, path)
    name, desc = parse_frontmatter(text)
    # 规范的 Agent Skill 必须有 name + description;否则多半是同名无关文件,跳过
    if not name or not desc:
        return None
    return {
        "name": name,
        "src": SRC_BY_REPO.get(repo, "ext"),
        "repo": repo,
        "path": path[:-len("/SKILL.md")] if path.lower().endswith("/skill.md") else path,
        "cat": classify(name, desc),
        "desc": desc,
        "kw": make_kw(name, repo),
        "verified": verified,
        "stars": stars,
        "url": html or f"https://github.com/{repo}/blob/{branch}/{path}",
    }


def main():
    found = discover()
    by_repo = {}
    for (repo, path), html in found.items():
        by_repo.setdefault(repo, []).append((path, html))

    repos = list(by_repo.keys())[:MAX_REPOS]
    workers = int(os.environ.get("WORKERS", "12"))
    print(f"涉及 {len(repos)} 个仓库,并发({workers})核 star(≥{MIN_STARS} 才收)…", flush=True)

    # 阶段一:并发查每个仓库的 star / 默认分支
    metas, done = {}, 0
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(repo_meta, r): r for r in repos}
        for fu in cf.as_completed(futs):
            metas[futs[fu]] = fu.result()
            done += 1
            if done % 300 == 0:
                print(f"  …已核 {done}/{len(repos)} 仓库", flush=True)

    # 过滤出通过 star 门槛的文件
    tasks = []
    for repo in repos:
        m = metas.get(repo, {"stars": 0, "branch": "main"})
        verified = repo in VERIFIED
        if not verified and m["stars"] < MIN_STARS:
            continue
        for path, html in by_repo[repo]:
            tasks.append((repo, m["branch"], path, html, verified, m["stars"]))

    print(f"过 star 门槛 {len(tasks)} 个文件,并发({workers})读取与解析…", flush=True)

    # 阶段二:并发读取 SKILL.md 并解析(raw 不计 API 限额,可放心并发)
    out, done = [], 0
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for res in ex.map(lambda t: build_entry(*t), tasks):
            done += 1
            if res:
                out.append(res)
            if done % 400 == 0:
                print(f"  …已读 {done}/{len(tasks)},已收 {len(out)} 个", flush=True)

    # 排序:已验证优先,再按 star 降序
    out.sort(key=lambda s: (not s["verified"], -s["stars"], s["name"].lower()))

    meta = {"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "count": len(out), "min_stars": MIN_STARS, "source": "GitHub code search"}
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("// 自动生成,请勿手改。由 update_skills.py 每日重建。\n")
        f.write("window.SKILLS_META = " + json.dumps(meta, ensure_ascii=False) + ";\n")
        f.write("window.CRAWLED = " + json.dumps(out, ensure_ascii=False) + ";\n")
    print(f"完成:写入 {len(out)} 个技能 → {OUT}", flush=True)


if __name__ == "__main__":
    main()
