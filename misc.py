from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from email.mime import audio
import os
from threading import Thread
import pathlib
from sympy import true
import wikipedia
import keyword
import subprocess
import re
import json
import requests
import webbrowser as web
import winsound as wav
from functools import reduce
from time import sleep
import pyautogui
import requests
import pyttsx3
import pyperclip
from bs4 import BeautifulSoup as bs4
from googletrans import Translator


load_dotenv(dotenv_path=r"./source.env")
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
NEURAL = (os.getenv('NEURAL', 'False') == 'True')

wikipedia.set_lang("pt")
translator = Translator()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def copy_clipboard():
    pyautogui.hotkey("ctrl", "c")
    sleep(0.01)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()

def findapp(search: str):
    if search == "calculadora":
        subprocess.call(["calc.exe"])
        # playsound("audio/openapp.wav", asyncplay=True)
    if search == "whatsapp":
        web.open("https://web.whatsapp.com/")
        # playsound("audio/openpag.wav", asyncplay=True)
    if search == "youtube":
        web.open("https://www.youtube.com/")
        # playsound("audio/openpag.wav", asyncplay=True)
    if search == "downloads" or search == "download":
        os.startfile(r"C:\Users\augus\Downloads")
        # playsound("audio/openfolder.wav", asyncplay=True)
    else:
        lista = []
        search = search.lower()
        programs = pathlib.Path(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs")
        for x in programs.rglob("*.lnk"):
            if search in str(x).lower():
                lista.append(str(x))
        programs = pathlib.Path(r"C:\Users\augus\AppData\Roaming\Microsoft\Windows\Start Menu\Programs")
        for x in programs.rglob("*.lnk"):
            if search in str(x).lower():
                lista.append(str(x))
        if lista:
            return lista

def temperatura():

    # link do open_weather: https://openweathermap.org/

    API_KEY = "3d6dbc169a239f24eada6faa74fc9dc4"
    lat, lon = (-23.530191074503403, -46.57741224422659)
    link = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&lang=pt_br"

    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    descricao = requisicao_dic["weather"][0]["description"] 
    temperatura = requisicao_dic["main"]["temp"] - 273.15
    return (descricao, f"{round(temperatura)}°")


timers = {}
timercount = 0


def countdown(t: int, text: str, nome=""):
    nome = nome.capitalize()
    global timers
    global timercount
    print(f"Timer ({nome}) Adicionado | {text}") if nome else print(
        f"Timer Adicionado | {text}"
    )
    timercount += 1
    timernum = timercount
    handle = nome or timernum
    while t:
        min, sec = divmod(t, 60)
        hour, min = divmod(min, 60)
        if nome:
            timers[nome] = f"{hour:02d}:{min:02d}:{sec:02d}"
        else:
            timers[timernum] = f"{hour:02d}:{min:02d}:{sec:02d}"
        sleep(1)
        t -= 1

    timers.pop(handle)
    if DEBUG:
        print(f"\nTimer ({handle}) chegou ao fim\n\nDigite o comando: ", end="")
    else:
        print(f"\nTimer ({handle}) chegou ao fim\n\nListening...")
    playsound("audio/alarm.wav", asyncplay=True)


def soletrar(text):
    pattern = r"[^\w](\w \w \w (?:\w |\w$)*)"
    match = re.search(pattern, text)
    if match is not None:
        matchsemspace = match.group(1).replace(" ", "").strip()
        return text.replace(match.group(1), matchsemspace + " ")
    else:
        return text
    


def img_search(keyword, numimages):
    list = []
    url = f"https://www.google.com/search?q={keyword}"
    page = requests.get(url)
    soup = bs4(page.text, "html.parser")
    images = soup.find_all(href=re.compile(".jpg"))
    i = 0
    for idx, image in enumerate(images):
        if i == numimages:
            return list
        img = image.get("href")
        img = re.search("imgurl=(.*?)&", img)
        if img:
            img = img.group(1)
            print(img)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            }
            img_data = requests.get(img, headers=headers).content
            with open(f"temp/{keyword}{idx}.jpg", "wb") as handler:
                handler.write(img_data)
                list.append(f"temp/{keyword}{idx}.jpg")
        i += 1
    return list


def rimas(word, max: int | bool = False):
    resp = requests.get(f"https://www.dicionarioinformal.com.br/rimas/{word}/")
    data = bs4(resp.text, "html.parser")
    parent = data.select("table>tr>td>ul>li")
    if max == False:
        max = len(parent)
    for li in parent[:max]:
        print(li.text, end=" | ")



def talk(texto, neural=True):

    if neural == True:
        # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True) #type: ignore

        # The language of the voice that speaks.
        speech_config.speech_synthesis_voice_name='pt-BR-YaraNeural' #type: ignore

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Get text from the console and synthesize to the default speaker.
        text = texto

        speech_synthesizer.speak_text_async(text)

    else:
        engine.say(texto)
        engine.runAndWait()
    

def playsound(
    path,
    *flags,
    asyncplay=False,
):
    if asyncplay == False:
        flags = [wav.SND_FILENAME, wav.SND_NODEFAULT, *flags]
    if asyncplay == True:
        flags = [wav.SND_FILENAME, wav.SND_NODEFAULT, wav.SND_ASYNC, *flags]
    flags = reduce(lambda x, y: x | y, flags)
    wav.PlaySound(path, flags)


def playonyt(
    topic: str, use_api: bool = False, open_video: bool = True, fs: bool = False
) -> str:
    """Play a YouTube Video"""
    if fs:
        topic = topic.replace("tela cheia", "")
    url = f"https://www.youtube.com/results?q={topic}"
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == "WEB_PAGE_TYPE_WATCH":
            break
    if lst[count - 5] == "/results":
        raise Exception("No Video Found for this Topic!")
    if open_video:
        web.open(f"https://www.youtube.com{lst[count - 5]}")
        if fs:
            sleep(2)
            pyautogui.press("f")

    return f"https://www.youtube.com{lst[count - 5]}"


def rule3(num1, num2, num3):
    x = (num2 * num3) / num1
    return x


def ttsmp3(text):
    form = {"msg": text, "lang": "Vitoria", "source": "ttsmp3"}
    resp = requests.post("https://ttsmp3.com/makemp3_new.php", form).text
    resp = json.loads(resp)["URL"]
    doc = requests.get(resp)
    filename = re.search(r"https:\/\/ttsmp3\.com\/created_mp3\/(.*\.mp3)", resp)
    assert filename is not None
    filename = filename.group(1)
    with open(f"temp/{filename}", "wb") as f:
        f.write(doc.content)
    filenamewav = filename.replace(".mp3", ".wav")
    subprocess.call(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "quiet",
            "-i",
            f"temp/{filename}",
            f"temp/{filenamewav}",
        ]
    )
    return f"temp/{filenamewav}"


def wiki_search(command):
    try:
        resumo = wikipedia.summary(command, sentences=2)
        resumonobrack = re.sub(r"\([^()]*\)", "", resumo)
        resumonobrack = re.sub(r"\[.*?\]", "", resumonobrack)
        resumonobrack = re.sub(r"==.*?==", "", resumonobrack)
        resumonobrack = resumonobrack.replace("\n\n\n\n", " ")
        print(resumonobrack)

        if os.getenv('NEURAL', 'False') == 'True':
            talk(resumonobrack)
        else:
            engine.setProperty("voice", voices[0].id)
            engine.save_to_file(resumonobrack, "temp/speech.mp3")
            engine.runAndWait()
            playsound("temp/speech.mp3")

        # audio = ttsmp3(resumonobrack)
        # playsound(audio)

    except Exception as e:
        print(e)


def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
