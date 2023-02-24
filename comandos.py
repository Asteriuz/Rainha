from datetime import datetime
from tabulate import tabulate
import json
import sympy
from random import randint, choice
import pyperclip
import pyautogui
import winsound as wav
import os
import pathlib
import re
import subprocess
from time import sleep
from misc import (
    Thread,
    findapp,
    playonyt,
    rule3,
    temperatura,
    translator,
    playsound,
    talk,
    web,
    copy_clipboard,
    engine,
    voices,
    ttsmp3,
    img_search,
    representsInt,
    rimas,
    wiki_search,
    countdown,
    timers,
)


actpath = pathlib.Path(__file__).parent.resolve()

with open("intents.json", "r", encoding="utf8") as file:
    intents = json.load(file)["intents"]


def has(list, command):
    return any(word in command for word in list)


# ---------------------------------------------------------------------------- #
#                          Seção de comandos da Rainha                         #
# ---------------------------------------------------------------------------- #


def gettimers(command):
    print("\n# ------ Timers ------ #")
    if not timers:
        print("Sem timers no momento")
    else:
        for x, y in timers.items():
            print(f"Timer {x} -> {y}")
    print()


def deltimers(command):
    print("Em manutenção")


def timer(command):
    hour = re.search(r"(\d+) hora[s]?", command) or 0
    min = re.search(r"(\d+) minuto[s]?", command) or 0
    seg = re.search(r"(\d+) segundo[s]?", command) or 0
    nome = re.search(r"(.*)? (?:de|\d+)", command) or ""
    if nome:
        nome = nome.group(1)
    text = ""
    if hour:
        text += f"{hour.group(1)} hora "
        hour = int(hour.group(1))
    if min:
        text += f"{min.group(1)} minutos "
        min = int(min.group(1))
    if seg:
        text += f"{seg.group(1)} segundos"
        seg = int(seg.group(1))
    time = (hour * 3600) + (min * 60) + (seg)

    if not hour and not min and not seg:
        text += f"1 minuto"
        time = 60

    timeoutThread = Thread(target=countdown, args=([time, text, nome]))
    timeoutThread.start()


def imagens(command):
    command = command.replace("imagens de ", "")
    command = command.replace("imagem de ", "")
    paths = img_search(keyword=command, numimages=4)
    for path in paths:
        os.startfile(actpath / path)
        sleep(0.5)


def pesquisa(command):
    playsound("audio/pesquisando.wav", wav.SND_ASYNC)
    web.open(f"https://www.google.com/search?q={command}")


def tocar(command):
    playsound("audio/tocando.wav", wav.SND_ASYNC)
    if "tela cheia" in command:
        playonyt(command, fs=True)
    else:
        playonyt(command)


def traduzir(command):
    engine.setProperty("voice", voices[1].id)
    translated_text = translator.translate(command)
    # print(translated_text.text)  # type: ignore
    wav.PlaySound(None, wav.SND_PURGE)
    talk(translated_text.text)  # type: ignore


def continuar(command):
    pyautogui.press("space")


def calculo(command):
    command = command.replace("x", "*")
    command = command.replace("dividido por ", "/")
    command = command.replace("subtraído por ", "-")
    engine.setProperty("voice", voices[0].id)
    num = sympy.sympify(command)
    # print(int(num))
    talk(str(num))
    


def rimar(command):
    num = re.search(r"\d+", command)
    if num:
        num = int(num.group())
    else:
        num = False
    command = re.sub(r"\/d+", "", command)
    rimas(command, num)


def bye(command):
    playsound("./audio/bye.wav")
    quit()


def fullscreen(command):
    pyautogui.press("f")


def nextvideo(command):
    pyautogui.hotkey("shift", "n")


def prevvideo(command):
    pyautogui.hotkey("alt", "left")


def aumvol(command):
    number = re.search(r"\d+", command)
    if number:
        number = int(number.group())
        number = int(rule3(100, 65535, number))
    else:
        number = 3276
    os.system(f'cmd /c "{actpath / "utilities/nircmd.exe"}" changesysvolume {number}')


def dimvol(command):
    number = re.search(r"\d+", command)
    if number:
        number = int(number.group())
        number = int(rule3(100, 65535, number))
    else:
        number = 3276
    os.system(f'cmd /c "{actpath / "utilities/nircmd.exe"}" changesysvolume -{number}')


