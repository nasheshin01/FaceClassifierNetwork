using System;
using System.Windows.Forms;
using System.Drawing;
using System.IO;

namespace FacesDetector
{
    /// <summary>
    ///  Класс стандартного исполнителя - нужен, чтобы получить все директории и провести необходимое выделение лиц.
    /// </summary>
    class DefaultFileProcessor : IFileProcessing
    {
        public string FolderInputPath { get; set; }
        public string FolderOutputPath { get; set; }
        public string FolderDebugOutputPath { get; set; }

        /// <summary>
        ///  Возвращает стандартный объект класса, параллельно организуются директории по умолчанию.
        /// </summary>
        public DefaultFileProcessor()
        {
            // Стандартная директория для фотографий на ввод - мои изображения
            FolderInputPath = Environment.GetFolderPath(Environment.SpecialFolder.MyPictures);

            // В начальной директории исполняемого файла создается папка Output и ставится директорией по умолчанию (для вырезаемых лиц из изображений).
            if (!Directory.Exists(Path.Combine(Environment.CurrentDirectory, "Output")))
                Directory.CreateDirectory(Path.Combine(Environment.CurrentDirectory, "Output"));
            FolderOutputPath = Path.Combine(Environment.CurrentDirectory, "Output");

            // В начальной директории исполняемого файла создается папка Debug и ставится директорией по умолчанию (для изображений с выделенными лицами).
            if (!Directory.Exists(Path.Combine(Environment.CurrentDirectory, "Debug")))
                Directory.CreateDirectory(Path.Combine(Environment.CurrentDirectory, "Debug"));
            FolderDebugOutputPath = Path.Combine(Environment.CurrentDirectory, "Debug");
        }

        public bool OpenFolderInput()
        {
            // Открываем окно с выбором директории, если что-то выло выбрано возвращается True,
            // и происходить перезапись директории для изображений на ввод, иначе False.
            FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();
            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                FolderInputPath = folderBrowserDialog.SelectedPath;
                return true;
            }
            return false;
        }

        public bool OpenFolderOutput()
        {
            // Открываем окно с выбором директории, если что-то выло выбрано возвращается True,
            // и происходить перезапись директории для изображений с вырезанными лицами, иначе False.
            FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();
            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                FolderOutputPath = folderBrowserDialog.SelectedPath;
                return true;
            }
            return false;
        }

        public bool OpenFolderDebugOutput()
        {
            // Открываем окно с выбором директории, если что-то выло выбрано возвращается True,
            // и происходить перезапись директории для изображений с выделенными лицами, иначе False.
            FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();
            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                FolderDebugOutputPath = folderBrowserDialog.SelectedPath;
                return true;
            }
            return false;
        }

        public FileInfo[] GetImages()
        {
            return new DirectoryInfo(FolderInputPath).GetFiles("*.jpg");
        }

        /// <summary>
        /// Сохранение изображения с выделенными лицами.
        /// </summary>
        /// <param name="bitmap"></param>
        /// <param name="name"></param>
        public void SaveToDebug(Bitmap bitmap, int index)
        {
            bitmap.Save(Path.Combine(FolderDebugOutputPath, $"debug{index}.jpg"), System.Drawing.Imaging.ImageFormat.Jpeg);
        }

        /// <summary>
        /// Сохранение изображений лицами.
        /// </summary>
        /// <param name="bitmaps"></param>
        /// <param name="names"></param>
        public void SaveToOutput(Bitmap[] bitmaps, ref int indexStart)
        {
            for (int i = 0; i < bitmaps.Length; i++)
            {
                bitmaps[i].Save(Path.Combine(FolderOutputPath, $"output{indexStart}.jpg"), System.Drawing.Imaging.ImageFormat.Jpeg);
                indexStart++;
            }
        }
    }
}
