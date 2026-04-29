import asyncio
from pprint import pprint

from src.scrapper import get_top_matches, get_movie_details
from src import logger
from src.banner import banner


async def start():
    title = input("Enter the title of the movie you want to search for: ")
    logger.info(f"Searching for: {title}")
    matches = await get_top_matches(title)

    # pprint(matches)


if __name__ == "__main__":
    logger.info("Starting the IMDB Scrapper Bot...")
    banner("IMDB Scrapper")

    asyncio.run(start())
