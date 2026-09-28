import frappe

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

	# Only override when the series is empty or still the generic default;
	# an explicitly chosen series is respected.
	if not doc.naming_series or doc.naming_series == DEFAULT_SERIES:
		doc.naming_series = target_series
