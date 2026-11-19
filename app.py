import json
import os
import flet as ft

# --- COLOR PALETTE DEFINITIONS ---
COLOR_BLUE = "#1A237E"
COLOR_PURPLE = "#4A148C"
COLOR_GOLD = "#FFC107"
COLOR_GREEN = "#2ECC71"
COLOR_WHITE = "#FFFFFF"
COLOR_DARK_TEXT = "#212121"

# CREATING A DIRECTORY AND FILES USING JSON
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "prayer": os.path.join(DATA_DIR, "form_prayer.json"),
    "membership": os.path.join(DATA_DIR, "form_membership.json"),
    "volunteer": os.path.join(DATA_DIR, "form_volunteer.json"),
    "announcements": os.path.join(DATA_DIR, "form_announcements.json"),
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
        json.dump(data, file, indent=4)


def main(page: ft.Page):
    page.title = "Miracles Church of God International"
    page.bgcolor = COLOR_WHITE
    page.padding = 0

    is_minister = False
    current_tab = 0

    # --- NOTIFICATION ---
    def notify(msg, bg_color=COLOR_GREEN, text_color=COLOR_WHITE):
        page.show_dialog(
            ft.SnackBar(
                ft.Text(msg, color=text_color, weight=ft.FontWeight.BOLD),
                bgcolor=bg_color,
            )
        )

    # --- LOGIN ---
    username_input = ft.TextField(label="Username", width=260, border_color=COLOR_PURPLE)
    password_input = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=260,
        border_color=COLOR_PURPLE,
    )

    def close_login(e=None):
        login_dialog.open = False
        page.update()

    def perform_login(e):
        nonlocal is_minister

        if username_input.value == "minister" and password_input.value == "grace2026":
            is_minister = True
            username_input.value = ""
            password_input.value = ""
            login_dialog.open = False
            notify("Logged in successfully as Minister!", COLOR_GREEN)
            rebuild_ui()
        else:
            notify("Invalid credentials!", COLOR_PURPLE)

    def perform_logout(e):
        nonlocal is_minister, current_tab
        is_minister = False
        if current_tab == 4:
            current_tab = 0
        notify("Logged out", COLOR_BLUE)
        rebuild_ui()

    login_dialog = ft.AlertDialog(
        title=ft.Text("Minister Login Portal", color=COLOR_BLUE, weight=ft.FontWeight.BOLD),
        content=ft.Column([username_input, password_input], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=close_login),
            ft.Button("Login", bgcolor=COLOR_GREEN, color=COLOR_WHITE, on_click=perform_login),
        ],
    )

    def open_login(e):
        login_dialog.open = True
        page.show_dialog(login_dialog)

    def submit_prayer(e):
        if not prayer_name.value or not prayer_req.value:
            notify("Please fill in the fields", COLOR_PURPLE)
            return
        save_json("prayer", {"name": prayer_name.value, "request": prayer_req.value})
        prayer_name.value = ""
        prayer_req.value = ""
        notify("Prayer request submitted successfully!", COLOR_GREEN)
        rebuild_ui()

    def submit_membership(e):
        if not mem_name.value or not mem_email.value or not mem_phone.value:
            notify("Please fill in the fields", COLOR_PURPLE)
            return
        save_json(
            "membership",
            {"name": mem_name.value, "email": mem_email.value, "phone": mem_phone.value},
        )
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
    prayer_req = ft.TextField(
        label="Prayer Request",
        multiline=True,
        min_lines=3,
        max_lines=5,
        border_color=COLOR_BLUE,
    )

    mem_name = ft.TextField(label="Full Name", border_color=COLOR_BLUE)
    mem_email = ft.TextField(label="Email Address", border_color=COLOR_BLUE)
    mem_phone = ft.TextField(label="Phone Number", border_color=COLOR_BLUE)

    vol_name = ft.TextField(label="Full Name", border_color=COLOR_BLUE)
    vol_dept = ft.Dropdown(
        label="Department Choice",
        border_color=COLOR_BLUE,
        options=[
            ft.dropdown.Option("Ushering"),
            ft.dropdown.Option("Media & Tech"),
            ft.dropdown.Option("Worship Ministry"),
            ft.dropdown.Option("Children's Ministry"),
        ],
        value="Ushering",
    )

    contact_name = ft.TextField(label="Your Name", border_color=COLOR_PURPLE)
    contact_email = ft.TextField(label="Your Email", border_color=COLOR_PURPLE)
    contact_msg = ft.TextField(
        label="Your Message",
        multiline=True,
        min_lines=4,
        max_lines=6,
        border_color=COLOR_PURPLE,
    )

    anc_title = ft.TextField(label="Announcement Title", border_color=COLOR_GOLD)
    anc_content = ft.TextField(
        label="Details",
        multiline=True,
        min_lines=4,
        max_lines=6,
        border_color=COLOR_GOLD,
    )

    # --- VIEWS ---
    def get_home_view():
        home_tabs = ft.Tabs(
            length=3,
            selected_index=0,
            width=700,
            content=ft.Column(
                [
                    ft.TabBar(
                        indicator_color=COLOR_GOLD,
                        label_color=COLOR_PURPLE,
                        unselected_label_color=COLOR_BLUE,
                        tabs=[
                            ft.Tab(label="Prayer Request"),
                            ft.Tab(label="Church Membership"),
                            ft.Tab(label="Volunteer Signup"),
                        ],
                    ),
                    ft.TabBarView(
                        height=260,
                        controls=[
                            ft.Container(
                                content=ft.Column([
                                    prayer_name,
                                    prayer_req,
                                    ft.Button(
                                        "Submit Prayer Request",
                                        bgcolor=COLOR_GREEN,
                                        color=COLOR_WHITE,
                                        on_click=submit_prayer,
                                    ),
                                ]),
                                padding=15,
                            ),
                            ft.Container(
                                content=ft.Column([
                                    mem_name,
                                    mem_email,
                                    mem_phone,
                                    ft.Button(
                                        "Submit Application",
                                        bgcolor=COLOR_GREEN,
                                        color=COLOR_WHITE,
                                        on_click=submit_membership,
                                    ),
                                ]),
                                padding=15,
                            ),
                            ft.Container(
                                content=ft.Column([
                                    vol_name,
                                    vol_dept,
                                    ft.Button(
                                        "Sign Up to Serve",
                                        bgcolor=COLOR_GREEN,
                                        color=COLOR_WHITE,
                                        on_click=submit_volunteer,
                                    ),
                                ]),
                                padding=15,
                            ),
                        ],
                    ),
                ]
            ),
        )

        return ft.ListView(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Welcome to Miracles Church of God",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_GOLD,
                            ),
                            ft.Text(
                                "Being Good, Doing Good",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_WHITE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    bgcolor=COLOR_BLUE,
                    padding=30,
                    border_radius=10,
                ),
                ft.Text("Upcoming Events", size=18, weight=ft.FontWeight.BOLD, color=COLOR_PURPLE),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Sunday Worship", weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                            ft.Text("Every Sunday at 10:00 A.M.", color=COLOR_GOLD),
                        ]),
                        bgcolor=COLOR_PURPLE,
                        padding=15,
                        border_radius=8,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Midweek Bible Study", weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                            ft.Text("Wednesdays at 7:00 P.M.", color=COLOR_GOLD),
                        ]),
                        bgcolor=COLOR_BLUE,
                        padding=15,
                        border_radius=8,
                        expand=True,
                    ),
                ]),
                ft.Divider(color=COLOR_GOLD, height=2),
                ft.Text("Important Information", size=20, weight=ft.FontWeight.BOLD, color=COLOR_PURPLE),
                ft.Container(
                    content=ft.Text(
                        "Online streaming is active on all our social platforms", color=COLOR_DARK_TEXT
                    ),
                    border=ft.Border.all(2, COLOR_GOLD),
                    padding=12,
                    border_radius=6,
                ),
                ft.Divider(color=COLOR_GOLD, height=2),
                ft.Text("Get Connected", size=20, weight=ft.FontWeight.BOLD, color=COLOR_BLUE),
                home_tabs,
            ],
            expand=True,
            spacing=15,
        )

    def get_about_view():
        return ft.ListView(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("About Miracles Church of God International (MCOG)", size=22, weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                        ft.Text("Slogan: Being Good, Doing Good", color=COLOR_GOLD),
                    ]),
                    bgcolor=COLOR_PURPLE,
                    padding=20,
                    border_radius=8,
                ),
                ft.Text("Pastoral Leadership", size=18, weight=ft.FontWeight.BOLD, color=COLOR_BLUE),
                ft.Row(
                    [
                        ft.Column([
                            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=60, color=COLOR_GOLD),
                            ft.Text("Senior Pastor", color=COLOR_DARK_TEXT),
                        ]),
                        ft.Column([
                            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=60, color=COLOR_GOLD),
                            ft.Text("Associate Pastor", color=COLOR_DARK_TEXT),
                        ]),
                    ],
                    spacing=40,
                ),
                ft.Divider(color=COLOR_GOLD, height=2),
                ft.Text("Location & Hours", size=18, weight=ft.FontWeight.BOLD, color=COLOR_BLUE),
                ft.Text("123 Faith Avenue | Mon - Fri: 9:00 A.M. - 4:00 P.M.", color=COLOR_DARK_TEXT),
            ],
            expand=True,
            spacing=15,
        )

    def get_contact_view():
        return ft.ListView(
            [
                ft.Text("Contact Pastoral Team", size=22, weight=ft.FontWeight.BOLD, color=COLOR_PURPLE),
                contact_name,
                contact_email,
                contact_msg,
                ft.Button("Send Message", bgcolor=COLOR_GREEN, color=COLOR_WHITE, on_click=submit_contact),
            ],
            expand=True,
            spacing=15,
        )

    def get_announcement_view():
        controls = [ft.Text("Church Announcements", size=22, weight=ft.FontWeight.BOLD, color=COLOR_BLUE)]

        if is_minister:
            controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("Publish New Announcement", weight=ft.FontWeight.BOLD, color=COLOR_BLUE),
                        anc_title,
                        anc_content,
                        ft.Button(
                            "Publish Announcement",
                            bgcolor=COLOR_GREEN,
                            color=COLOR_WHITE,
                            on_click=submit_announcement,
                        ),
                    ]),
                    border=ft.Border.all(2, COLOR_GOLD),
                    padding=15,
                    border_radius=8,
                )
            )

        items = load_json("announcements")
        if not items:
            controls.append(ft.Text("No announcements posted yet", color=COLOR_DARK_TEXT))
        else:
            for item in reversed(items):
                controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                item.get("title", "Untitled"),
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_WHITE,
                            ),
                            ft.Text(item.get("content", ""), color=COLOR_GOLD),
                        ]),
                        bgcolor=COLOR_PURPLE,
                        padding=15,
                        border_radius=8,
                    )
                )

        return ft.ListView(controls, expand=True, spacing=15)

    def format_record_format(title: str, fields: list[tuple[str, str]]):
        field_controls = [
            ft.Text(
                f"{label}: {value or 'N/A'}",
                size=14,
                color=COLOR_DARK_TEXT,
            )
            for label, value in fields
        ]
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=COLOR_BLUE),
                *field_controls
            ], spacing=4),
            bgcolor="#F9F9F9",
            border=ft.Border.all(2, COLOR_GOLD),
            border_radius=8,
            padding=12
        )

    def dashboard_view():
        if not is_minister:
            return ft.Column([
                ft.Text("Access Restricted. Minister credentials required", color=COLOR_PURPLE, size=16)
            ])

        prayer_data = load_json("prayer")
        mem_data = load_json("membership")
        vol_data = load_json("volunteer")

        prayer_cards = [
            format_record_format(
                title=f"Prayer Request {idx + 1}",
                fields=[
                    ("Full Name", p.get("name", "")),
                    ("Prayer Request", p.get("request", ""))
                ]
            )
            for idx, p in enumerate(prayer_data)
        ] or [ft.Text("No prayer request found", color=COLOR_DARK_TEXT)]

        membership_cards = [
            format_record_format(
                title=f"Membership Application {idx + 1}",
                fields=[
                    ("Full Name", m.get("name", "")),
                    ("Email Address", m.get("email", "")),
                    ("Phone Number", m.get("phone", ""))
                ]
            )
            for idx, m in enumerate(mem_data)
        ] or [ft.Text("No memberships applications found.", color=COLOR_DARK_TEXT)]

        volunteer_cards = [
            format_record_format(
                title=f"Volunteer Signup {idx + 1}",
                fields=[
                    ("Full Name", v.get("name", "")),
                    ("Department", v.get("department", ""))
                ]
            )
            for idx, v in enumerate(vol_data)
        ] or [ft.Text("No volunteer signup found", color=COLOR_DARK_TEXT)]

        dashboard_tabs = ft.Tabs(
            length=3,
            selected_index=0,
            content=ft.Column(
                [
                    ft.TabBar(
                        indicator_color=COLOR_GOLD,
                        label_color=COLOR_PURPLE,
                        unselected_label_color=COLOR_BLUE,
                        tabs=[
                            ft.Tab(label=f"Prayer Requests ({len(prayer_data)})"),
                            ft.Tab(label=f"Memberships ({len(mem_data)})"),
                            ft.Tab(label=f"Volunteers ({len(vol_data)})"),
                        ],
                    ),
                    ft.TabBarView(
                        height=360,
                        controls=[
                           ft.ListView(prayer_cards, spacing=10, padding=10),
                           ft.ListView(membership_cards, spacing=10, padding=10),
                           ft.ListView(volunteer_cards, spacing=10, padding=10)
                        ],
                    ),
                ]
            ),
        )

        return ft.ListView(
            [
                ft.Text("Minister Data Dashboard", size=22, weight=ft.FontWeight.BOLD, color=COLOR_BLUE),
                ft.Text("Credential Records", color=COLOR_DARK_TEXT),
                dashboard_tabs,
            ],
            expand=True,
            spacing=15,
        )

    # --- NAVIGATION BAR & ROUTING ---
    def navigate(e):
        nonlocal current_tab
        current_tab = e.control.selected_index
        rebuild_ui()

    def rebuild_ui():
        page.controls.clear()

        nav_items = [
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationRailDestination(icon=ft.Icons.INFO, label="About"),
            ft.NavigationRailDestination(icon=ft.Icons.EMAIL, label="Contact Us"),
            ft.NavigationRailDestination(icon=ft.Icons.CAMPAIGN, label="Announcements"),
        ]

        if is_minister:
            nav_items.append(ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Dashboard"))

        rail = ft.NavigationRail(
            selected_index=current_tab if current_tab < len(nav_items) else 0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=nav_items,
            on_change=navigate,
            bgcolor=COLOR_WHITE,
            indicator_color=COLOR_GOLD,
        )

        views = [get_home_view(), get_about_view(), get_contact_view(), get_announcement_view()]
        if is_minister:
            views.append(dashboard_view())

        active_content = views[current_tab] if current_tab < len(views) else views[0]

        action_button = (
            ft.Button("Logout Minister", on_click=perform_logout)
            if is_minister
            else ft.Button(
                "Minister Login",        
                bgcolor=COLOR_GOLD,
                color=COLOR_DARK_TEXT,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=8,
                ),
                on_click=open_login,
            )
        )

        app_bar = ft.Container(
            content=ft.Row(
                [
                    ft.Row([
                        ft.Icon(ft.Icons.CHURCH, size=30, color=ft.Colors.WHITE),
                        ft.Text(
                            "Miracles Church of God",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                    ]),
                    action_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.Colors.BLUE_800,
            padding=15,
        )

        page.add(
            app_bar,
            ft.Row(
                [rail, ft.VerticalDivider(width=1), ft.Container(content=active_content, expand=True, padding=20)],
                expand=True,
            ),
        )

    rebuild_ui()


# Launch in browser mode or desktop mode
ft.run(main, view=ft.AppView.WEB_BROWSER)