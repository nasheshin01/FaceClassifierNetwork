using System;
using System.Windows;
using System.IO;
using System.Drawing;
using System.Threading;
using System.Threading.Tasks;

namespace FacesDetector
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        // Инициализация
        private DefaultFileProcessor fileProcessor = new DefaultFileProcessor();

        public MainWindow()
        {
            InitializeComponent();

            // Опреление директорий по умолчанию.
            folderInputPathBox.Text = fileProcessor.FolderInputPath;
            folderOutputPathBox.Text = fileProcessor.FolderOutputPath;
            folderDebugOutputBox.Text = fileProcessor.FolderDebugOutputPath;
        }

        private void Execute()
        {
            FileInfo[] files = fileProcessor.GetImages();

            // Переменная для счета кол-во выделенных лиц.
            int outputFileIndex = 0;

            // Цикл по каждому файлу.
            for (int i = 0; i < files.Length; i++)
            {
                try
                {
                    // Получение bitmap из файла.
                    Bitmap bitmap = new Bitmap(files[i].FullName);

                    // Инициализация стандартного обработчика изображений.
                    DefaultPictureProcessor defaultPictureProcessor = new DefaultPictureProcessor();

                    // Определение прямоугольников, обводящих все лица, в изображении.
                    Rectangle[] rectangles = defaultPictureProcessor.DetectFaces(bitmap);

                    // Выделение найденных лиц(путем их обводки) и сохранение нового bitmap в директорию для изображений с выделенными лицами.
                    Bitmap bitmapWithFaceBorders = defaultPictureProcessor.DrawRectangles(bitmap, rectangles);
                    fileProcessor.SaveToDebug(bitmapWithFaceBorders, i);

                    // Вырезание найденных лиц и сохранение их.
                    Bitmap[] faceBitmaps = defaultPictureProcessor.GetFaces(bitmap, rectangles);
                    fileProcessor.SaveToOutput(faceBitmaps, ref outputFileIndex);
                }
                catch
                {
                    MessageBoxResult messageBoxResult = MessageBox.Show($"Произошла ошибка при обработке изображения {files[i].FullName}. Продолжить выполнение?",
                                                                        "Ошибка", MessageBoxButton.YesNo);
                    if (messageBoxResult == MessageBoxResult.No)
                        return;
                }
            }
        }

        /// <summary>
        /// Метод для нажатия по кнопке запуска
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void executeButton_Click(object sender, RoutedEventArgs e)
        {
            // По нажатию на кнопку запуска, начинается выполнение действий по выделению лиц и их сохранению,
            // если происходит какая-то ошибка выводится сообщение об ошибке.
            try
            {
                Execute();
                MessageBox.Show("Выделение лиц произведено!");
            }
            catch
            {
                MessageBox.Show("Произошла ошибка при обработке. Пожалуйста проверьте корректность введенных директорий.");
            }
        }

        /// <summary>
        /// Метод для нажатия по кнопке выбора директории для изображений на ввод.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void chooseFolderInputButton_Click(object sender, RoutedEventArgs e)
        {
            // Если была выбрана какая-либо директория, ее путь отображается в необходимом textbox'е
            if (fileProcessor.OpenFolderInput())
                folderInputPathBox.Text = fileProcessor.FolderInputPath;
        }

        /// <summary>
        /// Метод для нажатия по кнопке выбора директории для изображений вырезанных лиц на вывод.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void chooseFolderOutputButton_Click(object sender, RoutedEventArgs e)
        {
            // Если была выбрана какая-либо директория, ее путь отображается в необходимом textbox'е
            if (fileProcessor.OpenFolderOutput())
                folderOutputPathBox.Text = fileProcessor.FolderOutputPath;
        }

        /// <summary>
        /// Метод для нажатия по кнопке выбора директории для изображений выделенных лиц на вывод.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void chooseFolderDebugOutputButton_Click(object sender, RoutedEventArgs e)
        {
            // Если была выбрана какая-либо директория, ее путь отображается в необходимом textbox'е
            if (fileProcessor.OpenFolderDebugOutput())
                folderDebugOutputBox.Text = fileProcessor.FolderDebugOutputPath;
        }
    }
}
