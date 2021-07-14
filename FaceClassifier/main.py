import numpy as np
import sys
import os

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore


# Функция для предобработки изображения.
def preprocess(x):
    return (x - 127.5) / 128


# Класс для обработчика, который будет получать модель,
# использовать ее для тестирования и для показа результатов.
class ModelViewer:
    def __init__(self, model_path: str):
        """
        Конструктор класса для обработки моделей
        :param model_path: путь к файлу модели
        """

        # Загрузка модели
        self.model = tf.keras.models.load_model(model_path)

        # Инициализация специальных групп, на которые входные изображения
        # будут делиться: FN - False Negative(0), FP - False Positive(1),
        # TN - True Negative(2), TP - True Positive(3).
        self.groups = [[], [], [], []]

        # Индексы номера группы и номера изображения,
        # которые показываются в определенный момент.
        self.group_indexes = [0, 0, 0, 0]
        self.group_index = 0

        # Проверка существование папок "pos" и "neg",
        if not os.path.exists(os.path.join('data', 'pos')):
            raise FileNotFoundError('Directory "pos" was not found')
        if not os.path.exists(os.path.join('data', 'neg')):
            raise FileNotFoundError('Directory "neg" was not found')

        # Инициализация генераторов, через которые будут получаться изображения
        image_gen = ImageDataGenerator(preprocessing_function=preprocess)
        data_gen = image_gen.flow_from_directory(shuffle=False,
                                                 directory='data',
                                                 target_size=(96, 96),
                                                 class_mode='binary')

        # Проверка присутствия изображений в папках "pos" и "neg".
        if not (0 in data_gen.classes):
            raise FileNotFoundError('Images was not found in directory "neg"')
        if not(1 in data_gen.classes):
            raise FileNotFoundError('Images was not found in directory "pos"')

        # Распределение путей к изображениями по группам.
        predicts = self.model.predict(data_gen) >= 0.5
        for i, (predict, file_path) in enumerate(zip(predicts, data_gen.filepaths)):
            if i < np.unique(data_gen.classes, return_counts=True)[1][0]:
                if predict:
                    self.groups[1].append(file_path)
                else:
                    self.groups[2].append(file_path)
            else:
                if predict:
                    self.groups[3].append(file_path)
                else:
                    self.groups[0].append(file_path)

    def accuracy(self):
        """
        Возвращает метрику accuracy для модели.
        :return: float
        """

        # (TP + TN) / (TP + TN + FP + FN).
        return (len(self.groups[3]) + len(self.groups[2])) / \
               (len(self.groups[3]) + len(self.groups[2]) + len(self.groups[1]) + len(self.groups[0]))

    def precision(self):
        """
        Возвращает метрику precision для модели.
        :return: float
        """

        # TP / (TP + FP)
        return len(self.groups[3]) / (len(self.groups[3]) + len(self.groups[1]))

    def recall(self):
        """
        Возвращает метрику recall для модели.
        :return: float
        """

        # TP / (TP + FN)
        return len(self.groups[3]) / (len(self.groups[3]) + len(self.groups[0]))

    def f1_measure(self):
        """
        Возвращает метрику f1-меру для модели.
        :return: float
        """
        return 2 * self.accuracy() * self.precision() / (self.accuracy() + self.precision())

    def get_length(self):
        """
        Возвращает длину выбранной группы в данный момент.
        :return: int
        """
        return len(self.groups[self.group_index])

    def get_index(self):
        """
        Возвращает индекс выбранного изображения в текущей группе.
        :return: int
        """
        return self.group_indexes[self.group_index]

    def get_image(self):
        """
        Возвращает путь к текущему изображению.
        :return: str
        """
        if self.get_length() == 0:
            return 'not_found_image.jpg'
        else:
            return self.groups[self.group_index][self.get_index()]

    def change_group(self, group_index: int):
        """
        Меняет группу на новую и возвращает текущее изображение в данной группе.
        :param group_index: индекс выбранной группы.
        :return: str
        """
        self.group_index = group_index
        return self.get_image()

    def next_image(self):
        """
        Увеличивается индекс текущего изображения в группе и возвращается текущее изображение.
        :return:
        """

        # Индекс меняется только если это возможно
        if self.get_index() < self.get_length() - 1:
            self.group_indexes[self.group_index] += 1

        # Возвращаем путь к изображению.
        return self.get_image()

    def previous_image(self):
        """
        Уменьшается индекс текущего изображения в группе и возвращается текущее изображение.
        :return:
        """

        # Индекс меняется только если это возможно
        if self.get_index() > 0:
            self.group_indexes[self.group_index] -= 1

        # Возвращаем путь к изображению.
        return self.get_image()


