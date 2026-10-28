# plot-debug-publish-skill

Claude Code Skill：B 站 / 抖音精选 / 小红书影视解说号「剧情Debug」的发布物料。

- **起标题**：参考同剧同类视频，按「大事件 / 吐槽判断 / 反问 / 身份」四个方向出候选，附抖音（≤30 字）和小红书（≤20 字）版本
- **做封面**：按定下的标题，用原片真实画面做 B 站 16:9（1920×1080）和竖版 3:4（1242×1656），HTML 模板 + Playwright 无头浏览器截图
- **出 tag**：B 站 ≤10、抖音精选最多 5、小红书 8–10，`scripts/check.py` 自动数个数、量标题长度

只出物料，不代替人发布。

```
SKILL.md              主流程
references/标题.md     标题写法和踩过的坑
references/封面.md     封面规格、风格、步骤
templates/cover.html  封面模板（16:9 + 3:4）
scripts/render_cover.cjs  无头浏览器截图
scripts/check.py      检查标题长度和 tag 个数
```

依赖：Node + Playwright（`@playwright/test` 全局安装，自带 chromium-headless-shell）、ffmpeg、macOS `sips`。
