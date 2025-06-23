from PyQt6 import QtCore, QtGui, QtWidgets



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 260)
        Form.setMinimumSize(QtCore.QSize(400, 260))
        Form.setMaximumSize(QtCore.QSize(400, 260))
        self.btn_save = QtWidgets.QPushButton(parent=Form)
        self.btn_save.setGeometry(QtCore.QRect(150, 160, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_save.setFont(font)
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_save.setStyleSheet("QPushButton{\n"
"    border-radius:15px;\n"
"    color:white;\n"
"    background-color:#239b56;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"    background-color:#283747;\n"
"}")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 19, 361, 131))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.verticalLayoutWidget.setFont(font)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.combo_users = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.combo_users.setMinimumSize(QtCore.QSize(0, 50))
        self.combo_users.setObjectName("combo_users")
        self.combo_users.addItem("")
        self.verticalLayout.addWidget(self.combo_users)
        self.box_amount = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_amount.sizePolicy().hasHeightForWidth())
        self.box_amount.setSizePolicy(sizePolicy)
        self.box_amount.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.box_amount.setFont(font)
        self.box_amount.setText("")
        self.box_amount.setObjectName("box_amount")
        self.verticalLayout.addWidget(self.box_amount)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_save.setText(_translate("Form", "إداع المبلغ"))
        self.combo_users.setItemText(0, _translate("Form", "-"))
        self.box_amount.setPlaceholderText(_translate("Form", "المبلغ"))
        self.box_amount.setMaxLength(6)
        self.box_amount.setValidator(QtGui.QIntValidator())
        self.btn_save.setEnabled(False)
