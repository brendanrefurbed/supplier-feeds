# Supplier Feeds — Pat's Guitars

Automated daily sync of the Pat's Guitars product catalog from their Shopify store.

## How it works

A GitHub Actions workflow runs daily at **05:00 UTC** (`daily_sync.yml`). It:

1. Installs Python dependencies (`requests`, `openpyxl`).
2. Runs `scrape_patsguitars.py`, which paginates through the Shopify products JSON endpoint.
3. Outputs `patsguitars_listings.csv` and `patsguitars_listings.xlsx` with categorized product/variant data.
4. Commits any changes back to `main`.

You can also trigger the workflow manually from the **Actions** tab.

## Integrations team access

Always-current CSV (requires repo read access):

```
https://raw.githubusercontent.com/refurbed/supplier-feeds/main/patsguitars_listings.csv
```

## Columns

| Column | Description |
|---|---|
| product_id | Shopify product ID |
| title | Product name |
| vendor | Brand / vendor |
| product_type | Shopify product type |
| category | Derived: Electric, Acoustic, Bass, or Other |
| variant_id | Shopify variant ID |
| variant_title | Variant label (e.g. color/size) |
| sku | Vendor SKU |
| price | Variant price (EUR) |
| available | Stock availability |
| created_at | Product creation timestamp |
| updated_at | Last update timestamp |
| handle | Shopify URL slug |
| url | Full product page URL |

## Maintenance

- **Script**: `scrape_patsguitars.py` — edit categorization keywords in `CATEGORY_KEYWORDS` if Pat's adds new instrument types.
- **Schedule**: change the cron in `.github/workflows/daily_sync.yml`.
- **Dependencies**: `requirements.txt` — bump versions as needed.
- **If the Shopify endpoint changes**: Pat's Guitars uses the standard Shopify `/products.json` public API. If they move to a custom storefront or require auth, the script will need updating.

## Handover notes

- No secrets or API keys are required; the Shopify products JSON endpoint is public.
- The workflow uses the built-in `GITHUB_TOKEN` for commits — no PAT needed.
- The `cache/` directory is gitignored (reserved for future local caching).
- To add another supplier, duplicate the scrape script pattern and add a new workflow step or a separate workflow file.
