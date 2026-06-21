// 人工核实的精选技能(中文描述、已验证)。此文件不被抓取脚本覆盖。
// 字段:name/src/repo/path/cat/desc/kw  + verified/stars/url 由下方统一补齐
window.CURATED = [
  // ---- 官方 anthropics/skills ----
  {name:"docx", src:"off", repo:"anthropics/skills", path:"skills/docx", cat:"文档办公", desc:"创建/编辑 Word:目录、表格、页码、信头、批注、查找替换。", kw:["word","文档","报告","docx","公文"]},
  {name:"pdf", src:"off", repo:"anthropics/skills", path:"skills/pdf", cat:"文档办公", desc:"PDF 全套:读取提取、合并拆分、旋转、水印、填表单、加密、OCR。", kw:["pdf","文档","合并","表单","ocr"]},
  {name:"pptx", src:"off", repo:"anthropics/skills", path:"skills/pptx", cat:"文档办公", desc:"制作/编辑 PPT:模板、版式、图表、演讲者备注。", kw:["ppt","幻灯片","演示","pptx","汇报"]},
  {name:"xlsx", src:"off", repo:"anthropics/skills", path:"skills/xlsx", cat:"文档办公", desc:"Excel:公式、图表、透视表、清洗整理混乱数据。", kw:["excel","表格","数据","xlsx","公式"]},
  {name:"doc-coauthoring", src:"off", repo:"anthropics/skills", path:"skills/doc-coauthoring", cat:"文档办公", desc:"与你协作共同撰写长文档。", kw:["文档","协作","写作","共创"]},
  {name:"internal-comms", src:"off", repo:"anthropics/skills", path:"skills/internal-comms", cat:"文档办公", desc:"撰写企业内部沟通、公告、通知。", kw:["沟通","公告","企业","通知"]},
  {name:"claude-api", src:"off", repo:"anthropics/skills", path:"skills/claude-api", cat:"开发编程", desc:"Claude API/SDK 参考:模型 id、价格、参数、工具调用、缓存。", kw:["api","模型","开发","sdk","anthropic"]},
  {name:"mcp-builder", src:"off", repo:"anthropics/skills", path:"skills/mcp-builder", cat:"开发编程", desc:"构建高质量 MCP 服务器,把外部系统接入 Claude。", kw:["mcp","集成","服务器","对接"]},
  {name:"webapp-testing", src:"off", repo:"anthropics/skills", path:"skills/webapp-testing", cat:"开发编程", desc:"用 Playwright 测试网页应用,做 UI 验证与调试。", kw:["测试","网页","playwright","ui","验证"]},
  {name:"web-artifacts-builder", src:"off", repo:"anthropics/skills", path:"skills/web-artifacts-builder", cat:"开发编程", desc:"构建复杂网页 artifact(React + Tailwind + shadcn/ui)。", kw:["网页","react","artifact","前端"]},
  {name:"frontend-design", src:"off", repo:"anthropics/skills", path:"skills/frontend-design", cat:"设计创意", desc:"前端界面设计与布局指导。", kw:["前端","ui","界面","设计","网页"]},
  {name:"canvas-design", src:"off", repo:"anthropics/skills", path:"skills/canvas-design", cat:"设计创意", desc:"画布式视觉设计与排版。", kw:["设计","画布","排版","视觉"]},
  {name:"theme-factory", src:"off", repo:"anthropics/skills", path:"skills/theme-factory", cat:"设计创意", desc:"生成主题与配色方案。", kw:["主题","配色","theme","样式"]},
  {name:"algorithmic-art", src:"off", repo:"anthropics/skills", path:"skills/algorithmic-art", cat:"设计创意", desc:"用代码生成算法/生成式艺术图案。", kw:["艺术","生成","图案","art","创意"]},
  {name:"brand-guidelines", src:"off", repo:"anthropics/skills", path:"skills/brand-guidelines", cat:"设计创意", desc:"按品牌规范(配色/字体/logo)产出统一材料。", kw:["品牌","设计","branding","规范"]},
  {name:"slack-gif-creator", src:"off", repo:"anthropics/skills", path:"skills/slack-gif-creator", cat:"设计创意", desc:"为 Slack 制作动图 GIF。", kw:["gif","slack","动图"]},
  {name:"skill-creator", src:"off", repo:"anthropics/skills", path:"skills/skill-creator", cat:"技能开发", desc:"从零创建、修改、优化 skill,并测试触发准确率。", kw:["skill","技能","创建","制作"]},

  // ---- 社区 obra/superpowers(开发工作流)----
  {name:"test-driven-development", src:"sp", repo:"obra/superpowers", path:"skills/test-driven-development", cat:"工作流·质量", desc:"TDD 红-绿-重构:先写失败测试,再实现,再重构。", kw:["测试","tdd","开发","重构"]},
  {name:"systematic-debugging", src:"sp", repo:"obra/superpowers", path:"skills/systematic-debugging", cat:"工作流·质量", desc:"系统化排错四阶段:复现、隔离、定位、验证修复。", kw:["调试","排错","debug","bug"]},
  {name:"using-git-worktrees", src:"sp", repo:"obra/superpowers", path:"skills/using-git-worktrees", cat:"工作流·质量", desc:"用 git worktree 并行开发、快速切换上下文。", kw:["git","分支","worktree","并行"]},
  {name:"finishing-a-development-branch", src:"sp", repo:"obra/superpowers", path:"skills/finishing-a-development-branch", cat:"工作流·质量", desc:"开发分支收尾:合并/PR 决策,保持 git 历史干净。", kw:["git","合并","分支","pr"]},
  {name:"requesting-code-review", src:"sp", repo:"obra/superpowers", path:"skills/requesting-code-review", cat:"工作流·质量", desc:"提交前准备与 PR 最佳实践,生成规范 diff。", kw:["评审","review","pr","代码"]},
  {name:"receiving-code-review", src:"sp", repo:"obra/superpowers", path:"skills/receiving-code-review", cat:"工作流·质量", desc:"处理评审反馈,基于评论迭代改进。", kw:["评审","反馈","review"]},
  {name:"brainstorming", src:"sp", repo:"obra/superpowers", path:"skills/brainstorming", cat:"工作流·质量", desc:"苏格拉底式提问,精炼设计与功能构思。", kw:["头脑风暴","设计","构思","创意"]},
  {name:"writing-plans", src:"sp", repo:"obra/superpowers", path:"skills/writing-plans", cat:"工作流·质量", desc:"编写详细实现策略与架构文档。", kw:["计划","方案","架构","规划"]},
  {name:"executing-plans", src:"sp", repo:"obra/superpowers", path:"skills/executing-plans", cat:"工作流·质量", desc:"分批执行计划,带检查点便于跟踪与恢复。", kw:["执行","计划","检查点"]},
  {name:"subagent-driven-development", src:"sp", repo:"obra/superpowers", path:"skills/subagent-driven-development", cat:"工作流·质量", desc:"多智能体质量门控迭代,处理复杂任务。", kw:["智能体","多代理","subagent"]},
  {name:"dispatching-parallel-agents", src:"sp", repo:"obra/superpowers", path:"skills/dispatching-parallel-agents", cat:"工作流·质量", desc:"并行派发多个子代理同时干活。", kw:["并行","代理","subagent","调度"]},
  {name:"verification-before-completion", src:"sp", repo:"obra/superpowers", path:"skills/verification-before-completion", cat:"工作流·质量", desc:"标记完成前先验证修复确实生效。", kw:["验证","质量","完成"]},
  {name:"using-superpowers", src:"sp", repo:"obra/superpowers", path:"skills/using-superpowers", cat:"工作流·质量", desc:"superpowers 技能集的总入口与用法。", kw:["superpowers","入口","用法"]},
  {name:"writing-skills", src:"sp", repo:"obra/superpowers", path:"skills/writing-skills", cat:"技能开发", desc:"按最佳实践写 skill,正确的 YAML frontmatter。", kw:["skill","技能","编写"]},

  // ---- 社区 cloudflare/skills ----
  {name:"workers-best-practices", src:"cf", repo:"cloudflare/skills", path:"skills/workers-best-practices", cat:"开发编程", desc:"按生产最佳实践审查/编写 Cloudflare Workers 代码。", kw:["cloudflare","workers","最佳实践","部署"]},
  {name:"wrangler", src:"cf", repo:"cloudflare/skills", path:"skills/wrangler", cat:"开发编程", desc:"Cloudflare Wrangler CLI 的使用与配置。", kw:["cloudflare","wrangler","cli","部署"]},
  {name:"durable-objects", src:"cf", repo:"cloudflare/skills", path:"skills/durable-objects", cat:"开发编程", desc:"Cloudflare Durable Objects 开发模式。", kw:["cloudflare","durable","状态","存储"]},
  {name:"agents-sdk", src:"cf", repo:"cloudflare/skills", path:"skills/agents-sdk", cat:"开发编程", desc:"Cloudflare Agents SDK 构建智能体应用。", kw:["cloudflare","agents","sdk","智能体"]},
  {name:"sandbox-sdk", src:"cf", repo:"cloudflare/skills", path:"skills/sandbox-sdk", cat:"开发编程", desc:"Cloudflare Sandbox SDK 的使用。", kw:["cloudflare","sandbox","sdk"]},
  {name:"web-perf", src:"cf", repo:"cloudflare/skills", path:"skills/web-perf", cat:"开发编程", desc:"网页性能优化(加载、渲染、指标)。", kw:["性能","web","优化","perf"]},
  {name:"turnstile-spin", src:"cf", repo:"cloudflare/skills", path:"skills/turnstile-spin", cat:"开发编程", desc:"集成 Cloudflare Turnstile 人机验证。", kw:["cloudflare","turnstile","验证","captcha"]},
  {name:"cloudflare-email-service", src:"cf", repo:"cloudflare/skills", path:"skills/cloudflare-email-service", cat:"开发编程", desc:"Cloudflare 邮件服务集成。", kw:["cloudflare","email","邮件"]},
  {name:"cloudflare-one", src:"cf", repo:"cloudflare/skills", path:"skills/cloudflare-one", cat:"开发编程", desc:"Cloudflare One(Zero Trust)配置。", kw:["cloudflare","zero trust","安全","网络"]},
  {name:"cloudflare-one-migrations", src:"cf", repo:"cloudflare/skills", path:"skills/cloudflare-one-migrations", cat:"开发编程", desc:"迁移到 Cloudflare One 的流程指引。", kw:["cloudflare","迁移","zero trust"]},
  {name:"cloudflare", src:"cf", repo:"cloudflare/skills", path:"skills/cloudflare", cat:"开发编程", desc:"Cloudflare 平台通用开发最佳实践。", kw:["cloudflare","平台","最佳实践"]},

  // ---- 社区 vercel-labs/skills ----
  {name:"find-skills", src:"vc", repo:"vercel-labs/skills", path:"skills/find-skills", cat:"技能开发", desc:"在你的项目里查找并推荐合适的 skill。", kw:["skill","查找","推荐","vercel"]},
].map(s => ({verified:true, stars:null, url:`https://github.com/${s.repo}/tree/main/${s.path}`, ...s}));
