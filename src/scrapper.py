from bs4 import BeautifulSoup
import requests
from pprint import pprint
import calendar
from src import logger
import httpx

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    )
}

base_url = "https://www.imdb.com"


async def get_top_matches(search_term):
    logger.info("Searching IMDb")

    url = f"{base_url}/find/?q={search_term}"

    # try:
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    
    matches = []

    for link in soup.select('a[href^="/title/"]'):
        title = link.get_text(strip=True)
        href = link["href"]

        if title:
            matches.append({"title": title, "link": href})

    return matches[:10]

    # except Exception as e:
    #     logger.error(f"Search failed: {e}")
    #     return []


async def get_movie_details(link, title):
    try:
        url = f"{base_url}{link}"
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")

        genre_div = [
            div for div in soup.find_all("div") if div.get("data-testid") == "interests"
        ][0]
        genres = [genre.text for genre in genre_div.find_all("span")]

        plot = soup.find("p", {"data-testid": "plot"}).text

        # ratings
        try:
            rating_div = soup.find(
                "div", {"data-testid": "hero-rating-bar__aggregate-rating__score"}
            )
            rating = rating_div.find_all("span")[0].text
            try:
                rating = float(rating)
            except:
                rating = ""
        except AttributeError:
            rating = ""
            pass

        movie_type = soup.select("div > ul.sc-16bda17f-3 > li")[0].text

        # possible a tags containing the date
        a_tags = soup.find("li", {"data-testid": "title-details-releasedate"}).find_all(
            "a"
        )
        release_date = ""
        for i in range(1, 13):
            for a in a_tags:
                if a.text.split(" ")[0] == calendar.month_name[i]:
                    release_date = a.text.split("(")[0].strip()

        # finding countries of origin
        details_origin = soup.find("li", {"data-testid": "title-details-origin"}).find(
            "ul"
        )
        details_a_tags = details_origin.find_all("a")
        countries_of_origin = [a.text for a in details_a_tags]

        # language
        language = ""
        for lan in soup.find_all("a"):
            if lan["href"].startswith(
                "/search/title/?title_type=feature&primary_language="
            ):
                language = lan.text

        # creator
        creator = (
            soup.find("li", {"data-testid": "title-pc-principal-credit"}).find("a").text
        )

        # stars
        stars = []
        stars_container = soup.find_all(
            "li", {"data-testid": "title-pc-principal-credit"}
        )
        for container in stars_container:
            first_a_tag = container.find("a").text
            # print(first_a_tag)
            if first_a_tag.strip().lower() == "stars":
                a_tags = container.find_all("a")
                # print(a_tags)
                stars = [
                    star.text for star in a_tags if star["href"].startswith("/name/")
                ]

        # trailer title
        trailer_title = soup.find("div", {"data-testid": "video-player-slate-overlay"})[
            "aria-label"
        ]

        featured_img = soup.find("div", {"data-testid": "hero-media__poster"}).find(
            "img"
        )["src"]

        details = {
            "title": title,
            "type": movie_type,
            "rating": rating,
            "genres": genres,
            "plot": plot,
            "release_date": release_date,
            "countries_of_origin": countries_of_origin,
            "language": language,
            "creator": creator,
            "stars": stars,
            "trailer_link": f"{url}?ref_=ext_shr_lnk",
            "trailer_title": trailer_title,
            "featured_image": featured_img,
        }

        return details

    except Exception as e:
        return f"Error while trying to fetch details: {e}"
