import frappe

MODULE_NAME = "Stock Entry Series"
APP_NAME = "stock_entry_series"

SEED_MAP = {
	"Purchase": "MREQ-PUR-.YY.-.####",
	"Material Transfer": "MREQ-MTR-.YY.-.####",
	"Material Issue": "MREQ-MIS-.YY.-.####",
	"Manufacture": "MREQ-MFG-.YY.-.####",
	"Subcontracting": "MREQ-SBC-.YY.-.####",
	"Customer Provided": "MREQ-CUS-.YY.-.####",
}


def execute():
	"""Seed Naming Series Map rows for Material Request types (UI-editable)."""
	ensure_module_def()

	for type_value, series in SEED_MAP.items():
		if not frappe.db.exists(
			"Naming Series Map", {"document_type": "Material Request", "type_value": type_value}
		):
			frappe.get_doc({
				"doctype": "Naming Series Map",
				"document_type": "Material Request",
				"type_value": type_value,
				"naming_series": series,
			}).insert(ignore_permissions=True)


def ensure_module_def():
	if not frappe.db.exists("Module Def", MODULE_NAME):
		frappe.get_doc({
			"doctype": "Module Def",
			"module_name": MODULE_NAME,
			"app_name": APP_NAME,
		}).insert(ignore_permissions=True)
