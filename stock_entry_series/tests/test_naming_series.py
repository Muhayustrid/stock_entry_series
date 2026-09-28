import frappe
from frappe.tests import IntegrationTestCase
from stock_entry_series.overrides.material_request import (
	SERIES_MAP as MR_SERIES_MAP,
	set_naming_series as set_mr_naming_series,
)
from stock_entry_series.overrides.stock_entry import DEFAULT_SERIES, set_naming_series


TEST_TYPE = "_Test SE Type With Series"
TEST_SERIES = "TSE-.YY.-.####"


def _ensure_test_type():
	if not frappe.db.exists("Stock Entry Type", TEST_TYPE):
		frappe.get_doc({
			"doctype": "Stock Entry Type",
			"__newname": TEST_TYPE,
			"purpose": "Material Transfer",
			"custom_naming_series": TEST_SERIES,
		}).insert(ignore_permissions=True)


class TestStockEntrySeries(IntegrationTestCase):
	def test_series_assigned_from_stock_entry_type(self):
		_ensure_test_type()
		doc = frappe.new_doc("Stock Entry")
		doc.stock_entry_type = TEST_TYPE
		set_naming_series(doc)
		self.assertEqual(doc.naming_series, TEST_SERIES)

	def test_series_not_overridden_when_explicit(self):
		doc = frappe.new_doc("Stock Entry")
		doc.stock_entry_type = "Material Transfer"
		doc.naming_series = "MY-OWN-.YY.-"
		set_naming_series(doc)
		self.assertEqual(doc.naming_series, "MY-OWN-.YY.-")

	def test_fallback_naming_series_for_type_without_series(self):
		type_name = "_Test SE Type No Series"
		if not frappe.db.exists("Stock Entry Type", type_name):
			frappe.get_doc({
				"doctype": "Stock Entry Type",
				"__newname": type_name,
				"purpose": "Material Transfer",
			}).insert(ignore_permissions=True)

		doc = frappe.new_doc("Stock Entry")
		doc.stock_entry_type = type_name
		set_naming_series(doc)
		self.assertEqual(doc.naming_series, DEFAULT_SERIES)

	def test_e2e_insert_uses_type_series(self):
		company = frappe.get_all("Company", pluck="name", limit=1)
		items = frappe.get_all("Item", pluck="name", limit=2)
		warehouses = frappe.get_all(
			"Warehouse",
			filters={"is_group": 0, "company": company[0]} if company else {"is_group": 0},
			pluck="name",
			limit=2,
		)
		if not (company and len(items) >= 1 and len(warehouses) >= 2):
			self.skipTest("Site lacks company/item/warehouses needed for e2e test")

		_ensure_test_type()
		series_prefix = "TSE-26-"
		series_before = frappe.db.sql(
			"SELECT `current` FROM `tabSeries` WHERE `name` = %s", series_prefix
		)
		series_before = series_before[0][0] if series_before else None

		doc = frappe.get_doc({
			"doctype": "Stock Entry",
			"stock_entry_type": TEST_TYPE,
			"company": company[0],
			"items": [{
				"item_code": items[0],
				"s_warehouse": warehouses[0],
				"t_warehouse": warehouses[1],
				"qty": 1,
				"basic_rate": 1000,
			}],
		}).insert(ignore_permissions=True)

		self.assertEqual(doc.naming_series, TEST_SERIES)
		self.assertTrue(doc.name.startswith(series_prefix))

		# keep site data and series counter clean
		frappe.delete_doc("Stock Entry", doc.name, force=True, ignore_permissions=True)
		if series_before is not None:
			frappe.db.sql(
				"UPDATE `tabSeries` SET `current` = %s WHERE `name` = %s", (series_before, series_prefix)
			)


class TestMaterialRequestSeries(IntegrationTestCase):
	def test_series_assigned_from_type(self):
		doc = frappe.new_doc("Material Request")
		doc.material_request_type = "Purchase"
		set_mr_naming_series(doc)
		self.assertEqual(doc.naming_series, MR_SERIES_MAP["Purchase"])

	def test_series_not_overridden_when_explicit(self):
		doc = frappe.new_doc("Material Request")
		doc.material_request_type = "Purchase"
		doc.naming_series = "MY-OWN-.YY.-"
		set_mr_naming_series(doc)
		self.assertEqual(doc.naming_series, "MY-OWN-.YY.-")

	def test_e2e_insert_uses_type_series(self):
		company = frappe.get_all("Company", pluck="name", limit=1)
		items = frappe.get_all("Item", pluck="name", limit=1)
		warehouses = frappe.get_all(
			"Warehouse",
			filters={"is_group": 0, "company": company[0]} if company else {"is_group": 0},
			pluck="name",
			limit=1,
		)
		if not (company and items and warehouses):
			self.skipTest("Site lacks company/item/warehouses needed for e2e test")

		series_prefix = "MREQ-PUR-26-"
		series_before = frappe.db.sql(
			"SELECT `current` FROM `tabSeries` WHERE `name` = %s", series_prefix
		)
		series_before = series_before[0][0] if series_before else None

		doc = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": "Purchase",
			"company": company[0],
			"items": [{
				"item_code": items[0],
				"qty": 1,
				"schedule_date": frappe.utils.add_days(None, 7),
				"warehouse": warehouses[0],
			}],
		}).insert(ignore_permissions=True)

		self.assertEqual(doc.naming_series, MR_SERIES_MAP["Purchase"])
		self.assertTrue(doc.name.startswith(series_prefix))

		# keep site data and series counter clean
		frappe.delete_doc("Material Request", doc.name, force=True, ignore_permissions=True)
		if series_before is not None:
			frappe.db.sql("UPDATE `tabSeries` SET `current` = %s WHERE `name` = %s", (series_before, series_prefix))
