import json
from bs4 import BeautifulSoup

# 文件路径
HTML_FILE = "index.html"
JSON_FILE = "index.json"
OUTPUT_FILE = "index_updated.html"  # 可覆盖 HTML_FILE

# 读取 JSON
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# 读取 HTML
with open(HTML_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 找到文章容器
container = soup.find("div", class_="page home", attrs={"data-home": "posts"})
if not container:
    print("未找到文章容器 div.page.home[data-home='posts']")
    exit(1)

# 清空旧文章
container.clear()

# 按 objectID 排序 JSON 内容，保证顺序
data_sorted = sorted(data, key=lambda x: x.get("objectID", ""))

# 生成 HTML 并插入
for item in data_sorted:
    article = soup.new_tag("article",
                           **{"class": "single summary", "itemscope": "", "itemtype": "http://schema.org/Article"})

    # 标题
    h1 = soup.new_tag("h1", **{"class": "single-title", "itemprop": "name headline"})
    a_title = soup.new_tag("a", href=item["uri"])
    a_title.string = item["title"]
    h1.append(a_title)
    article.append(h1)

    # 作者与日期
    meta_div = soup.new_tag("div", **{"class": "post-meta"})
    span_author = soup.new_tag("span", **{"class": "post-author"})
    a_author = soup.new_tag("a", href="/", title="Author", rel="author", **{"class": "author"})
    i_icon = soup.new_tag("i", **{"class": "fas fa-user-circle fa-fw", "aria-hidden": "true"})
    a_author.append(i_icon)
    a_author.append("Brian Liu")
    span_author.append(a_author)
    meta_div.append(span_author)
    meta_div.append(" ")  # &nbsp;
    span_date = soup.new_tag("span", **{"class": "post-publish"})
    span_date.append("published on ")
    time_tag = soup.new_tag("time", datetime=item["date"])
    time_tag.string = item["date"]
    span_date.append(time_tag)
    meta_div.append(span_date)
    article.append(meta_div)

    # 内容
    content_div = soup.new_tag("div", **{"class": "content"})
    content_div.append(BeautifulSoup(item["content"], "html.parser"))
    article.append(content_div)

    # Read More
    footer_div = soup.new_tag("div", **{"class": "post-footer"})
    a_read = soup.new_tag("a", href=item["uri"])
    a_read.string = "Read More"
    footer_div.append(a_read)
    article.append(footer_div)

    # 添加到容器
    container.append(article)

# 保存更新后的 HTML
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"HTML 已更新并保存到 {OUTPUT_FILE}")
