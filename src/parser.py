from bs4 import BeautifulSoup
from config import RATING_MAP, DEFAULT_CURRENCY
from urllib.parse import urljoin


def parse_books(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    records = []
    BASE_SITE = "https://books.toscrape.com/catalogue/"

    for item in soup.find_all("article", {"class":"product_pod"}):
        try:
            title_tag = item.find("h3").find("a")
            title = title_tag.get("title", "").strip()
            relative_url = title_tag.get("href", "")
            product_url = urljoin(BASE_SITE, relative_url)
            price_el = item.find("p", class_="price_color")
            raw_price = price_el.get_text(strip=True) if price_el else ""
            raw_price = raw_price.replace("Â", "").strip()

            currency = raw_price[0] if raw_price else ""
            price_value = float(raw_price[1:].replace(",", "")) if raw_price else 0.0

            # Availability
            stock_el = item.find("p", class_="availability")
            stock_text = stock_el.get_text(" ", strip=True) if stock_el else ""
            in_stock = "In stock" in stock_text

            # Rating (digit)
            rating_tag = item.find("p", class_="star-rating")
            rating_word = rating_tag["class"][-1] if rating_tag else None
            rating = RATING_MAP.get(rating_word, 0)

            records.append({
                "Title": title,
                "Product URL": product_url,
                "Price": price_value,
                "Currency": currency,
                "Availability": stock_text,
                "InStock": in_stock,
                "Rating": rating
            })
        except Exception as err:
            print(f"[PARSE ERROR] {err}")

    return records


def has_next_page(html: str) -> bool:
    soup = BeautifulSoup(html, "lxml")
    return bool(soup.select_one("li.next"))
