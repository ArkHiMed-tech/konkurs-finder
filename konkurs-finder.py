from bs4 import BeautifulSoup
import requests
import csv
import sys
from PyQt6 import QtWidgets, QtCore

HOST = 'https://xn--80aayamnhpkade1j.xn--p1ai/'  # Объявление констант для запросов на сайт
URL = 'https://xn--80aayamnhpkade1j.xn--p1ai/events?date=2021-2022'
HEADER = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

sl = {  # cловарь для считывания команд из терминала
    'title': ['название', 'заголовок', 'н', 'титл', 'title'],
    'theme': ['тема', 'раздел', 'т', 'тематика', 'предмет', 'отрасль', 'theme'],
    'organizator': ['организатор', 'устроитель', 'ор', 'organizator'],
    'description': ['описание', 'оп', 'description'],
    'link': ['ссылка', 'с', 'линк', 'link'],
    'all': ['везде', 'все', 'всюду', 'в', 'all'],
    'terminal': ['in terminal', 'terminal', 'в терминал', 'терминал', 'тер'],
    'file': ['in file', 'file', 'в файл', 'файл', 'ф']
}


def get_html(url, params=''):
    responce = requests.get(url, headers=HEADER, params=params)
    return responce 


def get_content(html):   # Парсинг данных
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='toggles-b js-toggle-row')
    contests = []
    for i, item in enumerate(items):
        organ = item.find('div', class_='card card-body').find('div', style='margin-bottom: 5px;').text.partition(
            'Организаторы')[2].strip() if item.find('div', class_='card card-body').find('div',
                                                                                         style='margin-bottom: 5px;') else '-'
        descr = item.find('div', class_='card card-body').text.partition('Профили')[2].replace('Cайт мероприятия',
                                                                                               '').strip() if item.find(
            'div', class_='card card-body').find('h4') else '-'
        lnk = item.find('div', class_='card-body').find('a').get('href') if item.find('div', class_='card-body').find(
            'a') else '-'
        contests.append(
            {
                'title': item.find('div', class_='col-8').get_text(),
                'theme': item.find('div', class_='col-3').get_text(),
                'organizator': organ,
                'description': descr,
                'link': lnk
            }
        )
    return contests


def filtrate(lst, path, find: str):
    if path == 'all':
        items = []
        for item in lst:
            for value in item.values():
                if find.lower() in value.lower() or find.lower().capitalize() in value:
                    items.append(item)
                    break
        return items
    elif path == 'title' or path == 'theme' or path == 'organizator' or path == 'description' or path == 'link':
        items = []
        for item in lst:
            if find in item[path]:
                items.append(item)
        return items
    else:
        return [{
            'title': 'Ошибка \'path\'',
            'theme': 'Ошибка \'path\'',
            'organizator': 'Ошибка \'path\'',
            'description': 'Ошибка \'path\'',
            'link': 'Ошибка \'path\''
        }]


