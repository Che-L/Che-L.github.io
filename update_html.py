import json
from bs4 import BeautifulSoup

# 文件路径
json_file = "index.json"
html_file = "index.html"
output_file = "index_updated.html"  # 可以改为 index.html 覆盖原文件

# 读取 JSON 数据
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 构建一个 dict，key 用 URI 或 title 方便查找
json_dict = {}
for item in data:
    json_dict[item["uri"]] = item["content"]

# 读取 HTML
with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 更新每个文章的内容
for article in soup.find_all("article", class_="single summary"):
    a_tag = article.find("a", href=True)
    if not a_tag:
        continue
    uri = a_tag['href']
    if uri in json_dict:
        content_div = article.find("div", class_="content")
        if content_div:
            content_div.clear()
            content_div.append(BeautifulSoup(json_dict[uri], "html.parser"))

# 写入更新后的 HTML
with open(output_file, "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"HTML 已更新，输出文件: {output_file}")
