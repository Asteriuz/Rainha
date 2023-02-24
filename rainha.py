from dotenv import load_dotenv
from tkinter import E
import speech_recognition as sr
import winsound as wav
import pyttsx3
import json
import os
import pathlib
import pvporcupine
import winsound
import subprocess
from pvrecorder import PvRecorder
from comandos import playsound, run_Rainha
import glob
import logging
import re

from misc import soletrar


os.system("title " + "Rainha")
load_dotenv(dotenv_path=r"./source.env")

ACCESS_KEY = os.getenv("ACcESS_KEY")
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# ---------------------------------------------------------------------------- #
#                             Váriaveis importantes                            #
# ---------------------------------------------------------------------------- #

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

files = glob.glob("temp/*")
for f in files:
    os.remove(f)


actpath = pathlib.Path(__file__).parent.resolve()

rec = sr.Recognizer()


gsettings = {}

affirmative = [
    "sim",
    "autorizado",
    "autorizada",
    "permitida",
    "permitido",
    "afirmativo",
    "positivo",
    "certo",
    "isso",
    "está bem",
    "está certo",
    "com certeza",
    "de acordo",
    "efetivamente",
]
negative = [
    "não",
    "nunca",
    "jamais",
    "de jeito nenhum",
    "de jeito algum",
    "de maneira nenhuma",
    "de maneira alguma",
    "de modo algum",
    "de modo nenhum",
]


# ---------------------------------------------------------------------------- #
#                                Seção de Login                                #
# ---------------------------------------------------------------------------- #


def yesno():
    command = ""
    while command == "":
        try:
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic)
                audio = rec.listen(mic)
                # if NEURAL:
                    # resp = str(rec.recognize_azure(audio, key=ACCESS_KEY));
                # else:
                resp = str(rec.recognize_google(audio))
                resp = resp.lower()
                if any(word in resp for word in negative):
                    command = False
                if any(word in resp for word in affirmative):
                    command = True
        except:
            playsound("audio/yesno.wav")
            pass
    print(command)
    return command


def gsetupdate():
    with open("data/settings.json", "w+") as file:
        json.dump(gsettings, file, indent=4)


def authentication():
    pass


def login():
    global gsettings
    print("Logando no UVR...")
    default_settings = {"remember_login": False, "talk_benefits": True}

    if not os.path.exists("data/settings.json"):
        with open("data/settings.json", "w+") as file:
            json.dump(default_settings, file, indent=4)
            gsettings = default_settings
    else:
        with open("data/settings.json", "r+") as file:
            gsettings = json.load(file)

    if gsettings["talk_benefits"]:
        playsound("audio/welcome.wav")
        resp = yesno()
        if resp == False:
            gsettings["talk_benefits"] = False
            gsetupdate()


login()
""
main_mic = sr.Microphone()


# ---------------------------------------------------------------------------- #
#                                Glória a Rainha                               #
# ---------------------------------------------------------------------------- #


def main():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=["utilities/wakeWord/Rainha_pt_windows_v2_1_0.ppn"],
        model_path="utilities/wakeWord/porcupine_params_pt.pv",
    )
    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)  # type: ignore

    if DEBUG:
        # try:
        print("Logado!")
        first = True
        while True:
            if first:
                first = False
            command = input("Digite o comando: ")
            command = command.lower()
            command = soletrar(command)
            wav.PlaySound(None, wav.SND_PURGE)
            run_Rainha(command)
            first = True
        # except Exception as error:
        #     logger.exception(error)
        #     print(error)
    else:
        try:
            recorder.start()  # type: ignore
            playsound("audio/logado.wav", asyncplay=True)
            print("Logado!")
            first = True
            while True:
                if first:
                    first = False
                    print("Listening...")
                keyword_index = porcupine.process(recorder.read())  # type: ignore
                if keyword_index >= 0:
                    recorder.stop()  # type: ignore
                    print(f"Detected")
                    winsound.Beep(600, 300)
                    os.system(
                        f'cmd /c "{actpath / "utilities/nircmd.exe"}" mutesysvolume 1'
                    )
                    playsound("audio/welcome.wav", wav.SND_ASYNC)
                    try:
                        with main_mic as mic:

                            cwd = os.getcwd()
                            os.chdir(actpath / "utilities/DenVis")
                            subprocess.Popen("DenVis.exe")
                            os.chdir(cwd)
                            audio = rec.listen(mic, timeout=5, phrase_time_limit=5)
                            command = str(rec.recognize_google(audio, language="pt-BR"))
                            command = command.lower()
                            command = soletrar(command)
                            subprocess.check_call(
                                "taskkill /f /im DenVis.exe",
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                            )
                            wav.PlaySound(None, wav.SND_PURGE)
                            run_Rainha(command)
                            first = True
                    except Exception as error:
                        wav.PlaySound(None, wav.SND_PURGE)
                        os.system(
                            f'cmd /c "{actpath / "utilities/nircmd.exe"}" mutesysvolume 0'
                        )
                        # subprocess.call(
                        #         [
                        #             actpath / "utilities/ahk/ahk.exe",
                        #             actpath / "utilities/ahk/scripts/switchlistendevice.ahk",
                        #         ]
                        #     )
                        # logger.exception(error)
                        # print(Error)
                        print("Não houve mensagem")
                        first = True
                        pass
                recorder.start()  # type: ignore
        except KeyboardInterrupt:
            recorder.stop()  # type: ignore
        finally:
            porcupine.delete()
            recorder.delete()  # type: ignore


if __name__ == "__main__":
    main()
