using System;
using System.Drawing;

namespace FacesDetector
{
    /// <summary>
    /// Интерфейс для определения функционала обработчика изображения.
    /// </summary>
    interface IPictureProcessing
    {
        /// <summary>
        /// Функция для нахождения лиц - на вход подается изображение, возвращаются прямоугольники, обводящие лица.
        /// </summary>
        Rectangle[] DetectFaces(Bitmap bitmap);

        /// <summary>
        /// Функция для рисования прямоугольников на изображении - на вход подается изображение и массив прямоугольников, возвращается измененное изображение.
        /// </summary>
        Bitmap DrawRectangles(Bitmap bitmap, Rectangle[] rectangles);

        /// <summary>
        /// Функция для вырезания участков из изображения - на входе изображение и массив прямоугольников, возвращается массив вырезанных изображений.
        /// </summary>
        Bitmap[] GetFaces(Bitmap bitmap, Rectangle[] rectangles);
    }
}
