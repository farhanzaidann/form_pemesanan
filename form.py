# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
# Created by: PyQt5 UI code generator 5.15.10

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import (
    QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QLineEdit, QFormLayout
)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 550)

        self.mainLayout = QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.mainLayout.addWidget(self.label)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")

        self.usernameLabel = QLabel(Form)
        self.usernameLabel.setObjectName("usernameLabel")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.usernameLabel)
        self.usernameLineEdit = QLineEdit(Form)
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.usernameLineEdit)

        self.passwordLabel = QLabel(Form)
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QLineEdit(Form)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.passwordLineEdit)

        self.passwordLabel_2 = QLabel(Form)
        self.passwordLabel_2.setObjectName("passwordLabel_2")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.passwordLabel_2)
        self.passwordLineEdit_2 = QLineEdit(Form)
        self.passwordLineEdit_2.setObjectName("passwordLineEdit_2")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.passwordLineEdit_2)

        self.mainLayout.addLayout(self.formLayout)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.buttonLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.buttonLayout.addWidget(self.pushButton_2)

        self.deleteButton = QPushButton(Form)
        self.deleteButton.setObjectName("deleteButton")
        self.buttonLayout.addWidget(self.deleteButton)

        self.mainLayout.addLayout(self.buttonLayout)

        self.orderTable = QTableWidget(Form)
        self.orderTable.setObjectName("orderTable")
        self.orderTable.setColumnCount(3)
        self.orderTable.setHorizontalHeaderLabels(["Nama Barang", "Jumlah", "Harga"])
        self.orderTable.horizontalHeader().setStretchLastSection(True)
        self.orderTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.orderTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.mainLayout.addWidget(self.orderTable)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Manajemen Pesanan Barang"))
        self.label.setText(_translate("Form", "Input Pesanan Baru"))
        self.usernameLabel.setText(_translate("Form", "Nama Barang"))
        self.passwordLabel.setText(_translate("Form", "Jumlah"))
        self.passwordLabel_2.setText(_translate("Form", "Harga"))
        self.pushButton.setText(_translate("Form", "Batalkan"))
        self.pushButton_2.setText(_translate("Form", "Simpan Pesanan"))
        self.deleteButton.setText(_translate("Form", "Hapus Pesanan yang Dipilih"))

class OrderForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_db()
        self.connect_signals()
        self.load_and_display_orders()

    def init_db(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def connect_signals(self):
        self.pushButton.clicked.connect(self.cancel_order)
        self.pushButton_2.clicked.connect(self.save_order)
        self.deleteButton.clicked.connect(self.delete_order)

    def cancel_order(self):
        self.usernameLineEdit.clear()
        self.passwordLineEdit.clear()
        self.passwordLineEdit_2.clear()
        print("Fields cleared.")

    def save_order(self):
        nama_barang = self.usernameLineEdit.text()
        jumlah_str = self.passwordLineEdit.text()
        harga_str = self.passwordLineEdit_2.text()

        if not nama_barang or not jumlah_str or not harga_str:
            QMessageBox.warning(self, "Input Error", "Semua field harus diisi.")
            return

        try:
            jumlah = int(jumlah_str)
            harga = float(harga_str)
            if jumlah <= 0 or harga < 0:
                QMessageBox.warning(self, "Input Error", "Jumlah harus lebih dari 0 dan Harga tidak boleh negatif.")
                return
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Jumlah dan Harga harus berupa angka.")
            return

        try:
            self.cursor.execute(
                'INSERT INTO orders (item_name, quantity, price) VALUES (?, ?, ?)',
                (nama_barang, jumlah, harga)
            )
            self.conn.commit()
            QMessageBox.information(self, "Sukses", "Pesanan berhasil disimpan!")
            print(f"Pesanan disimpan: Nama Barang={nama_barang}, Jumlah={jumlah}, Harga={harga}")
            self.cancel_order()
            self.load_and_display_orders()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Gagal menyimpan pesanan: {e}")
            print(f"Database error during save: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")
            print(f"An unexpected error occurred: {e}")

    def load_and_display_orders(self):
        """Mengambil data pesanan dari database (termasuk ID) dan menampilkannya di tabel."""
        try:
            self.cursor.execute("SELECT id, item_name, quantity, price FROM orders ORDER BY order_time DESC")
            orders_data = self.cursor.fetchall()
            self.display_orders(orders_data)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Gagal memuat pesanan: {e}")
            print(f"Database error during load: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat menampilkan pesanan: {e}")
            print(f"An unexpected error occurred during display: {e}")

    def display_orders(self, orders_data):
        """Menampilkan data pesanan di QTableWidget."""
        self.orderTable.setRowCount(len(orders_data))
        for row_index, row_data in enumerate(orders_data):
            order_id = row_data[0]
            display_data = row_data[1:]
            for col_index, item in enumerate(display_data):
                item_str = str(item)
                if self.orderTable.horizontalHeaderItem(col_index).text() == "Harga":
                    item_str = f"Rp{item:,.2f}"
                cell_item = QTableWidgetItem(item_str)
                if col_index == 0:
                    cell_item.setData(QtCore.Qt.UserRole, order_id)
                self.orderTable.setItem(row_index, col_index, cell_item)

    def delete_order(self):
        """Menghapus pesanan yang dipilih dari database."""
        selected_indexes = self.orderTable.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Peringatan", "Pilih pesanan yang ingin dihapus.")
            return

        reply = QMessageBox.question(
            self, 'Konfirmasi Hapus',
            "Apakah Anda yakin ingin menghapus pesanan yang dipilih?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                ids_to_delete = []
                processed_rows = set()
                for index in selected_indexes:
                    if index.row() not in processed_rows:
                        item = self.orderTable.item(index.row(), 0)
                        if item is not None:
                            order_id = item.data(QtCore.Qt.UserRole)
                            if order_id is not None:
                                ids_to_delete.append(order_id)
                                processed_rows.add(index.row())
                if not ids_to_delete:
                    QMessageBox.warning(self, "Peringatan", "Tidak ada ID pesanan yang valid ditemukan untuk dihapus.")
                    return
                placeholders = ', '.join('?' * len(ids_to_delete))
                delete_query = f"DELETE FROM orders WHERE id IN ({placeholders})"
                self.cursor.execute(delete_query, ids_to_delete)
                self.conn.commit()
                QMessageBox.information(self, "Sukses", f"{len(ids_to_delete)} pesanan berhasil dihapus.")
                print(f"Dihapus pesanan dengan ID: {ids_to_delete}")
                self.load_and_display_orders()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"Gagal menghapus pesanan: {e}")
                print(f"Database error during delete: {e}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat menghapus pesanan: {e}")
                print(f"An unexpected error occurred during delete: {e}")

    def closeEvent(self, event):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            print("Database connection closed.")
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = OrderForm()
    form.show()
    sys.exit(app.exec_())
