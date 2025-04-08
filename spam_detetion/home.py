from flask import Flask, render_template, jsonify
import speech_recognition as sr

app = Flask(__name__)

def write_transcription_to_file(text: str, output_file: str) -> None:
    with open(output_file, 'w') as f:
        f.write(text)

def read_transcription_from_file(output_file: str) -> str:
    with open(output_file, 'r') as f:
        return f.read()

def is_spam(text: str) -> tuple:
    spam_keywords = ["win", "free", "click here", "subscribe", "buy now", "limited time","otp","bank account","bank","pin"]
    found_keywords = [keyword for keyword in spam_keywords if keyword in text.lower()]
    return len(found_keywords) > 0, found_keywords

def transcribe_audio_from_mic(language: str) -> dict:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak now...")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio_data = recognizer.listen(source)
            print("Processing your speech...")
            text = recognizer.recognize_google(audio_data, language=language)
            write_transcription_to_file(text, "project.txt")  
            print(text)

            saved_text = read_transcription_from_file("project.txt")

            spam_status, spam_words = is_spam(saved_text)
            return {"transcription": saved_text, "is_spam": spam_status, "spam_words": spam_words}
        except sr.UnknownValueError:
            return {"error": "Sorry, I could not understand the audio."}
        except sr.RequestError:
            return {"error": "Sorry, there was an error with the speech recognition service."}

@app.route('/' ,methods=['POST','GET'])
def sign_in():
    return render_template('sign_in.html')

@app.route('/index',methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')



@app.route('/start-detection', methods=['GET'])
def start_detection():
    try:
        language = "en-US"  
        result = transcribe_audio_from_mic(language)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)