import requests
import json
from urllib.parse import urljoin
from lxml import html

headers = {"User-Agent": "Mozilla/5.0"}

def extract_page_data(url):
    res = requests.get(url, headers=headers)
    return html.fromstring(res.text)

def process(url):
    data = extract_page_data(url)

    movie_name = data.xpath("string(//rt-text[@size='1.25,1.75']/text())")
    score = data.xpath("string(//rt-text[@slot='critics-score'])") or "0%"
    revie = data.xpath("string((//rt-link[@slot='critics-reviews']))").strip()
    desc = data.xpath("string(//div[@slot='description']//rt-text)").strip()
    img = data.xpath("string(//img[@slot='poster']/@src)")
    want_to_know = data.xpath("string(//div[@id='critics-consensus']//p)").strip() or None

    # CAST & CREW
    cast_url = url.rstrip("/") + "/cast-and-crew"
    cast_data = extract_page_data(cast_url)

    people = []
    cards = cast_data.xpath("//cast-and-crew-card")

    for card in cards:
        name = card.xpath("string(.//rt-text)").strip()

        credits = card.xpath(".//rt-text[contains(@slot,'credit') or contains(@class,'credit')]//text()")
        credits = [c.strip() for c in credits if c.strip()]

        person_img = card.xpath("string(.//rt-img/@src | .//rt-img/@data-src)")

        people.append({
            "name": name,
            "image": person_img,
            "credits": credits
        })

    # REVIEWS 
    main_url = 'https://www.rottentomatoes.com/'

    reviews_href = data.xpath("string(//section[@aria-labelledby='critics-reviews-label']//rt-button/@href)").strip()

    all_reviews = []

    if reviews_href:
        review_page_url = urljoin(main_url, reviews_href)

        review_html = requests.get(review_page_url, headers={"User-Agent": "Mozilla/5.0"}).text
        review_tree = html.fromstring(review_html)

        json_obj = review_tree.xpath("//script[@data-json='props']/text()")

        if json_obj:
            json_data = json.loads(json_obj[0])
            page_id = json_data.get("media").get("emsId")

            if page_id:
                review_api = f"https://www.rottentomatoes.com/napi/rtcf/v1/movies/{page_id}/reviews?after=&before=&pageCount=20&type=critic"

                res = requests.get(review_api, headers={"User-Agent": "Mozilla/5.0"})

                try:
                    review_json = res.json()

                    for r in review_json.get("reviews"):
                        all_reviews.append({
                            "name": (r.get("critic")).get("displayName"),
                            "publication": (r.get("publication")).get("name"),
                            "count": r.get("originalScore"),
                            "review": r.get("reviewQuote")
                        })

                except Exception as e:
                    print("API error:", e)
   
    # VIDEOS
    video_url = url.rstrip("/") + "/videos"
    video_data = extract_page_data(video_url)

    Videos = []
    cards = video_data.xpath("//div[@class='video-item']")

    for card in cards:
        name = card.xpath("string(.//a[@class='titlethumbnail'])").strip()
        name_url = card.xpath("string(.//a[@class='titlethumbnail']/@href)").strip()
        duration = card.xpath("string(.//span[contains(@class,'duration')])").strip()

        Videos.append({
            "name": name,
            "url": urljoin(url, name_url),
            "duration": duration
        })

    return {
        "movie_name": movie_name,
        "score": score,
        'review': revie,
        "description": desc,
        "image_url": img,
        "critics_consensus": want_to_know,
        "Cast_Crew": people,
        "reviews": all_reviews,
        "videos": Videos
    }
     
# RUN
# result = process("https://www.rottentomatoes.com/m/i_swear_2025")

# with open("movie_data.json", "w", encoding="utf-8") as f:
#     json.dump(result, f)