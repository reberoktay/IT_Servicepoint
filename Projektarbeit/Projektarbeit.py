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
FONT_TITLE = ("Segoe UI", 28)
FONT_HEAD  = ("Segoe UI", 14, "bold")
FONT_BTN   = ("Segoe UI", 13)
FONT_BTN_MAIN = ("Segoe UI", 18)


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

    # Grosse Buttons fuer Hauptfenster (farblos, blau bei Hover)
    style.configure("MainButton.TButton", background=COLORS["bg_card"],
                    foreground=COLORS["text"], font=FONT_BTN_MAIN, padding=(24, 28),
                    borderwidth=1, relief="solid")
    style.map("MainButton.TButton",
              background=[("active", COLORS["accent_blue"])],
              foreground=[("active", "white")])

    # Akzent-Buttons fuer die Haupt-Aktionen der Azubis: Ausleihen (gruen) und Abgeben (blau)
    # Permanent gefuellt, Hover wird minimal heller
    style.configure("MainGreen.TButton", background=COLORS["accent_green"],
                    foreground="white", font=FONT_BTN_MAIN, padding=(24, 28),
                    borderwidth=0, relief="flat",
                    lightcolor=COLORS["accent_green"],
                    darkcolor=COLORS["accent_green"],
                    bordercolor=COLORS["accent_green"])
    style.map("MainGreen.TButton",
              background=[("active", "#22c55e"), ("pressed", "#15803d")],
              foreground=[("active", "white")])

    style.configure("MainBlue.TButton", background=COLORS["accent_blue"],
                    foreground="white", font=FONT_BTN_MAIN, padding=(24, 28),
                    borderwidth=0, relief="flat",
                    lightcolor=COLORS["accent_blue"],
                    darkcolor=COLORS["accent_blue"],
                    bordercolor=COLORS["accent_blue"])
    style.map("MainBlue.TButton",
              background=[("active", "#3b82f6"), ("pressed", "#1e40af")],
              foreground=[("active", "white")])

    style.configure("Form.TButton", background=COLORS["accent_blue"],
                    foreground="white", font=FONT_BTN, padding=(20, 10))
    style.map("Form.TButton",
              background=[("active", "#1d4ed8"), ("pressed", "#1e40af")])

    # Close Button (X oben rechts)
    style.configure("Close.TButton", background=COLORS["bg_topbar"],
                    foreground=COLORS["text_muted"], font=("Segoe UI", 14),
                    padding=(8, 2), borderwidth=0, relief="flat")
    style.map("Close.TButton",
              foreground=[("active", COLORS["red_text"])],
              background=[("active", COLORS["bg_topbar"])])

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
    """Zeigt eine Meldung die sich nach timeout (ms) automatisch schliesst.
    Popup ist zentriert auf dem Bildschirm und deutlich groesser als Standard."""
    popup = tk.Toplevel(parent)
    popup.title(title)
    popup.configure(bg=COLORS["bg"])
    popup.resizable(False, False)

    # Feste Groesse + auf dem Bildschirm zentrieren
    popup_width  = 600
    popup_height = 240
    # update_idletasks() damit winfo_screenwidth korrekte Werte liefert
    popup.update_idletasks()
    screen_w = popup.winfo_screenwidth()
    screen_h = popup.winfo_screenheight()
    x = (screen_w - popup_width) // 2
    y = (screen_h - popup_height) // 2
    popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    # Immer im Vordergrund anzeigen (auch gegen Fullscreen-Parent)
    popup.attributes('-topmost', True)
    popup.transient(parent)
    popup.lift()
    popup.focus_force()
    # Nach kurzer Verzoegerung nochmal nach oben ziehen - manche
    # Window-Manager (v.a. auf dem Pi) ueberschreiben sonst das topmost-Flag
    popup.after(50, lambda: (popup.lift(), popup.focus_force()))

    type_colors = {
        "info":    (COLORS["success_bg"], COLORS["success_fg"]),
        "error":   (COLORS["error_bg"],   COLORS["error_fg"]),
        "warning": (COLORS["warning_bg"], COLORS["warning_fg"]),
    }
    bg_color, fg_color = type_colors.get(msg_type, (COLORS["bg_card"], COLORS["text"]))

    frame = tk.Frame(popup, bg=bg_color, padx=32, pady=24)
    frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

    # Groessere Schrift fuer bessere Lesbarkeit aus der Ferne
    msg_font = ("Segoe UI", 16)
    tk.Label(frame, text=message, font=msg_font, bg=bg_color, fg=fg_color,
             wraplength=500, justify="center").pack(pady=(8, 20), expand=True)

    ok_btn = ttk.Button(frame, text="OK", command=popup.destroy, style="Form.TButton")
    ok_btn.pack()

    def safe_destroy():
        try:
            if popup.winfo_exists():
                popup.destroy()
        except:
            pass

    popup.after(timeout, safe_destroy)


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
    """Erstellt ein neues Toplevel-Fenster im Dark Theme. Zentriert auf dem Bildschirm."""
    window = tk.Toplevel(root)
    window.title(title)
    window.configure(bg=COLORS["bg"])
    window.resizable(False, False)

    # Im Singleton-Tracker registrieren
    _register_window(title, window)

    # Topbar
    topbar = ttk.Frame(window, style="Topbar.TFrame")
    topbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
    topbar.columnconfigure(0, weight=1)
    ttk.Label(topbar, text="IT-Servicepoint", style="Topbar.TLabel").grid(
        row=0, column=0, sticky="w", padx=16, pady=8)
    ttk.Button(topbar, text="\u2715", style="Close.TButton",
               command=window.destroy).grid(row=0, column=1, sticky="e", padx=(0, 8), pady=4)

    # Separator
    sep = tk.Frame(window, bg=COLORS["border"], height=1)
    sep.grid(row=1, column=0, columnspan=2, sticky="ew")

    # Titel
    ttk.Label(window, text=title, style="Heading.TLabel").grid(
        row=2, column=0, columnspan=2, pady=(20, 16), padx=24)

    # Fenster auf dem Bildschirm zentrieren - nach dem Layout aller Widgets
    def center_window():
        window.update_idletasks()
        w = window.winfo_reqwidth()   # reqwidth = was die Widgets wirklich brauchen
        h = window.winfo_reqheight()
        # Mindestbreite fuer mehr Luft in den Formularen
        if w < 500:
            w = 500
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        window.geometry(f"{w}x{h}+{x}+{y}")

    # Deutlich warten, damit alle Felder und Buttons vom Aufrufer schon da sind.
    # after_idle war zu frueh und hat das Fenster auf die Topbar-Hoehe fixiert.
    window.after(100, center_window)

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


