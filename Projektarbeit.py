# from asyncio import windows_events
import tkinter as tk
from tkinter import END, Button, messagebox
from datetime import datetime
import sqlite3
from tkinter import simpledialog
#import RPi.GPIO as GPIO
import time

# zeitlich begrenzte PopUps konfigurieren
def show_timed_message(parent, title, message, timeout=10000, msg_type="info"):
    """Zeigt eine Meldung die sich nach timeout (ms) automatisch schließt"""
    popup = tk.Toplevel(parent)
    popup.title(title)
    
    colors = {"info": "#d4edda", "error": "#f8d7da", "warning": "#fff3cd"}
    bg_color = colors.get(msg_type, "#ffffff")
    popup.configure(bg=bg_color)
    
    label = tk.Label(popup, text=message, font=("Arial", 14), bg=bg_color, padx=20, pady=20)
    label.pack()
    
    ok_button = tk.Button(popup, text="OK", command=popup.destroy, width=10)
    ok_button.pack(pady=10)
    
    popup.after(timeout, popup.destroy)

# GPIO-Pins festlegen
TRIG_PIN1 = 2399923081678425
99923081678425

ECHO_PIN1 = 24
TRIG_PIN2 = 21
ECHO_PIN2 = 22

# GPIO-Modus festlegen
#GPIO.setmode(GPIO.BCM)

# GPIO-Pins als Ein- oder Ausgang konfigurieren
#GPIO.setup(TRIG_PIN, GPIO.OUT)
#GPIO.setup(ECHO_PIN, GPIO.IN)


password = "Projektarbeit"
distance = 30

#def get_distance():
    # # Trigger-Pin auf HIGH setzen (Signal senden)
    # GPIO.output(TRIG_PIN, True)
    # time.sleep(0.00001)
    # GPIO.output(TRIG_PIN, False)

    # # Start- und Endzeitpunkt der Echo-Impulse festlegen
    # start_time = time.time()
    # end_time = time.time()

    # while GPIO.input(ECHO_PIN) == 0:
    #     start_time = time.time()

    # while GPIO.input(ECHO_PIN) == 1:
    #     end_time = time.time()

    # # Dauer des Echo-Impulses berechnen
    # duration = end_time - start_time

    # # Schallgeschwindigkeit (343 m/s) und Formel s = v * t / 2 verwenden, um die Entfernung zu berechnen
    # distance = (343 * duration) / 2

    # return distance

def get_person(stammnummer: int):
    conn = sqlite3.connect('laptopverwaltung1.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personen WHERE stammnummer= ' + stammnummer)
    person_data = cursor.fetchall()
    conn.close()
    return person_data

def get_laptop(laptopnummer: int):
    conn = sqlite3.connect('laptopverwaltung1.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM laptop WHERE laptopnummer= ' + laptopnummer)
    laptop_data = cursor.fetchall()
    conn.close()
    return laptop_data

