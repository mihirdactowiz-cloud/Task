import json
import jmespath
import requests
from lxml import html

# url = "https://www.igus.in/iglidur-ibh/sleeve-bearings/product-details/iglidur-glw-m?artnr=GLWSM-1012-10"

# header = {
#     "content-type": "text/html; charset=utf-8",
#     "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
# }

# response = requests.get(url, headers=header)

# if response.status_code == 200:
#     with open("page.html", "w", encoding="utf-8") as file:
#         file.write(response.text)  
#     print("HTML file saved successfully!")

# with open("new.html", "r", encoding="utf-8") as f:
#     data = f.read()

with open("output.json", "r", encoding="utf-8") as f:
    response = json.load(f)

# tree = html.fromstring(response.text)

# script = tree.xpath('string(.//script[@id="__NEXT_DATA__"]/text())')

# result = json.loads(script)

# with open("output.json", "w", encoding="utf-8") as f:
#     json.dump(result,f)

all_item =  jmespath.search("props.pageProps", response)

#img_1
image_url_1 = jmespath.search("akeneoProductData.assets[3].sources[0].uri", all_item)
image_url_2 = jmespath.search("akeneoProductData.assets[4].sources[0].uri", all_item)
Part_number = jmespath.search("articleNumber", all_item)
Material = jmespath.search("articleData.material.name", all_item)
Shape = jmespath.search("selectedShape.shapePath", all_item)
Dimensions = jmespath.search("articleData.dimensions", all_item) # DICT
Material_propertie = html.fromstring(jmespath.search("akeneoProductData.attributes.attr_USP.value",all_item))
Material_propertie = Material_propertie.xpath(".//li/text()")

#img_2
Product_descriptio = html.fromstring(jmespath.search("akeneoProductData.description",all_item))
Product_description = " ".join(Product_descriptio.xpath(".//text()"))

first_paragraph = Product_description.split("<br />")[:2]

Tecnical_data = {}
categories = [
    "Dimension",
    "Manufacturing_and_installation_tolerance",
    "General_propertie",
    "Mechanical_propertie",
    "Requirement",
    "Electricity_attribute",
    "Thermal_propertie"
]

for idx, cat_name in enumerate(categories):
    attributes = jmespath.search(f"technicalDataCategories[{idx}].attributes[]", all_item)
    if attributes:
        attributes_dict = {item['description']: item['value'] for item in attributes}
    else:
        attributes_dict = {}
    Tecnical_data[cat_name] = attributes_dict

final_output = {
    "Images": {
        "image_1": image_url_1,
        "image_2": image_url_2
    },
    "Part_number": Part_number,
    "Material": Material,
    "Shape": Shape,
    "Dimensions": Dimensions,
    "Material_properties": Material_propertie,
    "Product_description": first_paragraph,
    "Technical_data": Tecnical_data
}

with open("final_output.json", "w", encoding='utf-8') as f:
    json.dump(final_output, f)

print("Final done.")