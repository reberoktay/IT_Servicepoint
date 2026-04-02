import tkinter as tk
from tkinter import ttk, END, messagebox, simpledialog
from datetime import datetime
import sqlite3
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


# ==================== Dark Theme Farben ====================

COLORS = {
    "bg":          "#1a1d23",
    "bg_topbar":   "#22262e",
    "bg_card":     "#22262e",
    "bg_hover":    "#2a2f38",
    "border":      "#2d323c",
    "text":        "#e8ecf1",
    "text_muted":  "#6b7280",
    "text_label":  "#8b919a",
    "accent_blue": "#2563eb",
    "accent_green":"#16a34a",
    "green_bg":    "#0f2918",
    "green_text":  "#4ade80",
    "red_bg":      "#1e1215",
    "red_text":    "#f87171",
    "entry_bg":    "#2a2f38",
    "entry_fg":    "#e8ecf1",
    "success_bg":  "#0f2918",
    "success_fg":  "#4ade80",
    "error_bg":    "#1e1215",
    "error_fg":    "#f87171",
    "warning_bg":  "#1e1a0f",
    "warning_fg":  "#fbbf24",
}

FONT       = ("Segoe UI", 12)
FONT_SMALL = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 20)
FONT_HEAD  = ("Segoe UI", 14, "bold")
FONT_BTN   = ("Segoe UI", 13)


def setup_styles():
    """Konfiguriert ttk-Styles fuer das Dark Theme."""
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(".", background=COLORS["bg"], foreground=COLORS["text"], font=FONT)

    # Frames
    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Topbar.TFrame", background=COLORS["bg_topbar"])
    style.configure("Card.TFrame", background=COLORS["bg_card"])

    # Labels
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=FONT)
    style.configure("Topbar.TLabel", background=COLORS["bg_topbar"],
                    foreground=COLORS["text_muted"], font=FONT_SMALL)
    style.configure("Title.TLabel", background=COLORS["bg"],
                    foreground=COLORS["text"], font=FONT_TITLE)
    style.configure("Heading.TLabel", background=COLORS["bg"],
                    foreground=COLORS["text"], font=FONT_HEAD)
    style.configure("Muted.TLabel", background=COLORS["bg"],
                    foreground=COLORS["text_muted"], font=FONT_SMALL)
    style.configure("CardLabel.TLabel", background=COLORS["bg_card"],
                    foreground=COLORS["text"], font=FONT)

    # Stat-Kacheln im Bestand
    style.configure("GreenStat.TFrame", background=COLORS["green_bg"])
    style.configure("GreenStatTitle.TLabel", background=COLORS["green_bg"],
                    foreground=COLORS["green_text"], font=FONT_SMALL)
    style.configure("GreenStatNum.TLabel", background=COLORS["green_bg"],
                    foreground=COLORS["text"], font=("Segoe UI", 26, "bold"))
    style.configure("RedStat.TFrame", background=COLORS["red_bg"])
    style.configure("RedStatTitle.TLabel", background=COLORS["red_bg"],
                    foreground=COLORS["red_text"], font=FONT_SMALL)
    style.configure("RedStatNum.TLabel", background=COLORS["red_bg"],
                    foreground=COLORS["text"], font=("Segoe UI", 26, "bold"))

    # Buttons
    style.configure("Primary.TButton", background=COLORS["accent_blue"],
                    foreground="white", font=FONT_BTN, padding=(16, 12))
    style.map("Primary.TButton",
              background=[("active", "#1d4ed8"), ("pressed", "#1e40af")])

    style.configure("Success.TButton", background=COLORS["accent_green"],
                    foreground="white", font=FONT_BTN, padding=(16, 12))
    style.map("Success.TButton",
              background=[("active", "#15803d"), ("pressed", "#166534")])

    style.configure("Secondary.TButton", background=COLORS["bg_card"],
                    foreground=COLORS["text"], font=FONT_BTN, padding=(16, 12),
                    borderwidth=1, relief="solid")
    style.map("Secondary.TButton",
              background=[("active", COLORS["bg_hover"]), ("pressed", COLORS["border"])])

    style.configure("Form.TButton", background=COLORS["accent_blue"],
                    foreground="white", font=FONT_BTN, padding=(20, 10))
    style.map("Form.TButton",
              background=[("active", "#1d4ed8"), ("pressed", "#1e40af")])

    # Entry
    style.configure("TEntry", fieldbackground=COLORS["entry_bg"],
                    foreground=COLORS["entry_fg"], insertcolor=COLORS["entry_fg"],
                    borderwidth=1, relief="solid", padding=6)
    style.map("TEntry",
              fieldbackground=[("readonly", COLORS["bg_card"])],
              foreground=[("readonly", COLORS["text_muted"])])

    # Treeview (fuer Bestandsliste)
    style.configure("Treeview",
                    background=COLORS["bg"],
                    foreground=COLORS["text"],
                    fieldbackground=COLORS["bg"],
                    borderwidth=0,
                    font=FONT_SMALL,
                    rowheight=28)
    style.configure("Treeview.Heading",
                    background=COLORS["bg_card"],
                    foreground=COLORS["text_muted"],
                    font=FONT_SMALL,
                    borderwidth=0,
                    relief="flat")
    style.map("Treeview",
              background=[("selected", COLORS["accent_blue"])],
              foreground=[("selected", "white")])
    style.map("Treeview.Heading",
              background=[("active", COLORS["bg_hover"])])

    # Scrollbar
    style.configure("Vertical.TScrollbar",
                    background=COLORS["bg_card"],
                    troughcolor=COLORS["bg"],
                    borderwidth=0,
                    arrowsize=0)


