import json

Final = []
productLink = "https://www.bonkerscorner.com/products/"

# Load your JSON file
with open("bonker.json", "r") as f:
    data = json.load(f)
    products = data["products"]
    for i in range(len(data["products"])):
        productsName = products[i]["variants"][0]["name"].split(" - ")[0].strip()
        vendor = products[i]["vendor"]
        handle = products[i]["handle"]
        productUrl  = productLink + handle
        productPrice = int(products[i]["variants"][0]["price"]) / 100
        variantCount = len(products[i]["variants"])
        variantOptions = []
        variants = []
        for j in range(variantCount):
            variantOptions.append(products[i]["variants"][j]["public_title"])

            temp = {
                "variantName" :products[i]["variants"][j]["public_title"],
                "variantId" : products[i]["variants"][j]["id"],
                "variantUrl" : f"{productLink}{products[i]['handle']}?variant={products[i]['variants'][j]['id']}",
                "variantPrice" : int(products[i]["variants"][j]["price"])  / 100
            }
            variants.append(temp)

        optionValues =  [
            {
                "optionName": "Size",
                "optionValues": variantOptions
            }
        ]
        product = {
            "productName": productsName,
            "vendor": vendor,
            "productUrl": productUrl,
            "productPrice": productPrice,
            "variantCount": variantCount,
            "optionValues": optionValues,
            "variants": variants
        }
        Final.append(product)
        
    with open("output.json", "w") as f:
        json.dump(Final, f, indent=4)