# Класс главного окна.
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Инициализация виджетов, которым необходимо будет обращаться,
        # в течении работы всей программы.
        self.group_select_box = None
        self.image = None
        self.label_counter = None
        self.label_accuracy = None
        self.label_precision = None
        self.label_recall = None
        self.label_f1 = None

        # Инициализация переменной для модели.
        self.model_viewer = None

        # Инициализация интерфейса.
        self.initUI()

    def initUI(self):
        """
        Метод для инициализации интерфейса.
        :return:
        """

        layout_main = QVBoxLayout()         # Макет всего окна.
        layout_load = QHBoxLayout()         # Макет верхней части интерфейса (выбор модели и группы).
        layout_choose_type = QHBoxLayout()  # Макет интерфейса для выбора изображения.
        layout_metrics = QVBoxLayout()      # Макет нижней части интерфейса с метриками.

        # Формирование макета для кнопки обзора.
        # Инициализация виджет для выбора группы.
        self.group_select_box = QComboBox()
        self.group_select_box.addItems(
            ['Неверно выбранные лица (FN)', 'Неверно выбранные не лица (FP)',
             'Верно выбранные лица (TN)', 'Верно выбранные не лица (TP)']
        )
        self.group_select_box.activated[int].connect(self.change_images_group)

        # Инициализация кнопки.
        btn_load = QPushButton('Выбрать модель')
        btn_load.clicked.connect(self.load_data)

        # Добавление виджетов в макет.
        layout_load.addWidget(self.group_select_box)
        layout_load.addWidget(btn_load)

        # Инициализация виджета для изображения.
        self.image = QLabel()
        self.image.setPixmap(QPixmap('not_found_image.jpg').scaledToWidth(300).scaledToHeight(300))

        # Формирование макета для кнопок выбора.
        # Инициализация кнопки для определения изображения в папку pos.
        btn_pos = QPushButton('<---')
        btn_pos.clicked.connect(self.previous_image)

        # Инициализация кнопки для определения изображения в папку neg.
        btn_neg = QPushButton('--->')
        btn_neg.clicked.connect(self.next_image)

        # Инициализация текста с для номера изображения.
        self.label_counter = QLabel('0/0')
        self.label_counter.setAlignment(QtCore.Qt.AlignCenter)

        # Добавление виджетов в макет.
        layout_choose_type.addWidget(btn_pos)
        layout_choose_type.addWidget(self.label_counter)
        layout_choose_type.addWidget(btn_neg)

        # Формирование макета с метриками модели.
        # Инициализация виджетов надписей для метрик.
        self.label_accuracy = QLabel('Accuracy: ???')
        self.label_precision = QLabel('Precision: ???')
        self.label_recall = QLabel('Recall: ???')
        self.label_f1 = QLabel('F1: ???')

        # Добавление виджетов в макет.
        layout_metrics.addWidget(self.label_accuracy)
        layout_metrics.addWidget(self.label_precision)
        layout_metrics.addWidget(self.label_recall)
        layout_metrics.addWidget(self.label_f1)

        # Формирование главного макета.
        layout_main.addLayout(layout_load)
        layout_main.addWidget(self.image)
        layout_main.addLayout(layout_choose_type)
        layout_main.addLayout(layout_metrics)

        self.setLayout(layout_main)
        self.setGeometry(100, 100, 100, 100)
        self.setWindowTitle('FaceChooser')
        self.show()

    def update_image(self, image_path: str):
        """
        Метод для обновления виджета изображения и виджета счетчика.
        :param image_path: путь к изображению, которое надо отобразить.
        :return:
        """

        # Установка изображения и счетчика.
        self.image.setPixmap(QPixmap(image_path).scaledToWidth(300).scaledToHeight(300))
        self.label_counter.setText(
            f'{self.model_viewer.get_index() + 1}/{self.model_viewer.get_length()}'
        )

    def load_data(self):
        """
        Метод для выбора директории с изображениями.
        :return:
        """

        # Выбор файла модели.
        model_path = QFileDialog.getOpenFileName(self, 'Выбрать модель')[0]

        # Если директория была выбрана, то производится загрузка модели.
        if model_path:
            try:
                self.model_viewer = ModelViewer(model_path)
                self.model_viewer.change_group(self.group_select_box.currentIndex())
                self.update_image(self.model_viewer.get_image())
                self.label_accuracy.setText(f'Accuracy: {self.model_viewer.accuracy()}')
                self.label_precision.setText(f'Precision: {self.model_viewer.precision()}')
                self.label_recall.setText(f'Recall: {self.model_viewer.recall()}')
                self.label_f1.setText(f'F1: {self.model_viewer.f1_measure()}')
            # Выдача ошибки, если не найдены нужные директории, либо какая-то директория пуста.
            except FileNotFoundError:
                QMessageBox.about(self, 'Ошибка загрузки',
                                  'Отсутствует директория pos, либо neg, либо одна из них пуста')
            # Выдача ошибки, если загрузка модели прошла неуспешно.
            except (ImportError, IOError):
                QMessageBox.about(self, 'Ошибка загрузки',
                                  'Выбран неверный файл модели, либо модель невозможно загрузить')

    def change_images_group(self, item_index: int):
        """
        Метод для изменения группы изображений, которые показываются.
        :param item_index: индекс выбранного элемента в списке.
        :return:
        """

        # Если модель загружена, то меняется группа и обновляятся изображение.
        if self.model_viewer is not None:
            self.model_viewer.change_group(item_index)
            self.update_image(self.model_viewer.get_image())

    def next_image(self):
        """
        Метод для перехода к следующему изображению в группе.
        :return:
        """

        # Если модель загружена, то производится переход,
        # иначе выдается ошибка.
        if self.model_viewer is not None:
            self.update_image(self.model_viewer.next_image())
        else:
            QMessageBox.about(self, 'Ошибка', 'Необходимо выбрать модель')

    def previous_image(self):
        """
        Метод для перехода к предыдущему изображению в группе.
        :return:
        """

        # Если модель загружена, то производится переход,
        # иначе выдается ошибка.
        if self.model_viewer is not None:
            self.update_image(self.model_viewer.previous_image())
        else:
            QMessageBox.about(self, 'Ошибка', 'Необходимо выбрать модель')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())
