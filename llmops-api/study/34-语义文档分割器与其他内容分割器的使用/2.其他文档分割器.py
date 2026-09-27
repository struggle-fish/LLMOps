"""
@Time   : 2026/9/23 16:23
@Author : jzy
@File   : 2.其他文档分割器.py
"""
from langchain_text_splitters import HTMLHeaderTextSplitter

# 1.构建文本与分割标题
html_string = """
<!DOCTYPE html>
<html>
<body>
    <div>
        <h1>标题1</h1>
        <p>关于标题1的一些介绍文本。</p>
        <div>
            <h2>子标题1</h2>
            <p>关于子标题1的一些介绍文本。</p>
            <h3>子子标题1</h3>
            <p>关于子子标题1的一些文本。</p>
            <h3>子子标题2</h3>
            <p>关于子子标题2的一些文本。</p>
        </div>
        <div>
            <h2>子标题2</h2>  <!-- 修复：原来写错成 h3开头 h2闭合 -->
            <p>关于子标题2的一些文本。</p>
        </div>
        <br>
        <p>关于标题1的一些结束文本。</p>
    </div>
</body>
</html>
"""
headers_to_split_on = [
    ("h1", "一级标题"),
    ("h2", "二级标题"),
    ("h3", "三级标题"),
]
# 2.创建分割器并分割
text_splitter = HTMLHeaderTextSplitter(headers_to_split_on)
chunks = text_splitter.split_text(html_string)

# 3.输出分割内容（修改打印方式，查看内容+标题元数据）
for chunk in chunks:
    print("=" * 50)
    print(f"元数据: {chunk.metadata}")
    print(f"文本内容: {chunk.page_content}")
