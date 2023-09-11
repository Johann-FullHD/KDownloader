from pytube import YouTube
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
import datetime
import os
import pyautogui

# Funktion zum Herunterladen des Videos
def download_video():
    # YouTube-Video-URL eingeben
    url = url_entry.get()

    # YouTube-Video-Objekt erstellen
    video = YouTube(url)

    # Video-Titel als Dateiname verwenden
    file_name = video.title  # Verwende den Titel des Videos als Dateiname

    # Video-Auflösungen auswählen
    resolutions = [stream.resolution for stream in video.streams.filter(progressive=True)]
    resolution = resolution_var.get()

    if resolution not in resolutions:
        result_label.config(text=translations["resolution_not_available"])
        return

    # Video-Format auswählen
    video_format = format_var.get()

    # Initialisieren von video_stream außerhalb der if-Bedingung
    video_stream = None

    # Dialog zum Speichern des Videos öffnen
    file_path = filedialog.asksaveasfilename(defaultextension=f".{video_format}", filetypes=[(f"{video_format.upper()} files", f"*.{video_format}")], initialfile=f"{file_name}.{video_format}")

    # Video-Format aus dem Dropdown-Menü auswählen
    selected_format = format_var.get()
    if "Audio" in selected_format:
        audio_stream = video.streams.filter(only_audio=True).first()
        if audio_stream:
            audio_stream.download(output_path=file_path)
    else:
        video_format = selected_format.split(" ")[0]  # Get the format part (e.g., "mp4")

        video_stream = video.streams.filter(progressive=True, resolution=resolution, file_extension=video_format).first()
        if video_stream:
            video_stream.download(output_path=file_path)

        file_size = video_stream.filesize_approx
        file_size_mb = file_size / (1024 * 1024)
        download_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result_label.config(text=f"{translations['download_success']} {file_size_mb:.2f} MB ({download_time})")

        # Überprüfen, ob video_stream gesetzt ist, bevor du ihn in open_file_path verwendest
        if video_stream:
        # Öffnen des Dateipfads nach dem Herunterladen
            open_file_path(file_path)

        # Video-Informationen zur Historie hinzufügen
        video_info = f"Title: {video.title}\nURL: {url}\nResolution: {resolution}\nFormat: {video_format}\nFile Size: {file_size_mb:.2f} MB\nDownload Time: {download_time}"
        history_listbox.insert(0, video_info)  # Hinzufügen am Anfang der Liste

       

def open_file_path(file_path):
    try:
        os.startfile(file_path)
    except AttributeError:
        # Wenn os.startfile unter Linux nicht verfügbar ist, kann stattdessen ein Befehl wie 'xdg-open' verwendet werden.
        os.system(f"xdg-open '{file_path}'")

# Funktion zum Anzeigen der About-Informationen
def show_about():
    about_text = f"{translations['about_text']}\n\n{translations['about_version']}"
    messagebox.showinfo(translations['about_title'], about_text)

# Funktion zum Anzeigen des Videos im Browser
def watch_video_online():
    url = url_entry.get()
    webbrowser.open(url)

# Funktion zum Löschen der Historie
def clear_history():
    history_listbox.delete(0, tk.END)

# Funktion zum Speichern der Historie in einer TXT-Datei
def save_history():
    history_text = "\n\n".join(history_listbox.get(0, tk.END))
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(history_text)

# Funktion zum Anzeigen des Changelogs
def show_changelog():
    changelog_text = """
    Version 1.0.1 (9.09.2023):
    - Added an history.
    - Added .mov format.
    - Added the ability to download the history as a TXT file.
    - Added a Changelog menu to view update details.
    - Fixed Performance Issues.
    - Fixed Language Bug.
    """
    messagebox.showinfo("Changelog", changelog_text)

# Funktion zum Ändern der Sprache
def set_language(language):
    global translations
    translations = language_translations[language]
    update_language()

