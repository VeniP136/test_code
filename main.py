# import cv2
# import numpy as np
# import PIL

# def main(video_file):
#     cap = cv2.VideoCapture(video_file)
#     success, image = cap.read()

#     fps = cap.get(cv2.CAP_PROP_FPS)
#     est_video_length_minutes = 10.28         # Округлите, если не уверены.
#     est_tot_frames = est_video_length_minutes * fps  # Устанавливает верхнюю границу количества кадров в видеоклипе

#     n = 15                             # Desired interval of frames to include
#     desired_frames = n * np.arange(est_tot_frames) 

#     for i in desired_frames:
#         cap.set(1,i-1)                      
#         success,image = cap.read(1)         # image is an array of array of [R,G,B] values
#         frameId = cap.get(1)                # The 0th frame is often a throw-away
#         frameId = frameId.crop((115,210,350,445))
#         frameId.resize((116, 116), PIL.Image.ANTIALIAS)
#         cv2.imwrite("videoplayback-cv/frame%d.jpg" % frameId, image)
        
#     cap.release()




from datetime import timedelta
import cv2
import numpy as np
import os


def main(video_file):
    filename, _ = os.path.splitext(video_file)
    filename += "-cv"
    # создаем папку по названию видео файла
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # читать видео файл    
    cap = cv2.VideoCapture(video_file)
    # получить FPS видео
    fps = cap.get(cv2.CAP_PROP_FPS)
    # получаем продолжительность клипа, разделив количество кадров на количество кадров в секунду
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # использование np.arange () для получения таймкодов нужных кадров
    saving_frames_durations = []
    for i in np.arange(0, clip_duration, 15 / fps): #делим нужное количество кадров на fps чтобы получить интервалы между нужными кадрами
        saving_frames_durations.append(i)
    # запускаем цикл
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # выйти из цикла, если нет фреймов для чтения
            break
        # получаем продолжительность, разделив количество кадров на FPS
        frame_duration = count / fps
        try:
            # получить самую раннюю продолжительность для сохранения
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # список пуст, все кадры длительности сохранены
            break
        if frame_duration >= closest_duration:
            # если ближайшая длительность меньше или равна длительности кадра,
            # затем сохраняем фрейм
            format_timedelta = str(timedelta(seconds=frame_duration))
            frame_duration_formatted = format_timedelta.replace(":", "-")


            xmax, ymax = 350, 445
            xmin, ymin = 115, 210

            #Вырезаю нужный участок
            frame = frame[ymin:ymax, xmin:xmax]
            #Изменяю рамер
            frame = cv2.resize(frame, (116, 116))

            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}0.jpg"), frame) 
            # удалить точку продолжительности из списка, так как эта точка длительности уже сохранена
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # увеличить количество кадров
        count += 1



if __name__ == "__main__":
    main("videoplayback.mp4")