def fecharpag(command):
    pyautogui.hotkey("ctrl", "w")


def pausar(command):
    pyautogui.press("space")


def desligar(command):
    playsound("audio/turnoffmonitor.wav", wav.SND_ASYNC)
    subprocess.call(
        [
            actpath / "utilities/ahk/ahk.exe",
            actpath / "utilities/ahk/scripts/screenoff.ahk",
        ]
    )


def nextchapter(command):
    pyautogui.hotkey("alt", "d")
    texto = copy_clipboard()
    newchapter = re.search(r"chapter-(\d+)", texto)
    assert newchapter is not None
    newchapter = int(newchapter.group(1)) + 1
    newurl = re.sub(r"(chapter-)(\d+)", r"\1", texto)
    newurl = newurl + str(newchapter)
    pyperclip.copy(newurl)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")


def prevchapter(command):
    pyautogui.hotkey("alt", "d")
    texto = copy_clipboard()
    newchapter = re.search(r"chapter-(\d+)", texto)
    assert newchapter is not None
    newchapter = int(newchapter.group(1)) - 1
    newurl = re.sub(r"(chapter-)(\d+)", r"\1", texto)
    newurl = newurl + str(newchapter)
    pyperclip.copy(newurl)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")


def wiki(command):
    wiki_search(command)


def supremacy(command):
    web.open("https://www.webnovelpub.com/novel/supremacy-games-29121057")


def parar(command):
    wav.PlaySound(None, wav.SND_PURGE)


def randomnum(command):
    command = command.replace(".", "")
    numbers = re.search(r"(\d+).*?(\d+)", command)
    if numbers is not None:
        a, b = numbers.group(1), numbers.group(2)
        num = randint(int(a), int(b))
        print(num)
        talk(str(num))
    else:
        print("Problema com os números")


def goodnight(command):
    sleep(2)
    quit()


def horario(command):
    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M")
    print("São", currentTime)
    talk("São " + currentTime)


def clima(command):
    temp = temperatura()
    print(temp[1], temp[0])
    talk(temp[1] + " " + temp[0])


def audiochange(command):
    subprocess.Popen(["powershell", actpath / "utilities/ahk/scripts/changeaudio.ps1"])


def abrir(command):
    apps = findapp(command)
    if isinstance(apps, list):
        # playsound("audio/openapp.wav", asyncplay=True)
        os.startfile(apps[0])
    

def fecharapp(command):
    pyautogui.hotkey("alt", "f4")


def listarcomandos(command):
    os.system("cls")
    # print(f"Tenho {len(intents)} comandos disponíves no momento")
    # print("# ----------------- comandos ----------------- #")
    table = []
    for idx in intents:
        if "description" in idx:
            # table.append((idx["tag"],idx['pattern'][0].capitalize(), idx["description"]))
            table.append((idx['pattern'][0].capitalize(), idx["description"]))
        else:
            # table.append((idx["tag"],idx['pattern'][0].capitalize()))
            table.append(( idx['pattern'][0].capitalize()))

    # print(tabulate(table, headers=["Tag","Comando", "Descrição"], tablefmt="simple_grid"))
    print(tabulate(table, headers=["Comando", "Descrição"], tablefmt="simple_grid"))
# ---------------------------------------------------------------------------- #
#                     Executa as tarefas e procura no json                     #
# ---------------------------------------------------------------------------- #


def run_Rainha(command: str):
    first = True
    if "me " in command:
        command = re.sub("^me ", "", command)

    print(command)

    engine.setProperty("voice", voices[0].id)
    palavras = command.split(" ")
    os.system(f'cmd /c "{actpath / "utilities/nircmd.exe"}" mutesysvolume 0')

    for idx, intent in enumerate(intents):  # type : ignore
        if not first:
            break
        for pattern in intent["pattern"]:
            if not first:
                break
            if re.search(rf"\b{pattern}\b", command):
                first = False
                if "replace" in intents[idx]:
                    command = command.replace(pattern + " ", "")
                if "fala" in intents[idx]:
                    filename = choice(intents[idx]["tag"])
                    filename = choice(intents[idx]["fala"])
                    playsound(f"audio/{filename}.wav", True)
                if intents[idx]["tag"] in globals():
                    func = globals()[intents[idx]["tag"]]
                    func(command)
