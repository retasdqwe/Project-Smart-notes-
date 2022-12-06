#imports

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout 
import json

#window setup

app = QApplication([])
main_win = QWidget()

main_win.setWindowTitle('Умные заметки')
main_win.resize(900, 600)
notes = {
    "Добро пожаловать" : {
        "текст" : "Это самая лучшее приложение для заметок в мире!",
        "теги" : ["добро", "инструкция"]
    }
}
with open('notes_data.json', 'w') as file:
    json.dump(notes, file)

#interface

tip_text = QTextEdit()
tip_list_label = QLabel("Создайте новую заметку")
tip_list = QListWidget()
tcreate = QPushButton("Создать заметку")
tdelete = QPushButton("Удалить заметку")
tsave = QPushButton("Сохранить заметку")
tag_list_label = QLabel("Добавьте тег к вашей свежей заметке!")
tag_list = QListWidget()
tag_input = QLineEdit()
tag_input.setPlaceholderText('Введите тег...')
add_toTip = QPushButton("Добавить тег")
del_toTip = QPushButton("Удалить тег")
tag_search = QPushButton("Искать заметки по тегу")

lay_main = QHBoxLayout()
#lay_left_main = QVBoxLayout()
lay_right_main = QVBoxLayout()
create_del_lay = QHBoxLayout()
add_del_totip_lay = QHBoxLayout()

lay_main.addWidget(tip_text)
lay_main.addLayout(lay_right_main)
lay_right_main.addWidget(tip_list_label)
lay_right_main.addWidget(tip_list)
lay_right_main.addLayout(create_del_lay)
create_del_lay.addWidget(tcreate)
create_del_lay.addWidget(tdelete)
lay_right_main.addWidget(tsave)
lay_right_main.addWidget(tag_list_label)
lay_right_main.addWidget(tag_list)
lay_right_main.addWidget(tag_input)
lay_right_main.addLayout(add_del_totip_lay, stretch = 2)
add_del_totip_lay.addWidget(add_toTip)
add_del_totip_lay.addWidget(del_toTip)
lay_right_main.addWidget(tag_search)
main_win.setLayout(lay_main)

#functional

def show_note():
    key = tip_list.selectedItems()[0].text()
    print(key)
    tip_text.setText(notes[key]["текст"])
    tag_list.clear()
    tag_list.addItems(notes[key]["теги"])


main_win.show()
with open('notes_data.json', 'r') as file:
    notes = json.load(file)
tip_list.addItems(notes)


def add_note():
    tip_name, ok = QInputDialog.getText(main_win, "Добавить новенькую заметку", "Название")
    if ok and tip_name != "":
        notes[tip_name] = {'текст' : '', "теги" : []}
        tip_list.addItem(tip_name)
        tag_list.addItems(notes[tip_name]["теги"])
        print(notes)

def save_note():
    if tip_list.selectedItems():
        key = tip_list.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        print(notes)
    else:
        print("Не выбрана заметка для сохранения!")

def del_note():
    if tip_list.selectedItems():
        key = tip_list.selectedItems()[0].text()
        del notes[key]
        tip_list.clear()
        tag_list.clear()


def add_tag():
    if tip_list.selectedItems():
        key = tip_list.selectedItems()[0].text()
        tag = tag_input.text()
        if not tag in notes[key]["теги"]:
            notes[key]['теги'].append(tag)
            tag_list.addItem(tag)
            tag_input.clear()
            with open("notes_data.json", "w") as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii= False)
        else:
            print("Заметка для добавления тега не выбрана!")


def del_tag():
    if tag_list.selectedItems():
        key = tip_list.selectedItems()[0].text()
        tag = tag_list.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        tag_list.clear()
        tag_list.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii= False)
    else:
        print("Тег для удаления не выбрана!")


def search_tag():
    print(tag_search.text())
    tag = tag_input.text()
    if tag_search.text() == "Искать заметки по тегу" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        tag_search.setText('Сброс поиска')
        tip_list.clear()
        tag_list.clear()
        tip_list.addItems(notes_filtered)
        print(tag_search.text())
    elif tag_search.text() == 'Сброс поиска':
        tag_input.clear()
        tip_list.clear()
        tag_list.clear()
        tip_list.addItems(notes)
        tag_search.setText('Искать заметки по тегу')
        print(tag_search.text())
    else:
        pass


#execute
tip_list.itemClicked.connect(show_note)
tcreate.clicked.connect(add_note)
tsave.clicked.connect(save_note)
tdelete.clicked.connect(del_note)
add_toTip.clicked.connect(add_tag)
del_toTip.clicked.connect(del_tag)
tag_search.clicked.connect(search_tag)

app.exec()