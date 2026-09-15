import os
import requests
import json
import re

ARKESEL_KEY = "anNXeFZuZUdlRmtnemZPY3NvVUY"
SENDER_ID = "UGDS"
SEND_URL = "https://sms.arkesel.com/api/v2/sms/send"
BALANCE_URL = "https://sms.arkesel.com/api/v2/clients/balance-details"

celebrants = [
    {"name": "Dora Dickson", "phone": "0541111144", "folder": "K/13 4422"},
    {"name": "Dina Asiedu Nyanteh", "phone": "0242828068", "folder": "K/13 4543"},
    {"name": "Veronica Mensah", "phone": "0244101637", "folder": "K/13 5098"},
    {"name": "Turkson Amissah", "phone": "0244839467", "folder": "K/13 4951"},
    {"name": "Hannah Akpabli", "phone": "0242871184", "folder": "K/13 2031"},
    {"name": "Dankyi Berko", "phone": "0249975948", "folder": "K/13 4131"},
]

def format_phone(p):
    p = re.sub(r'\D', '', p)
    if p.startswith('0') and len(p) == 10:
        return '233' + p[1:]
    if p.startswith('233') and len(p) == 12:
        return p
    return p

print("=== Checking Arkesel Balance ===")
headers = {"api-key": ARKESEL_KEY}
try:
    bal_res = requests.get(BALANCE_URL, headers=headers, timeout=10)
    print("Balance response:", bal_res.status_code, bal_res.text)
except Exception as e:
    print("Error fetching balance:", e)

print("\n=== Sending Birthday SMS to Today's Celebrants ===")
template = (
    "Happy Birthday {name}! 🎂 Best wishes from all of us at the University of Ghana Dental School, Korle Bu. "
    "May your new year bring you good health, happiness, and glowing smiles. Have a blessed and memorable celebration!"
)

for person in celebrants:
    recipient = format_phone(person["phone"])
    msg = template.format(name=person["name"])
    payload = {
        "sender": SENDER_ID,
        "message": msg,
        "recipients": [recipient]
    }
    print(f"\nDispatching to {person['name']} ({recipient})...")
    try:
        resp = requests.post(SEND_URL, json=payload, headers={"api-key": ARKESEL_KEY, "Content-Type": "application/json"}, timeout=15)
        print(f"Status: {resp.status_code} | Response: {resp.text}")
    except Exception as e:
        print(f"Error sending to {person['name']}: {e}")
