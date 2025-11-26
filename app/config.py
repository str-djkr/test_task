import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://popuser:poppass@db:5432/population_db")
SOURCE_URL = os.environ.get(
    "SOURCE_URL",
    "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_%28United_Nations%29&oldid=1215058959",
)
