# FaceClassifierNetwork
Проект содержащий полный цикл создания нейросети для классификации лиц - от генерации данных до тестирования итоговой сети
Данный репозиторий содержит в себе 4 различных проекта для разных задач:
1. FacesDetector - проект, написанный на C# на WPF с использованием библиотеки EmguCV (OpenCV на C#). 
Задача данного проекта заключается в том, чтобы из определенного набора картинок вырезать лица и различные ложные результаты, определяемые стандартным OpenCV детектором.
2. FacesChooser - проект, написанный на python для того, чтобы все полученные лица и не лица разделить по группам, и таким образом подготовить выборку для обучения.
3. FacesClassifier - данный проект также написан на python и выполняет задачу итогового графического приложения для тестирования полученных сетей.
С его помощью можно посмотреть текущую точность сети, также посмотреть как распределены ложные и правильные результаты дабы далее можно было проще понять как улучшить точность.
4. NeuralNetwork - проект, в котором находится блокнот с обучением сети и с самой сетью.
