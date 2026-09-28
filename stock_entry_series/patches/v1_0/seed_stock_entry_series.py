import frappe

SERIES_MAP = {
	"Material Issue": "ISS-.YY.-.####",
	"Material Receipt": "RCP-.YY.-.####",
	"Material Transfer": "MTR-.YY.-.####",
	"Manufacture": "MFG-.YY.-.####",
	"Repack": "RPK-.YY.-.####",
	"Disassemble": "DSA-.YY.-.####",
	"Send to Subcontractor": "STS-.YY.-.####",
	"Material Transfer for Manufacture": "MTF-.YY.-.####",
	"Material Consumption for Manufacture": "MCF-.YY.-.####",
	"Receive from Customer": "RFC-.YY.-.####",
	"Return Raw Material to Customer": "RRM-.YY.-.####",
	"Subcontracting Delivery": "SCD-.YY.-.####",
	"Subcontracting Return": "SCR-.YY.-.####",
}


def execute():
	"""Seed existing Stock Entry Types with their corresponding default naming series."""
	if not frappe.db.has_column("Stock Entry Type", "custom_naming_series"):
		return

	for stock_entry_type, series in SERIES_MAP.items():
		if frappe.db.exists("Stock Entry Type", stock_entry_type):
			current = frappe.db.get_value("Stock Entry Type", stock_entry_type, "custom_naming_series")
			if not current:
				frappe.db.set_value("Stock Entry Type", stock_entry_type, "custom_naming_series", series)
