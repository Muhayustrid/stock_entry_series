# Stock Entry Series

Custom Frappe app for ERPNext to dynamically set Stock Entry `naming_series` based on the selected `Stock Entry Type`.

## Features
- **Naming Series per Stock Entry Type**: Configure the series directly on each `Stock Entry Type` document (field **Naming Series**).
- **No Hardcoded Client Scripts**: Adding a new Stock Entry Type + series needs zero code changes.
- **Dual-Layer Guarantee**:
  - **Desk UI**: Auto-fills `naming_series` the moment a Stock Entry Type is picked on the Stock Entry form.
  - **Server-Side Hook**: Also applies to entries created via Data Import (Excel/CSV) or REST API.
- **Fallback**: Falls back to ERPNext default `MAT-STE-.YYYY.-` when the type has no series configured.

## Example
`Material Transfer` with series `MTR-.YY.-.####` names entries like `MTR-26-00001`.

## License
MIT
