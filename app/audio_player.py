import threading
import requests
import urllib.parse
from playsound import playsound
import tempfile
import os
import logging
from tkinter import messagebox

def play_ulster_audio(app):
    play_audio(app, 'U')

def play_munster_audio(app):
    play_audio(app, 'M')

def play_connacht_audio(app):
    play_audio(app, 'C')

def play_audio(app, dialect_code):
    threading.Thread(target=_play_audio_thread, args=(app, dialect_code), daemon=True).start()

def _play_audio_thread(app, dialect_code):
    try:
        verb = app.correct_verb
        encoded_verb = urllib.parse.quote(verb)
        if dialect_code == 'U':
            url = f'https://www.teanglann.ie/CanU/{encoded_verb}.mp3'
        elif dialect_code == 'M':
            url = f'https://www.teanglann.ie/CanM/{encoded_verb}.mp3'
        elif dialect_code == 'C':
            url = f'https://www.teanglann.ie/CanC/{encoded_verb}.mp3'
        else:
            raise ValueError(f"Unknown dialect code: {dialect_code}")
        # Download the mp3 file
        response = requests.get(url)
        if response.status_code == 200:
            # Save to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(response.content)
                temp_file.flush()  # Ensure data is written
                temp_file_name = temp_file.name
            # Play the audio file
            playsound(temp_file_name)
            # Remove the temp file after playing
            os.remove(temp_file_name)
        else:
            app.root.after(0, messagebox.showerror, "Error", f"Audio file not found for '{verb}' in dialect '{dialect_code}'")
    except Exception as e:
        logging.error(f"Error playing audio: {e}")
        # Since we're in a thread, need to use tkinter's thread-safe method to show messagebox
        app.root.after(0, messagebox.showerror, "Error", f"An error occurred while playing audio: {e}")