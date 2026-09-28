import frappe

DEFAULT_SERIES = "MAT-STE-.YYYY.-"


def set_naming_series(doc, method=None):
	"""Set doc.naming_series based on Stock Entry Type before insert.

	Ensures Stock Entries created via Desk, Data Import, or API follow the
	naming series configured on their Stock Entry Type.
	"""
	if not doc.stock_entry_type:
		return

	type_series = frappe.db.get_value("Stock Entry Type", doc.stock_entry_type, "custom_naming_series")
	target_series = type_series or DEFAULT_SERIES

	# Only override when the series is empty or still the generic default;
	# an explicitly chosen series is respected.
	if not doc.naming_series or doc.naming_series == DEFAULT_SERIES:
		doc.naming_series = target_series
