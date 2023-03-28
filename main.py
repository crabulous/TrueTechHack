from flask import Flask

app = Flask(__name__)

@app.route('/audio_description')
def send_audio_description():
    pass

if __name__ == '__main__':
    app.run('0.0.0.0')