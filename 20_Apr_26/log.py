import requests as re
import requests
from lxml import html
from urllib.parse import urljoin


base_url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest"

headers = {
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}

# response = re.get(base_url, headers=headers)

# tree = html.fromstring(response.text)

# links = tree.xpath('//div(contains[@class,"flex-container"]') # using the xpath
# print(len(links))

def get_all_movie_urls(url):
    main_url = "https://www.rottentomatoes.com/"

    all_movies = []

    api_url = "https://www.rottentomatoes.com/cnapi/browse/movies_in_theaters/sort:newest"

    while True:
        res = requests.get(api_url, headers=headers).json()

        grid = res.get("grid").get("list")
        page_info = res.get("pageInfo")

        for item in grid:
            media_url = item.get("mediaUrl")
            if media_url:
                full_url = urljoin(main_url, media_url)
                if full_url not in all_movies:
                    all_movies.append(full_url)

        end_cursor = page_info.get("endCursor")

        if not end_cursor:
            break

        api_url = f"https://www.rottentomatoes.com/cnapi/browse/movies_in_theaters/sort:newest?after={end_cursor}"

    return all_movies



    # while True:
    #     api_url = f'https://www.rottentomatoes.com/cnapi/browse/movies_in_theaters/sort:newest?after={unique_key}'
    #     other_page = find_url(api_url)
    #     cursor = other_page.get('pageInfo').get('endCursor')

    #     if not cursor:
    #         break

    #     unique_key = cursor

    #     all_movie_data.extend([{
    #         'movie_name':i.get('title'),
    #         'date':i.get('releaseDateText'),
    #         'image':i.get('posterUri'),
    #         'url':urljoin(main_url,i.get('mediaUrl'))
    #     } for i in other_page.get('grid').get('list')])

    
    # with open('all_movies.json','w',encoding='utf-8') as f:
    #     json.dump(all_movie_data,f,indent=4,default=str)

# main("https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest")

# find_url('https://www.rottentomatoes.com/cnapi/browse/movies_in_theaters/sort:newest?after=Mjg%3D')

