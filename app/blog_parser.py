'''
BlogParser类试图从.md文件内容中提取并返回博客的标题，内容，标签，分类。摘要等信息
要求的.md文件格式：
---
title: <title>
date: <date>
categories: [<category1>(,category2, ...)]
tags: [<tag1>(,tag2, ...)]
---
[<summary>
<!-- more -->]
<blog-text>
注意：
1. 其中两个'---'之间的内容是header；
2. <summary>内容可选，如有<summary>需在最后一行添上'<!-- more -->'标记，如无则不能添加；
'''
import re


def parse(body):
    body_pattern = r'^---([\s\S]*)---[\s\S]*?([\s\S]*)<!-- more -->([\s\S]*)$'
    header_pattern = r'^title:\s(.*?)[\r\n|\n|\r][\s\S]*?categories:\s+([\s\S]*?)[\r\n|\r|\n][\s\S]*?tags:\s+(.*?)$'
    title = ''
    category = ''
    tags = ''
    summary_text = ''
    content = ''
    header = ''
    try:
        m = re.match(body_pattern, body)
        header = m.group(1).strip()
        summary_text = m.group(2).strip()
        content = m.group(3).strip()
    except Exception as e:
        print(e, 'wrong match in body parsing.')
    try:
        m = re.match(header_pattern, header)
        title = m.group(1).strip()
        category = m.group(2).strip()
        tags = m.group(3).strip()
    except Exception as e:
        print(e, 'wrong match in header parsing.')

    return title, category, tags, summary_text, content