# Funktion zum Aktualisieren der Benutzeroberfläche für die ausgewählte Sprache
def update_language():
    url_label.config(text=translations["url_label"])
    resolution_label.config(text=translations["resolution_label"])
    format_label.config(text=translations["format_label"])
    download_button.config(text=translations["download_button"])
    result_label.config(text=translations["result_label"])
    file_menu.entryconfig(file_menu_exit_index, label=translations["file_menu_exit"])
    file_menu.entryconfig(file_menu_save_history_index, label=translations["file_menu_save_history"])
    about_menu.entryconfig(about_menu_about_index, label=translations["about_menu_about"])
    help_menu.entryconfig(help_menu_about_index, label=translations["help_menu_about"])
    file_menu.entryconfig(file_menu_changelog_index, label=translations["file_menu_changelog"])
    language_menu.entryconfig(0, label=translations["language_menu_english"], command=lambda: set_language("english"))
    language_menu.entryconfig(1, label=translations["language_menu_german"], command=lambda: set_language("german"))
    language_menu.entryconfig(2, label=translations["language_menu_french"], command=lambda: set_language("french"))
    language_menu.entryconfig(3, label=translations["language_menu_spanish"], command=lambda: set_language("spanish"))
    language_menu.entryconfig(4, label=translations["language_menu_italian"], command=lambda: set_language("italian"))

# GUI erstellen
root = tk.Tk()
root.title("Video Downloader")
root.geometry("800x475")  # Breite x Höhe

# Mindestfenstergröße festlegen
root.minsize(800, 475)

