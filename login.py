# Form implementation generated from reading ui file 'C:\Users\Geber.Cruz\OneDrive - Inchcape\Desktop\My Work\Image Processing\login.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgLogin(object):
    def setupUi(self, dlgLogin):
        dlgLogin.setObjectName("dlgLogin")
        dlgLogin.resize(400, 300)
        self.txtUser = QtWidgets.QTextEdit(parent=dlgLogin)
        self.txtUser.setGeometry(QtCore.QRect(50, 100, 300, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtUser.setFont(font)
        self.txtUser.setObjectName("txtUser")
        self.txtPassword = QtWidgets.QLineEdit(parent=dlgLogin)
        self.txtPassword.setGeometry(QtCore.QRect(50, 160, 300, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtPassword.setFont(font)
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txtPassword.setObjectName("txtPassword")
        self.btnSignIn = QtWidgets.QPushButton(parent=dlgLogin)
        self.btnSignIn.setGeometry(QtCore.QRect(150, 240, 100, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnSignIn.setFont(font)
        self.btnSignIn.setObjectName("btnSignIn")
        self.lblStatus = QtWidgets.QLabel(parent=dlgLogin)
        self.lblStatus.setGeometry(QtCore.QRect(100, 200, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblStatus.setFont(font)
        self.lblStatus.setText("")
        self.lblStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblStatus.setObjectName("lblStatus")
        self.label = QtWidgets.QLabel(parent=dlgLogin)
        self.label.setGeometry(QtCore.QRect(100, 30, 200, 35))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:\\Users\\Geber.Cruz\\OneDrive - Inchcape\\Desktop\\My Work\\Image Processing\\Resources/inchcapelogo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(dlgLogin)
        QtCore.QMetaObject.connectSlotsByName(dlgLogin)

    def retranslateUi(self, dlgLogin):
        _translate = QtCore.QCoreApplication.translate
        dlgLogin.setWindowTitle(_translate("dlgLogin", "Inchcape Digital PartScribe™ Sign In"))
        self.txtUser.setPlaceholderText(_translate("dlgLogin", "User name"))
        self.txtPassword.setPlaceholderText(_translate("dlgLogin", "Password"))
        self.btnSignIn.setText(_translate("dlgLogin", "Sign In"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlgLogin = QtWidgets.QDialog()
    ui = Ui_dlgLogin()
    ui.setupUi(dlgLogin)
    dlgLogin.show()
    sys.exit(app.exec())
