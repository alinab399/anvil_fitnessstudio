import sqlite3
import random
from datetime import datetime, timedelta


def setup_fitness_db():
    conn = sqlite3.connect('fitness_studio.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Tabellen löschen für sauberen Neustart
    cursor.execute('DROP TABLE IF EXISTS besucht')
    cursor.execute('DROP TABLE IF EXISTS Kurs')
    cursor.execute('DROP TABLE IF EXISTS Trainer')
    cursor.execute('DROP TABLE IF EXISTS Mitglied')
    cursor.execute('DROP TABLE IF EXISTS Studio')

    # Tabellen erstellen (Keine Trainingsgeräte!)
    cursor.execute('CREATE TABLE Studio (Studionr INTEGER PRIMARY KEY, Name TEXT NOT NULL, Adresse TEXT)')

    cursor.execute('''CREATE TABLE Trainer
                      (
                          Personalnr      INTEGER PRIMARY KEY,
                          Name            TEXT NOT NULL,
                          Spezialisierung TEXT,
                          Studionr        INTEGER,
                          FOREIGN KEY (Studionr) REFERENCES Studio (Studionr)
                      )''')

    cursor.execute('''CREATE TABLE Kurs
                      (
                          KursId      INTEGER PRIMARY KEY,
                          Bezeichnung TEXT NOT NULL,
                          Dauer       TEXT,
                          Personalnr  INTEGER,
                          FOREIGN KEY (Personalnr) REFERENCES Trainer (Personalnr)
                      )''')

    cursor.execute('''CREATE TABLE Mitglied
                      (
                          MitgliedId     INTEGER PRIMARY KEY,
                          Name           TEXT NOT NULL,
                          Eintrittsdatum DATE,
                          Studionr       INTEGER,
                          FOREIGN KEY (Studionr) REFERENCES Studio (Studionr)
                      )''')

    cursor.execute('''CREATE TABLE besucht
                      (
                          ID             INTEGER PRIMARY KEY AUTOINCREMENT,
                          Teilnahmedatum DATE,
                          MitgliedId     INTEGER,
                          KursId         INTEGER,
                          FOREIGN KEY (MitgliedId) REFERENCES Mitglied (MitgliedId),
                          FOREIGN KEY (KursId) REFERENCES Kurs (KursId)
                      )''')

    # --- Daten-Generierung ---
    studios = [(1, 'Fit-O-Mat City', 'Hauptstraße 1, Berlin'), (2, 'Power Gym Nord', 'Alsterweg 5, Hamburg'),
               (3, 'Eisen-Biege', 'Ringstraße 12, München'), (4, 'Wellness Oase', 'Parkallee 3, Köln'),
               (5, 'The Box', 'Hafenstraße 8, Bremen')]

    kurs_typen = ["Morning Yoga", "Bauch-Beine-Po", "HIIT Blast", "Heavy Lifting", "Rückenschule", "Zumba", "Spinning"]
    vornamen = ["Max", "Erika", "John", "Sarah", "Kevin", "Elena", "Markus", "Laura"]
    nachnamen = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer"]

    trainer_data, kurs_data = [], []
    t_id_counter, k_id_counter = 501, 201

    for s_id, _, _ in studios:
        for _ in range(10):
            t_name = f"{random.choice(vornamen)} {random.choice(nachnamen)}"
            t_spez = random.choice(kurs_typen)
            trainer_data.append((t_id_counter, t_name, t_spez, s_id))
            kurs_data.append((k_id_counter, t_spez, f"{random.choice([30, 45, 60, 90])} Min", t_id_counter))
            t_id_counter += 1
            k_id_counter += 1

    mitglieder_data = []
    for m_id in range(1001, 1501):
        eintritt = (datetime.now() - timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d')
        mitglieder_data.append(
            (m_id, f"{random.choice(vornamen)} {random.choice(nachnamen)}", eintritt, random.randint(1, 5)))

    cursor.executemany('INSERT INTO Studio VALUES (?,?,?)', studios)
    cursor.executemany('INSERT INTO Trainer VALUES (?,?,?,?)', trainer_data)
    cursor.executemany('INSERT INTO Kurs VALUES (?,?,?,?)', kurs_data)
    cursor.executemany('INSERT INTO Mitglied VALUES (?,?,?,?)', mitglieder_data)

    besuche_data = []
    for _ in range(5000):
        besuch_datum = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 400))).strftime('%Y-%m-%d')
        besuche_data.append((besuch_datum, random.randint(1001, 1500), random.randint(201, k_id_counter - 1)))

    cursor.executemany('INSERT INTO besucht (Teilnahmedatum, MitgliedId, KursId) VALUES (?,?,?)', besuche_data)
    conn.commit()
    conn.close()
    print("Datenbank erfolgreich erstellt.")


if __name__ == "__main__":
    setup_fitness_db()