# Öffne neues Fenster "Ausleihen"
def open_ausleihen():
    # Erstelle ein neues Fenster
    new_window = tk.Toplevel(root)
    new_window.title("Ausleihen")
    new_window.configure (bg="grey")

    # Erstelle Label und Entry Widgets für Name, Stammnummer, Laptopnummer und Datum
    stammnummer_label = tk.Label(new_window, text="Stammnummer:")
    stammnummer_label.grid(row=0, column=0, padx=10, pady=5)
    stammnummer_entry = tk.Entry(new_window)
    stammnummer_entry.grid(row=0, column=1, padx=10, pady=5)

    nachname_label = tk.Label(new_window, text="Nachname:")
    nachname_label.grid(row=1, column=0, padx=10, pady=5)
    nachname_entry = tk.Entry(new_window)
    nachname_entry.grid(row=1, column=1, padx=10, pady=5)

    vorname_label = tk.Label(new_window, text="Vorname:")
    vorname_label.grid(row=2, column=0, padx=10, pady=5)
    vorname_entry = tk.Entry(new_window)
    vorname_entry.grid(row=2, column=1, padx=10, pady=5)

    laptopnummer_label = tk.Label(new_window, text="Laptopnum    mer:")
    laptopnummer_label.grid(row=3, column=0, padx=10, pady=5)
    laptopnummer_entry = tk.Entry(new_window)
    laptopnummer_entry.grid(row=3, column=1, padx=10, pady=5)

    datum_label = tk.Label(new_window, text="Datum:")
    datum_label.grid(row=4, column=0, padx=10, pady=5)

    # Setze das aktuelle Datum als Standardwert im Datumseingabefeld
    today = datetime.today().strftime('%Y-%m-%d')
    datum_entry = tk.Entry(new_window)
    datum_entry.insert(0, today)
    datum_entry.grid(row=4, column=1, padx=10, pady=5)

       # Erstelle Label Widget für Uhrzeit
    uhrzeit_label = tk.Label(new_window, text="Uhrzeit:")
    uhrzeit_label.grid(row=5, column=0, padx=10, pady=5)

    # Die Funktion wird durch ein Event gesteuert, dann werden alle Personendaten zu der jeweiligen Stammnummer
    # gespeichert. Inhalt der Felder wird gelöscht. Neuer Inhalt wird aus person_data extrahiert und in die 
    # Spalte geschrieben 
    def stammnummer_focusout(event):
        person_data = get_person(stammnummer_entry.get())
        nachname_entry.delete(0,END)
        nachname_entry.insert(0, person_data[0][1])
        vorname_entry.delete(0,END)
        vorname_entry.insert(0, person_data[0][2])

    #stammnummer_focusout wird an ein Ereignis gebunden 
    stammnummer_entry.bind("<FocusOut>", stammnummer_focusout)

    # Aktualisiere die Uhrzeit alle 1000 Millisekunden
    def update_uhrzeit():
        now = datetime.now().strftime("%H:%M:%S")
        uhrzeit_entry.configure(state='normal')
        uhrzeit_entry.delete(0, tk.END)
        uhrzeit_entry.insert(0, now)
        uhrzeit_entry.configure(state='readonly')
        new_window.after(1000, update_uhrzeit)

    # Erstelle Eingabefeld für Uhrzeit und starte den Update-Prozess
    uhrzeit_entry = tk.Entry(new_window, state='readonly')
    uhrzeit_entry.grid(row=5, column=1, padx=10, pady=5)
    update_uhrzeit()

    def ausleihen_speichern():
        person_data = get_person(stammnummer_entry.get())
        laptop_data = get_laptop(laptopnummer_entry.get())
        personId = person_data[0][0]
        laptopId = laptop_data[0][0]

         # Prüfung ob Laptop schon ausgeliehen wurde
        conn = sqlite3.connect('laptopverwaltung1.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM ausleihen 
                      WHERE laptopId = ? AND datum_zurueck IS NULL''', (laptopId,))
        if cursor.fetchone():
        show_timed_message(new_window, "Fehler", "Dieser Laptop ist bereits ausgeliehen!", 5000, "error")
        conn.close()
            return

        datum = datum_entry.get()
        uhrzeit = datetime.now().strftime("%H:%M:%S")
        print(laptopId)

       # Füge die Daten in die Datenbank ein
        conn = sqlite3.connect('laptopverwaltung1.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO ausleihen (personenId, laptopId, datum_ausleih, uhrzeit_ausleih)
                          VALUES (?, ?, ?, ?)''', (personId, laptopId, datum, uhrzeit))
    
        cursor.execute('''DELETE FROM laptop_lagerplatz WHERE laptopId = ?'''
                    ,(laptopId,))
        conn.commit()
        conn.close()

        # Hier können die Eingaben gespeichert werden
        show_timed_message(new_window, "Erfolgreich", "Die Daten wurden erfolgreich gespeichert!", 10000, "info")

        # Schließe das Fenster
        new_window.destroy()

    # Senden Button
    button_senden = Button(new_window, text="Senden", command=ausleihen_speichern)
    button_senden.grid(row=6, column=1, padx=5, pady=5)
    
