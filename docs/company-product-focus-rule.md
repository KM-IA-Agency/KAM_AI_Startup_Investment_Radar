# Company Product Focus Rule

## Principle

The radar should display products and tools together with their owning company whenever possible.

Useful analysis unit:

```text
company_name -> product_or_tool
```

## Why

A product can be visible without being directly investable.
A company can own several products.
A public comparable can differ from the product brand.
A startup focus should therefore propagate through related views.

## UI rule

Tables should prefer showing:

- `company_name`
- product, tool, or brand name
- `company_product_label`

Recommended label format:

```text
company_name -> product_or_tool
```

## Startup focus propagation

The sidebar `Startup focus` should propagate to compatible tabs:

- AI Tools Stack
- Benchmark
- Forecasts
- Financial Timeline
- IPO and Actions
- Products and Events
- Startup Detail

When the selected company exists in the target table, the tab should default to that company.
If the selected company is absent, the tab should remain usable and show the full list.

## Implemented behavior

AI Tools Stack normalizes `company_name` and legacy `company_or_owner`, adds a company-product label, and can apply the sidebar focus.

Products and Events accepts the sidebar company focus and shows company-product labels.

IPO and Actions accepts the sidebar company focus when a matching public comparable exists.

Benchmark shows a focus benchmark block for the selected startup when metrics exist.

Startup Detail shows related tools and product mappings when available.

## Data rule

New tables and ingestion scripts should preserve both the company name and the product/tool/brand name.
