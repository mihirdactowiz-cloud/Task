from lxml import html

with open("test.html", "r", encoding="utf-8") as f:
    data = html.fromstring(f.read())

# print(data.xpath("//div[@class='sidebar']/text()"))
all_data=data.xpath("//div[@class='button']//div/text()")
print(all_data)