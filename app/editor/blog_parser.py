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
1. 其中两个'---'之间的内容是header，必须按照此格式并注意冒号后的空格；
2. <summary>内容可选，如有<summary>需在最后一行添上'<!-- more -->'标记，如无则不能添加；
'''

import mistune


class BlogParser():
    def __init__(self, blog):
        self.lines = blog.split('\r\n')
        print(self.lines)
        self.header = {}
        self.summary = ''
        self.blog_text = ''
        self.blog_html = ''
        # 将'<!-- more -->'的行号初始化为0
        self.more_line_number = 0
        # 将header的开始行（第一个'---'）号初始化为0
        self.header_start = 0
        # 将header的结束行（第二个'---'）号初始化为0
        self.header_end = 0
        # 遍历每一行找到'<!-- more -->'的行号（从0开始）
        for line_number, line in enumerate(self.lines):
            if line == '---':
                self.header_end = line_number
            elif line == '<!-- more -->':
                self.more_line_number = line_number
                break
        # 直接执行获得header函数
        self.get_header()

    def get_header(self):
        if self.header_end > self.header_start:
            items = []
            # 遍历header内容的每一行
            for line in self.lines[self.header_start + 1:self.header_end]:
                try:
                    # 将header每一行的内容转换为header字典的键值对
                    items.append(line.split(': '))
                except:
                    pass
            self.header = dict(items)

    # 获得文章标题
    def get_title(self):
        return self.header.get('title', 'Title undefined.')

    # 获得文章创作时间
    def get_date(self):
        return self.header.get('date', 'Date undefined.')

    # 获得分类
    def get_categories(self):
        return self.header.get('categories', [])

    # 获得标签
    def get_tags(self):
        return self.header.get('tags', [])

    def get_summary(self):
        # summary 应该写在header下面，并以header的下一行为默认起点
        if not self.summary:
            if self.more_line_number and self.more_line_number > self.header_end:
                self.summary = ''.join(
                    self.lines[self.header_end + 1:self.more_line_number])
        else:
            self.summary = 'No summary available.'
        return self.summary

    def get_blog_text(self):
        # 正文内容从'<!-- more -->'标记下一行开始直到结束
        if not self.blog_text:
            self.blog_text = '\n'.join(self.lines[self.more_line_number + 1:])
        return self.blog_text

    # 获得富文本正文
    def get_blog_html(self):
        if not self.blog_html:
            # 如果还没有获得纯文本正文先获得纯文本正文
            if not self.blog_text:
                self.blog_text = self.get_blog_text()
            # 初始化markdown解析器
            markdown = mistune.Markdown()
            # 利用markdown解析器将markdown转换为html
            self.blog_html = markdown(self.blog_text)
        return self.blog_html