def make_scan_only(entry, max_gap_ms=50):
    """Macht ein Entry-Feld zu einem Nur-Scan-Feld.

    Ein Barcode-Scanner 'tippt' Zeichen in unter 30ms Abstand, ein Mensch
    braucht >100ms pro Taste. Wir akzeptieren nur Eingaben, bei denen
    aufeinanderfolgende Zeichen weniger als max_gap_ms auseinanderliegen.
    Paste wird komplett blockiert.
    """
    state = {"last_time": 0, "scanning": False}

    def on_key(event):
        # Steuertasten (Tab, Enter, Backspace zum Loeschen, Pfeile etc.) erlauben
        if event.keysym in ("Tab", "Return", "BackSpace", "Delete",
                            "Left", "Right", "Home", "End"):
            return None

        # Nur druckbare Zeichen pruefen
        if not event.char or not event.char.isprintable():
            return None

        now = int(time.time() * 1000)
        gap = now - state["last_time"]

        if state["last_time"] == 0:
            # Erstes Zeichen - Timer starten, zulassen
            state["last_time"] = now
            state["scanning"] = True
            # Nach max_gap_ms * 3 ohne weiteres Zeichen -> Feld wurde "fertig gescannt"
            entry.after(max_gap_ms * 3, lambda: state.update({"last_time": 0, "scanning": False}))
            return None

        if gap > max_gap_ms:
            # Zu langsam - das ist eine Tastatureingabe, blockieren
            return "break"

        state["last_time"] = now
        return None

    def on_paste(event):
        # Paste komplett blockieren
        return "break"

    entry.bind("<KeyPress>", on_key)
    entry.bind("<<Paste>>", on_paste)
    entry.bind("<Control-v>", on_paste)
    entry.bind("<Control-V>", on_paste)
    entry.bind("<Button-3>", lambda e: "break")  # Rechtsklick-Menue blockieren


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


