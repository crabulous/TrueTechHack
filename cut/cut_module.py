import cv2
import numpy as np


SAVING_FRAMES_PER_SECOND = 1

def get_saving_frames_durations(cap, saving_fps):
    """Функция, которая возвращает список длительностей, в которые следует сохранять кадры."""
    s = []
    # получаем продолжительность клипа, разделив количество кадров на количество кадров в секунду
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # используйте np.arange () для выполнения шагов с плавающей запятой
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def main(video_file, segments):
    frames = {"segments":
        [
            {"start": seg[0],
             "end": seg[1],
             "frames": []} for seg in segments
        ]
    }

    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)

    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break

        frame_duration = count / fps
        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            break
        if frame_duration >= closest_duration:
            for seg in range(len(segments)):
                if int(segments[seg][0]) <= frame_duration <= int(segments[seg][1]):
                    frames["segments"][seg]["frames"].append(frame)
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        count += 1
    return frames
