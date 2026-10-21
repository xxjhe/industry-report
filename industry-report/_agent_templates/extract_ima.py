#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IMA 检索结果提取器：从 tool-results 存档 JSON 提取 标题/简介/media_id，输出 markdown。
用法: python extract_ima.py <result_file> <输出md路径> [关键词标签]
"""
import json, sys, os

def extract(fpath, outpath, tag=""):
    with open(fpath, encoding='utf-8') as f:
        d = json.load(f)
    items = d.get('searched_knowledge_list', [])
    lines = [f"# IMA 检索结果 {tag}", f"**源文件**: {os.path.basename(fpath)}", f"**命中数**: {len(items)}", ""]
    for i, it in enumerate(items, 1):
        k = it.get('knowledge', {})
        title = k.get('title', '')
        intro = k.get('introduction', '')[:200].replace('\n', ' ')
        mid = k.get('media_id', '')
        tw = k.get('time_wording', '')
        ct = k.get('create_time', '')
        lines.append(f"### {i}. [{tw}] {title}")
        if intro:
            lines.append(f"简介: {intro}")
        lines.append(f"media_id: `{mid}` | create_time: {ct}")
        lines.append("")
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"OK: {len(items)} 条 -> {outpath}")

if __name__ == '__main__':
    fpath = sys.argv[1]
    outpath = sys.argv[2]
    tag = sys.argv[3] if len(sys.argv) > 3 else ""
    extract(fpath, outpath, tag)
