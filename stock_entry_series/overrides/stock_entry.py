import frappe
from frappe.model.naming import get_default_naming_series

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

	field_meta = frappe.get_meta("Stock Entry").get_field("naming_series")
	# The framework prefills naming_series with its own default at insert;
	# treat all of those as "not chosen". An explicitly chosen series is respected.
	replaceable = {
		"",
		(field_meta and field_meta.default) or "",
		get_default_naming_series("Stock Entry") or "",
		DEFAULT_SERIES,
	}
	if (doc.naming_series or "") in replaceable:
		doc.naming_series = target_series
