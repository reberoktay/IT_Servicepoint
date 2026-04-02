# from asyncio import windows_events
import tkinter as tk
from tkinter import END, Button, messagebox
from datetime import datetime
import sqlite3
from tkinter import simpledialog
#import RPi.GPIO as GPIO
import time

# ==================== Konfiguration ====================

DB_PATH = 'laptopverwaltung1.db'
password = "Projektarbeit"
distance = 30

# GPIO-Pins festlegen
TRIG_PIN1 = 23
ECHO_PIN1 = 24
TRIG_PIN2 = 21
ECHO_PIN2 = 22

# GPIO-Modus festlegen
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(TRIG_PIN, GPIO.OUT)
#GPIO.setup(ECHO_PIN, GPIO.IN)

#def get_distance():
    # GPIO.output(TRIG_PIN, True)
    # time.sleep(0.00001)
    # GPIO.output(TRIG_PIN, False)
    # start_time = time.time()
    # end_time = time.time()
    # while GPIO.input(ECHO_PIN) == 0:
    #     start_time = time.time()
    # while GPIO.input(ECHO_PIN) == 1:
    #     end_time = time.time()
    # duration = end_time - start_time
    # distance = (343 * duration) / 2
    # return distance

# ==================== Helper-Funktionen ====================

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


