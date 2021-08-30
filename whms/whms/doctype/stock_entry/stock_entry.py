# Copyright (c) 2021, Dhinesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
def wh_qnt(qt,warehouse):
	t=0
	wh_qt=frappe.db.get_value("WH",{"wh_name":warehouse},"wh_qt")
	if(wh_qt-qt>=0):
		#frappe.db.set_value("WH",{"wh_name":warehouse},"wh_qt",wh_qt-qt)
		t=(wh_qt-qt)
	return t





def add(warehouse,item,qt):
	C_WH_doc=frappe.get_doc("WH",warehouse)
	item_exist=frappe.db.get_value("WHi",{"item":item,"parent":warehouse})
	if item_exist:
		if(wh_qnt(qt,warehouse)):
			c_qt=frappe.db.get_value("WHi",{"item":item,"parent":warehouse},"qt")
			frappe.db.set_value("WHi",item_exist,"qt",c_qt+qt)
		else:
			frappe.throw("warehouse is full")
	else:
		qty = wh_qnt(qt,warehouse)
		if(qty):
			C_WH_doc.wh_qt = qty
			C_WH_doc.append("wh_item",{"item":item,"qt":qt,"parenttype":"WH","parentfeild":"wh_item"})
			C_WH_doc.save()
		else:
			frappe.throw("warehouse is full")

def remove(warehouse,item,qt):
	t=False
	wh_qt=frappe.db.get_value("WH",{"wh_name":warehouse},"wh_qt")
	#C_WH_doc=frappe.get_doc("WH",warehouse)
	item_exist=frappe.db.get_value("WHi",{"item":item,"parent":warehouse})
	if item_exist:
		c_qt=frappe.db.get_value("WHi",{"item":item,"parent":warehouse},"qt")
		if(c_qt>qt):
			frappe.db.set_value("WHi",item_exist,"qt",c_qt-qt)
			frappe.db.set_value("WH",{"wh_name":warehouse},"wh_qt",wh_qt+qt)
			frappe.msgprint("Changes are done")

			t=True	
		elif(c_qt==qt):
			frappe.db.set_value("WHi",item_exist,"qt",c_qt-qt)
			rappe.db.set_value("WH",{"wh_name":warehouse},"wh_qt",wh_qt+qt)
			frappe.msgprint("Changes are done")
			t=True
		else:
			frappe.msgprint("qty  avalibale for"+str(item)+" is"+str(c_qt))
	else:
		frappe.msgprint("warehouse have no  stock"+str(item))
	return t
def move(from_warehouse,to_warehouse,item,qt):
	if(remove(from_warehouse,item,qt)):
		add(to_warehouse,item,qt)

class stock_entry(Document):
	def on_submit(self):
		if self.type=="ADD":
			add(self.warehouse,self.item,self.qt)
			frappe.msgprint("Changes are done")
		elif self.type =="REMOVE":
			remove(self.warehouse,self.item,self.qt)
		else:
			move(self.from_warehouse,self.to_warehouse,self.item,self.qt)

