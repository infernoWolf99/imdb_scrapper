"""
searches saved movies for movie details and prints them
scrapes for movie if not found in saved movies
"""
def find_movie_in_archive(title):
    if title is not None:
        data_path = "../data/output.json"