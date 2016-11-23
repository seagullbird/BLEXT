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
    try:
        body_pattern = r'^---([\s\S]*)---[\s\S]*?([\s\S]*)<!-- more -->([\s\S]*)$'
        m = re.match(body_pattern, body)
        header = m.group(1).strip()
        print(header)
        summary_text = m.group(2).strip()
        content = m.group(3).strip()
        header_pattern = r'^title:\s(.*?)[\r\n|\n|\r][\s\S]*?categories:\s+([\s\S]*?)[\r\n|\r|\n][\s\S]*?tags:\s+(.*?)$'
        m = re.match(header_pattern, header)
        title = m.group(1)
        category = m.group(2)
        tags = m.group(3)
        return title, category, tags, summary_text, content
    except AttributeError as e:
        print(e)
        return '', '', '', '', ''
