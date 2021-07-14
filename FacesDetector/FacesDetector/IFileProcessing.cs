using System;
using System.Drawing;
using System.IO;

namespace FacesDetector
{
    /// <summary>
    /// Интерфейс для определения функционала класса исполнителя.
    /// </summary>
    interface IFileProcessing
    {
        /// <summary>
        /// Строка для хранения директории с изображениями на ввод.
        /// </summary>
        string FolderInputPath { get; set; }

        /// <summary>
        /// Строка для хранения директории для изображений лиц на вывод.
        /// </summary
        string FolderOutputPath { get; set; }

        /// <summary>
        /// Строка для хранения директории для изображений с выделенными лицами на вывод.
        /// </summary>
        string FolderDebugOutputPath { get; set; }

        /// <summary>
        /// Функция выбора директории с изображениями на ввод, возвращается True, если функция была выполнена успешно.
        /// </summary>
        bool OpenFolderInput();

        /// <summary>
        /// Функция выбора директории для изображений лиц на вывод, возвращается True, если функция была выполнена успешно.
        /// </summary>
        bool OpenFolderOutput();

        /// <summary>
        /// Функция выбора директории для изображений с выделенными лицами на вывод, возвращается True, если функция была выполнена успешно.
        /// </summary>
        bool OpenFolderDebugOutput();

        /// <summary>
        /// Функция для получения входных изображений.
        /// </summary>
        FileInfo[] GetImages();
    }
}