# Öffne das Fenster "Abgeben"
def open_abgeben():

    # Erstelle ein neues Fenster
    new_window = tk.Toplevel(root)
    new_window.title("Abgeben")
    new_window.configure (bg="grey")

    #laptop_data = get_laptop_status()

    laptopnummer_label = tk.Label(new_window, text="Laptopnummer:")
    laptopnummer_label.grid(row=1, column=0, padx=10, pady=5)
    laptopnummer_entry = tk.Entry(new_window)
    laptopnummer_entry.grid(row=1, column=1, padx=10, pady=5)

    lagerplatz_label = tk.Label(new_window, text="Lagerplatz:")
    lagerplatz_label.grid(row=2, column=0, padx=10, pady=5)
    lagerplatz_entry = tk.Entry(new_window)
    lagerplatz_entry.grid(row=2, column=1, padx=10, pady=5)

    datum_label = tk.Label(new_window, text="Datum:")
    datum_label.grid(row=3, column=0, padx=10, pady=5)

    uhrzeit_label = tk.Label(new_window, text="Uhrzeit:")
    uhrzeit_label.grid(row=4, column=0, padx=10, pady=5)

    # Setze das aktuelle Datum als Standardwert im Datumseingabefeld
    today = datetime.today().strftime('%Y-%m-%d')
    datum_entry = tk.Entry(new_window)
    datum_entry.insert(0, today)
    datum_entry.grid(row=3, column=1, padx=10, pady=5)

    def update_uhrzeit():
        now = datetime.now().strftime("%H:%M:%S")
        uhrzeit_entry.configure(state='normal')
        uhrzeit_entry.delete(0, tk.END)
        uhrzeit_entry.insert(0, now)
        uhrzeit_entry.configure(state='readonly')
        new_window.after(1000, update_uhrzeit)

    uhrzeit_entry = tk.Entry(new_window, state='readonly')
    uhrzeit_entry.grid(row=4, column=1, padx=10, pady=5)
    update_uhrzeit()

    def abgeben_speichern():

        laptop_data = get_laptop(laptopnummer_entry.get())
        laptopId = laptop_data[0][0]
        datum = datum_entry.get()
        uhrzeit = datetime.now().strftime("%H:%M:%S")
        lagerplatz_data = get_lagerplatz(lagerplatz_entry.get())
        lagerplatzId = lagerplatz_data[0][0]

        print(lagerplatzId)

        # Hier können die Eingaben weiterverarbeitet oder gespeichert werden
        messagebox.showinfo("Erfolgreich abgegeben", "Die Daten wurden erfolgreich abgegeben!")

        # Füge die Daten in die Datenbank ein
        conn = sqlite3.connect('laptopverwaltung1.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE ausleihen SET datum_zurueck = ?, uhrzeit_zurueck = ? 
                  WHERE laptopId = ? AND datum_zurueck IS NULL AND uhrzeit_zurueck IS NULL''',
               (datum, uhrzeit, laptopId))
        cursor.execute('''INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId)
                          VALUES (?, ?)''', (lagerplatzId, laptopId))
        conn.commit()
        conn.close()

        # Schließe das Fenster
        new_window.destroy()

    # Abgeben Button
    button_abgeben = Button(new_window, text="Abgeben", command=abgeben_speichern)
    button_abgeben.grid(row=5, column=1, padx=5, pady=5)
# Öffne das Fenster "Laptop hinzufügen"

def get_lagerplatz(lagerplatz: int):
    conn = sqlite3.connect('laptopverwaltung1.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lagerplatz WHERE lagerplatz= ' + lagerplatz)
    lagerplatz_data = cursor.fetchall()
    conn.close()
    return lagerplatz_data

def open_laptop_hinzufuegen():

    while True:
        # Überprüfe das Passwort
        user_password = simpledialog.askstring("Passwort", "Passwort eingeben", show="*")
        if user_password == password:
            # Passwort korrekt - Öffne das Fenster
            # Erstelle ein neues Fenster
            new_window = tk.Toplevel(root)
            new_window.title("Laptop hinzufügen") 
            new_window.configure (bg="blue")

            laptopnummer_label = tk.Label(new_window, text="Laptopnummer:")
            laptopnummer_label.grid(row=1, column=0, padx=10, pady=5)
            laptopnummer_entry = tk.Entry(new_window)
            laptopnummer_entry.grid(row=1, column=1, padx=10, pady=5)

            beschreibung_label = tk.Label(new_window, text="Beschreibung:")
            beschreibung_label.grid(row=2, column=0, padx=10, pady=5)
            beschreibung_entry = tk.Entry(new_window)
            beschreibung_entry.grid(row=2, column=1, padx=10, pady=5)

            lagerplatz_label = tk.Label(new_window, text="Lagerplatz:")
            lagerplatz_label.grid(row=3, column=0, padx=10, pady=5)
            lagerplatz_entry = tk.Entry(new_window)
            lagerplatz_entry.grid(row=3, column=1, padx=10, pady=5)

            def lap_hinzufuegen_speichern():
                laptopnummer = laptopnummer_entry.get()
                beschreibung = beschreibung_entry.get()
                lagerplatz_data = get_lagerplatz(lagerplatz_entry.get())
                lagerplatzId = lagerplatz_data[0][0]

               # print(lagerplatzId)

                # Hier können die Eingaben weiterverarbeitet oder gespeichert werden
                messagebox.showinfo("Erfolgreich hinzugefügt", "Der Laptop wurde erfplgreich hinzugefügt!")

                # Füge die Daten in die Datenbank ein
                conn = sqlite3.connect('laptopverwaltung1.db')
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO laptop (laptopnummer, beschreibung)
                        VALUES (?, ?)''', (laptopnummer, beschreibung))
                conn.commit()

                laptop_data = get_laptop(laptopnummer_entry.get())
                laptopId = laptop_data[0][0]

                cursor.execute('''INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId)
                    VALUES (?, ?)''', (lagerplatzId, laptopId))
                conn.commit()
                conn.close()

                # Schließe das Fenster
                new_window.destroy()

            # Hinzufügen Button
            button_hinzufuegen = Button(new_window, text="Hinzufügen", command=lap_hinzufuegen_speichern)
            button_hinzufuegen.grid(row=4, column=1, padx=5, pady=5)

            break  # Beende die Schleife, da das Passwort korrekt ist
        elif user_password is None:
            # Der Benutzer hat das Dialogfeld abgebrochen
            break  # Beende die Schleife, da der Benutzer abgebrochen hat
        else:
            # Passwort falsch - Zeige Fehlermeldung an
            retry = messagebox.askretrycancel("Falsches Passwort", "Das eingegebene Passwort ist nicht korrekt. Erneut versuchen?")
            if not retry:
                break  # Beende die Schleife, da der Benutzer keinen erneuten Versuch möchte
