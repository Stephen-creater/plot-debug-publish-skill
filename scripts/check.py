"""检查发布文案里的标题长度和 tag 数量，超了就报错（退出码 1）。

用法：python3 check.py <06_成片/作品名/发布文案.md>

认法：每个代码块归到它上面最近一行提到的平台（B 站 / 抖音 / 小红书），
那一行里有「标题」就按标题查长度，代码块里有 # 就按话题查个数，B 站不带 # 的逗号列表按标签查个数。
"""
import re, sys

LIMITS = {
    "B站": {"标题": 80, "tag": 10},
    "抖音": {"标题": 30, "tag": 5},
    "小红书": {"标题": 20, "tag": 10},
}


def platform(line):
    if "小红书" in line:
        return "小红书"
    if "抖音" in line:
        return "抖音"
    if re.search(r"B\s?站", line):
        return "B站"
    return None


def main(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    errors, report = [], []
    plat, label, in_block, block, section = None, "", False, [], ""
    for line in lines:
        if line.startswith("```"):
            if in_block:
                text = "\n".join(block).strip()
                if plat:
                    tags = re.findall(r"#[^\s#]+", text)
                    if tags:
                        n, lim = len(tags), LIMITS[plat]["tag"]
                        report.append(f"{plat} 话题 {n} 个（上限 {lim}）")
                        if n > lim:
                            errors.append(f"{plat} 话题 {n} 个，超过 {lim} 个：{' '.join(tags)}")
                    elif "标题" in label or ("标题" in section and "简介" not in label):
                        n, lim = len(text), LIMITS[plat]["标题"]
                        report.append(f"{plat} 标题 {n} 字（上限 {lim}）：{text}")
                        if n > lim:
                            errors.append(f"{plat} 标题 {n} 字，超过 {lim} 字：{text}")
                    elif plat == "B站" and "," in text and "\n" not in text:
                        n = len([t for t in text.split(",") if t.strip()])
                        report.append(f"B站 标签 {n} 个（上限 10）")
                        if n > 10:
                            errors.append(f"B站 标签 {n} 个，超过 10 个")
                block = []
            in_block = not in_block
            continue
        if in_block:
            block.append(line)
        elif line.strip():
            if line.startswith("## "):
                section = line
            p = platform(line)
            if p:
                plat, label = p, line
            elif plat and ("标题" in line or "话题" in line or "简介" in line or "正文" in line):
                label = line
            elif line.startswith("#"):
                plat, label = None, ""
    print("\n".join(report) or "没认出任何标题或话题，检查文案格式")
    if errors:
        print("\n问题：\n- " + "\n- ".join(errors))
        sys.exit(1)
    print("\n通过")


if __name__ == "__main__":
    main(sys.argv[1])