def save_doc(items, path):
    with open(path, 'w', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Тема', 'Организатор', 'Описание', 'Ссылка'])
        for item in items:
            writer.writerow([
                item['title'],
                item['theme'],
                item['organizator'],
                item['description'],
                item['link']
            ])


def findword(word: str, d: dict[str, list[str]]):
    for key, value in d.items():
        if word in value:
            print('Успешно')
            return key


def outprint(url):
    html = get_html(url)
    c = get_content(html)
    way = findword(input('Способ вывода (файл/терминал) >>>'), sl)
    filtrated = filtrate(c, findword(input('Раздел >>>').lower(), sl), input('Поиск >>>'))
    if way == 'terminal':
        outwhat = str(findword(input('Вывод раздела >>>').lower(), sl))
        if outwhat == 'all':
            for i in filtrated:
                print(i['title'], '\n', i['theme'], '\n', i['organizator'], '\n', i['description'], '\n', i['link'],
                      '\n')
        else:
            for i in filtrated:
                print(i[outwhat])
    elif way == 'file':
        with open("C:\\Users\\Ученик\\Desktop\\Рабочая папка\\Python_logs\\activities.txt", 'w+',
                  encoding='utf-8') as activities:
            for i in filtrated:
                print(i['title'], '\n', i['theme'], '\n', i['organizator'], '\n', i['description'], '\n', i['link'],
                      '\n\n', file=activities)


def out_print_program(url, path, find, out_path):
    html = get_html(url)
    c = get_content(html)
    filtrated = filtrate(c, path, find)
    outwhat = out_path
    string = ''
    if outwhat == 'all':
        for i in filtrated:
            string = string + i['title']
            string = string + '\n'
            string = string + i['theme']
            string = string + '\n'
            string = string + i['organizator']
            string = string + '\n'
            string = string + i['description']
            string = string + '\n'
            string = string + i['link']
            string = string + '\n\n_____________________\n'
    else:
        for i in filtrated:
            string = string + i[outwhat]
            string = string + '\n'
    with open("activities.txt", 'w+', encoding='utf-8') as activities:
        for i in filtrated:
            print(i['title'], '\n', i['theme'], '\n', i['organizator'], '\n', i['description'], '\n', i['link'], '\n\n',
                  file=activities)
    return string


class Ui_FindKonkurs(object):
    def setupUi(self, FindKonkurs):
        FindKonkurs.setObjectName("FindKonkurs")
        FindKonkurs.resize(464, 513)
        FindKonkurs.setMinimumSize(QtCore.QSize(464, 513))
        FindKonkurs.setMaximumSize(QtCore.QSize(464, 513))
        FindKonkurs.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(FindKonkurs)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 111, 171))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 10, 47, 13))
        self.label.setObjectName("label")
        self.groupIn = QtWidgets.QGroupBox(self.frame)
        self.groupIn.setGeometry(QtCore.QRect(0, 30, 120, 131))
        self.groupIn.setTitle("")
        self.groupIn.setObjectName("groupIn")
        self.FindInTitle = QtWidgets.QRadioButton(self.groupIn)
        self.FindInTitle.setGeometry(QtCore.QRect(10, 10, 82, 17))
        self.FindInTitle.setObjectName("FindInTitle")
        self.FindInTheme = QtWidgets.QRadioButton(self.groupIn)
        self.FindInTheme.setGeometry(QtCore.QRect(10, 30, 82, 17))
        self.FindInTheme.setObjectName("FindInTheme")
        self.FindInOrganizators = QtWidgets.QRadioButton(self.groupIn)
        self.FindInOrganizators.setGeometry(QtCore.QRect(10, 50, 101, 17))
        self.FindInOrganizators.setObjectName("FindInOrganizators")
        self.FindInDescription = QtWidgets.QRadioButton(self.groupIn)
        self.FindInDescription.setGeometry(QtCore.QRect(10, 70, 82, 17))
        self.FindInDescription.setObjectName("FindInDescription")
        self.FindInLink = QtWidgets.QRadioButton(self.groupIn)
        self.FindInLink.setGeometry(QtCore.QRect(10, 90, 82, 17))
        self.FindInLink.setObjectName("FindInLink")
        self.FindAll = QtWidgets.QRadioButton(self.groupIn)
        self.FindAll.setGeometry(QtCore.QRect(10, 110, 82, 17))
        self.FindAll.setObjectName("FindAll")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(260, 0, 111, 171))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 47, 13))
        self.label_2.setObjectName("label_2")
        self.groupOut = QtWidgets.QGroupBox(self.frame_2)
        self.groupOut.setGeometry(QtCore.QRect(0, 30, 120, 131))
        self.groupOut.setTitle("")
        self.groupOut.setObjectName("groupOut")
        self.OutTitle = QtWidgets.QRadioButton(self.groupOut)
        self.OutTitle.setGeometry(QtCore.QRect(10, 10, 82, 17))
        self.OutTitle.setObjectName("OutTitle")
        self.OutTheme = QtWidgets.QRadioButton(self.groupOut)
        self.OutTheme.setGeometry(QtCore.QRect(10, 30, 82, 17))
        self.OutTheme.setObjectName("OutTheme")
        self.OutOrganizator = QtWidgets.QRadioButton(self.groupOut)
        self.OutOrganizator.setGeometry(QtCore.QRect(10, 50, 101, 17))
        self.OutOrganizator.setObjectName("OutOrganizator")
        self.OutDescription = QtWidgets.QRadioButton(self.groupOut)
        self.OutDescription.setGeometry(QtCore.QRect(10, 70, 82, 17))
        self.OutDescription.setObjectName("OutDescription")
        self.OutLink = QtWidgets.QRadioButton(self.groupOut)
        self.OutLink.setGeometry(QtCore.QRect(10, 90, 82, 17))
        self.OutLink.setObjectName("OutLink")
        self.OutAll = QtWidgets.QRadioButton(self.groupOut)
        self.OutAll.setGeometry(QtCore.QRect(10, 110, 82, 17))
        self.OutAll.setObjectName("OutAll")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(130, 0, 120, 161))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.FindWord = QtWidgets.QTextEdit(self.frame_3)
        self.FindWord.setGeometry(QtCore.QRect(0, 50, 111, 31))
        self.FindWord.setObjectName("FindWord")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label_3.setObjectName("label_3")
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(390, 80, 75, 23))
        self.StartButton.setAutoDefault(False)
        self.StartButton.setDefault(True)
        self.StartButton.setObjectName("StartButton")
        self.OutputText = QtWidgets.QTextEdit(self.centralwidget)
        self.OutputText.setGeometry(QtCore.QRect(0, 170, 464, 343))
        self.OutputText.setReadOnly(True)
        self.OutputText.setCursorWidth(1)
        self.OutputText.setObjectName("OutputText")
        FindKonkurs.setCentralWidget(self.centralwidget)

        self.retranslateUi(FindKonkurs)
        QtCore.QMetaObject.connectSlotsByName(FindKonkurs)

    def retranslateUi(self, FindKonkurs):
        _translate = QtCore.QCoreApplication.translate
        FindKonkurs.setWindowTitle(_translate("FindKonkurs", "Поиск конкурсов"))
        self.label.setText(_translate("FindKonkurs", "Поиск в:"))
        self.groupIn.setTitle(_translate("FindKonkurs", ""))
        self.FindInTitle.setText(_translate("FindKonkurs", "Заголовке"))
        self.FindInTheme.setText(_translate("FindKonkurs", "Теме"))
        self.FindInOrganizators.setText(_translate("FindKonkurs", "Организаторах"))
        self.FindInDescription.setText(_translate("FindKonkurs", "Описании"))
        self.FindInLink.setText(_translate("FindKonkurs", "Ссылке"))
        self.FindAll.setText(_translate("FindKonkurs", "Везде"))
        self.FindInTitle.setChecked(True)
        self.label_2.setText(_translate("FindKonkurs", "Вывод:"))
        self.groupOut.setTitle(_translate("FindKonkurs", ""))
        self.OutTitle.setText(_translate("FindKonkurs", "Заголовок"))
        self.OutTitle.setChecked(True)
        self.OutTheme.setText(_translate("FindKonkurs", "Тема"))
        self.OutOrganizator.setText(_translate("FindKonkurs", "Организаторы"))
        self.OutDescription.setText(_translate("FindKonkurs", "Описание"))
        self.OutLink.setText(_translate("FindKonkurs", "Ссылка"))
        self.OutAll.setText(_translate("FindKonkurs", "Все"))
        self.label_3.setText(_translate("FindKonkurs", "Поиск:"))
        self.StartButton.setText(_translate("FindKonkurs", "Начать"))
        self.StartButton.clicked.connect(self.FindInFunc)

    url = 'https://xn--80aayamnhpkade1j.xn--p1ai/events'
    pathin = ''
    find = ''
    outpath = ''
    txt = ''

    def activate_button(self):
        self.txt = out_print_program(self.url, self.pathin, self.find, self.outpath)
        print('Текст настроен')
        self.textFormating()

    def FindInFunc(self):
        print('Кнопка кликнута')
        if self.FindInTitle.isChecked():
            self.pathin = 'title'
        elif self.FindInDescription.isChecked():
            self.pathin = 'description'
        elif self.FindInTheme.isChecked():
            self.pathin = 'theme'
        elif self.FindInOrganizators.isChecked():
            self.pathin = 'organizators'
        elif self.FindInLink.isChecked():
            self.pathin = 'link'
        elif self.FindAll.isChecked():
            self.pathin = 'all'

        if self.OutTitle.isChecked():
            self.outpath = 'title'
        elif self.OutDescription.isChecked():
            self.outpath = 'description'
        elif self.OutTheme.isChecked():
            self.outpath = 'theme'
        elif self.OutOrganizator.isChecked():
            self.outpath = 'organizators'
        elif self.OutLink.isChecked():
            self.outpath = 'link'
        elif self.OutAll.isChecked():
            self.outpath = 'all'

        self.find = self.FindWord.document().begin().text()

        print('Сбор параметров завершен')

        self.activate_button()

        print('Программа завершена\n__________\n')

    def textFormating(self):
        if self.txt == '' and self.OutputText.document().begin().text() == 'Ничего не найдено':
            self.txt = 'Все еще ничего не найдено\n\n\nСОВЕТ: попробуйте выбрать поиск в другом разделе или сменить текст для поиска.'
        if self.txt == '':
            self.txt = 'Ничего не найдено\n\n\nСОВЕТ: попробуйте выбрать поиск в другом разделе или сменить текст для поиска.'
        self.OutputText.clear()
        self.OutputText.setText(self.txt)
        print('Текст выведен')


class InputFrame(QtWidgets.QMainWindow, Ui_FindKonkurs):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = InputFrame()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение


if __name__ == '__main__':
    # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