# Öffne das Fenster "Lagerplatz hinzufügen"
def open_lager_hinzufuegen():

    while True:
        # Überprüfe das Passwort
        user_password = simpledialog.askstring("Passwort", "Passwort eingeben", show="*")
        if user_password == password:
            # Passwort korrekt - Öffne das Fenster
            # Erstelle ein neues Fenster
            new_window = tk.Toplevel(root)
            new_window.title("Lagerplatz hinzufügen") 
            new_window.configure (bg="blue")

            lagerplatznummer_label = tk.Label(new_window, text="Lagerplatznummer:")
            lagerplatznummer_label.grid(row=1, column=0, padx=10, pady=5)
            lagerplatznummer_entry = tk.Entry(new_window)
            lagerplatznummer_entry.grid(row=1, column=1, padx=10, pady=5)

            def lag_hinzufuegen_speichern():
                lagerplatznummer = lagerplatznummer_entry.get()

                # Hier können die Eingaben weiterverarbeitet oder gespeichert werden
                messagebox.showinfo("Erfolgreich hinzugefügt", "Der Lagerplatz wurde erfplgreich hinzugefügt!")

                # Füge die Daten in die Datenbank ein
                conn = sqlite3.connect('laptopverwaltung1.db')
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO lagerplatz (lagerplatz)
                        VALUES (?)''', (lagerplatznummer,)) #Tupel 
                conn.commit()
                conn.close()

                # Schließe das Fenster
                new_window.destroy()

            # Hinzufügen Button
            button_hinzufuegen = Button(new_window, text="Hinzufügen", command=lag_hinzufuegen_speichern)
            button_hinzufuegen.grid(row=2, column=1, padx=5, pady=5)

            break  # Beende die Schleife, da das Passwort korrekt ist
        elif user_password is None:
            # Der Benutzer hat das Dialogfeld abgebrochen
            break  # Beende die Schleife, da der Benutzer abgebrochen hat
        else:
            # Passwort falsch - Zeige Fehlermeldung an
            retry = messagebox.askretrycancel("Falsches Passwort", "Das eingegebene Passwort ist nicht korrekt. Erneut versuchen?")
            if not retry:
                break  # Beende die Schleife, da der Benutzer keinen erneuten Versuch möchte
# Öffne das Fenster "Person hinzufügen"
def open_person_hinzufuegen():

    new_window = tk.Toplevel(root)
    new_window.title("Lagerplatz hinzufügen") 
    new_window.configure (bg="blue")

    stammnummer_label = tk.Label(new_window, text="Stammnummer:")
    stammnummer_label.grid(row=0, column=0, padx=10, pady=5)
    stammnummer_entry = tk.Entry(new_window)
    stammnummer_entry.grid(row=0, column=1, padx=10, pady=5)

    nachname_label = tk.Label(new_window, text="Nachname:")
    nachname_label.grid(row=1, column=0, padx=10, pady=5)
    nachname_entry = tk.Entry(new_window)
    nachname_entry.grid(row=1, column=1, padx=10, pady=5)

    vorname_label = tk.Label(new_window, text="Vorname:")
    vorname_label.grid(row=2, column=0, padx=10, pady=5)
    vorname_entry = tk.Entry(new_window)
    vorname_entry.grid(row=2, column=1, padx=10, pady=5)

    def person_hinzufuegen_speichern():
        vorname = vorname_entry.get()
        nachname = nachname_entry.get()
        stammnummer = stammnummer_entry.get()

        # Hier können die Eingaben weiterverarbeitet oder gespeichert werden
        messagebox.showinfo("Erfolgreich hinzugefügt", "Die Person wurde erfolgreich hinzugefügt!")

        # Füge die Daten in die Datenbank ein
        conn = sqlite3.connect('laptopverwaltung1.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO personen (nachname, vorname, stammnummer)
                VALUES (?, ?, ?)''', (nachname, vorname, stammnummer)) 
        conn.commit()
        conn.close()

        # Schließe das Fenster
        new_window.destroy()

    # Hinzufügen Button
    button_hinzufuegen = Button(new_window, text="Hinzufügen", command=person_hinzufuegen_speichern)
    button_hinzufuegen.grid(row=3, column=1, padx=5, pady=5)

