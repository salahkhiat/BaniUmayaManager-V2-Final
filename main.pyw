from Windows.Main import Ui_MainWindow as MainWindow
from Windows.CreateEditUser import Ui_Form as CreateEditUser
from Windows.CreateEditProduct import Ui_Form as CreateEditProduct
from Windows.ShowTotalIncome import Ui_Form as ShowTotalIncome
from Windows.AddService import Ui_Form as AddService
from Windows.NewTransaction import Ui_Form as NewTransaction
from Windows.SellNow import Ui_Form as SellNow
from Windows.ShowUsers import Ui_Form as ShowUsers
from Windows.ShowOperations import Ui_Form as ShowSalesHistory
from Windows.ShowProducts import Ui_Form as ShowProducts
from Windows.ShowServices import Ui_Form as ShowServices
from Windows.ShowDepositsWithdraws import Ui_Form as ShowTransactions

from PyQt6 import QtWidgets 
from PyQt6.QtGui import QIntValidator 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget , QMessageBox
from PyQt6.QtGui import QFontDatabase, QFont
import sqlite3 as db
from datetime import datetime 
import sys



"""
    Based application code
"""
def create_form(ui_class, base_class):
    class GenericForm(base_class):
        def __init__(self):
            super().__init__()
            self.ui = ui_class()
            self.ui.setupUi(self)  
    return GenericForm()
"""
    Error messages
"""

