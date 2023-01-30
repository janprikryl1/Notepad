import json
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QFontDialog, \
    QColorDialog, QShortcut, QAction
import sys
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtGui import QKeySequence
import os
import threading
from random import shuffle, sample

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("untitled.ui", self)
 
        #Titulek programu
        self.setWindowTitle("Poznámkový blok")  
        #Funkce po stisknutí tlačítka
        self.actionSavr.triggered.connect(self.save_as)
        self.actionClose.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.open)
        self.actionPo_et_slov.triggered.connect(self.countChars)
        self.actionPo_et_slov_2.triggered.connect(self.countwords)
        self.actionPo_et_definovan_ho_znaku.triggered.connect(self.countdefchar)
        self.actionUlo_it.triggered.connect(self.save)
        self.actionP_smo.triggered.connect(self.fontDialog)
        self.actionBarva.triggered.connect(self.colorDialog)
        self.actionTisk.triggered.connect(self.printDialog)
        self.actionN_hlad_tisku.triggered.connect(self.printpreviewDialog)
        self.actionVymazat_dvojit_mezery.triggered.connect(self.delete_double_spaces)
        self.actionSpustit_F5.triggered.connect(self.run_python)
        self.actionP_esmy_ky.triggered.connect(self.presmycka)
        self.actionKontroln_sou_et.triggered.connect(self.kontrolni_soucet)

        #Klávesové zkratky
        self.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self)
        self.shortcut_open.activated.connect(self.open)

        self.shortcut_save_as = QShortcut(QKeySequence('Ctrl+Shift+S'), self)
        self.shortcut_save_as.activated.connect(self.save_as)

        self.shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.shortcut_save.activated.connect(self.save)

        self.shortcut_run_python = QShortcut(QKeySequence('F5'), self)
        self.shortcut_run_python.activated.connect(self.run_python)


        self.file_name = None #Název otevřenho souboru

        self.recent_files()

 
        self.show()

    def recent_files(self):
        if os.path.exists("recent_files.json"):
            file = open("recent_files.json", "r", encoding="utf-8")
            data = json.loads(file.read())
            print(data)
            if len(data['recent-files']) >= 3:
                data1 = data['recent-files'][2]
                data2 = data['recent-files'][1]
                data3 = data['recent-files'][0]
                self.menuOtev_t_ned_vn.addAction(QAction(data1, self, triggered=lambda: self.open_recent(data1)))
                self.menuOtev_t_ned_vn.addAction(QAction(data2, self, triggered=lambda: self.open_recent(data2)))
                self.menuOtev_t_ned_vn.addAction(QAction(data3, self, triggered=lambda: self.open_recent(data3)))
            elif len(data['recent-files']) == 2:
                data1 = data['recent-files'][1]
                data2 = data['recent-files'][0]
                self.menuOtev_t_ned_vn.addAction(QAction(data1, self, triggered=lambda: self.open_recent(data1)))
                self.menuOtev_t_ned_vn.addAction(QAction(data2, self, triggered=lambda: self.open_recent(data2)))
            elif len(data['recent-files']) == 1:
                data1 = data['recent-files'][0]
                self.menuOtev_t_ned_vn.addAction(QAction(data1, self, triggered=lambda: self.open_recent(data1)))
            else:
                self.menuOtev_t_ned_vn.addAction(QAction("Žádné nedávné soubory", self))
        else:
            json_text = {"recent-files": []}
            file = open("recent_files.json", "w")
            json.dump(json_text, file)
            file.close()
            self.menuOtev_t_ned_vn.addAction(QAction("Žádné nedávné soubory", self))


    def open_recent(self, file_name):
        if os.path.exists(file_name):
            self.file_name = file_name
            text = open(str(self.file_name), 'r', encoding="utf-8")
            self.textEdit.setText(text.read())
            self.actionUlo_it.setEnabled(True)
        else:
            QMessageBox.about(self, "Chyba", "Není možné najít soubor")

    def fontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)
 
    def colorDialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)


    def countChars(self):
        QMessageBox.about(self, "Počet znaků", str(len(self.textEdit.toPlainText())))
        
    def countwords(self):
        words = (self.textEdit.toPlainText()).split(" ")
        QMessageBox.about(self, "Počet slov", str(len(words)))

    def countdefchar(self):
        char = self.textEdit.textCursor().selectedText()
        if not char:
            char, _ = QInputDialog.getText(self, "Definovaný znak","Který znak chcete vyhledat", QLineEdit.Normal, "")
        if char:
            QMessageBox.about(self, "Hledaný znak", str(self.textEdit.toPlainText().count(char)))


    def delete_double_spaces(self):
        text = self.textEdit.toPlainText()
        while "  " in text:
            text = text.replace("  ", " ")
        self.textEdit.setText(text)

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Vyberte soubor", "","Textové soubory (*.txt);;Python (*.py);;Všechny soubory (*)", options=options)
        if fileName:
            self.file_name = fileName
            text = open(str(self.file_name), 'r', encoding="utf-8") 
            self.textEdit.setText(text.read())
            self.actionUlo_it.setEnabled(True)

            file = open("recent_files.json", "r")
            data = json.loads(file.read())['recent-files']
            if len(data) > 3:
                data = data[-3:]
            data.append(self.file_name)
            json_text = {"recent-files": data}
            file.close()

            file = open("recent_files.json", "w")
            json.dump(json_text, file)
            file.close()

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Zadejte název souboru pro uložení",".txt","Textové soubory (*.txt);;Python (*.py);;Všechny soubory (*)", options=options)
        if fileName:
            self.file_name = fileName
            file = open(self.file_name, 'w', encoding="utf-8")
            file.write(self.textEdit.toPlainText())
            file.close()
            self.actionUlo_it.setEnabled(True)

            file = open("recent_files.json", "r")
            data = json.loads(file.read())['recent-files']
            if len(data) > 3:
                data = data[-3:]
            data.append(self.file_name)
            json_text = {"recent-files": data}
            file.close()

            file = open("recent_files.json", "w")
            json.dump(json_text, file)
            file.close()


    def save(self):
        if self.file_name:
            file = open(self.file_name, 'w', encoding="utf-8")
            file.write(self.textEdit.toPlainText())
            file.close()
        else:
            self.save_as()


    def printDialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)
 
 
    def printpreviewDialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()
 
 
    def printPreview(self, printer):
        self.textEdit.print_(printer)
    

    def run_python(self):
        if self.file_name and self.file_name.split(".")[-1] == "py":
            thread = threading.Thread(target=self.cmd_thread)
            thread.start()
        else:
            QMessageBox.information(self, "Není možné spustit skript", "Musíte mít otevřený soubor, který musí končit příponou .py")


    def cmd_thread(self):
        os.system(f'start /wait cmd /c python {self.file_name}')

    
    def close_alert(self, event):
        reply = QMessageBox.question(
                        self, "Zavřít?",
                        "Opravdu chcete odejít?\nNeuložené změny se zahodí.",
                        QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
                        QMessageBox.Save)

        if reply == QMessageBox.Close:
            event.accept()
        elif reply == QMessageBox.Cancel:
            event.ignore()
        else:
            if not self.file_name:
                self.save_as()
            else:
                self.save()
            event.accept()
            #event.ignore()


    def closeEvent(self, event):
        if self.file_name or self.textEdit.toPlainText():
            if self.file_name:
                original_file = open(str(self.file_name), 'r', encoding="utf-8") 
                original_file_text = original_file.read()
                if original_file_text != self.textEdit.toPlainText():
                    self.close_alert(event)
            else:
                self.close_alert(event)


    def presmycka(self):
        text = self.textEdit.toPlainText()
        self.textEdit.setText(''.join(sample(text, len(text))))

    def kontrolni_soucet(self):
        text = self.textEdit.toPlainText()
        soucet = 0
        for i in text:
            soucet += ord(i)
        while soucet > 255:
            text = str(soucet)
            soucet = 0
            for i in text:
                soucet += ord(i)
        QMessageBox.information(self, "Kontrolní součet",
                                f"Kontrolní součet textu je {soucet}")

    def close(self):
        sys.exit(0)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()