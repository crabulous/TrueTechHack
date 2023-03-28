import speech_recognition as sr
from pydub import AudioSegment

# указываем путь к аудиофайлу
audio_file = 'tetsts.wav'

# используем PyDub, чтобы прочитать аудиофайл
audio = AudioSegment.from_wav(audio_file)

sample_rate = audio.frame_rate
print(sample_rate)

# создаем объект Recognizer из библиотеки SpeechRecognition
r = sr.Recognizer()

# определяем порог громкости, ниже которого звук считается тишиной
silence_threshold = 10

# определяем длительность интервала тишины, чтобы не выводить слишком короткие промежутки
silence_duration = 1

# создаем список интервалов тишины
silence_intervals = []

# разбиваем аудиофайл на фрагменты по 10 секунд
step = 500
print(len(audio) / sample_rate)
for i in range(0, len(audio), step):
    # извлекаем фрагмент аудиофайла
    chunk = audio[i:i + step]

    # конвертируем PyDub AudioSegment в WAV формат для распознавания речи
    chunk.export("temp.wav", format="wav")

    # открываем временный файл и распознаем речь с помощью библиотеки SpeechRecognition
    with sr.AudioFile("temp.wav") as source:
        audio_data = r.record(source)
        try:
            # получаем громкость аудиофайла в децибелах
            db = sr.audioop.rms(audio_data.frame_data, audio_data.sample_width)
            if db < silence_threshold:
                # если громкость ниже порога тишины, добавляем интервал тишины в список
                if not silence_intervals or (i / 1000 - silence_intervals[-1][1]) >= silence_duration:
                    silence_intervals.append([i / 1000, (i + step) / 1000])
        except sr.UnknownValueError as e:
            print("Error:", str(e))

# выводим интервалы тишины
for interval in silence_intervals:
    print(f"{interval[0]:.2f} - {interval[1]:.2f}")
