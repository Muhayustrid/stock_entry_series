import frappe
from frappe.model.naming import get_default_naming_series

DEFAULT_SERIES = "MAT-MR-.YYYY.-"

# Code-level fallback when no row exists in the "Naming Series Map" doctype
# (which is the UI-editable source of truth seeded by after_migrate).
SERIES_MAP = {
	"Purchase": "MREQ-PUR-.YY.-.####",
	"Material Transfer": "MREQ-MTR-.YY.-.####",
	"Material Issue": "MREQ-MIS-.YY.-.####",
	"Manufacture": "MREQ-MFG-.YY.-.####",
	"Subcontracting": "MREQ-SBC-.YY.-.####",
	"Customer Provided": "MREQ-CUS-.YY.-.####",
}


def get_series_for_type(material_request_type):
	"""UI map first, code map second, generic default last."""
	series = None
	if frappe.db.table_exists("Naming Series Map"):
		series = frappe.db.get_value(
			"Naming Series Map",
			{"document_type": "Material Request", "type_value": material_request_type},
			"naming_series",
		)
	return series or SERIES_MAP.get(material_request_type, DEFAULT_SERIES)


def set_naming_series(doc, method=None):
	"""Set doc.naming_series based on material_request_type before insert.

	Ensures Material Requests created via Desk, Data Import, or API follow
	the series configured for their type.
	"""
	if not doc.material_request_type:
		return

	target_series = get_series_for_type(doc.material_request_type)

	field_meta = frappe.get_meta("Material Request").get_field("naming_series")
	# The framework prefills naming_series with its own default at insert;
	# treat all of those as "not chosen". An explicitly chosen series is respected.
	replaceable = {
		"",
		(field_meta and field_meta.default) or "",
		get_default_naming_series("Material Request") or "",
		DEFAULT_SERIES,
	}
	if (doc.naming_series or "") in replaceable:
		doc.naming_series = target_series
