import json
from flask import Flask, request, jsonify, Response
import os
from speech import speech_module
from cut import cut_module
from discription import discription_module

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/audio_description', methods=['POST'])
def send_audio_description():
    video_name = request.json['video_name']
    os.chdir('/home/cool/videos/')
    filename, _ = os.path.splitext(video_name)
    if os.path.isfile(filename + '.json'):
        with open(filename + '.json', encoding='utf-8') as f:
            data = json.load(f)
            return data
    segments = speech_module.main(video_name)
    frames = cut_module.main(video_name, segments)
    print(segments)
    disc = discription_module.predict_step(frames)
    print(disc)
    with open(f"{filename}.json", "w", encoding="utf-8") as file:
        json.dump(disc, file, ensure_ascii=False)
    return disc


if __name__ == '__main__':
    app.run('0.0.0.0')
