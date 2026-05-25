import csv
import time

import openpyxl
import requests

BASE_URL = "https://www.patsguitars.de/collections/all/products.json"
PER_PAGE = 250
MAX_PAGES = 50
REQUEST_DELAY = 1.0

CATEGORY_KEYWORDS = {
    "Electric": ["electric", "strat", "tele", "les paul", "sg ", "jazzmaster", "jaguar", "explorer", "flying v"],
    "Acoustic": ["acoustic", "dreadnought", "parlor", "parlour", "folk guitar", "classical", "nylon"],
    "Bass": ["bass"],
}


def categorize(title: str, product_type: str) -> str:
    text = f"{title} {product_type}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return category
    return "Other"


def fetch_products() -> list[dict]:
    products = []
    page = 1
    while page <= MAX_PAGES:
        resp = requests.get(BASE_URL, params={"page": page, "limit": PER_PAGE}, timeout=30)
        resp.raise_for_status()
        batch = resp.json().get("products", [])
        if not batch:
            break
        products.extend(batch)
        page += 1
        time.sleep(REQUEST_DELAY)
    return products


def build_rows(products: list[dict]) -> list[dict]:
    rows = []
    for p in products:
        category = categorize(p.get("title", ""), p.get("product_type", ""))
        for v in p.get("variants", [{}]):
            rows.append({
                "product_id": p.get("id"),
                "title": p.get("title"),
                "vendor": p.get("vendor"),
                "product_type": p.get("product_type"),
                "category": category,
                "variant_id": v.get("id"),
                "variant_title": v.get("title"),
                "sku": v.get("sku"),
                "price": v.get("price"),
                "available": v.get("available"),
                "created_at": p.get("created_at"),
                "updated_at": p.get("updated_at"),
                "handle": p.get("handle"),
                "url": f"https://www.patsguitars.de/products/{p.get('handle')}",
            })
    return rows


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_xlsx(rows: list[dict], path: str) -> None:
    if not rows:
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pat's Guitars Catalog"
    fieldnames = list(rows[0].keys())
    ws.append(fieldnames)
    for row in rows:
        ws.append([row[k] for k in fieldnames])
    wb.save(path)


def main() -> None:
    print("Fetching products from Pat's Guitars...")
    products = fetch_products()
    print(f"Fetched {len(products)} products.")

    rows = build_rows(products)
    print(f"Expanded to {len(rows)} variant rows.")

    write_csv(rows, "patsguitars_listings.csv")
    print("Wrote patsguitars_listings.csv")

    write_xlsx(rows, "patsguitars_listings.xlsx")
    print("Wrote patsguitars_listings.xlsx")


if __name__ == "__main__":
    main()
