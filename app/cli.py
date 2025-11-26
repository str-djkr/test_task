import sys
from config import SOURCE_URL
from db import Database
from models import Country
from scraper import Scraper
from sqlalchemy import text


class DataLoader:
    def __init__(self, db: Database, source_url: str = SOURCE_URL):
        self.db = db
        self.scraper = Scraper(source_url)

    def run(self):
        print("Connecting to database...")
        self.db.connect()
        self.db.create_tables()
        print("Fetching and parsing data...")
        records = self.scraper.parse()
        print(f"Parsed {len(records)} records. Saving to DB...")
        session = self.db.get_session()
        try:
            # clear existing data from same source to avoid duplicates
            session.query(Country).filter(Country.source == self.scraper.source_url).delete()
            session.commit()
            for r in records:
                c = Country(name=r.name, region=r.region, population=r.population, source=r.source)
                session.add(c)
            session.commit()
            print("Saved.")
        finally:
            session.close()


class DataPrinter:
    def __init__(self, db: Database):
        self.db = db

    def run(self):
        print("Conn")
        self.db.connect()
        sql = text("""
        SELECT
          co.region AS region,
          SUM(co.population) AS total_population,
          (SELECT name FROM countries c2 WHERE c2.region = co.region ORDER BY population DESC LIMIT 1) AS max_country,
          (SELECT population FROM countries c3 WHERE c3.region = co.region ORDER BY population DESC LIMIT 1) AS max_population,
          (SELECT name FROM countries c4 WHERE c4.region = co.region ORDER BY population ASC LIMIT 1) AS min_country,
          (SELECT population FROM countries c5 WHERE c5.region = co.region ORDER BY population ASC LIMIT 1) AS min_population
        FROM countries co
        GROUP BY co.region
        ORDER BY COALESCE(SUM(co.population),0) DESC;
        """)
        session = self.db.get_session()
        try:
            result = session.execute(sql)
            for row in result:
                region = row.region if row.region is not None else "Unknown"
                print(region)
                print(row.total_population if row.total_population is not None else 0)
                print(row.max_country if row.max_country else "")
                print(row.max_population if row.max_population is not None else 0)
                print(row.min_country if row.min_country else "")
                print(row.min_population if row.min_population is not None else 0)
                print("")  # blank separator
        finally:
            session.close()


def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    cmd = sys.argv[1]
    db = Database()
    if cmd == "get_data":
        loader = DataLoader(db)
        loader.run()
    elif cmd == "print_data":
        printer = DataPrinter(db)
        printer.run()
    else:
        print("Unknown command", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()