# Übersetzungen für die Benutzeroberfläche
language_translations = {
    "english": {
        "url_label": "Enter the YouTube video URL:",
        "resolution_label": "Select the resolution:",
        "format_label": "Select the video format:",
        "download_button": "Download",
        "result_label": "",
        "file_menu_exit": "Exit",
        "file_menu_save_history": "Save History",
        "about_menu_about": "About",
        "help_menu_about": "Help",
        "file_menu_changelog": "Changelog",
        "language_menu_english": "English",
        "language_menu_german": "German",
        "language_menu_french": "French",
        "language_menu_spanish": "Spanish",
        "language_menu_italian": "Italian",
        "about_title": "About",
        "about_text": "Welcome to KDownloads, your reliable partner for downloading files from the Internet. I am proud to offer you powerful download software that takes your download experience to the next level.\nMy mission is to make file downloads as simple and efficient as possible, saving you time and effort. I firmly believe that access to important content from the internet should be smooth and hassle-free.\nThank you for choosing KDownloads to meet your download needs. I look forward to continuing to provide you with the best possible service and exceeding your expectations.\n\n\nCreated by Johann Kramer in 2023©",
        "about_version": "Version 1.0.1",
        "resolution_not_available": "The selected resolution is not available.",
        "download_success": "Video was successfully downloaded. Approximate file size:",
        "download_canceled": "Download canceled.",
        "history_label": "Download History",
        "clear_history_button": "Clear History",
        "save_history_button": "Save History",
    },
    "german": {
        "url_label": "Geben Sie die URL des YouTube-Videos ein:",
        "resolution_label": "Wählen Sie die Auflösung:",
        "format_label": "Wählen Sie das Videoformat:",
        "download_button": "Herunterladen",
        "result_label": "",
        "file_menu_exit": "Beenden",
        "file_menu_save_history": "Historie speichern",
        "about_menu_about": "Über",
        "help_menu_about": "Hilfe",
        "file_menu_changelog": "Changelog",
        "language_menu_english": "Englisch",
        "language_menu_german": "Deutsch",
        "language_menu_french": "Französisch",
        "language_menu_spanish": "Spanisch",
        "language_menu_italian": "Italienisch",
        "about_title": "Über",
        "about_text": "Willkommen bei KDownloads, Ihrem zuverlässigen Partner für das Herunterladen von Dateien aus dem Internet. Ich bin stolz darauf, Ihnen eine leistungsstarke Download-Software anbieten zu können, die Ihr Download-Erlebnis auf die nächste Stufe hebt.\nMein Ziel ist es, das Herunterladen von Dateien so einfach und effizient wie möglich zu gestalten, damit Sie Zeit und Mühe sparen. Ich bin fest davon überzeugt, dass der Zugang zu wichtigen Inhalten aus dem Internet reibungslos und problemlos sein sollte.\nDanke, dass Sie sich für KDownloads entschieden haben, um Ihre Download-Anforderungen zu erfüllen. Ich freue mich darauf, Ihnen weiterhin den bestmöglichen Service zu bieten und Ihre Erwartungen zu übertreffen.\n\n\nErstellt von Johann Kramer im Jahr 2023©",
        "about_version": "Version 1.0.1",
        "resolution_not_available": "Die gewählte Auflösung ist nicht verfügbar.",
        "download_success": "Das Video wurde erfolgreich heruntergeladen. Ungefähre Dateigröße:",
        "download_canceled": "Der Download wurde abgebrochen.",
        "history_label": "Historie herunterladen.",
        "clear_history_button": "Historie löschen",
        "save_history_button": "Historie speichern",
    },
    "french": {
        "url_label": "Saisissez l'URL de la vidéo YouTube :",
        "resolution_label": "Choisissez la résolution :",
        "format_label": "Sélectionnez le format vidéo :",
        "download_button": "Télécharger",
        "result_label": "",
        "file_menu_exit": "Quitter",
        "file_menu_save_history": "Enregistrer l'historique",
        "about_menu_about": "Au sujet de",
        "help_menu_about": "L'aide",
        "file_menu_changelog": "Changelog",
        "language_menu_english": "Anglaise",
        "language_menu_german": "Allemande",
        "language_menu_french": "Français",
        "language_menu_spanish": "Espagnole",
        "language_menu_italian": "Italienne",
        "about_title": "Au sujet de",
        "about_text": "Bienvenue sur KDownloads, votre partenaire fiable pour le téléchargement de fichiers sur Internet. Je suis fier de vous offrir un logiciel de téléchargement puissant qui vous permet de passer à la vitesse supérieure.\nMa mission est de rendre le téléchargement de fichiers aussi simple et efficace que possible, afin de vous faire gagner du temps et de l'énergie. Je crois fermement que l'accès au contenu important d'Internet doit être fluide et sans problème.\nNous vous remercions d'avoir choisi KDownloads pour répondre à vos besoins de téléchargement. Je suis impatient de continuer à vous fournir le meilleur service possible et de dépasser vos attentes.\n\n\nCréé par Johann Kramer en 2023©.",
        "about_version": "Version 1.0.1",
        "resolution_not_available": "La résolution sélectionnée n'est pas disponible.",
        "download_success": "La vidéo a été téléchargée avec succès. Taille approximative du fichier :",
        "download_canceled": "Téléchargement annulé.",
        "history_label": "Télécharger l'historique",
        "clear_history_button": "Supprimer l'historique",
        "save_history_button": "Enregistrer l'historique",
    },
    "spanish": {
        "url_label": "Introduzca la URL del vídeo de YouTube:",
        "resolution_label": "Selecciona la resolución:",
        "format_label": "Selecciona el formato de vídeo:",
        "download_button": "Descargar",
        "result_label": "",
        "file_menu_exit": "Salida",
        "file_menu_save_history": "Guardar historial",
        "about_menu_about": "Acerca de",
        "help_menu_about": "Ayuda",
        "file_menu_changelog": "Changelog",
         "language_menu_english": "Inglés",
        "language_menu_german": "Alemán",
        "language_menu_french": "Francés",
        "language_menu_spanish": "Español",
        "language_menu_italian": "Italiano",
        "about_title": "Acerca de",
        "about_text": "Bienvenido a KDownloads, su socio de confianza para descargar archivos de Internet. Estoy orgulloso de ofrecerle un potente software de descarga que lleva su experiencia de descarga al siguiente nivel.\nMi misión es hacer que las descargas de archivos sean lo más sencillas y eficientes posible, ahorrándole tiempo y esfuerzo. Creo firmemente que el acceso a contenidos importantes de Internet debe ser sencillo y sin complicaciones.\nGracias por elegir KDownloads para satisfacer sus necesidades de descarga. Espero seguir ofreciéndole el mejor servicio posible y superar sus expectativas.\n\n\nCreado por Johann Kramer en 2023©.",
        "about_version": "Version 1.0.1",
        "resolution_not_available": "La resolución seleccionada no está disponible.",
        "download_success": "El vídeo se ha descargado correctamente. Tamaño aproximado del archivo:",
        "download_canceled": "Descarga cancelada.",
        "history_label": "Historial de descargas",
        "clear_history_button": "Borrar historial",
        "save_history_button": "Guardar historial",
    },
    "italian": {
        "url_label": "Inserire l'URL del video di YouTube:",
        "resolution_label": "Selezionare la risoluzione:",
        "format_label": "Selezionare il formato video:",
        "download_button": "Download",
        "result_label": "",
        "file_menu_exit": "Exit",
        "file_menu_save_history": "Salvare la cronologia",
        "about_menu_about": "Informazioni su",
        "help_menu_about": "Aiuto",
        "file_menu_changelog": "Changelog",
         "language_menu_english": "Inglese",
        "language_menu_german": "Tedesco",
        "language_menu_french": "Francese",
        "language_menu_spanish": "Spagnolo",
        "language_menu_italian": "Italiano",
        "about_title": "Informazioni su",
        "about_text": "Benvenuti su KDownloads, il vostro partner affidabile per scaricare file da Internet. Sono orgoglioso di offrirvi un potente software di download che porta la vostra esperienza di download a un livello superiore.\nLa mia missione è rendere il download dei file il più semplice ed efficiente possibile, facendovi risparmiare tempo e fatica. Credo fermamente che l'accesso a contenuti importanti da Internet debba essere agevole e senza problemi.\nGrazie per aver scelto KDownloads per soddisfare le vostre esigenze di download. Non vedo l'ora di continuare a fornirvi il miglior servizio possibile e di superare le vostre aspettative.\n\n\nCreata da Johann Kramer nel 2023©",
        "about_version": "Version 1.0.1",
        "resolution_not_available": "La risoluzione selezionata non è disponibile.",
        "download_success": "Il video è stato scaricato con successo. Dimensione approssimativa del file:",
        "download_canceled": "Download annullato.",
        "history_label": "Scarica la storia",
        "clear_history_button": "Cancellare la cronologia",
        "save_history_button": "Salvare la cronologia",
    },
}

