# Stock Entry Series

Custom Frappe app for ERPNext with dynamic document naming series:

- **Stock Entry** — series configured per **Stock Entry Type** (field *Naming Series* on each Stock Entry Type).
- **Material Request** — series configured per **Material Request Type** via the `SERIES_MAP` in `stock_entry_series/overrides/material_request.py` (the type is a fixed Select field with no master doctype).

## Features
- **No Hardcoded Client Scripts**: picking a type auto-fills the matching series on the form.
- **Dual-Layer Guarantee**:
  - **Desk UI**: auto-fills `naming_series` the moment a type is picked.
  - **Server-Side Hook**: also applies to documents created via Data Import (Excel/CSV) or REST API.
- **Fallback**: Stock Entry falls back to `MAT-STE-.YYYY.-`, Material Request to `MAT-MR-.YYYY.-`.
- **Explicit wins**: a manually chosen series is never overridden.

## Example
- `Material Transfer` Stock Entry with series `MTR-.YY.-.####` names entries like `MTR-26-00001`.
- `Purchase` Material Request with series `MREQ-PUR-.YY.-.####` names requests like `MREQ-PUR-26-00001`.

## License
MIT