def get_laptop_status():
    conn = sqlite3.connect('laptopverwaltung1.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM laptop_status')
    laptop_status_data = cursor.fetchall()
    conn.close()
    return laptop_status_data


# Öffne das Fenster "Laptopstatus anzeigen"
def open_laptop_status():
    # Erstelle ein neues Fenster
    new_window = tk.Toplevel(root)
    new_window.title("Bestand")
    new_window.attributes('-zoomed', True)
    laptop_status_data = get_laptop_status()

    # Trenne in vorrätige und ausgeliehene Laptops
    vorrätig = [x for x in laptop_status_data if x[4] is not None]
    ausgeliehen = [x for x in laptop_status_data if x[4] is None]
    
    # Sortiere jeweils nach Beschreibung
    vorrätig = sorted(vorrätig, key=lambda x: str(x[2] or ''))
    ausgeliehen = sorted(ausgeliehen, key=lambda x: str(x[2] or ''))

    # Erstelle ein Canvas-Widget
    canvas = tk.Canvas(new_window)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Erstelle ein Frame-Widget im Canvas
    frame = tk.Frame(canvas)
    frame.pack(fill=tk.BOTH, expand=True)

    # Füge den Frame dem Canvas hinzu
    canvas.create_window(0, 0, anchor=tk.NW, window=frame)

    # Linke Seite: Vorrätig
    frame_links = tk.Frame(frame)
    frame_links.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
    
    header_vorrätig = tk.Label(frame_links, text=f"Vorrätig ({len(vorrätig)})", font=("Arial", 18, "bold"), fg="green")
    header_vorrätig.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
    
    tk.Label(frame_links, text="Laptop", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(frame_links, text="Lagerplatz", font=("Arial", 14, "bold")).grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    for i, (laptopId, laptopnummer, beschreibung, lagerplatzId, lagerplatz, vorname, nachname) in enumerate(vorrätig):
        row = i + 2
        tk.Label(frame_links, text=f"Laptop {beschreibung}", font=("Arial", 14)).grid(row=row, column=0, padx=10, pady=3, sticky="w")
        tk.Label(frame_links, text=f"{lagerplatz}", font=("Arial", 14)).grid(row=row, column=1, padx=10, pady=3, sticky="w")

    # Rechte Seite: Ausgeliehen
    frame_rechts = tk.Frame(frame)
    frame_rechts.grid(row=0, column=1, padx=20, pady=10, sticky="nw")
    
    header_ausgeliehen = tk.Label(frame_rechts, text=f"Ausgeliehen ({len(ausgeliehen)})", font=("Arial", 18, "bold"), fg="red")
    header_ausgeliehen.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
    
    tk.Label(frame_rechts, text="Laptop", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(frame_rechts, text="Ausgeliehen an", font=("Arial", 14, "bold")).grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    for i, (laptopId, laptopnummer, beschreibung, lagerplatzId, lagerplatz, vorname, nachname) in enumerate(ausgeliehen):
        row = i + 2
        tk.Label(frame_rechts, text=f"Laptop {beschreibung}", font=("Arial", 14)).grid(row=row, column=0, padx=10, pady=3, sticky="w")
        tk.Label(frame_rechts, text=f"{vorname} {nachname}", font=("Arial", 14)).grid(row=row, column=1, padx=10, pady=3, sticky="w")

    # Füge die Scrollbar zum Canvas hinzu
    scrollbar = tk.Scrollbar(new_window, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Konfiguriere das Scrollverhalten
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    
#Erstelle das Hauptfenster des Programms                        
root = tk.Tk()
root.title("Laptopverwaltung")

# Erstelle ein Menü
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Erstelle ein Menü für "Ausleihen"
lend_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ausleihen", menu=lend_menu)

# Füge eine Option zum "Ausleihen"-Menü hinzu
lend_menu.add_command(label="Ausleihen", command=open_ausleihen)

# Erstelle ein Menü für "Abgeben"
lend_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Abgeben", menu=lend_menu)

# Füge eine Option zum "Abgeben"-Menü hinzu
lend_menu.add_command(label="Abgeben", command=open_abgeben)

# Erstelle ein Menü für "Neue Person hinzufügen"
lend_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Neue Person", menu=lend_menu)

# Füge eine Option zum "Neue Person"-Menü hinzu
lend_menu.add_command(label="Neue Person hinzufügen", command=open_person_hinzufuegen)

# Erstelle ein Menü für "Neuer Laptop hinzufügen"
lend_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Neuen Laptop", menu=lend_menu)

# Füge eine Option zum "Neuen Laptop"-Menü hinzu
lend_menu.add_command(label="Neuen Laptop hinzufügen", command=open_laptop_hinzufuegen)

# Erstelle ein Menü für "Neuen Lagerplatz hinzufügen"
lend_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Neuen Lagerplatz", menu=lend_menu)

# Füge eine Option zum "Neuen Lagerplatz"-Menü hinzu
lend_menu.add_command(label="Neuen Lagerplatz hinzufügen", command=open_lager_hinzufuegen)

# Erstelle ein Menü für "Aktueller Bestand"
lend_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Aktueller Bestand", menu=lend_menu)

# Füge eine Option zum "Aktueller Bestand"-Menü hinzu
lend_menu.add_command(label="Aktueller Bestand", command=open_laptop_status)

# Erstelle ein Label mit dem Titel der Anwendung
title_label = tk.Label(root, text="Laptopverwaltung", font=("Arial", 24))
title_label.pack(pady=20)

# Erstelle ein Frame-Widget für die Optionen
options_frame = tk.Frame(root)
options_frame.pack()

# Erstelle ein Label mit einer Beschreibung der verfügbaren Optionen
options_label = tk.Label(options_frame, text="Wähle eine Option aus dem Menü aus:", font=("Arial", 14))
options_label.pack(pady=10)

# Erstelle den "Ausleihen"-Button
lend_button = tk.Button(options_frame, text="Ausleihen", font=("Arial", 18), command=open_ausleihen)
lend_button.pack(pady=5)

# Erstelle den "Abgeben"-Button
lend_button = tk.Button(options_frame, text="Abgeben", font=("Arial", 18), command=open_abgeben)
lend_button.pack(pady=5)

# Erstelle den "Neue Person hinzufügen"-Button
lend_button = tk.Button(options_frame, text="Neue Person hinzufügen", font=("Arial", 18), command=open_person_hinzufuegen)
lend_button.pack(pady=5)

# Erstelle den "Neuen Laptop hinzufügen"-Button
lend_button = tk.Button(options_frame, text="Neuen Laptop hinzufügen", font=("Arial", 18), command=open_laptop_hinzufuegen)
lend_button.pack(pady=5)

# Erstelle den "Neuen Lagerplatz hinzufügen"-Button
lend_button = tk.Button(options_frame, text="Neuen Lagerplatz hinzufügen", font=("Arial", 18), command=open_lager_hinzufuegen)
lend_button.pack(pady=5)

# Erstelle den "Bestand"-Button
lend_button = tk.Button(options_frame, text="Aktueller Bestand", font=("Arial", 18), command=open_laptop_status)
lend_button.pack(pady=5)

#Hauptfenster bleibt geöffnet und reagiert auf Events
root.mainloop()