# ==================== Helper-Funktionen ====================

def show_timed_message(parent, title, message, timeout=10000, msg_type="info"):
    """Zeigt eine Meldung die sich nach timeout (ms) automatisch schliesst"""
    popup = tk.Toplevel(parent)
    popup.title(title)
    popup.configure(bg=COLORS["bg"])
    popup.resizable(False, False)

    type_colors = {
        "info":    (COLORS["success_bg"], COLORS["success_fg"]),
        "error":   (COLORS["error_bg"],   COLORS["error_fg"]),
        "warning": (COLORS["warning_bg"], COLORS["warning_fg"]),
    }
    bg_color, fg_color = type_colors.get(msg_type, (COLORS["bg_card"], COLORS["text"]))

    frame = tk.Frame(popup, bg=bg_color, padx=24, pady=16)
    frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

    tk.Label(frame, text=message, font=FONT, bg=bg_color, fg=fg_color,
             wraplength=350).pack(pady=(0, 12))

    ok_btn = ttk.Button(frame, text="OK", command=popup.destroy, style="Form.TButton")
    ok_btn.pack()

    popup.after(timeout, popup.destroy)


def db_query(sql, params=(), fetch=True, commit=False):
    """Zentrale DB-Funktion: fuehrt Query aus, gibt Ergebnis zurueck oder committed."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall() if fetch else None
    if commit:
        conn.commit()
    conn.close()
    return result


def create_form_window(title):
    """Erstellt ein neues Toplevel-Fenster im Dark Theme."""
    window = tk.Toplevel(root)
    window.title(title)
    window.configure(bg=COLORS["bg"])
    window.resizable(False, False)

    # Topbar
    topbar = ttk.Frame(window, style="Topbar.TFrame")
    topbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
    ttk.Label(topbar, text="IT-Servicepoint", style="Topbar.TLabel").pack(
        anchor="w", padx=16, pady=8)

    # Separator
    sep = tk.Frame(window, bg=COLORS["border"], height=1)
    sep.grid(row=1, column=0, columnspan=2, sticky="ew")

    # Titel
    ttk.Label(window, text=title, style="Heading.TLabel").grid(
        row=2, column=0, columnspan=2, pady=(20, 16), padx=24)

    return window


def add_field(window, label_text, row, focus=False, readonly=False, default=None):
    """Erstellt ein Label+Entry-Paar im Grid und gibt das Entry zurueck."""
    actual_row = row + 3  # Offset fuer Topbar + Separator + Titel

    ttk.Label(window, text=label_text, style="TLabel").grid(
        row=actual_row, column=0, padx=(24, 8), pady=6, sticky="e")

    entry = ttk.Entry(window, style="TEntry", width=28)
    if readonly:
        entry.configure(state='readonly')
    entry.grid(row=actual_row, column=1, padx=(0, 24), pady=6, sticky="w")

    if default and not readonly:
        entry.insert(0, default)
    if focus:
        entry.focus_set()
    return entry


def add_uhrzeit_field(window, row):
    """Erstellt ein sich automatisch aktualisierendes Uhrzeit-Feld."""
    actual_row = row + 3

    ttk.Label(window, text="Uhrzeit:", style="TLabel").grid(
        row=actual_row, column=0, padx=(24, 8), pady=6, sticky="e")

    uhrzeit_entry = ttk.Entry(window, style="TEntry", width=28, state='readonly')
    uhrzeit_entry.grid(row=actual_row, column=1, padx=(0, 24), pady=6, sticky="w")

    def update_uhrzeit():
        now = datetime.now().strftime("%H:%M:%S")
        uhrzeit_entry.configure(state='normal')
        uhrzeit_entry.delete(0, tk.END)
        uhrzeit_entry.insert(0, now)
        uhrzeit_entry.configure(state='readonly')
        window.after(1000, update_uhrzeit)

    update_uhrzeit()
    return uhrzeit_entry


def add_button(window, text, command, row, style="Form.TButton"):
    """Erstellt einen Button im Grid."""
    actual_row = row + 3
    btn = ttk.Button(window, text=text, command=command, style=style)
    btn.grid(row=actual_row, column=0, columnspan=2, padx=24, pady=(16, 24))
    return btn


def passwort_pruefen():
    """Prueft das Passwort in einer Schleife. Gibt True zurueck wenn korrekt, False bei Abbruch."""
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
    show_timed_message(root, "Bereinigt",
                       f"{len(inaktive)} inaktive Azubi(s) wurden geloescht.", 5000, "info")


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
        stnr = stammnummer_entry.get().strip()
        if not stnr:
            return
        person_data = get_person(stnr)
        if not person_data:
            nachname_entry.delete(0, END)
            vorname_entry.delete(0, END)
            show_timed_message(window, "Fehler",
                               f"Keine Person mit Stammnummer {stnr} gefunden!", 5000, "error")
            return
        nachname_entry.delete(0, END)
        nachname_entry.insert(0, person_data[0][1])
        vorname_entry.delete(0, END)
        vorname_entry.insert(0, person_data[0][2])

    stammnummer_entry.bind("<FocusOut>", stammnummer_focusout)

    def ausleihen_speichern():
        # Person pruefen
        stnr = stammnummer_entry.get().strip()
        if not stnr:
            show_timed_message(window, "Fehler",
                               "Bitte Stammnummer eingeben!", 5000, "error")
            return
        person_data = get_person(stnr)
        if not person_data:
            show_timed_message(window, "Fehler",
                               f"Keine Person mit Stammnummer {stnr} gefunden!", 5000, "error")
            return

        # Laptop pruefen
        lnr = laptopnummer_entry.get().strip()
        if not lnr:
            show_timed_message(window, "Fehler",
                               "Bitte Laptopnummer eingeben!", 5000, "error")
            return
        laptop_data = get_laptop(lnr)
        if not laptop_data:
            show_timed_message(window, "Fehler",
                               f"Kein Laptop mit Nummer {lnr} gefunden!", 5000, "error")
            return

        personId = person_data[0][0]
        laptopId = laptop_data[0][0]

        # Pruefung ob Laptop schon ausgeliehen wurde
        bereits_ausgeliehen = db_query(
            'SELECT * FROM ausleihen WHERE laptopId = ? AND datum_zurueck IS NULL',
            (laptopId,))
        if bereits_ausgeliehen:
            show_timed_message(window, "Fehler",
                               "Dieser Laptop ist bereits ausgeliehen!", 5000, "error")
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

        show_timed_message(window, "Erfolgreich",
                           "Die Daten wurden erfolgreich gespeichert!", 10000, "info")
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
        # Laptop pruefen
        lnr = laptopnummer_entry.get().strip()
        if not lnr:
            show_timed_message(window, "Fehler",
                               "Bitte Laptopnummer eingeben!", 5000, "error")
            return
        laptop_data = get_laptop(lnr)
        if not laptop_data:
            show_timed_message(window, "Fehler",
                               f"Kein Laptop mit Nummer {lnr} gefunden!", 5000, "error")
            return
        laptopId = laptop_data[0][0]

        # Pruefen ob Laptop ueberhaupt ausgeliehen ist
        offene_ausleihe = db_query(
            'SELECT * FROM ausleihen WHERE laptopId = ? AND datum_zurueck IS NULL',
            (laptopId,))
        if not offene_ausleihe:
            show_timed_message(window, "Fehler",
                               f"Laptop {lnr} ist nicht ausgeliehen!", 5000, "error")
            return

        # Lagerplatz pruefen
        lp = lagerplatz_entry.get().strip()
        if not lp:
            show_timed_message(window, "Fehler",
                               "Bitte Lagerplatz eingeben!", 5000, "error")
            return
        lagerplatz_data = get_lagerplatz(lp)
        if not lagerplatz_data:
            show_timed_message(window, "Fehler",
                               f"Lagerplatz {lp} existiert nicht!", 5000, "error")
            return
        lagerplatzId = lagerplatz_data[0][0]

        datum = datum_entry.get()
        uhrzeit = datetime.now().strftime("%H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''UPDATE ausleihen SET datum_zurueck = ?, uhrzeit_zurueck = ? 
                  WHERE laptopId = ? AND datum_zurueck IS NULL AND uhrzeit_zurueck IS NULL''',
               (datum, uhrzeit, laptopId))
        cursor.execute('''INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId)
                          VALUES (?, ?)''', (lagerplatzId, laptopId))
        conn.commit()
        conn.close()

        show_timed_message(window, "Erfolgreich",
                           "Die Daten wurden erfolgreich abgegeben!", 5000, "info")
        window.destroy()

    add_button(window, "Abgeben", abgeben_speichern, 5)


# ==================== Fenster: Laptop hinzufuegen ====================

def open_laptop_hinzufuegen():
    if not passwort_pruefen():
        return

    window = create_form_window("Laptop hinzufuegen")

    laptopnummer_entry = add_field(window, "Laptopnummer:", 1, focus=True)
    beschreibung_entry = add_field(window, "Beschreibung:", 2)
    lagerplatz_entry   = add_field(window, "Lagerplatz:", 3)

    def lap_hinzufuegen_speichern():
        laptopnummer = laptopnummer_entry.get()
        beschreibung = beschreibung_entry.get()
        lagerplatz_data = get_lagerplatz(lagerplatz_entry.get())
        lagerplatzId = lagerplatz_data[0][0]

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

        show_timed_message(root, "Erfolgreich",
                           "Der Laptop wurde erfolgreich hinzugefuegt!", 3000, "info")
        window.destroy()

    add_button(window, "Hinzufuegen", lap_hinzufuegen_speichern, 4)


# ==================== Fenster: Lagerplatz hinzufuegen ====================

def open_lager_hinzufuegen():
    if not passwort_pruefen():
        return

    window = create_form_window("Lagerplatz hinzufuegen")

    lagerplatznummer_entry = add_field(window, "Lagerplatznummer:", 1, focus=True)

    def lag_hinzufuegen_speichern():
        lagerplatznummer = lagerplatznummer_entry.get()
        db_query('INSERT INTO lagerplatz (lagerplatz) VALUES (?)',
                 (lagerplatznummer,), fetch=False, commit=True)

        show_timed_message(root, "Erfolgreich",
                           "Der Lagerplatz wurde erfolgreich hinzugefuegt!", 3000, "info")
        window.destroy()

    add_button(window, "Hinzufuegen", lag_hinzufuegen_speichern, 2)


# ==================== Fenster: Person hinzufuegen ====================

def open_person_hinzufuegen():
    window = create_form_window("Person hinzufuegen")

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
        show_timed_message(root, "Erfolgreich",
                           "Die Person wurde erfolgreich hinzugefuegt!", 3000, "info")
        pruefe_inaktive_azubis()

    add_button(window, "Hinzufuegen", person_hinzufuegen_speichern, 3)


# ==================== Fenster: Bestand anzeigen ====================

def open_laptop_status():
    new_window = tk.Toplevel(root)
    new_window.title("Bestand")
    new_window.configure(bg=COLORS["bg"])
    new_window.attributes('-zoomed', True)

    laptop_status_data = get_laptop_status()

    # Trenne in vorrätige und ausgeliehene Laptops
    vorr = sorted([x for x in laptop_status_data if x[4] is not None],
                  key=lambda x: str(x[2] or ''))
    ausg = sorted([x for x in laptop_status_data if x[4] is None],
                  key=lambda x: str(x[2] or ''))

    # Topbar
    topbar = ttk.Frame(new_window, style="Topbar.TFrame")
    topbar.pack(fill=tk.X)
    ttk.Label(topbar, text="IT-Servicepoint", style="Topbar.TLabel").pack(
        anchor="w", padx=16, pady=8)

    sep = tk.Frame(new_window, bg=COLORS["border"], height=1)
    sep.pack(fill=tk.X)

    # Titel
    ttk.Label(new_window, text="Aktueller Bestand", style="Heading.TLabel").pack(
        pady=(20, 16))

    # Stat-Kacheln
    stats_frame = ttk.Frame(new_window)
    stats_frame.pack(fill=tk.X, padx=24, pady=(0, 16))
    stats_frame.columnconfigure(0, weight=1)
    stats_frame.columnconfigure(1, weight=1)

    green_stat = ttk.Frame(stats_frame, style="GreenStat.TFrame", padding=16)
    green_stat.grid(row=0, column=0, sticky="ew", padx=(0, 8))
    ttk.Label(green_stat, text="VORRÄTIG", style="GreenStatTitle.TLabel").pack(anchor="w")
    ttk.Label(green_stat, text=str(len(vorr)), style="GreenStatNum.TLabel").pack(anchor="w")

    red_stat = ttk.Frame(stats_frame, style="RedStat.TFrame", padding=16)
    red_stat.grid(row=0, column=1, sticky="ew", padx=(8, 0))
    ttk.Label(red_stat, text="AUSGELIEHEN", style="RedStatTitle.TLabel").pack(anchor="w")
    ttk.Label(red_stat, text=str(len(ausg)), style="RedStatNum.TLabel").pack(anchor="w")

    # Zwei-Spalten-Layout fuer die Listen
    lists_frame = ttk.Frame(new_window)
    lists_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))
    lists_frame.columnconfigure(0, weight=1)
    lists_frame.columnconfigure(1, weight=1)

    # --- Linke Seite: Vorrätig (Treeview) ---
    left_frame = ttk.Frame(lists_frame)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
    left_frame.rowconfigure(1, weight=1)
    left_frame.columnconfigure(0, weight=1)

    ttk.Label(left_frame, text=f"Vorrätig ({len(vorr)})",
              foreground=COLORS["green_text"], font=FONT_HEAD,
              background=COLORS["bg"]).grid(row=0, column=0, sticky="w", pady=(0, 8))

    tree_left = ttk.Treeview(left_frame, columns=("laptop", "lagerplatz"),
                             show="headings", height=20)
    tree_left.heading("laptop", text="Laptop", anchor="w")
    tree_left.heading("lagerplatz", text="Lagerplatz", anchor="w")
    tree_left.column("laptop", width=200, anchor="w")
    tree_left.column("lagerplatz", width=100, anchor="w")

    for item in vorr:
        tree_left.insert("", "end", values=(item[2] or "", item[4] or ""))

    tree_left.grid(row=1, column=0, sticky="nsew")

    scroll_left = ttk.Scrollbar(left_frame, orient="vertical", command=tree_left.yview)
    scroll_left.grid(row=1, column=1, sticky="ns")
    tree_left.configure(yscrollcommand=scroll_left.set)

    # --- Rechte Seite: Ausgeliehen (Treeview) ---
    right_frame = ttk.Frame(lists_frame)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
    right_frame.rowconfigure(1, weight=1)
    right_frame.columnconfigure(0, weight=1)

    ttk.Label(right_frame, text=f"Ausgeliehen ({len(ausg)})",
              foreground=COLORS["red_text"], font=FONT_HEAD,
              background=COLORS["bg"]).grid(row=0, column=0, sticky="w", pady=(0, 8))

    tree_right = ttk.Treeview(right_frame, columns=("laptop", "person"),
                              show="headings", height=20)
    tree_right.heading("laptop", text="Laptop", anchor="w")
    tree_right.heading("person", text="Ausgeliehen an", anchor="w")
    tree_right.column("laptop", width=200, anchor="w")
    tree_right.column("person", width=200, anchor="w")

    for item in ausg:
        name = f"{item[5] or ''} {item[6] or ''}".strip()
        tree_right.insert("", "end", values=(item[2] or "", name))

    tree_right.grid(row=1, column=0, sticky="nsew")

    scroll_right = ttk.Scrollbar(right_frame, orient="vertical", command=tree_right.yview)
    scroll_right.grid(row=1, column=1, sticky="ns")
    tree_right.configure(yscrollcommand=scroll_right.set)


# ==================== Hauptfenster ====================

root = tk.Tk()
root.title("IT-Servicepoint")
root.configure(bg=COLORS["bg"])
root.geometry("460x520")
root.resizable(False, False)

setup_styles()

# Topbar
topbar = ttk.Frame(root, style="Topbar.TFrame")
topbar.pack(fill=tk.X)
ttk.Label(topbar, text="IT-Servicepoint", style="Topbar.TLabel").pack(
    anchor="w", padx=16, pady=8)

# Separator
sep = tk.Frame(root, bg=COLORS["border"], height=1)
sep.pack(fill=tk.X)

# Titel zentriert
ttk.Label(root, text="Laptopverwaltung", style="Title.TLabel").pack(pady=(28, 24))

# Button-Definitionen
MENU_ITEMS = [
    ("Ausleihen",              open_ausleihen,           "Primary.TButton"),
    ("Abgeben",                open_abgeben,             "Success.TButton"),
    ("Neue Person",            open_person_hinzufuegen,  "Secondary.TButton"),
    ("Neuer Laptop",           open_laptop_hinzufuegen,  "Secondary.TButton"),
    ("Neuer Lagerplatz",       open_lager_hinzufuegen,   "Secondary.TButton"),
    ("Aktueller Bestand",      open_laptop_status,       "Secondary.TButton"),
]

# Buttons im 2er-Grid
btn_frame = ttk.Frame(root)
btn_frame.pack(padx=24, fill=tk.X)
btn_frame.columnconfigure(0, weight=1)
btn_frame.columnconfigure(1, weight=1)

for i, (text, command, style) in enumerate(MENU_ITEMS):
    row = i // 2
    col = i % 2
    btn = ttk.Button(btn_frame, text=text, command=command, style=style)
    btn.grid(row=row, column=col, padx=4, pady=4, sticky="ew")

root.mainloop()
