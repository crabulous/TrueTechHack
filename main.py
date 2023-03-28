import json
from flask import Flask, requests
import os
from speech import speech_module
from cut import cut_module
from discription import discription_module

app = Flask(__name__)


@app.route('/audio_description', methods=['POST'])
def send_audio_description():
    video_name = request.json['video_name']
    os.chdir('/home/cool/videos/')
    filename, _ = os.path.splitext(video_name)
    if os.path.isfile(filename + '.json'):
        return json.load(open(filename + '.json'))
    segments = speech_module.main(video_name)
    frames = cut_module.main(video_name, segments)
    return discription_module.predict_step(frames)


if __name__ == '__main__':
    app.run('0.0.0.0')
