app_name = "stock_entry_series"
app_title = "Stock Entry Series"
app_publisher = "Muhammad Yusuf Tri Daryanto"
app_description = "Automatically select Stock Entry naming series based on Stock Entry Type in ERPNext"
app_email = "114971841+Muhayustrid@users.noreply.github.com"
app_license = "mit"

required_apps = ["erpnext"]

doctype_js = {
	"Stock Entry": "public/js/stock_entry_form.js",
	"Material Request": "public/js/material_request_form.js"
}

doc_events = {
	"Stock Entry": {
		"before_insert": "stock_entry_series.overrides.stock_entry.set_naming_series"
	},
	"Material Request": {
		"before_insert": "stock_entry_series.overrides.material_request.set_naming_series"
	}
}

fixtures = [
	{
		"dt": "Custom Field",
		"filters": [
			["name", "in", ["Stock Entry Type-custom_naming_series"]]
		]
	}
]

before_migrate = "stock_entry_series.patches.v1_0.ensure_naming_series_map.ensure_module_def"
after_migrate = [
	"stock_entry_series.patches.v1_0.seed_stock_entry_series.execute",
	"stock_entry_series.patches.v1_0.ensure_naming_series_map.execute",
]

# install-app on Frappe Cloud does not run migrate; seed right after the
# app's doctypes and fixtures are synced instead.
after_sync = [
	"stock_entry_series.patches.v1_0.seed_stock_entry_series.execute",
	"stock_entry_series.patches.v1_0.ensure_naming_series_map.execute",
]
