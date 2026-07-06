# Product Brand Disambiguation

The radar must distinguish between the company name, the public product brand, the ticker when public, and the underlying investable entity.

## Why this matters

Many AI companies are better known by their product than their legal company name.

Examples:

| Investable company | Public product / brand | Category | Status |
|---|---|---|---|
| Anysphere | Cursor | AI coding IDE / coding agent | Private |
| Nous Research | Hermes / DiStrO | Open-source models / decentralized training | Private |
| Apptronik | Apollo | Humanoid robot | Private |
| Agility Robotics | Digit | Warehouse robotics | Private |
| 1X Technologies | NEO | Humanoid home robot | Private |
| Arm Holdings | Arm Neoverse / Edge AI IP | Semiconductor IP | Public |
| UiPath | UiPath Business Automation Platform | RPA / agentic automation | Public |

## Data model logic

Use `company_product_mapping_seed.csv` as the canonical bridge between:

- company name;
- public name;
- flagship product;
- product category;
- comparable startup/segment;
- ticker;
- exchange;
- public/private status.

## Special case: Cursor

Cursor should be tracked as:

- Company: `Anysphere`
- Product: `Cursor`
- Segment: `AI Coding / Agentic Software Engineering`
- Status: private

Cursor is a product brand. Anysphere is the startup behind the product.

## Special case: Hermes

Hermes must be handled carefully because the name can refer to multiple AI projects.

Default mapping in this project:

- Company: `Nous Research`
- Product: `Hermes models / DiStrO`
- Segment: `AI Infrastructure / Open Source Models`
- Status: private

All Hermes-related entries should include a low or medium confidence score until manually verified.

## Upcoming events logic

Upcoming events should reference both company and product when useful.

Examples:

- `Anysphere / Cursor`: product release, pricing change, strategic partnership, acquisition option, IPO candidate.
- `Nous Research / Hermes`: model release, distributed training milestone, compute partnership.

## Rule

Never confuse product popularity with investability.

A product may be widely known, but the investable entity is the company or the public security behind it.
