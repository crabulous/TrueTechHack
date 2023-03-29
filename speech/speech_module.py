import speech_recognition as sr
from pydub import AudioSegment
import os
from moviepy.editor import VideoFileClip


def main(file):
    print(os.listdir())
    filename, _ = os.path.splitext(file)
    convert_video_to_audio_moviepy(file)
    segmentation = segmentation_audio(filename + '.wav')
    os.remove(filename + '.wav')
    return segmentation


def convert_video_to_audio_moviepy(file, output_ext="wav"):
    filename, ext = os.path.splitext(file)
    clip = VideoFileClip(file)
    clip.audio.write_audiofile(f"{filename}.{output_ext}")


def segmentation_audio(file):
    audio_file = file
    filename, _ = os.path.splitext(file)
    audio = AudioSegment.from_wav(audio_file)

    r = sr.Recognizer()
    silence_threshold = 500
    step = 500
    tmp = []
    for i in range(0, len(audio), step):

        chunk = audio[i:i + step]

        chunk.export(f"{filename}.wav", format="wav")

        with sr.AudioFile(f"{filename}.wav") as source:
            audio_data = r.record(source)
            try:

                db = sr.audioop.rms(audio_data.frame_data, audio_data.sample_width)
                if db < silence_threshold:

                    tmp.append([i / 1000, (i + step) / 1000])
            except sr.UnknownValueError as e:
                print("Error:", str(e))

    silence_intervals = [tmp[0]]
    for i in range(1, len(tmp)):
        cur = silence_intervals[-1]
        if tmp[i][0] == cur[1]:
            cur[1] = tmp[i][1]
        else:
            silence_intervals.append(tmp[i])
    return silence_intervals
