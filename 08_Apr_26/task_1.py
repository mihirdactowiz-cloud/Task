import json
from validation import ZomatoData

with open("data.json", "r") as f:
    data = json.load(f)

all_data = data.get('page_data').get('sections')
SECTION_RES_CONTACT = all_data.get("SECTION_RES_CONTACT")
SECTION_BASIC_INFO = all_data.get('SECTION_BASIC_INFO')
SECTION_RES_HEADER_DETAILS = all_data.get('SECTION_RES_HEADER_DETAILS')
menus = data.get('page_data').get('order').get('menuList').get('menus')

restaurant_id = SECTION_BASIC_INFO.get('res_id')
restaurant_name = SECTION_BASIC_INFO.get('name')
restaurant_url  = data.get('page_info').get('canonicalUrl')
restaurant_contact = SECTION_RES_CONTACT.get("phoneDetails").get("phoneStr")
fssai_licence_number = ""

full_address =  SECTION_RES_CONTACT.get('address')
region =  SECTION_RES_CONTACT.get('country_name')
city = SECTION_RES_CONTACT.get('city_name')
pincode =  SECTION_RES_CONTACT.get('zipcode')
state =  ""

CUISINES = []

for item in SECTION_RES_HEADER_DETAILS.get('CUISINES'):
    temp = {
        'name' : item.get('name'),
        'url' : item.get('url')
    }
    CUISINES.append(temp)

Time = SECTION_BASIC_INFO.get('timing').get('customised_timings').get('opening_hours')[0].get('timing')
if "–" in Time:
    fulltimes = Time.split("–")
    op = fulltimes[0].strip()
    close = fulltimes[1].strip()
else:
    op = Time.strip()
    close = Time.strip()
timings={
    "monday": {
        "open": op,
        "close": close
    },
    "tuesday": {
        "open": op,
        "close": close
    },
    "wednesday": {
        "open": op,
        "close": close
    },
    "thursday": {
        "open": op,
        "close": close
    },
    "friday": {
        "open": op,
        "close": close
    },
    "saturday": {
        "open": op,
        "close": close
    },
    "sunday": {
        "open": op,
        "close": close
    }
}
menu_categories = []
for item in menus:
    categories = item.get('menu').get('categories')
    items = []
    for category in categories:
        for subitem in category.get('category').get('items'):
            ite=subitem.get('item')
            temp_item = {
                "item_id": ite.get("id"),
                "item_name": ite.get("name"),
                "item_slugs": ite.get("tag_slugs"),
                "item_url": "",  
                "item_description": ite.get("desc"),
                "item_price": None,  
                "is_veg": True if ite.get('dietary_slugs')[0] == "veg" else False
            }
            items.append(temp_item)

    categories = {
        "category_name": item.get('menu').get('name'),
        "items": items
    }
    menu_categories.append(categories)

Zomato = {
        "restaurant_id":restaurant_id,
        "restaurant_name":restaurant_name,
        "restaurant_url":restaurant_url,
        "restaurant_contact":restaurant_contact,
        "fssai_licence_number":fssai_licence_number,
        "address_info":{
        "full_address":full_address,
        "region":region,
        "city":city,
        "pincode":pincode,
        "state":state
    },
    "cuisines":CUISINES,
    "timings":timings,
    "menu_categories":menu_categories
}

try:
    validated_data = ZomatoData(**Zomato)
    print("Validation successful! The data conforms to the defined schema.")
    with open("output.json","w",encoding="utf-8") as f:
        data = json.dump(Zomato,f)
except Exception as e:
    print("Validation failed! The data does not conform to the defined schema.")
    print("Error details:", e)