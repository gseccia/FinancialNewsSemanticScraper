from resources.gui.gen_query import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets


class QueryGUI(Ui_Dialog):

    def setupEvent(self):
        no_subgroup_item = QtWidgets.QListWidgetItem()
        self.subgroup_list.addItem(no_subgroup_item)
        item = self.subgroup_list.item(0)
        item.setText("No subgroup")
        self.generateButton.clicked.connect(self.generate_query)
        self.subgroup_list.currentItemChanged.connect(self.change_selected_item_color)
        self.order_list.currentItemChanged.connect(self.change_selected_item_color)
        self.limit_list.currentItemChanged.connect(self.change_selected_item_color)
        self.group_list.currentItemChanged.connect(self.change_selected_item_color)
        self.group_list.currentItemChanged.connect(self.add_subgroup_options)

    def change_selected_item_color(self, curr, prev):
        curr.setBackground(QtCore.Qt.red)
        if prev is not None:
            prev.setBackground(QtCore.Qt.transparent)

    def add_subgroup_options(self, curr, prev):
        self.subgroup_list.blockSignals(True)
        self.subgroup_list.clear()
        self.subgroup_list.blockSignals(False)
        if curr.text() == "Person":
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(0)
            item.setText("No subgroup")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(1)
            item.setText("NationalPersonality")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(2)
            item.setText("CompanyPersonality")
        elif curr.text() == "Country":
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(0)
            item.setText("No subgroup")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(1)
            item.setText("G20Counrty")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(2)
            item.setText("NonG20Country")
        elif curr.text() == "Company" or "Stock":
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(0)
            item.setText("No subgroup")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(1)
            item.setText("CommunicationServices")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(2)
            item.setText("ConsumerDiscretionary")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(3)
            item.setText("ConsumerStaples")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(4)
            item.setText("Energy")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(5)
            item.setText("Financials")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(6)
            item.setText("HealthCare")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(7)
            item.setText("InformationTechnology")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(8)
            item.setText("Materials")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(9)
            item.setText("NewsPublisher")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(10)
            item.setText("OtherEntity")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(11)
            item.setText("Utilities")
            item = QtWidgets.QListWidgetItem()
            self.subgroup_list.addItem(item)
            item = self.subgroup_list.item(12)
            item.setText("Real Estate")
        else:
            pass

    def generate_query(self):
        query_prefix = """
        PREFIX ont: <http://www.github.com/gseccia/FinancialNewsSemanticScraper/ontologies/FinancialNewsOntology#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        """
        items_group = self.group_list.selectedItems()
        items_subgroup = self.subgroup_list.selectedItems()
        items_order = self.order_list.selectedItems()
        items_limit = self.limit_list.selectedItems()
        if not (items_group and items_subgroup and items_order and items_limit):
            query = "Please select a field for each option"
        else:
            group = self.group_list.currentItem().text()
            subgroup = self.subgroup_list.currentItem().text()
            order = self.order_list.currentItem().text()
            limit = self.limit_list.currentItem().text()
            query = query_prefix
            if group == "Person":
                if subgroup == "NationalPersonality":
                    query = query + "\nSELECT ?person" \
                                    "\nWHERE { ?person rdf:type ont:Person\n " \
                                    "?person ont:isImportantPersonOf ?country\n" \
                                    "?country rdf:type ont:ISO3166DefinedCountry }\n" \
                                    "ORDER BY "+order+"(?person)\n" \
                                    "LIMIT "+limit
                elif subgroup == "CompanyPersonality":
                    query = query + "\nSELECT ?person" \
                                    "\nWHERE { ?person rdf:type ont:Person\n " \
                                    "?person ont:isImportantPersonOf ?company\n" \
                                    "?country rdf:type ont:Organization }\n" \
                                    "ORDER BY " + order + "(?person)\n" \
                                    "LIMIT " + limit
                else:
                    query = query + "\nSELECT ?person" \
                                    "\nWHERE { ?person rdf:type ont:Person }\n " \
                                    "ORDER BY " + order + "(?person)\n" \
                                    "LIMIT " + limit
            elif group == "Company":
                if subgroup == "No subgroup":
                    query = query + "\nSELECT ?company" \
                                    "\nWHERE { ?company rdf:type ?company_type\n " \
                                    "?company_type rfs:subclassOf ont:Organization }\n" \
                                    "ORDER BY " + order + "(?person)\n" \
                                    "LIMIT " + limit
                else:
                    query = query + "\nSELECT ?company" \
                                    "\nWHERE { ?company rdf:type ont:" + subgroup + "}\n " \
                                    "ORDER BY " + order + "(?company)\n" \
                                    "LIMIT " + limit
            elif group == "Country":
                if subgroup == "G20Counrty":
                    query = query + '\nSELECT ?country' \
                                    '\nWHERE { ?country rdf:type ont:ISO3166DefinedCountry \n ' \
                                    '?country ont:isG20Country "true"^^xsd:boolean }\n ' \
                                    'ORDER BY ' + order + '(?country)\n'\
                                    'LIMIT ' + limit
                elif subgroup == "NonG20Country":
                    query = query + '\nSELECT ?country' \
                                    '\nWHERE { ?country rdf:type ont:ISO3166DefinedCountry \n ' \
                                    'NOT EXISTS {?country ont:isG20Country "true"^^xsd:boolean}\n ' \
                                    'ORDER BY ' + order + '(?country)\n' \
                                    'LIMIT ' + limit
                else:
                    query = query + "\nSELECT ?country" \
                                    "\nWHERE { ?country rdf:type ont:ISO3166DefinedCountry }\n " \
                                    "ORDER BY " + order + "(?country)\n" \
                                    "LIMIT " + limit
            else:
                if subgroup == "No subgroup":
                    query = query + "\nSELECT ?stock ?company" \
                                    "\nWHERE { ?stock rdf:type ont:StockExchange \n " \
                                    " ?company rdf:type ?company_type \n " \
                                    " ?company_type rdfs:subclassOf ont:Organization \n" \
                                    "ORDER BY " + order + "(?company)\n" \
                                    "LIMIT " + limit
                else:
                    query = query + "\nSELECT ?stock ?company" \
                                    "\nWHERE { ?stock rdf:type ont:StockExchange \n " \
                                    " ?company rdf:type ont:" + subgroup + "\n " \
                                    "ORDER BY " + order + "(?company)\n" \
                                    "LIMIT " + limit
            print(query)
        self.queryTextArea.clear()
        self.queryTextArea.append(query)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    gui = QueryGUI()
    gui.setupUi(Dialog)
    gui.setupEvent()
    Dialog.show()
    sys.exit(app.exec_())