import frappe

DEFAULT_SERIES = "MAT-MR-.YYYY.-"

# material_request_type is a fixed Select field (no master doctype), so the
# per-type series lives here instead of on a master document. To change a
# series, edit this map and restart the containers.
SERIES_MAP = {
	"Purchase": "MREQ-PUR-.YY.-.####",
	"Material Transfer": "MREQ-MTR-.YY.-.####",
	"Material Issue": "MREQ-MIS-.YY.-.####",
	"Manufacture": "MREQ-MFG-.YY.-.####",
	"Subcontracting": "MREQ-SBC-.YY.-.####",
	"Customer Provided": "MREQ-CUS-.YY.-.####",
}


@frappe.whitelist()
def get_naming_series(material_request_type):
	"""Single source of truth for the client script."""
	return SERIES_MAP.get(material_request_type, DEFAULT_SERIES)


def set_naming_series(doc, method=None):
	"""Set doc.naming_series based on material_request_type before insert.

	Ensures Material Requests created via Desk, Data Import, or API follow
	the series configured for their type.
	"""
	if not doc.material_request_type:
		return

	target_series = SERIES_MAP.get(doc.material_request_type, DEFAULT_SERIES)

	# Only override when the series is empty or still the generic default;
	# an explicitly chosen series is respected.
	if not doc.naming_series or doc.naming_series == DEFAULT_SERIES:
		doc.naming_series = target_series
