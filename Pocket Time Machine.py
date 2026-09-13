
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

FILE = "time_capsules.json"

def load_capsules():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_capsules(capsules):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(capsules, f, indent=4)

def create_capsule():
    message = message_box.get("1.0", tk.END).strip()
    date = date_entry.get().strip()

    if not message:
        messagebox.showerror("Error", "Write a message first.")
        return

    try:
        unlock_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Invalid Date",
            "Please enter the date in YYYY-MM-DD format."
        )
        return

    if unlock_date.date() <= datetime.now().date():
        messagebox.showerror(
            "Invalid Date",
            "Choose a future date."
        )
        return

    capsules = load_capsules()

    capsules.append({
        "message": message,
        "unlock_date": date
    })

    save_capsules(capsules)

    message_box.delete("1.0", tk.END)
    date_entry.delete(0, tk.END)

    refresh_capsules()

    messagebox.showinfo(
        "Locked!",
        f"Your message is locked until {date}."
    )

def refresh_capsules():
    capsules_list.delete(0, tk.END)

    capsules = load_capsules()
    today = datetime.now().date()

    for i, capsule in enumerate(capsules):
        unlock_date = datetime.strptime(
            capsule["unlock_date"], "%Y-%m-%d"
        ).date()

        if today >= unlock_date:
            status = "🔓 READY TO OPEN"
        else:
            status = "🔒 LOCKED"

        capsules_list.insert(
            tk.END,
            f"{i + 1}. {status} — Opens: {capsule['unlock_date']}"
        )

def open_capsule():
    selection = capsules_list.curselection()

    if not selection:
        messagebox.showwarning(
            "Select a Capsule",
            "Choose a time capsule first."
        )
        return

    index = selection[0]
    capsules = load_capsules()
    capsule = capsules[index]

    unlock_date = datetime.strptime(
        capsule["unlock_date"], "%Y-%m-%d"
    ).date()

    if datetime.now().date() < unlock_date:
        remaining = (unlock_date - datetime.now().date()).days

        messagebox.showinfo(
            "Still Locked 🔒",
            f"This message is locked.\n\n"
            f"It will unlock on {capsule['unlock_date']}.\n"
            f"{remaining} day(s) remaining."
        )
        return

    messagebox.showinfo(
        "Your Message From The Past 💌",
        capsule["message"]
    )

# -----------------------------
# Pocket Time Machine UI
# -----------------------------

root = tk.Tk()
root.title("Pocket Time Machine ⏳")
root.geometry("650x600")
root.configure(bg="#101827")

title = tk.Label(
    root,
    text="⏳ Pocket Time Machine",
    font=("Arial", 26, "bold"),
    fg="#ffffff",
    bg="#101827"
)
title.pack(pady=(25, 5))

subtitle = tk.Label(
    root,
    text="Write something to your future self.",
    font=("Arial", 12),
    fg="#aab4c3",
    bg="#101827"
)
subtitle.pack(pady=(0, 20))

message_label = tk.Label(
    root,
    text="Your message",
    font=("Arial", 12, "bold"),
    fg="#ffffff",
    bg="#101827"
)
message_label.pack(anchor="w", padx=45)

message_box = tk.Text(
    root,
    height=10,
    width=65,
    font=("Arial", 11),
    bg="#1c2738",
    fg="#ffffff",
    insertbackground="white",
    relief="flat",
    padx=10,
    pady=10
)
message_box.pack(padx=45, pady=8)

date_label = tk.Label(
    root,
    text="Unlock date (YYYY-MM-DD)",
    font=("Arial", 12, "bold"),
    fg="#ffffff",
    bg="#101827"
)
date_label.pack(anchor="w", padx=45, pady=(10, 5))

date_entry = tk.Entry(
    root,
    font=("Arial", 12),
    width=25,
    bg="#1c2738",
    fg="#ffffff",
    insertbackground="white",
    relief="flat"
)
date_entry.pack(anchor="w", padx=45)

lock_button = tk.Button(
    root,
    text="🔒 Lock Message",
    command=create_capsule,
    font=("Arial", 12, "bold"),
    bg="#6c5ce7",
    fg="white",
    activebackground="#5848c7",
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)
lock_button.pack(pady=20)

list_label = tk.Label(
    root,
    text="Your Time Capsules",
    font=("Arial", 14, "bold"),
    fg="#ffffff",
    bg="#101827"
)
list_label.pack(anchor="w", padx=45)

capsules_list = tk.Listbox(
    root,
    height=7,
    width=65,
    font=("Arial", 10),
    bg="#1c2738",
    fg="#ffffff",
    selectbackground="#6c5ce7",
    relief="flat"
)
capsules_list.pack(padx=45, pady=8)

open_button = tk.Button(
    root,
    text="🔓 Open Selected Capsule",
    command=open_capsule,
    font=("Arial", 11, "bold"),
    bg="#00b894",
    fg="white",
    activebackground="#009b7d",
    activeforeground="white",
    relief="flat",
    padx=15,
    pady=8,
    cursor="hand2"
)
open_button.pack(pady=10)

refresh_capsules()

root.mainloop()
