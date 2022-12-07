from gtts import gTTS
from io import BytesIO
import pygame

def speak(text):
    mp3_file_object = BytesIO()
    audio = gTTS(text=text, lang="en", slow=False)
    audio.write_to_fp(mp3_file_object)

    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file_object, 'mp3')
    pygame.mixer.music.play()