def db_query(sql, params=(), fetch=True, commit=False):
    """Zentrale DB-Funktion: führt Query aus, gibt Ergebnis zurück oder committed."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall() if fetch else None
    if commit:
        conn.commit()
    conn.close()
    return result


def create_form_window(title, bg="grey"):
    """Erstellt ein neues Toplevel-Fenster mit Titel und Hintergrundfarbe."""
    window = tk.Toplevel(root)
    window.title(title)
    window.configure(bg=bg)
    return window


def add_field(window, label_text, row, focus=False, readonly=False, default=None):
    """Erstellt ein Label+Entry-Paar im Grid und gibt das Entry zurück."""
    tk.Label(window, text=label_text).grid(row=row, column=0, padx=10, pady=5)
    state = 'readonly' if readonly else 'normal'
    entry = tk.Entry(window, state=state)
    entry.grid(row=row, column=1, padx=10, pady=5)
    if default and not readonly:
        entry.insert(0, default)
    if focus:
        entry.focus_set()
    return entry


def add_uhrzeit_field(window, row):
    """Erstellt ein sich automatisch aktualisierendes Uhrzeit-Feld."""
    tk.Label(window, text="Uhrzeit:").grid(row=row, column=0, padx=10, pady=5)
    uhrzeit_entry = tk.Entry(window, state='readonly')
    uhrzeit_entry.grid(row=row, column=1, padx=10, pady=5)

    def update_uhrzeit():
        now = datetime.now().strftime("%H:%M:%S")
        uhrzeit_entry.configure(state='normal')
        uhrzeit_entry.delete(0, tk.END)
        uhrzeit_entry.insert(0, now)
        uhrzeit_entry.configure(state='readonly')
        window.after(1000, update_uhrzeit)

    update_uhrzeit()
    return uhrzeit_entry


def add_button(window, text, command, row):
    """Erstellt einen Button im Grid."""
    btn = Button(window, text=text, command=command)
    btn.grid(row=row, column=1, padx=5, pady=5)
    return btn


def passwort_pruefen():
    """Prüft das Passwort in einer Schleife. Gibt True zurück wenn korrekt, False bei Abbruch."""
    while True:
        user_password = simpledialog.askstring("Passwort", "Passwort eingeben", show="*")
        if user_password == password:
            return True
        elif user_password is None:
            return False
        else:
            retry = messagebox.askretrycancel("Falsches Passwort", 
                "Das eingegebene Passwort ist nicht korrekt. Erneut versuchen?")
            if not retry:
                return False


# ==================== DB-Abfragen ====================

def get_person(stammnummer):
    return db_query('SELECT * FROM personen WHERE stammnummer= ' + stammnummer)

def get_laptop(laptopnummer):
    return db_query('SELECT * FROM laptop WHERE laptopnummer= ' + laptopnummer)

def get_lagerplatz(lagerplatz):
    return db_query('SELECT * FROM lagerplatz WHERE lagerplatz= ' + lagerplatz)

def get_laptop_status():
    return db_query('SELECT * FROM laptop_status')


# ==================== Inaktive Azubis ====================

def get_inaktive_azubis():
    return db_query('''
        SELECT p.id, p.vorname, p.nachname, MAX(a.datum_ausleih) as letzte_ausleihe
        FROM personen p
        LEFT JOIN ausleihen a ON p.id = a.personenId
        GROUP BY p.id
        HAVING letzte_ausleihe IS NULL 
           OR letzte_ausleihe < date("now", "-2 years")
        ORDER BY p.nachname
    ''')

def loesche_inaktive_azubis(azubi_ids):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for azubi_id in azubi_ids:
        cursor.execute('DELETE FROM personen WHERE id = ?', (azubi_id,))
    conn.commit()
    conn.close()

def pruefe_inaktive_azubis():
    inaktive = get_inaktive_azubis()
    if not inaktive:
        return
    azubi_ids = [a[0] for a in inaktive]
    loesche_inaktive_azubis(azubi_ids)
    show_timed_message(root, "Bereinigt", f"{len(inaktive)} inaktive Azubi(s) wurden gelöscht.", 5000, "info")


# ==================== Fenster: Ausleihen ====================

def open_ausleihen():
    window = create_form_window("Ausleihen")
    today = datetime.today().strftime('%Y-%m-%d')

    stammnummer_entry  = add_field(window, "Stammnummer:", 0, focus=True)
    nachname_entry     = add_field(window, "Nachname:", 1)
    vorname_entry      = add_field(window, "Vorname:", 2)
    laptopnummer_entry = add_field(window, "Laptopnummer:", 3)
    datum_entry        = add_field(window, "Datum:", 4, default=today)
    uhrzeit_entry      = add_uhrzeit_field(window, 5)

    def stammnummer_focusout(event):
        person_data = get_person(stammnummer_entry.get())
        nachname_entry.delete(0, END)
        nachname_entry.insert(0, person_data[0][1])
        vorname_entry.delete(0, END)
        vorname_entry.insert(0, person_data[0][2])

    stammnummer_entry.bind("<FocusOut>", stammnummer_focusout)

    def ausleihen_speichern():
        person_data = get_person(stammnummer_entry.get())
        laptop_data = get_laptop(laptopnummer_entry.get())
        personId = person_data[0][0]
        laptopId = laptop_data[0][0]

        # Prüfung ob Laptop schon ausgeliehen wurde
        bereits_ausgeliehen = db_query(
            'SELECT * FROM ausleihen WHERE laptopId = ? AND datum_zurueck IS NULL',
            (laptopId,))
        if bereits_ausgeliehen:
            show_timed_message(window, "Fehler", "Dieser Laptop ist bereits ausgeliehen!", 5000, "error")
            return

        datum = datum_entry.get()
        uhrzeit = datetime.now().strftime("%H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO ausleihen (personenId, laptopId, datum_ausleih, uhrzeit_ausleih)
                          VALUES (?, ?, ?, ?)''', (personId, laptopId, datum, uhrzeit))
        cursor.execute('DELETE FROM laptop_lagerplatz WHERE laptopId = ?', (laptopId,))
        conn.commit()
        conn.close()

        show_timed_message(window, "Erfolgreich", "Die Daten wurden erfolgreich gespeichert!", 10000, "info")
        window.destroy()

    add_button(window, "Senden", ausleihen_speichern, 6)


# ==================== Fenster: Abgeben ====================

def open_abgeben():
    window = create_form_window("Abgeben")
    today = datetime.today().strftime('%Y-%m-%d')

    laptopnummer_entry = add_field(window, "Laptopnummer:", 1, focus=True)
    lagerplatz_entry   = add_field(window, "Lagerplatz:", 2)
    datum_entry        = add_field(window, "Datum:", 3, default=today)
    uhrzeit_entry      = add_uhrzeit_field(window, 4)

    # Kopiere Laptopnummer automatisch in Lagerplatz
    def laptopnummer_changed(event):
        lagerplatz_entry.delete(0, END)
        lagerplatz_entry.insert(0, laptopnummer_entry.get())

    laptopnummer_entry.bind("<FocusOut>", laptopnummer_changed)
    laptopnummer_entry.bind("<Return>", laptopnummer_changed)

    def abgeben_speichern():
        laptop_data = get_laptop(laptopnummer_entry.get())
        laptopId = laptop_data[0][0]
        datum = datum_entry.get()
        uhrzeit = datetime.now().strftime("%H:%M:%S")
        lagerplatz_data = get_lagerplatz(lagerplatz_entry.get())
        lagerplatzId = lagerplatz_data[0][0]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''UPDATE ausleihen SET datum_zurueck = ?, uhrzeit_zurueck = ? 
                  WHERE laptopId = ? AND datum_zurueck IS NULL AND uhrzeit_zurueck IS NULL''',
               (datum, uhrzeit, laptopId))
        cursor.execute('''INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId)
                          VALUES (?, ?)''', (lagerplatzId, laptopId))
        conn.commit()
        conn.close()

        messagebox.showinfo("Erfolgreich abgegeben", "Die Daten wurden erfolgreich abgegeben!")
        window.destroy()

    add_button(window, "Abgeben", abgeben_speichern, 5)


# ==================== Fenster: Laptop hinzufügen ====================

def open_laptop_hinzufuegen():
    if not passwort_pruefen():
        return

    window = create_form_window("Laptop hinzufügen", bg="blue")

    laptopnummer_entry = add_field(window, "Laptopnummer:", 1, focus=True)
    beschreibung_entry = add_field(window, "Beschreibung:", 2)
    lagerplatz_entry   = add_field(window, "Lagerplatz:", 3)

    def lap_hinzufuegen_speichern():
        laptopnummer = laptopnummer_entry.get()
        beschreibung = beschreibung_entry.get()
        lagerplatz_data = get_lagerplatz(lagerplatz_entry.get())
        lagerplatzId = lagerplatz_data[0][0]

        messagebox.showinfo("Erfolgreich hinzugefügt", "Der Laptop wurde erfolgreich hinzugefügt!")

        conn = sqlite3.connect(DB_PATH)
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

        window.destroy()

    add_button(window, "Hinzufügen", lap_hinzufuegen_speichern, 4)


# ==================== Fenster: Lagerplatz hinzufügen ====================

def open_lager_hinzufuegen():
    if not passwort_pruefen():
        return

    window = create_form_window("Lagerplatz hinzufügen", bg="blue")

    lagerplatznummer_entry = add_field(window, "Lagerplatznummer:", 1, focus=True)

    def lag_hinzufuegen_speichern():
        lagerplatznummer = lagerplatznummer_entry.get()
        messagebox.showinfo("Erfolgreich hinzugefügt", "Der Lagerplatz wurde erfolgreich hinzugefügt!")
        db_query('INSERT INTO lagerplatz (lagerplatz) VALUES (?)', 
                 (lagerplatznummer,), fetch=False, commit=True)
        window.destroy()

    add_button(window, "Hinzufügen", lag_hinzufuegen_speichern, 2)


# ==================== Fenster: Person hinzufügen ====================

def open_person_hinzufuegen():
    window = create_form_window("Person hinzufügen", bg="blue")

    stammnummer_entry = add_field(window, "Stammnummer:", 0, focus=True)
    nachname_entry    = add_field(window, "Nachname:", 1)
    vorname_entry     = add_field(window, "Vorname:", 2)

    def person_hinzufuegen_speichern():
        vorname = vorname_entry.get()
        nachname = nachname_entry.get()
        stammnummer = stammnummer_entry.get()

        db_query('INSERT INTO personen (nachname, vorname, stammnummer) VALUES (?, ?, ?)',
                 (nachname, vorname, stammnummer), fetch=False, commit=True)

        window.destroy()
        show_timed_message(root, "Erfolgreich", "Die Person wurde erfolgreich hinzugefügt!", 3000, "info")
        pruefe_inaktive_azubis()

    add_button(window, "Hinzufügen", person_hinzufuegen_speichern, 3)


# ==================== Fenster: Bestand anzeigen ====================

def open_laptop_status():
    new_window = tk.Toplevel(root)
    new_window.title("Bestand")
    new_window.attributes('-zoomed', True)
    laptop_status_data = get_laptop_status()

    # Trenne in vorrätige und ausgeliehene Laptops
    vorrätig = sorted([x for x in laptop_status_data if x[4] is not None], key=lambda x: str(x[2] or ''))
    ausgeliehen = sorted([x for x in laptop_status_data if x[4] is None], key=lambda x: str(x[2] or ''))

    # Scrollbares Layout
    canvas = tk.Canvas(new_window)
    canvas.pack(fill=tk.BOTH, expand=True)
    frame = tk.Frame(canvas)
    frame.pack(fill=tk.BOTH, expand=True)
    canvas.create_window(0, 0, anchor=tk.NW, window=frame)

    # Linke Seite: Vorrätig
    frame_links = tk.Frame(frame)
    frame_links.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
    
    tk.Label(frame_links, text=f"Vorrätig ({len(vorrätig)})", font=("Arial", 18, "bold"), fg="green")\
        .grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
    tk.Label(frame_links, text="Laptop", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(frame_links, text="Lagerplatz", font=("Arial", 14, "bold")).grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    for i, (laptopId, laptopnummer, beschreibung, lagerplatzId, lagerplatz, vorname, nachname) in enumerate(vorrätig):
        row = i + 2
        tk.Label(frame_links, text=f"Laptop {beschreibung}", font=("Arial", 14)).grid(row=row, column=0, padx=10, pady=3, sticky="w")
        tk.Label(frame_links, text=f"{lagerplatz}", font=("Arial", 14)).grid(row=row, column=1, padx=10, pady=3, sticky="w")

    # Rechte Seite: Ausgeliehen
    frame_rechts = tk.Frame(frame)
    frame_rechts.grid(row=0, column=1, padx=20, pady=10, sticky="nw")
    
    tk.Label(frame_rechts, text=f"Ausgeliehen ({len(ausgeliehen)})", font=("Arial", 18, "bold"), fg="red")\
        .grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
    tk.Label(frame_rechts, text="Laptop", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(frame_rechts, text="Ausgeliehen an", font=("Arial", 14, "bold")).grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    for i, (laptopId, laptopnummer, beschreibung, lagerplatzId, lagerplatz, vorname, nachname) in enumerate(ausgeliehen):
        row = i + 2
        tk.Label(frame_rechts, text=f"Laptop {beschreibung}", font=("Arial", 14)).grid(row=row, column=0, padx=10, pady=3, sticky="w")
        tk.Label(frame_rechts, text=f"{vorname} {nachname}", font=("Arial", 14)).grid(row=row, column=1, padx=10, pady=3, sticky="w")

    scrollbar = tk.Scrollbar(new_window, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


# ==================== Hauptfenster ====================

root = tk.Tk()
root.title("Laptopverwaltung")

# Menü und Buttons aus einer Liste aufbauen
MENU_ITEMS = [
    ("Ausleihen",         "Ausleihen",                   open_ausleihen),
    ("Abgeben",           "Abgeben",                     open_abgeben),
    ("Neue Person",       "Neue Person hinzufügen",      open_person_hinzufuegen),
    ("Neuen Laptop",      "Neuen Laptop hinzufügen",     open_laptop_hinzufuegen),
    ("Neuen Lagerplatz",  "Neuen Lagerplatz hinzufügen", open_lager_hinzufuegen),
    ("Aktueller Bestand", "Aktueller Bestand",           open_laptop_status),
]

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

for menu_label, command_label, command in MENU_ITEMS:
    menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=menu_label, menu=menu)
    menu.add_command(label=command_label, command=command)

title_label = tk.Label(root, text="Laptopverwaltung", font=("Arial", 24))
title_label.pack(pady=20)

options_frame = tk.Frame(root)
options_frame.pack()

options_label = tk.Label(options_frame, text="Wähle eine Option aus dem Menü aus:", font=("Arial", 14))
options_label.pack(pady=10)

for _, button_text, command in MENU_ITEMS:
    tk.Button(options_frame, text=button_text, font=("Arial", 18), command=command).pack(pady=5)

root.mainloop()
