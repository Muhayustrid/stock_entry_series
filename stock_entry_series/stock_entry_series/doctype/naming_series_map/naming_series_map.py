import frappe
from frappe.model.document import Document


class NamingSeriesMap(Document):
	def validate(self):
		self.type_value = (self.type_value or "").strip()

		duplicate = frappe.db.exists(
			"Naming Series Map",
			{
				"document_type": self.document_type,
				"type_value": self.type_value,
				"name": ["!=", self.name],
			},
		)
		if duplicate:
			frappe.throw(
				frappe._("A series mapping for {0} / {1} already exists.").format(
					frappe.bold(self.document_type), frappe.bold(self.type_value)
				)
			)
