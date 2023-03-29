## Аудиосопровождение происходящего на экране для людей с нарушением зрения

#### Репозиторий серверной части сервиса для тифлокомментирования 

## Другие части:
* <a href=https://github.com/LaMileyn/hackaton>Веб-клиент</a>
* <a href=https://github.com/DanonAno/MtsHackNew/tree/main/MtsHackNew>iOS-приложение</a>
* <a href=https://www.figma.com/file/iaXHdRTE5LTgKpJXRo5tQa/>Figma</a>


## О проекте

Сервис решает ряд задач, необходимых для обработки фильмов для людей, имеющих проблемы со зрением:
* Распознаёт речь в сценах и возвращает таймкоды, для того, чтобы между речью можно было всавить аудиодискрипцию
* Разделяет сцены на кадры для создания описания происходящего в кадре
* Сбор аудиодискрипции из описания кадров



### Стек

* Python
* Flask
* Transformers
* ChatGPT
* SpeechRecognition
* Nginx
* MoviePy
* nlpconnect/vit-gpt2-image-captioning


## Использование

Сервис будет доступен на 91.185.84.113:5000/audio_description,
где в тело запроса необходимо передать имя фильма
н-р



{
    "video_name": "breaking_gum.mp4"
}



вернёт аудиодескрипцию в формате:



{
    "scene": [
            {
            "start": int,
            "end": int,
            "comment": str
        }, ...
    ]
}
