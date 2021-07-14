import sys
import os
import shutil

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore


# Класс обработчика всех изображений, путей к ним и так далее.
class ImagesReader:

    def __init__(self, path: str):
        """
        Конструктор класса
        :param path: путь к директории с изображениями
        """

        # Сохранение пути к директории.
        self.path = path

        # Сохранение всех путей к изображениям
        self.image_paths = []
        for file_path in os.listdir(path):
            if os.path.splitext(file_path)[1] == '.jpg':
                self.image_paths.append(os.path.join(path, file_path))
        self.image_index = -1

    def get_length(self):
        """
        Возвращает кол-во изображений в директории.
        :return: int
        """

        return len(self.image_paths)

    def copy_image_to(self, copy_folder: str):
        """
        Метод для копирования изображения в выбранную директорию.
        :param copy_folder: путь, куда надо скопировать изображение.
        :return:
        """

        # Копирование.
        shutil.copy(
            self.image_paths[self.image_index],
            os.path.join(
                copy_folder, os.path.basename(self.image_paths[self.image_index])
            )
        )

    def next_image(self):
        """
        Функция для получения пути к следующему изображентию в директории.
        :return: str
        """

        # Если непроверенные изображения еще остались,
        # то переводим индекс на следующий элемент в списке путей.
        # Иначе возвращается стандартное изображение not_found_image.jpg.
        if self.image_index < self.get_length() - 1:
            self.image_index += 1
        else:
            return 'not_found_image.jpg'

        # Возвращаем путь к изображению.
        return self.image_paths[self.image_index]


# Класс главного окна.
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Инициализация виджетов изображения и счетчика,
        # чтобы их можно было позже обновлять.
        self.image = None
        self.label_counter = None

        # Инициализация обработчика изображений
        self.images_reader = None

        # Инициализация интерфейса
        self.initUI()

    def initUI(self):
        """
        Метод для инициализации интерфейса.
        :return:
        """

        layout_main = QVBoxLayout()         # Макет всего окна.
        layout_load = QHBoxLayout()         # Макет верхней части интерфейса (для кнопки обзора.
        layout_choose_type = QHBoxLayout()  # Макет нижней части интерфейса (для кнопок выбора).

        # Формирование макета для кнопки обзора.
        # Инициализация кнопки.
        btn_load = QPushButton('Обзор')
        btn_load.clicked.connect(self.load_data)

        # Добавление виджетов в макет.
        layout_load.addWidget(QWidget())
        layout_load.addWidget(btn_load)

        # Инициализация виджета для изображения.
        self.image = QLabel()
        self.image.setPixmap(QPixmap('not_found_image.jpg'))

        # Формирование макета для кнопок выбора.
        # Инициализация кнопки для определения изображения в папку pos.
        btn_pos = QPushButton('pos')
        btn_pos.clicked.connect(self.copy_to_pos)

        # Инициализация кнопки для определения изображения в папку neg.
        btn_neg = QPushButton('neg')
        btn_neg.clicked.connect(self.copy_to_neg)

        # Инициализация текста с для номера изображения.
        self.label_counter = QLabel('0/0')
        self.label_counter.setAlignment(QtCore.Qt.AlignCenter)

        # Добавление виджетов в макет.
        layout_choose_type.addWidget(btn_pos)
        layout_choose_type.addWidget(self.label_counter)
        layout_choose_type.addWidget(btn_neg)

        # Формирование главного макета.
        layout_main.addLayout(layout_load)
        layout_main.addWidget(self.image)
        layout_main.addLayout(layout_choose_type)

        self.setLayout(layout_main)
        self.setGeometry(100, 100, 100, 100)
        self.setWindowTitle('FaceChooser')
        self.show()

    def update_image(self, image_path: str):
        """
        Метод для обновления виджета изображения и виджета счетчика.
        :param image_path: путь к изображению, которое надо отобразить (string).
        :return:
        """

        # Установка изображения и счетчика.
        self.image.setPixmap(QPixmap(image_path).scaledToWidth(192).scaledToHeight(192))
        self.label_counter.setText(f'{self.images_reader.image_index + 1}/{self.images_reader.get_length()}')

    def load_data(self):
        """
        Метод для выбора директории с изображениями.
        :return:
        """

        # Выбор директории.
        folder_path = QFileDialog.getExistingDirectory(self, 'Выбрать папку')

        # Если директория была выбрана, то производится загрузка изображений и обновление изображения.
        if folder_path:
            self.images_reader = ImagesReader(folder_path)
            self.update_image(self.images_reader.next_image())

    def copy_to_pos(self):
        """
        Метод для копирования текущего изображения в папку pos.
        :return:
        """
        # Если обработчик изображений загружен,
        # то производится копирование в pos и обновление изображения.
        # Иначе выводится сообщение об ошибке.
        if self.images_reader is not None:
            self.images_reader.copy_image_to('pos')
            self.update_image(self.images_reader.next_image())
        else:
            QMessageBox.about(self, 'Ошибка', 'Необходимо выбрать директорию с изображениями')

    def copy_to_neg(self):
        """
        Метод для копирования текущего изображения в папку neg.
        :return:
        """

        # Если обработчик изображений загружен,
        # то производится копирование в neg и обновление изображения.
        # Иначе выводится сообщение об ошибке.
        if self.images_reader is not None:
            self.images_reader.copy_image_to('neg')
            self.update_image(self.images_reader.next_image())
        else:
            QMessageBox.about(self, 'Ошибка', 'Необходимо выбрать директорию с изображениями')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создание папок pos и neg.
    if not os.path.exists('pos'):
        os.mkdir('pos')
    if not os.path.exists('neg'):
        os.mkdir('neg')

    window = MainWindow()

    sys.exit(app.exec_())
