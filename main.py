# main.py
import tkinter as tk
from app.gui import VerbConjugationApp
# from app.verb_conjugation_app import VerbConjugationApp

def main():
    root = tk.Tk()
    app = VerbConjugationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
