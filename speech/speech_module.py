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

    audio = AudioSegment.from_wav(audio_file)

    r = sr.Recognizer()
    silence_threshold = 10
    silence_duration = 1
    silence_intervals = []
    step = 500

    for i in range(0, len(audio), step):

        chunk = audio[i:i + step]

        chunk.export("temp.wav", format="wav")

        with sr.AudioFile("temp.wav") as source:
            audio_data = r.record(source)
            try:

                db = sr.audioop.rms(audio_data.frame_data, audio_data.sample_width)
                if db < silence_threshold:

                    if not silence_intervals or (i / 1000 - silence_intervals[-1][1]) >= silence_duration:
                        silence_intervals.append([i / 1000, (i + step) / 1000])
            except sr.UnknownValueError as e:
                print("Error:", str(e))
    os.remove("temp.wav")
    return silence_intervals
    
