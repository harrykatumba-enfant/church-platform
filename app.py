import json
import os 
import flet as ft

# --- COLOR PALETTE DEFINITIONS ---
COLOR_BLUE = "#1A237E"       
COLOR_PURPLE = "#4A148C"
COLOR_GOLD = "#FFC107"
COLOR_GREEN = "#2ECC71"
COLOR_WHITE = "#FFFFFF"
COLOR_DARK_TEXT ="#212121"

#CREATING A DIRECTORY AND FILES USING JSON
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exits_ok=True)

FILES = {
    "prayer": os.path.join(DATA_DIR, "form_prayer.json"),
    "membership": os.path.join(DATA_DIR, "form_membership.json"),
    "volunteer": os.path.join(DATA_DIR, "form_volunteer.json"),
    "announcements": os.path.join(DATA_DIR, "form_announcements.json")
}

def load_json(key):
    path = FILES.get(key)
    if not path or not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_json(key, record):
    path = FILES.get(key)
    data = load_json(key)
    data.append(record)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, inden=4)

def main(page:ft.Page):
    page.title = "Miracles Church of God International"
    page.bgcolor = COLOR_WHITE
    page.padding = 0

    is_minister = False

    # --- NOTIFICATION --- 
    def notify(msg, bg_color=COLOR_GREEN, text_color=COLOR_WHITE):
        page.snack_bar = ft.SnackBar(
            ft.Text(msg, color=text_color, weight=ft.FontWeight.BOLD),       
            bgcolor=bg_color
        )
        page.snack_bar.open = True
        page.update()

    # --- LOGIN --- 
    username_input = ft.TextField(label="Username", width=260, border_color=COLOR_PURPLE)
    password_input = ft.TextField(label="Password", password=True, width=260, border_color=COLOR_PURPLE)

    def perform_login(e):
        nonlocal is_minister

        if username_input.vale == "minister" and password_input == "grace2026":
            is_minister = True
            login_dialog.open = False
            notify("Loggedin successfully as Minister!", COLOR_GREEN)
            rebuild_ui()
        else:
            notify("Invalid credentials!", COLOR_PURPLE)

    def perform_logout(e):
        nonlocal is_minister
        is_minister = False
        notify("Logged out", COLOR_BLUE)
        rebuild_ui()

    login_dialog = ft.AlertDialog(
        title=ft.Text("Minister Login Portal", color=COLOR_BLUE, weight=ft.FontWeight.BOLD),
        content = ft.Column([username_input, password_input], tight=True),
        actions = [
            ft.TextButton("Cancel", on_click=lambda e: setattr(login_dialog, "open", False) or page.update()),
            ft.Button("Login", bgcolor=COLOR_GREEN, color=COLOR_WHITE, on_click=perform_login),
        ],
    )

    def open_login(e):
        page.dialog = login_dialog
        login_dialog.open = True
        page.update()

    def submit_prayer(e):
        if not prayer_name.value or not prayer_req.value:
            notify("Please fill in the filelds", COLOR_PURPLE)
            return
        save_json("prayer", {"name" : prayer_name.value, "request": prayer_req.value})
        prayer_name.value = ""
        prayer_req.value = ""
        notify("Prayer request submitted successfully!", COLOR_GREEN)
        rebuild_ui()

    def submit_membership(e):
        if not mem_name.value or not mem_email.value or not mem_phone.value:
            notify("Please fill in the fields", COLOR_PURPLE)
            return
        save_json("membership", {"name": mem_name.value, "email": mem_email.value, "phone": mem_phone.value})
        mem_name.value = ""
        mem_email.value = ""
        mem_phone.value = ""
        notify("Membership application submitted!", COLOR_GREEN)
        rebuild_ui()

    def submit_volunteer(e):
        if not vol_name.value:
            notify("Please provide your name", COLOR_PURPLE)
            return
        save_json("volunteer", )