# Standardübersetzungen auf Englisch setzen
translations = language_translations["english"]

# Menü erstellen
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=translations["file_menu_exit"], menu=file_menu)
file_menu_exit_index = file_menu.index("end")
file_menu_save_history_index = file_menu_exit_index 
file_menu.add_separator()
file_menu.add_command(label=translations["file_menu_save_history"], command=save_history)
file_menu.add_command(label=translations["file_menu_exit"], command=root.quit)

about_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=translations["about_menu_about"], menu=about_menu)
about_menu_about_index = about_menu.index("end")
about_menu.add_command(label=translations["about_menu_about"], command=show_about)

help_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=translations["help_menu_about"], menu=help_menu)
help_menu_about_index = help_menu.index("end")
help_menu.add_command(label=translations["help_menu_about"], command=lambda: webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

changelog_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=translations["file_menu_changelog"], command=show_changelog)

# Sprachmenü erstellen
language_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Language", menu=language_menu)
language_menu.add_command(label=translations["language_menu_english"], command=lambda: set_language("english"))
language_menu.add_command(label=translations["language_menu_german"], command=lambda: set_language("german"))
language_menu.add_command(label=translations["language_menu_french"], command=lambda: set_language("french"))
language_menu.add_command(label=translations["language_menu_spanish"], command=lambda: set_language("spanish"))
language_menu.add_command(label=translations["language_menu_italian"], command=lambda: set_language("italian"))

# Eingabefeld für die URL
url_label = tk.Label(root, text=translations["url_label"])
url_label.pack(pady=15)
url_entry = tk.Entry(root, width=70)
url_entry.pack(pady=5)

# Dropdown-Menü für die Auflösung
resolution_label = tk.Label(root, text=translations["resolution_label"])
resolution_label.pack(pady=15)
resolution_var = tk.StringVar()
resolutions = ["144p", "240p", "360p", "480p", "720p"]
resolution_var.set("720p")
resolution_dropdown = ttk.Combobox(root, textvariable=resolution_var, values=resolutions, state="readonly")
resolution_dropdown.pack(pady=5)

# Dropdown-Menü für das Videoformat
format_label = tk.Label(root, text=translations["format_label"])
format_label.pack()
format_var = tk.StringVar()
formats = ["mp4 (Video)", "webm (Video)", "3gp (Video)", "mp3 (Audio)", "mov (Video)", "mp4 (Audio)"]  # Hinzugefügt "mp4 (Audio)"
format_var.set("mp4 (Video)")
format_dropdown = ttk.Combobox(root, textvariable=format_var, values=formats, state="readonly")
format_dropdown.pack(pady=5)

# Button zum Herunterladen
download_button = tk.Button(root, text=translations["download_button"], command=download_video, bg="red", fg="white")
download_button.pack(pady=15)

# Historie-Label
history_label = tk.Label(root, text=translations["history_label"])
history_label.pack()

# Liste für die Historie
history_listbox = tk.Listbox(root, width=100, height=5)
history_listbox.pack()

# Button zum Löschen der Historie
clear_history_button = tk.Button(root, text=translations["clear_history_button"], command=clear_history)
clear_history_button.pack(pady=10)

# Button zum Speichern der Historie
save_history_button = tk.Button(root, text=translations["save_history_button"], command=save_history)
save_history_button.pack(pady=5)

# Ergebnislabel
result_label = tk.Label(root, text=translations["result_label"])
result_label.pack()

root.mainloop()









#Created with Love by Johann Kramer