def get_ladekabel_fuer_laptop(laptopId):
    """Gibt das Ladekabel zurueck, das einem Laptop zugeordnet ist, oder None."""
    result = db_query('SELECT * FROM ladekabel WHERE laptopId = ?', (laptopId,))
    return result[0] if result else None

def get_ladekabel_by_nummer(ladekabelnummer):
    """Gibt das Ladekabel anhand seiner Nummer zurueck, oder None."""
    result = db_query('SELECT * FROM ladekabel WHERE ladekabelnummer = ?',
                      (ladekabelnummer,))
    return result[0] if result else None


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
    ladekabel_entry    = add_field(window, "Ladekabel (scannen):", 4)
    make_scan_only(ladekabel_entry)
    datum_entry        = add_field(window, "Datum:", 5, default=today)
    uhrzeit_entry      = add_uhrzeit_field(window, 6)

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

    # Wenn Laptopnummer eingegeben wird: pruefen ob Ladekabel vorhanden ist
    def laptopnummer_focusout(event):
        lnr = laptopnummer_entry.get().strip()
        ladekabel_entry.configure(state='normal')
        ladekabel_entry.delete(0, END)
        if not lnr:
            return
        laptop_data = get_laptop(lnr)
        if not laptop_data:
            return  # Laptop existiert nicht - wird beim Senden abgefangen
        laptopId = laptop_data[0][0]
        erwartetes = get_ladekabel_fuer_laptop(laptopId)
        if erwartetes is None:
            # Laptop hat kein Ladekabel -> Feld sperren und Hinweis anzeigen
            ladekabel_entry.insert(0, "nicht vorhanden")
            ladekabel_entry.configure(state='readonly')

    laptopnummer_entry.bind("<FocusOut>", laptopnummer_focusout)

    # Wenn vollstaendig gescannt wurde: Scanner-Nummer durch Laptopnummer ersetzen.
    # Der echte Wert wird in einer Variable gemerkt und spaeter beim Speichern geprueft.
    scan_state = {"echte_nummer": None}

    def ladekabel_key(event):
        # Scan endet mit Tab oder Enter (Scanner-Suffix)
        if event.keysym not in ("Tab", "Return"):
            return
        # Nicht triggern, wenn Feld auf readonly steht ("nicht vorhanden"-Fall)
        if str(ladekabel_entry.cget('state')) == 'readonly':
            return
        lnr = laptopnummer_entry.get().strip()
        if not lnr:
            return
        gescannt = ladekabel_entry.get().strip()
        if not gescannt or gescannt == lnr:
            return
        # Echte Scanner-Nummer fuer spaeteren Vergleich merken
        scan_state["echte_nummer"] = gescannt
        # Feld-Anzeige durch Laptopnummer ersetzen
        ladekabel_entry.delete(0, END)
        ladekabel_entry.insert(0, lnr)

    ladekabel_entry.bind("<KeyPress>", ladekabel_key, add="+")

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

        # Ladekabel pruefen
        erwartetes_ladekabel = get_ladekabel_fuer_laptop(laptopId)
        if erwartetes_ladekabel is not None:
            # Laptop hat ein Ladekabel hinterlegt -> Scan ist Pflicht
            # Die echte gescannte Nummer wurde vom ladekabel_key-Handler abgefangen.
            echte_nummer = scan_state["echte_nummer"]
            if not echte_nummer:
                show_timed_message(window, "Fehler",
                                   "Bitte Ladekabel scannen!", 5000, "error")
                return
            if str(erwartetes_ladekabel[1]) != echte_nummer:
                show_timed_message(window, "Fehler",
                                   f"Falsches Ladekabel fuer Laptop {lnr}!",
                                   5000, "error")
                return
        else:
            # Altbestand: Laptop hat (noch) kein Ladekabel im System -> Warnung, aber durchlassen
            show_timed_message(window, "Hinweis",
                               f"Fuer Laptop {lnr} ist kein Ladekabel hinterlegt (Altbestand).",
                               4000, "warning")

        datum = datum_entry.get()
        uhrzeit = datetime.now().strftime("%H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO ausleihen (personenId, laptopId, datum_ausleih, uhrzeit_ausleih)
                          VALUES (?, ?, ?, ?)''', (personId, laptopId, datum, uhrzeit))
        cursor.execute('DELETE FROM laptop_lagerplatz WHERE laptopId = ?', (laptopId,))
        conn.commit()
        conn.close()

        window.destroy()
        show_timed_message(root, "Erfolgreich",
                           "Die Daten wurden erfolgreich gespeichert!", 10000, "info")

    add_button(window, "Senden", ausleihen_speichern, 7)


# ==================== Fenster: Abgeben ====================

def open_abgeben():
    window = create_form_window("Abgeben")
    today = datetime.today().strftime('%Y-%m-%d')

    laptopnummer_entry = add_field(window, "Laptopnummer:", 1, focus=True)
    ladekabel_entry    = add_field(window, "Ladekabel (scannen):", 2)
    make_scan_only(ladekabel_entry)
    lagerplatz_entry   = add_field(window, "Lagerplatz:", 3)
    datum_entry        = add_field(window, "Datum:", 4, default=today)
    uhrzeit_entry      = add_uhrzeit_field(window, 5)

    # Kopiere Laptopnummer automatisch in Lagerplatz + Ladekabel-Status aktualisieren
    def laptopnummer_changed(event):
        lnr = laptopnummer_entry.get().strip()
        lagerplatz_entry.delete(0, END)
        lagerplatz_entry.insert(0, lnr)

        # Ladekabel-Feld auf "nicht vorhanden" setzen falls kein Ladekabel hinterlegt
        ladekabel_entry.configure(state='normal')
        ladekabel_entry.delete(0, END)
        if not lnr:
            return
        laptop_data = get_laptop(lnr)
        if not laptop_data:
            return
        laptopId = laptop_data[0][0]
        erwartetes = get_ladekabel_fuer_laptop(laptopId)
        if erwartetes is None:
            ladekabel_entry.insert(0, "nicht vorhanden")
            ladekabel_entry.configure(state='readonly')

    laptopnummer_entry.bind("<FocusOut>", laptopnummer_changed)
    laptopnummer_entry.bind("<Return>", laptopnummer_changed)

    # Wie beim Ausleihen: echte Scanner-Nummer merken, Feld-Anzeige durch Laptopnummer ersetzen
    scan_state = {"echte_nummer": None}

    def ladekabel_key(event):
        if event.keysym not in ("Tab", "Return"):
            return
        # Nicht triggern, wenn Feld auf readonly steht ("nicht vorhanden"-Fall)
        if str(ladekabel_entry.cget('state')) == 'readonly':
            return
        lnr = laptopnummer_entry.get().strip()
        if not lnr:
            return
        gescannt = ladekabel_entry.get().strip()
        if not gescannt or gescannt == lnr:
            return
        scan_state["echte_nummer"] = gescannt
        ladekabel_entry.delete(0, END)
        ladekabel_entry.insert(0, lnr)

    ladekabel_entry.bind("<KeyPress>", ladekabel_key, add="+")

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

        # Ladekabel pruefen (selbe Logik wie beim Ausleihen)
        erwartetes_ladekabel = get_ladekabel_fuer_laptop(laptopId)
        if erwartetes_ladekabel is not None:
            echte_nummer = scan_state["echte_nummer"]
            if not echte_nummer:
                show_timed_message(window, "Fehler",
                                   "Bitte Ladekabel scannen!", 5000, "error")
                return
            if str(erwartetes_ladekabel[1]) != echte_nummer:
                show_timed_message(window, "Fehler",
                                   f"Falsches Ladekabel fuer Laptop {lnr}!",
                                   5000, "error")
                return
        else:
            show_timed_message(window, "Hinweis",
                               f"Fuer Laptop {lnr} ist kein Ladekabel hinterlegt (Altbestand).",
                               4000, "warning")

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

        window.destroy()
        show_timed_message(root, "Erfolgreich",
                           "Die Daten wurden erfolgreich abgegeben!", 5000, "info")

    add_button(window, "Abgeben", abgeben_speichern, 6)


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


# ==================== Fenster: Ladekabel hinzufuegen ====================

def open_ladekabel_hinzufuegen():
    if not passwort_pruefen():
        return

    window = create_form_window("Ladekabel hinzufuegen")

    laptopnummer_entry = add_field(window, "Laptopnummer:", 1, focus=True)
    ladekabel_entry    = add_field(window, "Ladekabel (scannen):", 2)
    make_scan_only(ladekabel_entry)

    def lade_hinzufuegen_speichern():
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

        # Pruefen ob Laptop schon ein Ladekabel hat
        if get_ladekabel_fuer_laptop(laptopId) is not None:
            show_timed_message(window, "Fehler",
                               f"Laptop {lnr} hat bereits ein Ladekabel zugeordnet!",
                               5000, "error")
            return

        # Ladekabel-Eingabe pruefen (muss gescannt sein)
        ladekabelnummer = ladekabel_entry.get().strip()
        if not ladekabelnummer:
            show_timed_message(window, "Fehler",
                               "Bitte Ladekabel scannen!", 5000, "error")
            return

        # Pruefen ob dieser Ladekabel-Barcode schon einem anderen Laptop zugewiesen ist
        if get_ladekabel_by_nummer(ladekabelnummer) is not None:
            show_timed_message(window, "Fehler",
                               "Dieses Ladekabel ist bereits einem Laptop zugewiesen!",
                               5000, "error")
            return

        db_query('INSERT INTO ladekabel (ladekabelnummer, laptopId) VALUES (?, ?)',
                 (ladekabelnummer, laptopId), fetch=False, commit=True)

        window.destroy()
        show_timed_message(root, "Erfolgreich",
                           f"Ladekabel wurde Laptop {lnr} zugewiesen!", 3000, "info")

    add_button(window, "Hinzufuegen", lade_hinzufuegen_speichern, 3)


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
        vorname = vorname_entry.get().strip()
        nachname = nachname_entry.get().strip()
        stammnummer = stammnummer_entry.get().strip()

        # Stammnummer validieren: genau 6 Ziffern
        if not stammnummer:
            show_timed_message(window, "Fehler",
                               "Bitte Stammnummer eingeben!", 5000, "error")
            return
        if not stammnummer.isdigit() or len(stammnummer) != 6:
            show_timed_message(window, "Fehler",
                               "Stammnummer muss genau 6 Ziffern haben (0-9)!", 5000, "error")
            return

        # Pruefen ob Stammnummer bereits existiert
        existing = get_person(stammnummer)
        if existing:
            show_timed_message(window, "Fehler",
                               f"Stammnummer {stammnummer} ist bereits vergeben!", 5000, "error")
            return

        if not nachname:
            show_timed_message(window, "Fehler",
                               "Bitte Nachname eingeben!", 5000, "error")
            return
        if not vorname:
            show_timed_message(window, "Fehler",
                               "Bitte Vorname eingeben!", 5000, "error")
            return

        db_query('INSERT INTO personen (nachname, vorname, stammnummer) VALUES (?, ?, ?)',
                 (nachname, vorname, stammnummer), fetch=False, commit=True)

        show_timed_message(root, "Erfolgreich",
                           "Die Person wurde erfolgreich hinzugefuegt!", 3000, "info")
        window.destroy()
        pruefe_inaktive_azubis()

    add_button(window, "Hinzufuegen", person_hinzufuegen_speichern, 3)


# ==================== Fenster: Bestand anzeigen ====================

def open_laptop_status():
    new_window = tk.Toplevel(root)
    new_window.title("Bestand")
    new_window.configure(bg=COLORS["bg"])
    try:
        new_window.attributes('-zoomed', True)
    except:
        pass
    new_window.attributes('-fullscreen', True)
    new_window.bind("<Escape>", lambda e: new_window.attributes('-fullscreen', False))

    # Im Singleton-Tracker registrieren
    _register_window("Bestand", new_window)

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
        side=tk.LEFT, padx=16, pady=8)
    ttk.Button(topbar, text="\u2715", style="Close.TButton",
               command=new_window.destroy).pack(side=tk.RIGHT, padx=(0, 12), pady=4)

    sep = tk.Frame(new_window, bg=COLORS["border"], height=1)
    sep.pack(fill=tk.X)

    # Titel
    ttk.Label(new_window, text="Aktueller Bestand", style="Heading.TLabel").pack(
        pady=(20, 16))

    # Stat-Kacheln
    stats_frame = ttk.Frame(new_window)
    stats_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
    stats_frame.columnconfigure(0, weight=1)
    stats_frame.columnconfigure(1, weight=1)

    green_stat = ttk.Frame(stats_frame, style="GreenStat.TFrame", padding=16)
    green_stat.grid(row=0, column=0, sticky="ew", padx=(0, 20))
    ttk.Label(green_stat, text="VORRÄTIG", style="GreenStatTitle.TLabel").pack(anchor="w")
    ttk.Label(green_stat, text=str(len(vorr)), style="GreenStatNum.TLabel").pack(anchor="w")

    red_stat = ttk.Frame(stats_frame, style="RedStat.TFrame", padding=16)
    red_stat.grid(row=0, column=1, sticky="ew", padx=(20, 0))
    ttk.Label(red_stat, text="AUSGELIEHEN", style="RedStatTitle.TLabel").pack(anchor="w")
    ttk.Label(red_stat, text=str(len(ausg)), style="RedStatNum.TLabel").pack(anchor="w")

    # Zwei-Spalten-Layout fuer die Listen
    lists_frame = ttk.Frame(new_window)
    lists_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 24))
    lists_frame.columnconfigure(0, weight=1, uniform="cols")
    lists_frame.columnconfigure(1, weight=1, uniform="cols")

    # --- Linke Seite: Vorrätig (Treeview) ---
    left_frame = ttk.Frame(lists_frame)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
    left_frame.rowconfigure(1, weight=1)
    left_frame.columnconfigure(0, weight=1)

    ttk.Label(left_frame, text=f"Vorrätig ({len(vorr)})",
              foreground=COLORS["green_text"], font=FONT_HEAD,
              background=COLORS["bg"]).grid(row=0, column=0, sticky="w", pady=(0, 8))

    tree_left = ttk.Treeview(left_frame, columns=("laptop", "lagerplatz"),
                             show="headings", height=20)
    tree_left.heading("laptop", text="Laptop", anchor="w")
    tree_left.heading("lagerplatz", text="Lagerplatz", anchor="w")
    tree_left.column("laptop", width=200, anchor="w", stretch=True)
    tree_left.column("lagerplatz", width=120, anchor="w", stretch=True)

    for item in vorr:
        tree_left.insert("", "end", values=(item[2] or "", item[4] or ""))

    tree_left.grid(row=1, column=0, sticky="nsew")

    scroll_left = ttk.Scrollbar(left_frame, orient="vertical", command=tree_left.yview)
    scroll_left.grid(row=1, column=1, sticky="ns")
    tree_left.configure(yscrollcommand=scroll_left.set)

    # --- Rechte Seite: Ausgeliehen (Treeview) ---
    right_frame = ttk.Frame(lists_frame)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
    right_frame.rowconfigure(1, weight=1)
    right_frame.columnconfigure(0, weight=1)

    ttk.Label(right_frame, text=f"Ausgeliehen ({len(ausg)})",
              foreground=COLORS["red_text"], font=FONT_HEAD,
              background=COLORS["bg"]).grid(row=0, column=0, sticky="w", pady=(0, 8))

    tree_right = ttk.Treeview(right_frame, columns=("laptop", "person"),
                              show="headings", height=20)
    tree_right.heading("laptop", text="Laptop", anchor="w")
    tree_right.heading("person", text="Ausgeliehen an", anchor="w")
    tree_right.column("laptop", width=150, anchor="w", stretch=True)
    tree_right.column("person", width=250, anchor="w", stretch=True)

    for item in ausg:
        name = f"{item[5] or ''} {item[6] or ''}".strip()
        tree_right.insert("", "end", values=(item[2] or "", name))

    tree_right.grid(row=1, column=0, sticky="nsew")

    scroll_right = ttk.Scrollbar(right_frame, orient="vertical", command=tree_right.yview)
    scroll_right.grid(row=1, column=1, sticky="ns")
    tree_right.configure(yscrollcommand=scroll_right.set)

    # Schliessen-Button unten - gross und deutlich sichtbar
    btn_frame = ttk.Frame(new_window)
    btn_frame.pack(fill=tk.X, padx=40, pady=(0, 24))
    ttk.Button(btn_frame, text="Schliessen", command=new_window.destroy,
               style="Form.TButton").pack(side=tk.RIGHT)


# ==================== Hauptfenster ====================

# Singleton-Tracker: verhindert mehrfaches Oeffnen desselben Fensters
_open_windows = {}

def open_singleton(name, open_func):
    """Oeffnet ein Fenster nur einmal. Bei erneutem Klick wird das bestehende hervorgehoben."""
    if name in _open_windows:
        win = _open_windows[name]
        try:
            if win.winfo_exists():
                win.lift()
                win.focus_force()
                return
        except:
            pass
        del _open_windows[name]
    open_func()

def _wrap_singleton(name, open_func):
    """Wrapped eine open_*-Funktion mit Singleton-Logik."""
    original = open_func

    def wrapper():
        if name in _open_windows:
            win = _open_windows[name]
            try:
                if win.winfo_exists():
                    win.lift()
                    win.focus_force()
                    return
            except:
                pass
            del _open_windows[name]
        original()

    return wrapper

def _register_window(name, window):
    """Registriert ein Fenster im Singleton-Tracker."""
    _open_windows[name] = window
    window.bind("<Destroy>", lambda e: _open_windows.pop(name, None) if e.widget == window else None)


root = tk.Tk()
root.title("IT-Servicepoint")
root.configure(bg=COLORS["bg"])

# Fullscreen: mehrere Methoden fuer maximale Kompatibilitaet (Pi + Desktop)
try:
    root.attributes('-zoomed', True)
except:
    pass
root.attributes('-fullscreen', True)

# Escape zum Beenden des Fullscreen (praktisch beim Entwickeln)
root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

setup_styles()

# Topbar
topbar = ttk.Frame(root, style="Topbar.TFrame")
topbar.pack(fill=tk.X)
ttk.Label(topbar, text="IT-Servicepoint", style="Topbar.TLabel").pack(
    side=tk.LEFT, padx=16, pady=8)
ttk.Button(topbar, text="\u2715", style="Close.TButton",
           command=root.destroy).pack(side=tk.RIGHT, padx=(0, 12), pady=4)

# Separator
sep = tk.Frame(root, bg=COLORS["border"], height=1)
sep.pack(fill=tk.X)

# Content zentriert (expand fuer vertikale Zentrierung)
content_frame = ttk.Frame(root)
content_frame.pack(expand=True, fill=tk.BOTH, padx=80, pady=40)


# ============================================================
# GRUPPE 1: Azubi-Funktionen (Ausleihen, Abgeben, Neue Person)
# ============================================================
azubi_frame = ttk.Frame(content_frame)
azubi_frame.pack(fill=tk.BOTH, expand=True)
azubi_frame.columnconfigure(0, weight=1)
azubi_frame.columnconfigure(1, weight=1)
azubi_frame.rowconfigure(0, weight=1)
azubi_frame.rowconfigure(1, weight=1)

ttk.Button(azubi_frame, text="Ausleihen",
           command=_wrap_singleton("Ausleihen", open_ausleihen),
           style="MainGreen.TButton").grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
ttk.Button(azubi_frame, text="Abgeben",
           command=_wrap_singleton("Abgeben", open_abgeben),
           style="MainBlue.TButton").grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
# Neue Person: volle Breite (ueber beide Spalten)
ttk.Button(azubi_frame, text="Neue Person",
           command=_wrap_singleton("Person hinzufuegen", open_person_hinzufuegen),
           style="MainButton.TButton").grid(row=1, column=0, columnspan=2,
                                            padx=0, pady=(10, 0), sticky="nsew")

# Visueller Trenner zwischen Azubi- und Admin-Bereich - subtil, viel Luft drumherum
separator = tk.Frame(content_frame, bg=COLORS["border"], height=1)
separator.pack(fill=tk.X, padx=120, pady=32)

# ============================================================
# GRUPPE 2: Admin-Funktionen (Laptop, Ladekabel, Lagerplatz, Bestand)
# ============================================================
admin_frame = ttk.Frame(content_frame)
admin_frame.pack(fill=tk.BOTH, expand=True)
admin_frame.columnconfigure(0, weight=1)
admin_frame.columnconfigure(1, weight=1)
admin_frame.rowconfigure(0, weight=1)
admin_frame.rowconfigure(1, weight=1)

ttk.Button(admin_frame, text="Neuer Laptop",
           command=_wrap_singleton("Laptop hinzufuegen", open_laptop_hinzufuegen),
           style="MainButton.TButton").grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
ttk.Button(admin_frame, text="Neues Ladekabel",
           command=_wrap_singleton("Ladekabel hinzufuegen", open_ladekabel_hinzufuegen),
           style="MainButton.TButton").grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
ttk.Button(admin_frame, text="Neuer Lagerplatz",
           command=_wrap_singleton("Lagerplatz hinzufuegen", open_lager_hinzufuegen),
           style="MainButton.TButton").grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")
ttk.Button(admin_frame, text="Aktueller Bestand",
           command=_wrap_singleton("Bestand", open_laptop_status),
           style="MainButton.TButton").grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")

root.mainloop()
