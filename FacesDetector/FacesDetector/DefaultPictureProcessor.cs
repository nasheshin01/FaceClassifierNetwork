using System;
using System.Drawing;
using Emgu.CV;
using Emgu.CV.Structure;

namespace FacesDetector
{
    /// <summary>
    ///  Класс стандартного обработчика изображений.
    /// </summary>
    class DefaultPictureProcessor : IPictureProcessing
    {
        public Rectangle[] DetectFaces(Bitmap bitmap)
        {
            // Получение обученного классификатора
            CascadeClassifier cascadeClassifier = new CascadeClassifier("haarcascade_frontalface_default.xml");

            // Переводим bitmap в формат нужный для классификатора, находим лица и возвращаем их обводки.
            Image<Bgr, byte> bitmapConverted = new Image<Bgr, byte>(bitmap);
            return cascadeClassifier.DetectMultiScale(bitmapConverted, 1.05);
        }

        public Bitmap DrawRectangles(Bitmap bitmap, Rectangle[] rectangles)
        {
            // Клонируем bitmap, чтобы при рисовании изменять копию.
            Bitmap bitmapClone = (Bitmap)bitmap.Clone();

            // Рисуем каждый прямоугольник и, по итогу, возвращаем измененный bitmap.
            foreach (Rectangle rectangle in rectangles)
            {
                using (Graphics graphics = Graphics.FromImage(bitmapClone))
                {
                    using (Pen pen = new Pen(Color.Red, 3))
                    {
                        graphics.DrawRectangle(pen, rectangle);
                    }
                }
            }
            return bitmapClone;
        }

        public Bitmap[] GetFaces(Bitmap bitmap, Rectangle[] rectangles)
        {
            // Инициализация массива изображений под лица.
            Bitmap[] bitmaps = new Bitmap[rectangles.Length];

            // Заполняем массив вырезанными учатсками из главного bitmap'а и, по итогу, его возвращаем.
            for (int i = 0; i < rectangles.Length; i++)
            {
                bitmaps[i] = bitmap.Clone(rectangles[i], bitmap.PixelFormat);
            }
            return bitmaps;
        }
    }
}