def confirm_delete():
    reply = QMessageBox.question(
        None,  # parent (optional)
        "نفذة تأكيد حذف العنصر",  # window title
        "هل أنت متأكد من رغبتك في حذف العنصر",  # message
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

    if reply == QMessageBox.StandardButton.Yes:
        return True
    else:
        return False
    

def show_success_message(parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("نجاح")
    msg.setText("تم حفظ البيانات بنجاح.")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()
# Notification message 
def show_fail_message(parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("فشلة العملية")
    msg.setText("فشلة العملية ، تأكد من أنه لديك كمية كافية")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()
# deposit messages 
def show_max_balance_msg(parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("فشلت العملية ")
    msg.setText("تأكد أن يكون المبلغ الذي تحاول إدخاله بين 5 دج و 200000 دج")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()

# custom message
def show_custom_msg(msg_title,msg_content):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle(msg_title)
    msg.setText(msg_content)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()

# Declare variables to hold selected product, user info

product_info = {"id": None, "name": None, "price": None}

user_info = {"id":None}
def show_sell_now():
    # Create and show the SellNow window
    sell_window = create_form(SellNow, QtWidgets.QWidget)
    sell_window.ui.box_quantity.setText("1")
    sell_window.ui.box_quantity.setValidator(QIntValidator())
    sell_window.setWindowTitle("بيع الآن")
    sell_window.ui.label.setText(product_info["name"])
    sell_window.ui.label_price.setText(product_info["price"])
    
    # Function to update total 
    def update_total():
        try:
            
            
            quantity = int(sell_window.ui.box_quantity.text())
            price =  float(sell_window.ui.label_price.text())
            total =quantity * price
            sell_window.ui.label_total.setText(f"{total:,.2f}")
            # disable sell now if quantity is 0 or ""
            quantity_test = sell_window.ui.box_quantity.text()

            if sell_window.ui.box_quantity.text() == str(''):
                sell_window.ui.box_sell.setEnabled(False)

            elif quantity_test == '0':
                sell_window.ui.box_sell.setEnabled(False)
                sell_window.ui.label_total.setText("0.00")
            else:
                sell_window.ui.box_sell.setEnabled(True)
           
        except ValueError:
            sell_window.ui.label_total.setText("0.00")
    # Connect quantity change to total update
    sell_window.ui.box_quantity.textChanged.connect(update_total)

    # Call once to initialize
    update_total()
    
    sell_window.show()
   
    # Sell this product now
    def sell_this_product():
        try:
            con = db.connect("data.db")
            cur = con.cursor()

            query = "SELECT quantity FROM Product where id = ?"
            cur.execute(query,(product_info["id"],))
            result = cur.fetchone()
            if result:
                stock = int(result[0])
                quantity = int(sell_window.ui.box_quantity.text())
                # check quantity
                if quantity <= stock:
                    new_stock = int(stock - quantity)
                    # update stock 
                    
                    cur.execute("UPDATE Product SET quantity = ? WHERE id = ?",(new_stock,product_info["id"]))
                    
                    # add new operation
                    default_customer_id = 1
                   
                    new_operation_query = "INSERT INTO Operation (user_id,product_id,quantity) VALUES (?,?,?)"
                    cur.execute(new_operation_query,(default_customer_id,product_info["id"],quantity))
                    show_success_message()
                    con.commit()
                    con.close()
                else:
                    show_fail_message()

                
            else:
                print(f"this id is not found in database {product_info['id']}")
        except db.Error as e:
            print(f"database Error: {e}")
    sell_window.ui.box_sell.clicked.connect(sell_this_product)
        
    # Keep a reference so it's not garbage collected
    windows.append(sell_window)
"""
    Show add service window
"""

def show_add_service():
    # Create and show the AddService window
    service_window = create_form(AddService, QtWidgets.QWidget)
    service_window.setWindowTitle("خدمة جديدة")
    service_window.show()
    service_window.ui.box_price.setValidator(QIntValidator())
    service_window.ui.box_deposit.setValidator(QIntValidator())
    # users[] stores users values (id,name) comes from database.
    selected_customer_id = None
    users = []

    def get_user_id_by_name():
        current_name = service_window.ui.combo_users.currentText()
        for user in users:
            if user[1] == current_name:
                nonlocal selected_customer_id
                selected_customer_id = user[0]
        print(selected_customer_id)

    service_window.ui.combo_users.currentTextChanged.connect(get_user_id_by_name)
    try:
        conn = db.connect("data.db")
        cur = conn.cursor()
        # Get  customers from database
        cur.execute("SELECT id, name FROM User WHERE type = 'customer'")

        customers = cur.fetchall()
        users = customers
        if not customers:
            show_custom_msg("تنبيه","تأكد من إضافة العملاء قبل التمكن من إستخدام هذه الميزة")
        else:
            service_window.ui.combo_users.addItem('-')
            for user in customers:
                if user[1] == '-':
                    continue
                else:
                    service_window.ui.combo_users.addItem(user[1])
    except db.Error as e:
        show_custom_msg("مشكل في قاعدة البيانات",f"{e}")
    finally:
        conn.close()

    
    def save_service():
        try:
            con = None
            default_user_id = selected_customer_id
            default_deposit = 0
            service_title = service_window.ui.box_title.text()
            service_price = service_window.ui.box_price.text()
            service_deposit = service_window.ui.box_deposit.text()
            service_selected_combo = service_window.ui.combo_users.currentText()

            
            # Check the inputs from AddService, then save them to the 'Service' table."
            
            
                
            if service_title == "" or service_price == "" :
                show_custom_msg("تنبيه","لا يمكن ترك عنوان أو سعر الخدمة فارغا")

            elif int(service_price) < 5 or int(service_price) > 200000 :
                show_custom_msg("تنبيه","سعر الخدمة يجب أن يكون بين 5دج و 200000 دج")
            else:
                con = db.connect("data.db")
                cur = con.cursor() 
                query = None
                if service_selected_combo == '-':
                    query = "INSERT INTO Service(user_id, description, price, deposit) VALUES (?,?,?,?) "
                    cur.execute(query,(default_user_id, service_title, int(service_price),default_deposit))

                else:
                    if service_deposit == "":
                        query = "INSERT INTO Service(user_id, description, price,deposit) VALUES (?,?,?,?) "
                        cur.execute(query,(default_user_id, service_title, int(service_price),default_deposit))
                
                    elif int(service_deposit) < 5 or int(service_deposit) > 200000:
                        show_custom_msg("تنبيه","مبلغ الإيداع يجب أن يكون بين 5دج و 200000 دج")

                    else:
                        query = "INSERT INTO Service(user_id, description, price,deposit) VALUES (?,?,?,?) "
                        cur.execute(query,(default_user_id, service_title, int(service_price),int(service_deposit)))

                con.commit()
                show_custom_msg("نجحت العملية","تم حفظ معاملة الخدمة بنجاح")
                service_window.ui.box_title.clear()
                service_window.ui.box_price.clear()
                service_window.ui.box_deposit.clear()
          

        except db.Error as e:
            show_custom_msg("مشكل في قاعدة البيانات",f"{e}")
        finally:
            if con:
                con.close()
    service_window.ui.btn_save.clicked.connect(save_service)
        

   
    # Keep a reference so it's not garbage collected
    windows.append(service_window)



"""
    Add new user supplier, customer and employee. reusable function
"""

def add_new_user(based_form, user_type):
    def is_valid_name(name):
        if len(name) < 1:
            show_custom_msg("تنبيه","لا يمكن أن يترك الإسم فارغا")
            return False
        elif len(name) > 1:
            return True
            
    def is_valid_balance(balance):
        if balance == "": 
            return int(0)
        elif balance != "":
            return int(balance)

    def add_user_to_database():
        con = None
        name = based_form.ui.box_name.text()
        phone = based_form.ui.box_phone.text()
        balance = based_form.ui.box_balance.text()
        valid_name = is_valid_name(name)
        valid_balance = is_valid_balance(balance)
        if valid_name == True:
            try:
                con = db.connect("data.db")
                cursor = con.cursor()
                sql = "INSERT INTO User (name,phone,type,balance) VALUES (?,?,?,?)"
                
                cursor.execute(sql,(name,phone,user_type,valid_balance,))
                con.commit()
                show_custom_msg("نجحت العملية","تم حفظ المستخدم بنجاح")
            
            except db.Error as e:
                show_custom_msg("مشكل في قاعدة البيانات",e)
            finally:
                if con:
                    con.close()
    add_user_to_database()
"""
    Add new employee window
"""
def show_add_employee():
    # Create and show the CreateEditUser window as AddEmployee
    employee_window = create_form(CreateEditUser, QtWidgets.QWidget)
    employee_window.setWindowTitle("إضافة عامل جديد")
    employee_window.ui.label.setText("إضافة عامل جديد")
    employee_window.show()    
    employee_window.ui.btn_save.clicked.connect(lambda:add_new_user(employee_window,"employee") )
   
    # Keep a reference so it's not garbage collected
    windows.append(employee_window)

"""
    Add new customer window
"""
def show_add_customer():
    # Create and show the CreateEditUser window as AddCustomer
    customer_window = create_form(CreateEditUser, QtWidgets.QWidget)
    customer_window.setWindowTitle("إضافة زبون جديد")
    customer_window.ui.label.setText("إضافة زبون جديد")
    customer_window.show()

    customer_window.ui.btn_save.clicked.connect(lambda: add_new_user(customer_window,"customer"))
   
    # Keep a reference so it's not garbage collected
    windows.append(customer_window)

"""
    Show a new supplier window
"""

def show_add_supplier():
    supplier_window = create_form(CreateEditUser, QtWidgets.QWidget)
    supplier_window.setWindowTitle("إضافة مورد جديد")
    supplier_window.ui.label.setText("إضافة مورد جديد")
    supplier_window.show()    
    supplier_window.ui.btn_save.clicked.connect(lambda : add_new_user(supplier_window,"supplier"))
    # Keep a reference so it's not garbage collected
    windows.append(supplier_window)
   
"""
    Show a new product window
"""

def show_add_product():
    # Create and show the CreateEditProduct window
    product_window = create_form(CreateEditProduct, QtWidgets.QWidget)
    product_window.setWindowTitle("إضافة سلعة جديد")
    

    product_window.show()

    # I want add combo box code here 
        # === Load data from DB and populate ComboBox ===
    try:
        con = db.connect("data.db")  # Replace with your DB file
        cur = con.cursor()
        cur.execute("SELECT name FROM User WHERE type = ?", ('supplier',))

        results = cur.fetchall()

        # Clear existing items and add new ones
        product_window.ui.combo_supplier.clear()
        for row in results:
            product_window.ui.combo_supplier.addItem(row[0])

        con.close()
    except Exception as e:
        QMessageBox.critical(product_window, "خطأ", f"حدث خطأ أثناء تحميل البيانات:\n{e}")

    #----
    supplier_name = product_window.ui.combo_supplier.currentText() or None 
    supplier_id = {"id":None} 
    
    def current_supplier_name(name):
        if name:
            try:
                con = db.connect("data.db")  
                cur = con.cursor()
                cur.execute("SELECT id FROM User WHERE name = ?", (name,))
                result = cur.fetchone()
                if result:
                    supplier_id["id"] = result[0]
                else:
                    supplier_id["id"] = None 
                con.close()
            except db.Error as e:
                print(e)

            supplier_name = name
    current_supplier_name(supplier_name)

        
    product_window.ui.combo_supplier.currentTextChanged.connect(current_supplier_name)

    # Add product to database
    def add_product_to_database():
        try:
            con = db.connect("data.db")
            cursor = con.cursor()
            
            name = product_window.ui.box_name.text()
            bought_at = product_window.ui.box_bought_at.text()
            sell_at = product_window.ui.box_sell_at.text()
            quantity = product_window.ui.box_quantity.text()
            deposit_text = product_window.ui.box_deposit.text().strip()
            deposit = int(deposit_text) if deposit_text else 0
            
            # Add new buying transation
            supplier_query = "INSERT INTO Transactions (user_id, type, amount) VALUES (?,?,?)"
            cursor.execute(supplier_query,(supplier_id["id"],"deposit",deposit,))

            # Add new product to the system
            product_query = "INSERT INTO Product (user_id,name,bought_at,sell_at,quantity) VALUES (?,?,?,?,?)"
            cursor.execute(product_query,(supplier_id["id"],name,bought_at,sell_at,quantity,))

            # Add new debt to the supplier's balance by multiplying the purchase price by the quantity.
            supplier_new_debt_query = "UPDATE User SET balance = balance + ? WHERE id = ?"
            cursor.execute(supplier_new_debt_query, (int(bought_at)*int(quantity), supplier_id["id"]))

            # Deducted the deposit amount from the balance.
            supplier_new_balance_query = "UPDATE User SET balance = balance - ? WHERE id = ?"
            cursor.execute(supplier_new_balance_query, (deposit, supplier_id["id"]))
            con.commit()
            show_success_message()
            # clear fields
            product_window.ui.box_name.clear()
            product_window.ui.box_bought_at.clear()
            product_window.ui.box_sell_at.clear()
            product_window.ui.box_quantity.clear()
            product_window.ui.box_deposit.clear()

        except db.Error as e:
            print(f"{e}")
        finally:
            if con:
                con.close()
    product_window.ui.btn_save.clicked.connect(add_product_to_database)


   
    # Keep a reference so it's not garbage collected
    windows.append(product_window)


# show operations window
def show_sales_history():
    # Show Operstions for current monther
    sales_history_window= create_form(ShowSalesHistory, QtWidgets.QWidget)
    sales_history_window.setWindowTitle("عمليات بيع هذا الشهر")
    sales_history_window.show()
    sales_history_window.ui.operations_table.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    # Set font  this table 
    

    normal_font_big = QFont()
    normal_font_big.setBold(True)
    normal_font_big.setPointSize(14)

        # set columns size
    header = sales_history_window.ui.operations_table.horizontalHeader()
    header.setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeMode.Stretch)
    sales_history_window.ui.operations_table.setFont(normal_font_big)
    sales_history_window.ui.operations_table.setColumnWidth(0,70)
    sales_history_window.ui.operations_table.setColumnWidth(2,50)


     # Hide raw id
    sales_history_window.ui.operations_table.verticalHeader().setVisible(False)
       # looking for a operation in search box
    def search_operations():
        search_term = sales_history_window.ui.box_search.text()
        con = db.connect('data.db')
        cur = con.cursor()
        # Change 'operations' to your actual table name
        query = """
            SELECT 
                Operation.id,
                Product.name,
                Operation.quantity,
                Product.sell_at,
                Operation.quantity * Product.sell_at AS total,
                Operation.created
            FROM
                Operation
            JOIN
                Product ON Operation.product_id = Product.id
            WHERE
                Product.name LIKE ?
        """
        cur.execute(query,('%' + search_term + '%',))

        
        results = cur.fetchall()
        sales_history_window.ui.operations_table.setRowCount(len(results))
      
        
        for row_index, row_data in enumerate(results):
            for column_index, cell_value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(cell_value))
                sales_history_window.ui.operations_table.setItem(row_index, column_index, item)
                
        con.close()



     # Connect the textChanged signal to search function
    sales_history_window.ui.box_search.textChanged.connect(search_operations)
    search_operations()

   
    # Keep a reference so it's not garbage collected
    windows.append(sales_history_window)




"""
        --- Version 2 of code ---
"""

"""
        Reusable Form class
"""
class Form(QWidget):
    def __init__(self, ui_class, **kwargs):
        super().__init__()
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.selected_user_id = None
        

        if "window_title":
            self.setWindowTitle(str(kwargs["window_title"]))
    """
        Deal with selected user raw in a table
    """
    def on_row_selected(self):
        selected_items = self.ui.items_table.selectedItems()
        if selected_items:
            # Assuming user_id is in column 0
            self.selected_user_id = selected_items[0].text()
        else:
            self.selected_user_id = None

    def on_edit_button_clicked(self):
        if self.selected_user_id is not None:
            self.edit_user_info(self.selected_user_id)
        else:
            QtWidgets.QMessageBox.warning(self, "No selection", "Please select a user row first.")

    def edit_user_info(self, user_id):
        # Replace this with your actual logic
        print(f"Editing user with ID: {user_id}")
        
    """
        Styling table
    """
    def styling_table(self,qt_table):
        # Hide raw id
        qt_table.verticalHeader().setVisible(False)
        # make table data appears right to left
        qt_table.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        # set columns size
        # header = qt_table.horizontalHeader()
        # header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        # shadow entire table raw with a color 
        self.ui.items_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        
        

    """
           Get data from database depending on keywords
    """
    def get_data_from_table(self,query,keywords=None):
        
        try:
            con = db.connect("data.db")
            cur = con.cursor()
            # Count how many parameters the query expects
            num_placeholders = query.count('?')

            if num_placeholders > 0 and  keywords is not None:
                cur.execute(query,(f'%{keywords}%',keywords))
            else:
                cur.execute(query)
            raws_list = cur.fetchall()
            con.close()
            self.table_raws = raws_list
            

           
        except db.Error as database_error:
            print(database_error)

    
    """
           Put data that already have got from get_data_form_table on Qt table (ShowProducts) window
    """
    def put_data_on_table(self):
        self.ui.items_table.setRowCount(len(self.table_raws))
        for row_idx, row_data in enumerate(self.table_raws):
            for col_idx, value in enumerate(row_data):     
                self.ui.items_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value).strip()))
    
    """
           put a list on a ComboBox
    """

    def put_data_on_combo(self,user_type):
        query = f"SELECT name FROM User WHERE type LIKE '{user_type}'  GROUP BY User.id;"
        self.get_data_from_table(query)
        users_list = self.table_raws
        combo = self.ui.combo_users

        for item in users_list:
            combo.addItem(str(item[0]))

    """
        Get user_id for Withdraw Or deposit
    """
    def get_user_id(self):
        name=self.ui.combo_users.currentText()
        # To disable, enable deposit now button depending on user(supplier or employee) name selected or not yet
        if(name == "-"):
            self.ui.btn_save.setEnabled(False)
        else:
            self.ui.btn_save.setEnabled(True)

        query = f"SELECT id FROM User WHERE name LIKE ?"
        try:
            con = db.connect("data.db")
            cur = con.cursor()
            cur.execute(query,(f"%{name}%",))
            self.user_id = cur.fetchone()
            con.close()
        except db.Error as e:
            print(e)
    """
        Deposit money to a supplier or record employee withdrawals.
    """

    def new_transaction(self,transaction_type):
        amount = int(self.ui.box_amount.text())
        
        if(amount >= 5 and amount <= 200000):
          
            try:
        
                query="INSERT INTO Transactions (user_id,type,amount) VALUES (?,?,?) "
                con = db.connect("data.db")
                cur = con.cursor()
                cur.execute(query,(self.user_id[0],transaction_type,amount,))

                # Deduct amount from user's balance
                updated_user_balance_query = "UPDATE User SET balance = balance - ? WHERE id = ?"
                cur.execute(updated_user_balance_query, (amount , self.user_id[0]))

                con.commit()
                if(cur.rowcount > 0):
                    show_success_message()
                else:
                    show_fail_message()
                
            except db.Error as e:
                print(e)
            finally:
                if con:
                    con.close()
        elif(amount > 200000):
            show_max_balance_msg()
        else:
            show_max_balance_msg()
    """
        Get selected user id 
    """
    def set_selected_user_id(self):
        self.ui.items_table.itemClicked.connect(lambda item:(
            user_info.update({
                "id": self.ui.items_table.item(item.row(), 0).text()
            })
        ))
    """
        Get user info from database by id and put them in a edit form
    """
   
    def put_selected_user_info(self,user_type):
        try:
            con = db.connect("data.db")
            cur = con.cursor()
            query = "SELECT name, phone, balance FROM User WHERE id LIKE ? AND type LIKE ?"
            cur.execute(query,(f"%{user_info['id']}%",f"%{user_type}%"),)
            result = cur.fetchall()
            if result:
                return result[0]
            else:
                print("There is no user info got")
        except db.Error as e:
            print(e)
        finally:
            con.close()

            


