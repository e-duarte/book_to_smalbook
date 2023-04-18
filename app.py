from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QLabel, QLineEdit, QPushButton, QVBoxLayout
from livreto import Livreto


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Livreto")

        # Criação dos widgets
        self.input_label = QLabel("Arquivo de entrada:", self)
        self.input_line_edit = QLineEdit(self)
        self.input_browse_button = QPushButton("Selecionar arquivo", self)

        self.output_label = QLabel("Pasta de saída:", self)
        self.output_line_edit = QLineEdit(self)
        self.output_browse_button = QPushButton("Selecionar pasta", self)

        self.convert_button = QPushButton("Converter", self)

        # Adição dos widgets ao layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_line_edit)
        layout.addWidget(self.input_browse_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_line_edit)
        layout.addWidget(self.output_browse_button)
        layout.addWidget(self.convert_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Conexão dos sinais aos slots
        self.input_browse_button.clicked.connect(self.browse_input_file)
        self.output_browse_button.clicked.connect(self.browse_output_folder)
        self.convert_button.clicked.connect(self.convert)

    def browse_input_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("PDF files (*.pdf)")
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]
            self.input_line_edit.setText(file_name)

    def browse_output_folder(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.Directory)
        if folder_dialog.exec_():
            folder_name = folder_dialog.selectedFiles()[0]
            self.output_line_edit.setText(folder_name)

    def convert(self):
        input_file = self.input_line_edit.text()
        output_folder = self.output_line_edit.text()


        if not input_file:
            QMessageBox.critical(self, "Erro", "Selecione um arquivo de entrada.")
            return

        if not output_folder:
            QMessageBox.critical(self, "Erro", "Selecione uma pasta de saída.")
            return
        try:
            livreto = Livreto(input_file, output_folder)
            livreto.generate_livreto()
            QMessageBox.information(self, "Sucesso", "A conversão foi concluída com sucesso.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"A conversão falhou: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
