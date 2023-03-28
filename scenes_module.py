import cv2
import datetime

video = cv2.VideoCapture('bjibibnnblo.mp4')

frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

threshold = 5000000

fps = int(video.get(cv2.CAP_PROP_FPS))

scene_changes = []

success, frame1 = video.read()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

prev_time = 0

for i in range(frame_count - 1):
    success, frame2 = video.read()
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    frame_diff = cv2.absdiff(gray1, gray2)
    diff_sum = frame_diff.sum()

    if diff_sum > threshold:
        curr_time = datetime.timedelta(milliseconds=int(i / fps * 1000))
        scene_changes.append(curr_time)

    gray1 = gray2

video.release()
cv2.destroyAllWindows()

for i in range(len(scene_changes)):
    tc = str(scene_changes[i])
    tc_parts = tc.split(':')
    tc_parts[0] = str(int(tc_parts[0]))
    if '.' in tc_parts[-1]:
        whole, fraction = tc_parts[-1].split('.')
        tc_parts[-1] = str(int(whole) * fps + int(fraction) * fps / (10 ** len(fraction)))
    else:
        tc_parts[-1] = str(int(float('0.' + tc_parts[-1]) * fps))

    tc_parts[-1] = tc_parts[-1].zfill(2)

    scene_changes[i] = ':'.join(tc_parts)

print(scene_changes)
