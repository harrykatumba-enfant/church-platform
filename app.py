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
        save_json("volunteer", {"name": vol_name.value, "department": vol_dept.value})
        vol_name.value = ""
        notify("Volunteer Registration submitted!", COLOR_GREEN)
        rebuild_ui()

    def submit_contact(e):
        if not contact_name.value or not contact_email.value or not contact_msg.value:
            notify("Please complete all contact fields.", COLOR_PURPLE)
            return

        contact_name.value = ""
        contact_email.value = ""
        contact_msg.value = ""
        notify("Message sent directly to the pastoral team!", COLOR_BLUE)

    def submit_announcement(e):
        if not anc_title.value or not anc_content.value:
            notify("Please fill in both the title and content!", COLOR_PURPLE)
            return

        save_json("announcements", {"title": anc_title.value, "content": anc_content.value})
        anc_title.value = ""
        anc_content.value = ""
        notify("Announcement posted successfully!", COLOR_GREEN)
        rebuild_ui()

    # --- FORM INPUT --- 
    prayer_name = ft.TextField(label="Full Name", border_color=COLOR_BLUE)
    prayer_req = ft.TextField(label="Prayer Request", multiline=True, rows=3 border_color=COLOR_BLUE)

    mem_name = ft.TextField(label="Full Name", border_color=COLOR_BLUE)
    mem_email = ft.TextField(label="Email Address", border_color=COLOR_BLUE)
    mem_phone = ft.TextField(label="Phone Number", border_color=COLOR_BLUE)

    vol_name = ft.TextField(label="Full Name", border_color=COLOR_BLUE)
    vol_dept = ft.Dropdown(
        label="Department Choice", border_color=COLOR_BLUE,
        options = [
            ft.dropdown.Option("Ushering"),
            ft.dropdown.Option("Media & Tech"),
            ft.dropdown.Option("Worship Ministry"),
            ft.dropdown.Option("Children's Ministry")
        ],
        value="Ushering"
    )

    contact_name = ft.TextField(label="Your Name", border_color=COLOR_PURPLE)
    contact_email = ft.TextField(label="Your Email", border_color=COLOR_PURPLE)
    contact_msg = ft.TextField(label="Your Message", multiline=True, rows=4, border_color=COLOR_PURPLE)

    anc_title = ft.TextField(label="Announcement Title", border_color=COLOR_GOLD)
    anc_content = ft.TextField(label="Details", multiline=True, rows=4, border_color=COLOR_GOLD)

    # --- VIEWS --- 
    def get_home_view():
        tabs = ft.Tabs(
            selected_index=0,
            indicator_color=COLOR_GOLD,
            label_color=COLOR_PURPLE,
            unselected_label_color=COLOR_BLUE,
            tabs = [
                ft.Tab(
                    text="Prayer Request",
                    content = ft.Container(
                        content=ft.Column([
                            prayer_name, prayer_req,
                            ft.Button("Submit Prayer Request", bgcolor=COLOR_GREEN, color=COLOR_WHITE, on_click=submit_prayer)
                        ]),
                        padding=15
                    )
                ),
                ft.Tab(
                    text="Church Membership",
                    content=ft.Container(
                        content=ft.Column([
                            mem_name, mem_email, mem_phone,
                            ft.Button("Submit Application", bgcolor=COLOR_GREEN, color=COLOR_WHITE, on_click=submit_membership)
                        ]),
                        padding=15
                    )
                ),
                ft.Tab(
                    text="Volunteer Signup",
                    content=ft.Container(
                        content=ft.Column([
                            vol_name, vol_dept,
                            ft.Button("Sign Up to Serve", bgcolor=COLOR_GREEN, color=COLOR_WHITE, on_click=submit_volunteer)
                        ]),
                        padding=15
                    ),
                ),
            ],
            width=700
        )

        return ft.ListView([
            #Hero Banner
            ft.Container(
                content=ft.Column([
                    ft.Text("Welcome to Miracles Church of God", size=26, weight=ft.FontWeight.BOLD, color=COLOR_GOLD),
                    ft.Text("Being Good, Doing Good", size=16, color=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.CENTER),
                bgcolor=COLOR_BLUE,
                padding=30,
                border_radius=10
            ),

            #Events
            ft.Text("Upcoming Events", size=10, weight=ft.FontWeight.BOLD, color=COLOR_PURPLE),
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Sunday Worship", weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                        ft.Text("Every Sunday at 10:00A.M", color=COLOR_GOLD)
                    ]),
                    bgcolor=COLOR_PURPLE,
                    padding=15,
                    border_radius=8,
                    expand=True
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Midweek Bible Study", weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                        ft.Text("Wednesdays at 7:00PM", color=COLOR_GOLD)
                    ]),
                    bgcolor=COLOR_BLUE,
                    padding=15,
                    border_radius=8, 
                    expand=True
                ),
            ]),

            ft.Divider(color=COLOR_GOLD, height=2),
            
            #Important Info
            ft.Text("Important Information", size=20, weight=ft.FontWeight.BOLD, color=COLOR_PURPLE),
            ft.Container(
                content=ft.Text("Online streaming is active on all our social platforms", color=COLOR_DARK_TEXT),
                border=ft.border.all(2, COLOR_GOLD),
                padding=12,
                border_radius=6,
            ),

            ft.Divider(color=COLOR_GOLD, height=2),

            ft.Text("Get Connected", size=20, weight=ft.FontWeight.BOLD, color=COLOR_BLUE),
            tabs,
        ], expand=True, spacing=15)

    def get_about_view():
        return ft.ListView([
            ft.Container(
                content=ft.Column([
                    ft.Text("About MCOG", size=22, weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                    ft.Text("Slogan: Being Good, Doing Good", color=COLOR_GOLD),
                ]),
                bgcolor=COLOR_PURPLE,
                padding=20,
                border_radius=8
            ),
            ft.Text("Pastrol Leadership", size=18, weight=ft.FontWeight.BOLD, color=COLOR_BLUE),
            ft.Row([
                ft.Column([ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=60, color=COLOR_GOLD,), ft.Text("Senior Pastor",color=COLOR_DARK_TEXT)]),
                ft.Column([ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=60, color=COLOR_GOLD), ft.Text("Associate Pastor", color=COLOR_DARK_TEXT)]),
            ], spacing=40),
            ft.Divider(color=COLOR_GOLD, height=2),
            ft.Text("Location & Hours", size=18, weight=ft.FontWeight.BOLD, color=COLOR_BLUE),
            ft.Text("123 Faith Avenue | Mon - Fri: 9:00A.M - 4:00PM", color=COLOR_DARK_TEXT)
        ], expand=True, spacing=15)
        