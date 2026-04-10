import json
import jmespath

with open("air_bnb.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("air_bnb2.json", "r", encoding="utf-8") as f:
    data1 = json.load(f)

with open("airbnb_review.json","r",encoding="utf-8") as f:
    data3 = json.load(f)

d = jmespath.search("niobeClientData[0][1].data.presentation.stayProductDetailPage.sections", data)
demo  =  jmespath.search("data.presentation.stayProductDetailPage.sections.sbuiData.sectionConfiguration.root",data1)

#img_1
Hotelname = jmespath.search("sections[21].section.listingTitle", d).split("|")[2].strip()
title =  jmespath.search("sections[0].sectionData.title", demo)
capacityName = jmespath.search("sections[0].sectionData.overviewItems[].title", demo)

capasity = []
for i in capacityName:
    temp = i.split(" ")
    num = temp[0]
    name = temp[1]
    temp1 = {name:num}
    capasity.append(temp1)

capasity = [{name: int(num) if num.isdigit() else num} for item in capacityName for num, name in [item.split(" ")]]
rating = jmespath.search("sections[0].sectionData.reviewData.ratingText", demo)
review = jmespath.search("sections[0].sectionData.reviewData.reviewCount", demo)

profile_url = jmespath.search("sections[1].sectionData.hostAvatar.avatarImage.baseUrl", demo)
name = jmespath.search("sections[1].sectionData.title", demo)
Years = jmespath.search("sections[1].sectionData.overviewItems[0].title", demo)
profile = {"profile_name": name, "year_of_experience": Years, "profile_url": profile_url}

highlights = jmespath.search("sections[17].section.highlights[].{ title: title, subtitle: subtitle }",d)

description = jmespath.search("sections[18].section.htmlDescription.htmlText", d)

discounted_price =  jmespath.search("data.presentation.stayProductDetailPage.sections.sections[1].section.structuredDisplayPrice.primaryLine.discountedPrice", data1)
original_price = jmespath.search("data.presentation.stayProductDetailPage.sections.sections[1].section.structuredDisplayPrice.primaryLine.originalPrice", data1)
price_type = jmespath.search("data.presentation.stayProductDetailPage.sections.sections[1].section.structuredDisplayPrice.primaryLine.qualifier", data1)
paymentDetails = {"currency": "INR", "discounted_price": int(discounted_price.replace("₹", "").replace(",", "")), "original_price": int(original_price.replace("₹", "").replace(",", "")),                                "price_unit": price_type}

#img_2
amenities = jmespath.search("niobeClientData[0][1].data.presentation.stayProductDetailPage.sections.sections[20].section.seeAllAmenitiesGroups[].{ category: title, amenities: amenities[].title }",data)

#img_3
Start = jmespath.search("data.presentation.stayProductDetailPage.reviews",data3)
reviewsNames = jmespath.search("reviews[].reviewer.firstName",Start)
reviewsDates = jmespath.search("reviews[].localizedDate",Start)
reviewsRating = jmespath.search("reviews[].rating",Start)
reviewsComments = jmespath.search("reviews[].commentV2",Start)

FinalReviews = []

for i in range(len(reviewsNames)) : 
    temp = {
        "name" : reviewsNames[i],
        "rating" : reviewsRating[i],
        "date" : reviewsDates[i],
        "Comments" :reviewsComments[i]
    }
    FinalReviews.append(temp)

#img_4
profile_data = jmespath.search( "niobeClientData[0][1].data.presentation.stayProductDetailPage.sections.sections[5].section.cardData.{ name: name, stats: stats[].value}", data)
keys = ["Reviews", "Rating", "Years hosting"]
ProfileDetails = {
    "name": profile_data["name"],
    "details": {k: int(v) if v.isdigit() else float(v) for k, v in zip(keys, profile_data["stats"])}
}

#final result
FinalData = {
    "restaurantsname": Hotelname,
    "details": {
        "Title": title,
        "Capacity": capasity,
        "Rating": float(rating),
        "Review": int(review),
        "Profile": profile,
        "Highlights": highlights,
        "Description": description,
    },
    "paymentDetails" : paymentDetails,
    "Amenities": amenities,
    "Reviews": FinalReviews ,
    "Profile": ProfileDetails
}

with open("FinalData.json", "w", encoding="utf-8") as f:
    json.dump(FinalData, f, indent=4)