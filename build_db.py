import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hades.db")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE prisoners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    crime TEXT NOT NULL,
    sentence TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE guards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rank TEXT NOT NULL,
    access_code TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

prisoners = [
    ("Sisyphus", "Deceiving Thanatos", "Eternal boulder labor"),
    ("Tantalus", "Serving the gods his own son", "Eternal hunger and thirst"),
    ("Ixion", "Attempted violation of Hera", "Bound to a burning wheel"),
    ("Prometheus", "Theft of fire", "Daily liver consumption"),
    ("Tityos", "Assault on Leto", "Liver devoured by vultures"),
]
cur.executemany("INSERT INTO prisoners (name, crime, sentence) VALUES (?, ?, ?)", prisoners)

guards = [
    ("Charon", "Ferryman", "STYX-0441-FERRY"),
    ("Cerberus Watch Captain", "Gatekeeper", "GATE-7782-TRIP"),
    ("Hecate's Warden", "Night Overseer", "NOCT-1190-KEY"),
]
cur.executemany("INSERT INTO guards (name, rank, access_code) VALUES (?, ?, ?)", guards)

staff = [
    ("Hades", "hades", "P0m3granate!Rule"),
    ("Persephone", "persephone", "SixSeeds_Spring22"),
    ("Thanatos", "thanatos", "Harvest0fSouls"),
    ("Hypnos", "hypnos", "SlumberGate#9"),
    ("Minos", "minos", "JudgeTheDead_01"),
]
cur.executemany("INSERT INTO staff (name, username, password) VALUES (?, ?, ?)", staff)

conn.commit()
conn.close()
print(f"Built {DB_PATH}")
