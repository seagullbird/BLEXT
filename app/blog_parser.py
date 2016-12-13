# -*- coding: utf-8 -*-
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
1. 其中两个'---'之间的内容是header (必须是---)；
2. <summary>内容可选，如有<summary>需在最后一行添上'<!-- more -->'标记，如无则不能添加；
'''
import re
from app.exceptions import ParsingError
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class Blog_Parser():
    title = ''
    category = ''
    tags = ''
    summary_text = ''
    content = ''

    body = ''
    header = ''

    def __init__(self, input):
        self.input = input
        self.re_input = r'^[\s\S]*?---([\s\S]*?)---([\s\S]*)$'
        self.re_header = r'^[\s\S]*?title:\s*([\w\W]*?)\n[\s\S]*?(category|categories):\s*([\w\W]*?)\n[\s\S]*?tags:\s*[[]([\w\W]*?)[]][\s\S]*?$'
        self.re_body = r'^([\s\S]*?)<!-- more -->([\s\S]*?)$'
        self.parse()

    def parse(self):
        # 先尝试将输入分成 header 和 body（也许包含ummary）两部分
        m = re.match(self.re_input, self.input)
        try:
            self.header = m.group(1).strip()
            self.body = m.group(2).strip()
        except:
            self.body = self.input
            raise ParsingError('wrong when parsing input')
        # 尝试从 header 中提取 title， category，tags
        m = re.match(self.re_header, self.header)
        try:
            self.title = m.group(1).strip()
            # group(2)是 (category|categories)
            self.category = m.group(3).strip()
            self.tags = m.group(4).strip()
        except:
            raise ParsingError('wrong when parsing header')
        # 尝试从 body 中分出content和summary
        m = re.match(self.re_body, self.body)
        if m:
            self.summary_text = m.group(1).strip()
            self.content = m.group(2).strip()
        else:
            self.content = self.body

        # 验证长度
        for tag_name in self.tags:
            if len(tag_name) > 128:
                tag_name = tag_name[:128]
        if len(self.title) < 128:
            self.title = self.title[:128]
        if len(self.category) < 128:
            self.category = self.category[:128]
        return self.title, self.category, self.tags, self.summary_text, self.content


# subclass to highlight code block
class HighlightRenderer(mistune.Renderer):

    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


def parse_markdown(markdown_text):
    # renderer for code highlight
    renderer = HighlightRenderer()
    parser = mistune.Markdown(renderer=renderer)
    return parser(markdown_text)
