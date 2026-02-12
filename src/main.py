from config import BASE_URL
from fetcher import get_html
from parser import parse_books, has_next_page
from writer import write_csv


def run():
    all_data = []
    page_no = 1

    print("[START] Scraping all available pages...")

    while True:
        url = BASE_URL.format(page_no)
        print(f"[SCRAPE] Page {page_no}")

        html = get_html(url)
        if not html:
            break

        page_data = parse_books(html)
        print(f"[SCRAPE] Extracted {len(page_data)} items")

        all_data.extend(page_data)

        if not has_next_page(html):
            print("[INFO] No more pages detected.")
            break

        page_no += 1

    write_csv(all_data, "output/books.csv")
    print(f"[DONE] Total books scraped: {len(all_data)}")


if __name__ == "__main__":
    run()
