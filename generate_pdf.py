"""Generate the LMU Clock Overlay PDF User Guide."""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "docs")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "LMUClockOverlay_UserGuide.pdf")


class Guide(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "LMU Clock Overlay v1.3.0 - User Guide", align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  Author: cento789", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 120, 0)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 170, 0)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(8, 6, "-")
        if bold_prefix:
            self.set_font("Helvetica", "B", 11)
            self.write(6, bold_prefix + " ")
            self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, text)

    def table_row(self, col1, col2, bold_first=True):
        x = self.get_x()
        y = self.get_y()
        if bold_first:
            self.set_font("Helvetica", "B", 10)
        else:
            self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(55, 7, col1, border=1)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 7, col2, border=1, new_x="LMARGIN", new_y="NEXT")


def generate():
    pdf = Guide()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # --- Title page content ---
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(0, 150, 0)
    pdf.cell(0, 15, "LMU Clock Overlay", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "User Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "Version 1.3.0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Author: cento789", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6,
        "A lightweight, fully transparent system clock overlay for Le Mans Ultimate "
        "and any other fullscreen or windowed game. Built because TinyPedal doesn't "
        "include a real-time clock.", align="C")

    # --- Features ---
    pdf.add_page()
    pdf.section_title("1. Features")
    features = [
        ("Real-time system clock", "updated every 200ms"),
        ("Fully transparent", "only the text is visible on screen"),
        ("Always on top", "stays visible over fullscreen and borderless games"),
        ("Draggable", "click and drag to reposition anywhere"),
        ("Settings menu", "configure everything with a live preview before starting"),
        ("Font selector", "choose from 9 fonts (Consolas, Arial, Segoe UI, Verdana, etc.)"),
        ("Font size", "adjustable from 10 to 60 pixels"),
        ("Color picker", "full RGB color chooser"),
        ("Opacity control", "from 20% to 100% transparency"),
        ("12h / 24h format", "switch between 15:30:00 and 03:30:00 PM"),
        ("Date display", "optional date shown below the time (dd/mm/yyyy)"),
        ("Text shadow", "dark drop shadow for readability on bright backgrounds"),
        ("System tray", "minimizes to the notification area after start"),
        ("Global hotkey", "Ctrl+Shift+H to toggle visibility in-game"),
        ("Persistent settings", "all preferences and position saved automatically"),
    ]
    for bold, text in features:
        pdf.bullet(text, bold_prefix=bold)

    # --- Installation ---
    pdf.section_title("2. Installation")
    pdf.body_text(
        "No installation required. LMU Clock Overlay is a portable, standalone .exe file.\n\n"
        "Steps:\n"
        "1. Download LMUClockOverlay.exe\n"
        "2. Place it in any folder\n"
        "3. Double-click to run\n\n"
        "Note: On first launch, Windows SmartScreen may show a warning. "
        "Click 'More info' then 'Run anyway' to proceed."
    )

    # --- Settings Menu ---
    pdf.section_title("3. Settings Menu")
    pdf.body_text(
        "When you launch the application, a dark-themed settings window appears. "
        "All options update the live preview in real-time so you can see exactly "
        "how the overlay will look before starting."
    )
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(0, 150, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(55, 7, "Setting", border=1, fill=True)
    pdf.cell(0, 7, "Description", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.set_fill_color(255, 255, 255)

    settings_rows = [
        ("Font", "Dropdown with 9 font families"),
        ("Font size (px)", "Slider from 10 to 60 pixels"),
        ("Color", "Click 'Pick Color' to open system color chooser"),
        ("Opacity", "Slider from 20% (very transparent) to 100% (solid)"),
        ("Format", "Radio buttons: 24h or 12h (AM/PM)"),
        ("Show date", "Checkbox to display date below the clock"),
        ("Text shadow", "Checkbox to add dark shadow behind text"),
    ]
    for col1, col2 in settings_rows:
        pdf.table_row(col1, col2)

    pdf.ln(4)
    pdf.body_text("Click the green START button to launch the overlay and minimize to the system tray.")

    # --- In-Game Controls ---
    pdf.section_title("4. In-Game Controls")
    pdf.body_text("Once the overlay is running, you can interact with it while gaming:")
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(0, 150, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(55, 7, "Action", border=1, fill=True)
    pdf.cell(0, 7, "How", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)

    controls = [
        ("Move overlay", "Left-click and drag"),
        ("Hide / Show", "Press Ctrl+Shift+H"),
        ("Close overlay", "Right-click on the overlay text"),
    ]
    for col1, col2 in controls:
        pdf.table_row(col1, col2)

    # --- System Tray ---
    pdf.ln(6)
    pdf.section_title("5. System Tray")
    pdf.body_text(
        "After pressing START, the application minimizes to the Windows system tray "
        "(notification area, near the clock). A small clock icon appears there.\n\n"
        "Right-click the tray icon for options:\n"
        "- Show/Hide (Ctrl+Shift+H) - toggle the overlay\n"
        "- Quit - close the application and save settings"
    )

    # --- Settings Persistence ---
    pdf.section_title("6. Settings Persistence")
    pdf.body_text(
        "All settings are automatically saved when you close the overlay and "
        "restored the next time you launch the application. This includes:\n\n"
        "- Font family, size, and color\n"
        "- Opacity level\n"
        "- Time format (12h/24h)\n"
        "- Date display toggle\n"
        "- Text shadow toggle\n"
        "- Overlay position on screen\n\n"
        "Settings are stored in:\n"
        "%APPDATA%\\LMUClockOverlay\\settings.json\n\n"
        "To reset all settings, simply delete this file."
    )

    # --- Tips ---
    pdf.section_title("7. Tips for Le Mans Ultimate")
    pdf.bullet("Run LMU in Borderless Windowed mode for best overlay compatibility.", bold_prefix="Display mode:")
    pdf.bullet("Use a small font size (14-20px) and position the clock in a corner that doesn't overlap with game HUD.", bold_prefix="Positioning:")
    pdf.bullet("Enable text shadow if racing on tracks with bright environments (e.g., Bahrain, COTA) for better readability.", bold_prefix="Readability:")
    pdf.bullet("Use the opacity slider to make the clock less distracting during intense racing moments.", bold_prefix="Opacity:")
    pdf.bullet("Use Ctrl+Shift+H to quickly hide the overlay during moments where you need full screen visibility (replays, menus).", bold_prefix="Quick hide:")

    # --- Command Line ---
    pdf.ln(4)
    pdf.section_title("8. Command Line")
    pdf.body_text("You can run the following command to check the version:")
    pdf.set_font("Courier", "", 11)
    pdf.cell(0, 7, "  LMUClockOverlay.exe --version", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.ln(2)
    pdf.body_text('This will print: "LMU Clock Overlay v1.3.0 by cento789"')

    # --- Building from Source ---
    pdf.section_title("9. Building from Source")
    pdf.body_text("Requirements: Python 3.10+")
    pdf.ln(1)
    pdf.body_text("Install dependencies:")
    pdf.set_font("Courier", "", 10)
    pdf.cell(0, 6, "  pip install pyinstaller pystray Pillow keyboard", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 11)
    pdf.body_text("Build command:")
    pdf.set_font("Courier", "", 9)
    pdf.multi_cell(0, 5,
        "  pyinstaller --onefile --noconsole --name LMUClockOverlay\n"
        "    --version-file version_info.py\n"
        "    --hidden-import pystray._win32 clock_overlay.py")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 11)
    pdf.body_text("The built executable will appear in the dist/ folder.")

    # --- Save ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf.output(OUTPUT_FILE)
    print(f"PDF generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate()