windows = [] 



"""
    ************ Main Part ***************
"""
def main():
    app = QtWidgets.QApplication([])

    """
        Set font this application
    """

    font_id = QFontDatabase.addApplicationFont("Design/bani_umaya_font.ttf")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        big_font = QFont(font_family, 19)
        medium_font = QFont(font_family, 15)
        small_font = QFont(font_family, 10)

    else:
        print("Failed to load font.")
        big_font = QFont()  # fallback default font
        medium = QFont(font_family, 15)
        small_font = QFont(font_family, 10)

    normal_font_big = QFont()
    normal_font_big.setBold(True)
    normal_font_big.setPointSize(15)
    
  
    """
        Show main window
    """
    main_window = create_form(MainWindow,QtWidgets.QMainWindow)
    main_window.setWindowTitle("بنوأمية-الإصدار الثالث-الآخير")
    # styling fonts 
    main_window.ui.basmala.setFont(medium_font)
    main_window.ui.label.setFont(big_font)
    main_window.ui.menubar.setFont(small_font)
    main_window.ui.btn_service.setFont(medium_font)
    main_window.ui.btn_sell.setFont(medium_font)
    main_window.ui.btn_del.setFont(medium_font)
    main_window.ui.btn_edit.setFont(medium_font)
    main_window.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
 
    # Make full row table selectable
    main_window.ui.products_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
    # Connect row click
    main_window.ui.products_table.itemClicked.connect(lambda item: (
        product_info.update({
            "id": main_window.ui.products_table.item(item.row(), 0).text(),
            "name": main_window.ui.products_table.item(item.row(), 1).text(),
            "price": main_window.ui.products_table.item(item.row(), 2).text()
        })
    ))


    
    # Hide raw id
    main_window.ui.products_table.verticalHeader().setVisible(False)
    # make table data appears right to left
    main_window.ui.products_table.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # Set products table size
    header = main_window.ui.products_table.horizontalHeader()
    header.setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeMode.Stretch)
    main_window.ui.products_table.setFont(normal_font_big)


   # looking for a products in search box
    def search_products():
        search_term = main_window.ui.search_box.text()
        con = db.connect('data.db')
        cur = con.cursor()

        query = """
                   SELECT
                    Product.id AS product_id,
                    Product.name AS p_name,
                    Product.quantity,
                    COALESCE(SUM(Operation.quantity), 0) AS sold_items_count,
                    Product.bought_at,
                    Product.sell_at,
                    User.name AS supplier_name,
                    COALESCE(SUM(Operation.quantity), 0) * (Product.sell_at - Product.bought_at) AS profits,
                    Product.created
                    FROM Product
                    JOIN User ON Product.user_id = User.id
                    LEFT JOIN Operation ON Product.id = Operation.product_id
                    WHERE Product.name LIKE ? OR ? = ''
                    GROUP BY Product.id;
        """
        cur.execute(query,(f'%{search_term}%',search_term))
        results = cur.fetchall()
        con.close()
    


        # Populate the table
        
        main_window.ui.products_table.setRowCount(len(results))
       
        for row_idx, row_data in enumerate(results):
            for col_idx, value in enumerate(row_data):
                
                main_window.ui.products_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value).strip()))
     # Connect the textChanged signal to search function
    main_window.ui.search_box.textChanged.connect(search_products)
    search_products()


    # Connect buttons
    main_window.ui.btn_sell.clicked.connect(show_sell_now)

    main_window.ui.btn_service.clicked.connect(show_add_service)
    main_window.ui.tab_employee.triggered.connect(show_add_employee)
    main_window.ui.tab_customer.triggered.connect(show_add_customer)
    main_window.ui.tab_supplier.triggered.connect(show_add_supplier)
    main_window.ui.tab_product.triggered.connect(show_add_product)
    # main_window.ui.tab_user_type.triggered.connect(show_add_user_type)
    main_window.ui.tab_sales_history.triggered.connect(show_sales_history)

    # --- Version 2 of this application ---
         


    """
        Deposit to supplier 
    """
    # show the window
    deposit_to_supplier = Form(NewTransaction,window_title="إيداع")
    main_window.ui.tab_deposit_to_supplier.triggered.connect(deposit_to_supplier.show)
    deposit_to_supplier.put_data_on_combo("supplier")
    

    deposit_to_supplier.ui.combo_users.currentIndexChanged.connect(deposit_to_supplier.get_user_id)
    
    deposit_to_supplier.ui.btn_save.clicked.connect(
        lambda:deposit_to_supplier.new_transaction("deposit")
    )

    """
        Employee withdraws money 
    """
    
    employee_withdraw = Form(NewTransaction,window_title="سحب")
    main_window.ui.tab_employee_withdraw.triggered.connect(employee_withdraw.show)
    employee_withdraw.put_data_on_combo("employee")

    employee_withdraw.ui.combo_users.currentIndexChanged.connect(employee_withdraw.get_user_id)

    employee_withdraw.ui.btn_save.clicked.connect(
        lambda:employee_withdraw.new_transaction("withdraw")
    )


    """
        Show Transcations
    """
    Trans_query = """
            SELECT 
            Transactions.id, 
            User.name, 
            Transactions.amount, 
            Transactions.created
            FROM 
                Transactions
            JOIN 
                User ON Transactions.user_id = User.id
            WHERE 
                User.name LIKE ? OR ? = ''
            GROUP BY 
                Transactions.id;
        """
    transactions_table = Form(ShowTransactions,window_title="سجل المعاملات")
    transactions_table.styling_table(transactions_table.ui.items_table)
    main_window.ui.tab_transactions_table.triggered.connect(transactions_table.show)

    transactions_header = transactions_table.ui.items_table.horizontalHeader()
    transactions_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    transactions_table.ui.search_box.textChanged.connect(
        lambda : (
            transactions_table.get_data_from_table(Trans_query,transactions_table.ui.search_box.text()),
            transactions_table.put_data_on_table()
                )
    )
    transactions_table.get_data_from_table(Trans_query,"")
  
    transactions_table.put_data_on_table()

    """
        Show products table
    """
    products_table = Form(ShowProducts,window_title="سجل السلع")
    main_window.ui.tab_products_table.triggered.connect(products_table.show)

    # Set products table size
    products_header = products_table.ui.items_table.horizontalHeader()
    products_header.setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeMode.Stretch)
    products_table.ui.items_table.setFont(normal_font_big)
    products_table.ui.items_table.setColumnWidth(0,60)
    products_table.ui.items_table.setColumnWidth(1,400)

    products_table.styling_table(products_table.ui.items_table)

    products_query = f"""
       SELECT
        Product.id AS product_id,
        Product.name AS p_name,
        Product.quantity,
        COALESCE(SUM(Operation.quantity), 0) AS sold_items_count,
        Product.bought_at,
        Product.sell_at,
        User.name AS supplier_name,
        COALESCE(SUM(Operation.quantity), 0) * (Product.sell_at - Product.bought_at) AS profits,
        Product.created
        FROM Product
        JOIN User ON Product.user_id = User.id
        LEFT JOIN Operation ON Product.id = Operation.product_id
        -- WHERE Product.name LIKE ?
        WHERE Product.name LIKE ? OR ? = ''
        GROUP BY Product.id;
        
    """
    products_table.ui.search_box.textChanged.connect(
        lambda : (
            products_table.get_data_from_table(products_query,products_table.ui.search_box.text()),
            products_table.put_data_on_table()
                )
    )
    products_table.get_data_from_table(products_query,"")
  
    products_table.put_data_on_table()


    """
        Edit product info
    """
    edit_product = Form(CreateEditProduct,window_title="تعديل بيانات السلعة")

    # product info as a tuple from database
    def get_product_info(product_id):
        con = None
        try:
            con = db.connect("data.db")
            cur = con.cursor()
            query = """
                    SELECT User.id, User.name, Product.name, Product.bought_at, Product.sell_at,Product.quantity, Product.deposit 
                    FROM Product 
                    JOIN User ON Product.user_id = User.id
                    WHERE Product.id = ?
                    """
            cur.execute(query,(product_id,))
            
            return cur.fetchone()

        except db.Error as e:
            show_custom_msg("مشكل في قاعدة البيانات",e)
        finally:
            if con:
                con.close()

    # Fill in the product's info fields
    def fill_product_info(base_form,p_info):
        base_form.ui.box_name.setText(p_info[2])
        base_form.ui.box_bought_at.setText(str(p_info[3]))
        base_form.ui.box_sell_at.setText(str(p_info[4]))
        base_form.ui.box_quantity.setText(str(p_info[5]))
        base_form.ui.box_deposit.setText(str(p_info[6]))
        con = None 
        try:
            con = db.connect("data.db")
            cur = con.cursor()
            query = "SELECT id, name FROM User WHERE type = 'supplier'"
            cur.execute(query)
            suppliers_list = cur.fetchall()
            base_form.ui.combo_supplier.clear()
    
            base_form.ui.combo_supplier.addItem(p_info[1])

            for supplier in suppliers_list:
                if supplier[0] == p_info[0]:
                    continue
                else:
                    base_form.ui.combo_supplier.addItem(supplier[1])
                
        except db.Error as e:
            show_custom_msg("مشكل في قاعدة البيانات",e)
        finally:
            if con:
                con.close()
    # validate products fields 
    def validate_product_fields():
        pass 
    
    # save changes
    def save_changes():
        pass



    def prepare_edit_product_window(based_form,product_id):
        if product_id is  None :
            show_custom_msg("تنبيه","قم بتحديد السلعة أولا")
        else:
            selected_product = get_product_info(product_id)
            fill_product_info(based_form,selected_product)
            based_form.show()
        
        
    main_window.ui.btn_edit.clicked.connect(lambda: prepare_edit_product_window(edit_product,product_info["id"]))



    """
        Delete a product
    """
    def delete_product():
        if product_info["id"] is None:
            show_custom_msg("تنبيه","قم بتحدد السلعة التي ترغب بحذفها من الجدول أولا")
        else:
            del_con = confirm_delete()
            if del_con is True:
                try:
                    con = db.connect("data.db")
                    con.execute("PRAGMA foreign_keys = ON")  # Ensure FK constraints are enforced
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Product WHERE id = ?",(product_info["id"],))
                    product = cur.fetchone()
                    if product is None:
                        show_custom_msg("فشلة العملية","قد يكون تم حذف العنصر مسبقا قم بتحدث جول السلع و جرب مرة أخرة")
                    else:
                        cur.execute("DELETE FROM Product WHERE id = ?", (product_info["id"],))
                        con.commit()
                        show_custom_msg("نجحت العملية","تم حذف العنصر بنجاح")
                except db.Error as e :
                    show_custom_msg("مشكل في قاعدة البيانات",str(e))
                    
                
            else:
                show_custom_msg("فشلة العملية"," فشلة عملية الحذف , أغلق البرنامج و فتحه مجدد و حاول مرة أخرة")

            
    main_window.ui.btn_del.clicked.connect(delete_product)
    


    """
        Show services table
    """
    services_query = """
            SELECT  Service.description, User.name, Service.price, Service.deposit, Service.created 
            FROM Service
            JOIN User ON Service.user_id = User.id
            WHERE User.name LIKE ? OR ? = ''
            GROUP BY Service.id;
        """
    services_table = Form(ShowServices,window_title="سجل الخدمات")
    services_table.styling_table(services_table.ui.items_table)
    main_window.ui.tab_services_table.triggered.connect(services_table.show)
    # set table size
    services_header = services_table.ui.items_table.horizontalHeader()
    services_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    services_table.ui.search_box.textChanged.connect(
        lambda : (
            services_table.get_data_from_table(services_query,services_table.ui.search_box.text()),
            services_table.put_data_on_table()
                )
    )
    services_table.get_data_from_table(services_query,"")
  
    services_table.put_data_on_table()

    """
        Show suppliers table
    """
    suppliers_query = """
            SELECT id, name, phone, balance, created
            FROM User WHERE type LIKE 'supplier'
            AND (name LIKE ? OR ? = '')
            GROUP BY User.id;
    """
    suppliers_table = Form(ShowUsers,window_title="سجل الموردين")
    suppliers_table.ui.search_box.setPlaceholderText("أكتب إسم المورد هنا للبحث")
    suppliers_table.styling_table(suppliers_table.ui.items_table)
    main_window.ui.tab_suppliers_table.triggered.connect(suppliers_table.show)
    # set user table size
    suppliers_header = suppliers_table.ui.items_table.horizontalHeader()
    suppliers_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    suppliers_table.ui.search_box.textChanged.connect(
        lambda : (
            suppliers_table.get_data_from_table(suppliers_query,suppliers_table.ui.search_box.text()),
            suppliers_table.put_data_on_table()
                )
    )
    suppliers_table.get_data_from_table(suppliers_query,"")
  
    suppliers_table.put_data_on_table()


    """
        Edit supplier info
    """

    def prepare_edit_user_window(based_form,sec_form,user_type):
        based_form.ui.btn_save.setText("حفظ التعديل")
        
        def get_selected_user():
            selected_user_info = sec_form.put_selected_user_info(user_type)
            based_form.ui.label.setText(f"تعديل بيانات {str(selected_user_info[0])}"),
            based_form.ui.box_name.setText(str(selected_user_info[0]))
            based_form.ui.box_phone.setText(str(selected_user_info[1]))
            based_form.ui.box_balance.setText(str(int(selected_user_info[2])))

        def save_changes():
            name = based_form.ui.box_name.text().strip()
            phone = based_form.ui.box_phone.text().strip()
            balance = based_form.ui.box_balance.text().strip()

            # Validate balance: allow negatives, but limit to absolute max of 200000
            try:
                valid_balance = int(balance) if balance else 0
                if abs(valid_balance) > 200000:
                    show_max_balance_msg()
                    return
            except ValueError:
                print("Invalid balance. Please enter a number.")
                return

            if user_info["id"] is not None and name != '':
                try:
                    query = "SELECT id FROM User WHERE id = ?"
                    con = db.connect("data.db")
                    cur = con.cursor()
                    cur.execute(query, (user_info["id"],))
                    if cur.fetchone():
                        cur.execute(
                            "UPDATE User SET name = ?, phone = ?, balance = ? WHERE id = ?",
                            (name, phone, valid_balance, user_info["id"])
                        )
                        con.commit()
                        show_success_message()
                    else:
                        print("Item didn't update (ID not found)")
                except db.Error as e:
                    print("Database error:", e)
                finally:
                    con.close()

        based_form.ui.btn_save.clicked.connect(save_changes)

        sec_form.ui.edit_btn.clicked.connect(
            lambda:(
                based_form.show(),
                sec_form.put_selected_user_info(user_type),
                get_selected_user(),
            )
        )

        
        


    edit_supplier = Form(CreateEditUser,window_title="تعديل بيانات المستخدم")
    
    suppliers_table.set_selected_user_id()

    prepare_edit_user_window(edit_supplier,suppliers_table,"supplier")


    

    """
        Show customers table
    """

    customers_query = """
            SELECT id, name, phone, balance, created
            FROM User WHERE type LIKE 'customer'
            AND (name LIKE ? OR ? = '')
            GROUP BY User.id;
    """
    customers_table = Form(ShowUsers,window_title="سجل العملاء")
    customers_table.ui.search_box.setPlaceholderText("أكتب إسم العميل هنا للبحث")
    customers_table.styling_table(customers_table.ui.items_table)
    main_window.ui.tab_customers_table.triggered.connect(customers_table.show)
    # set users table size
    customers_header = customers_table.ui.items_table.horizontalHeader()
    customers_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    customers_table.ui.search_box.textChanged.connect(
        lambda : (
            customers_table.get_data_from_table(customers_query,customers_table.ui.search_box.text()),
            customers_table.put_data_on_table()
                )
    )
    customers_table.get_data_from_table(customers_query,"")
  
    customers_table.put_data_on_table()


    """
        Edit customer info
    """

    edit_customer = Form(CreateEditUser,window_title="تعديل بيانات المستخدم")
    customers_table.set_selected_user_id()
    prepare_edit_user_window(edit_customer,customers_table,"customer")

    """
        Show employees table
    """

    employees_query = """
            SELECT id, name, phone, balance, created
            FROM User WHERE type LIKE 'employee'
            AND (name LIKE ? OR ? = '')
            GROUP BY User.id;
    """
    employees_table = Form(ShowUsers,window_title="سجل العملاء")
    employees_table.ui.search_box.setPlaceholderText("أكتب إسم العميل هنا للبحث")
    employees_table.styling_table(employees_table.ui.items_table)
    main_window.ui.tab_employees_table.triggered.connect(employees_table.show)
    # set users table size
    employees_header = employees_table.ui.items_table.horizontalHeader()
    employees_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    employees_table.ui.search_box.textChanged.connect(
        lambda : (
            employees_table.get_data_from_table(employees_query,employees_table.ui.search_box.text()),
            employees_table.put_data_on_table()
                )
    )
    employees_table.get_data_from_table(employees_query,"")
  
    employees_table.put_data_on_table()

    """
        Edit employee info
    """

    edit_employee = Form(CreateEditUser,window_title="تعديل بيانات المستخدم")
    employees_table.set_selected_user_id()
    prepare_edit_user_window(edit_employee,employees_table,"employee")

    """
        Delete a user
    """
    def delete_user():
        if user_info["id"] is None:
            show_custom_msg("تنبيه","قم بتحدد المستخدم الذي ترغب بحذفه من الجدول أولا")
        else:
            del_con = confirm_delete()
            if del_con is True:
                try:
                    con = db.connect("data.db")
                    con.execute("PRAGMA foreign_keys = ON")  # Ensure FK constraints are enforced
                    cur = con.cursor()
                    cur.execute("SELECT * FROM User WHERE id = ?",(user_info["id"],))
                    product = cur.fetchone()
                    if product is None:
                        show_custom_msg("فشلة العملية","قد يكون تم حذف المستخدم مسبقا قم بتحدث جول المستخدمين و جرب مرة أخرة")
                    else:
                        cur.execute("DELETE FROM User WHERE id = ?", (user_info["id"],))
                        con.commit()
                        show_custom_msg("نجحت العملية","تم حذف العنصر بنجاح")
                except db.Error as e :
                    show_custom_msg("مشكل في قاعدة البيانات",str(e))
                    
                
            else:
                show_custom_msg("فشلة العملية"," فشلة عملية الحذف , أغلق البرنامج و فتحه مجدد و حاول مرة أخرة")

            
    suppliers_table.ui.delete_btn.clicked.connect(delete_user)
    employees_table.ui.delete_btn.clicked.connect(delete_user)
    customers_table.ui.delete_btn.clicked.connect(delete_user)

    """
        Show total income of current month
    """
    total_income = Form(ShowTotalIncome,window_title="دخل هذا الشهر")
    def calculate_monthly_total():
        con = db.connect("data.db")
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()

        # Get the current month and year
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        # Format for SQLite (YYYY-MM)
        month_pattern = f"{current_year}-{str(current_month).zfill(2)}%"

        try:
            # 1.1 Sum of Service prices for current month when customer name is normal that labeled with '-'
            cur.execute("""
                    SELECT SUM( CASE WHEN User.name = '-' THEN Service.price ELSE 0 END) AS total_prices 
                        FROM Service 
                        JOIN User ON Service.user_id = User.id
                        WHERE Service.created LIKE ? 

            """,(month_pattern,))
            
            total_services = cur.fetchone()[0]
            # 1.1 Sum of Service deposit for current month when customer name is not '-' that labeled with his name User.name
            cur.execute("""
              SELECT SUM(CASE WHEN User.name != '-' THEN deposit ELSE 0 END) AS total_positive_deposit
                FROM Service
                JOIN User ON Service.user_id = User.id
                WHERE Service.created LIKE ?
                        """, (month_pattern,)
                        )
            total_deposits = cur.fetchone()[0]
            sum_deposits_services = total_deposits + total_services
            
            

            # 2. Sum of Operation revenue (quantity * product.sell_at) for current month
            cur.execute("""
                SELECT IFNULL(SUM(Operation.quantity * Product.sell_at), 0)
                FROM Operation
                LEFT JOIN Product ON Operation.product_id = Product.id
                WHERE Operation.created LIKE ?
            """, (month_pattern,))
            total_operations = cur.fetchone()[0]

            # 3. Total Transactions (subtract this)
            cur.execute("""
                SELECT IFNULL(SUM(amount), 0) FROM Transactions
                WHERE created LIKE ?
            """, (month_pattern,))
            total_transactions = cur.fetchone()[0]

            # Final total
            total = sum_deposits_services + total_operations - total_transactions

            total_income.ui.total_income.display(total)
            total_income.ui.sales_total.display(total_operations)
            total_income.ui.services_total.display(sum_deposits_services)
            total_income.ui.expenses_total.display(total_transactions)

        except Exception as e:
            show_custom_msg("فشل العملية","حدث مشكل أثناء حساب مداخيل و مصاريف المحل")
        finally:
            con.close()

    # Example usage
    calculate_monthly_total()

    
    main_window.ui.tab_total_income.triggered.connect(lambda:(
        total_income.show(),
        calculate_monthly_total()
    ))

    main_window.show()
    app.exec()

if __name__== '__main__':
    main()