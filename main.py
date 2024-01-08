""" Speech Recognition Example with GPT integration
https://www.mindluster.com/lesson/568
https://blog.enterprisedna.co/how-to-use-chatgpt-for-python/ 
environment variable OPENAI_TOKEN"""

from time import ctime, sleep
import os
import random
import playsound
import openai
from gtts import gTTS
import speech_recognition as sr

r = sr.Recognizer()

def rm_file(file_name):
    """ Deletes specified file """
    try:
        os.remove(file_name)
    except FileNotFoundError:
        return

def record_audio():
    """ Returns text string with recognized voice """
    with sr.Microphone() as source:
        loc_audio = r.listen(source)
        loc_voice_data = 'nothing'
        try:
            loc_voice_data = r.recognize_google(loc_audio)
        except sr.UnknownValueError:
            print('Sorry, I did not get that')
        except sr.RequestError:
            print('Sorry, my speech service is down')
        return loc_voice_data

def respond(res_voice_data):
    """ Analysis of the input data """
    if 'your name' in res_voice_data:
        alexis_speak('My name is Alexis')
    elif 'time' in res_voice_data:
        alexis_speak(ctime())
    elif 'question' in res_voice_data:
        alexis_speak("What question?")
        res_voice_data = record_audio()
        print(res_voice_data)
        res_voice_data = chat_with_chatgpt(res_voice_data, model="gpt-3.5-turbo")
        if res_voice_data:
            alexis_speak(res_voice_data)
    elif 'exit' in res_voice_data:
        alexis_speak('Goodbye!')
        exit()
    else:
        alexis_speak('Nothing to do when the entry is: ' + res_voice_data)

def chat_with_chatgpt(prompt, model="gpt-3.5-turbo"):
    """ Get response from Chat GPT """

    model = "text-davinci-002"

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

def alexis_speak(audio_string):
    """ Answers with synthetized voice """
    my_error = False
    print(audio_string)
    random_number = random.randint(1, 1234567)
    audio_file = 'audio-' + str(random_number) + '.mp3'
    
    try:
        tts = gTTS(text=audio_string, lang='en')
        tts.save(audio_file)
    except playsound.PlaysoundException:
        print("Playsound error")
        my_error = True

    if not my_error:
        try:
            playsound.playsound(audio_file)
            if os.path.exists(audio_file):
                rm_file(audio_file)
        except FileNotFoundError:
            print("Audio file not found (" + audio_file + ")")

if __name__ == "__main__":
    openai.api_key = os.getenv('OPENAI_TOKEN')
    print(os.getenv('OPENAI_TOKEN'))
    alexis_speak('Hallo')
    while True:
        alexis_speak('I\'m listening...')
        voice_data = record_audio()
        if voice_data:
            respond(voice_data)
        sleep(1)
        os.system('cls')

