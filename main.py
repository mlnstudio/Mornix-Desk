#!/usr.bin/env python3

import sys
import os
import subprocess
import shlex

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QPushButton, QLabel, QStackedWidget, QScrollArea, QFrame, QTextEdit,
    QInputDialog, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont, QTextCursor, QCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QSize

CRE = '\\033[1;31m'; CYE = '\\033[1;33m'; CGR = '\\033[1;32m'; CBL = '\\033[1;34m'; CNC = '\\033[0m'

DESKTOPS = [
    {
        "id": "bspwm_gh0stzk", "name": "bspwm (Rice by gh0stzk)",
        "summary": "استاندارد طلایی در دنیای Ricing. مینیمال، سریع و بی‌نهایت زیبا.",
        "description": "نصب کامل و خودکار محیط کاری محبوب gh0stzk. این گزینه تمام مخازن، پکیج‌ها، تم‌ها و کانفیگ‌های لازم برای داشتن یک تجربه بی‌نقص bspwm را فراهم می‌کند.",
        "icon": "bspwm.png", "screenshot": "bspwm.jpg", "packages": "",
        "post_install": [
            f"echo '{CBL}---> Step 1: Adding Repositories...{CNC}'",
            'sh -c "grep -q \'^\\[gh0stzk-dotfiles\\]\' /etc/pacman.conf || printf \'\\n[gh0stzk-dotfiles]\\nSigLevel = Optional TrustAll\\nServer = http://gh0stzk.github.io/pkgs/x86_64\\n\' | sudo tee -a /etc/pacman.conf"',
            "echo 'Adding Chaotic-AUR GPG Key...'", "sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com || true", "sudo pacman-key --lsign-key 3056513887B78AEB || true",
            "echo 'Installing Chaotic Keyring and Mirrorlist...'", "sudo pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst' || true",
            'sh -c "grep -q \'^\\[chaotic-aur\\]\' /etc/pacman.conf || printf \'\\n[chaotic-aur]\\nInclude = /etc/pacman.d/chaotic-mirrorlist\\n\' | sudo tee -a /etc/pacman.conf"',
            f"echo '{CGR}Repositories configured. Updating pacman database...{CNC}'", "sudo pacman -Syy",
            f"echo '{CBL}---> Step 2: Installing All Dependencies...{CNC}'", f"echo '{CYE}Installing packages from Official Repos...{CNC}'",
            "sudo pacman -S --noconfirm --needed alacritty base-devel bat brightnessctl bspwm clipcat dunst eza feh fzf thunar tumbler gvfs-mtp firefox geany git imagemagick jq jgmenu kitty libwebp maim mpc mpd mpv neovim ncmpcpp npm pamixer pacman-contrib papirus-icon-theme picom playerctl polybar lxsession-gtk3 python-gobject redshift rofi rustup sxhkd tmux xclip xdg-user-dirs xdo xdotool xsettingsd xorg-xdpyinfo xorg-xkill xorg-xprop xorg-xrandr xorg-xsetroot xorg-xwininfo yazi zsh zsh-autosuggestions zsh-history-substring-search zsh-syntax-highlighting ttf-inconsolata ttf-jetbrains-mono ttf-jetbrains-mono-nerd ttf-terminus-nerd ttf-ubuntu-mono-nerd webp-pixbuf-loader",
            f"echo '{CYE}Installing themes and icons from gh0stzk Repo...{CNC}'", "sudo pacman -S --noconfirm --needed gh0stzk-gtk-themes gh0stzk-cursor-qogirr gh0stzk-icons-beautyline gh0stzk-icons-candy gh0stzk-icons-catppuccin-mocha gh0stzk-icons-dracula gh0stzk-icons-glassy gh0stzk-icons-gruvbox-plus-dark gh0stzk-icons-hack gh0stzk-icons-luv gh0stzk-icons-sweet-rainbow gh0stzk-icons-tokyo-night gh0stzk-icons-vimix-white gh0stzk-icons-zafiro gh0stzk-icons-zafiro-purple",
            f"echo '{CYE}Installing packages from Chaotic-AUR...{CNC}'", "sudo pacman -S --noconfirm --needed paru eww-git i3lock-color simple-mtpfs fzf-tab-git",
            f"echo '{CYE}Installing packages from AUR using paru...{CNC}'", "paru -S --noconfirm --skipreview xqp xwinwrap-0.9-bin",
            f"echo '{CBL}---> Step 3: Cloning Dotfiles...{CNC}'", "rm -rf ~/dotfiles_old && mv ~/dotfiles ~/dotfiles_old || true", "git clone --depth=1 https://github.com/gh0stzk/dotfiles ~/dotfiles",
            f"echo '{CBL}---> Step 4: Backing Up Existing Configs...{CNC}'", "mkdir -p ~/.RiceBackup", "mv ~/.config/bspwm ~/.RiceBackup/bspwm.bak || true", "mv ~/.config/alacritty ~/.RiceBackup/alacritty.bak || true", "mv ~/.config/picom ~/.RiceBackup/picom.bak || true", "mv ~/.config/rofi ~/.RiceBackup/rofi.bak || true", "mv ~/.config/sxhkd ~/.RiceBackup/sxhkd.bak || true", "mv ~/.config/dunst ~/.RiceBackup/dunst.bak || true", "mv ~/.config/kitty ~/.RiceBackup/kitty.bak || true", "mv ~/.config/polybar ~/.RiceBackup/polybar.bak || true", "mv ~/.config/nvim ~/.RiceBackup/nvim.bak || true", "mv ~/.config/yazi ~/.RiceBackup/yazi.bak || true", "mv ~/.zshrc ~/.RiceBackup/zshrc.bak || true",
            f"echo '{CBL}---> Step 5: Installing New Dotfiles...{CNC}'", "cp -r ~/dotfiles/config/* ~/.config/", "cp -r ~/dotfiles/home/.zshrc ~/dotfiles/home/.gtkrc-2.0 ~/dotfiles/home/.icons ~/", "cp -r ~/dotfiles/misc/bin ~/.local/", "fc-cache -rv",
            f"echo '{CBL}---> Step 6: Configuring Services and Shell...{CNC}'", "sudo systemctl disable --now mpd.service || true", "systemctl --user enable --now mpd.service", "systemctl --user enable --now ArchUpdates.timer",
            "sh -c 'if systemd-detect-virt --quiet; then sed -i \"s/backend = \\\"glx\\\"/backend = \\\"xrender\\\"/\" ~/.config/bspwm/src/config/picom.conf; sed -i \"s/vsync = true/vsync = false/\" ~/.config/bspwm/src/config/picom.conf; fi'",
            "chsh -s $(which zsh)", f"echo '{CGR}---> All Done! Please REBOOT your system to apply all changes.{CNC}'"
        ]
    },
    { "id": "i3_modern", "name": "i3 (Modern Rice)", "summary": "یک کانفیگ مدرن و چشم‌نواز برای مدیر پنجره کلاسیک i3.", "description": "این گزینه i3-gaps را به همراه Polybar برای نوار وضعیت، Rofi برای لانچر و Picom برای افکت‌های شفافیت نصب می‌کند. یک مجموعه dotfiles زیبا و کاربردی برای شروع سریع کار با i3.", "icon": "i3.png", "screenshot": "i3.png", "packages": "i3-wm polybar rofi picom ttf-jetbrains-mono-nerd feh",
        "post_install": [ f"echo '{CYE}Cloning modern i3 dotfiles...{CNC}'", "git clone --depth=1 https://github.com/addy-dclxvi/i3-starterpack /tmp/i3-dots", f"echo '{CYE}Backing up existing configs...{CNC}'", "mkdir -p ~/.RiceBackup", "mv ~/.config/i3 ~/.RiceBackup/i3.bak || true", "mv ~/.config/polybar ~/.RiceBackup/polybar.bak || true", f"echo '{CYE}Installing new configs...{CNC}'", "cp -r /tmp/i3-dots/i3 ~/.config/", "cp -r /tmp/i3-dots/polybar ~/.config/", "rm -rf /tmp/i3-dots", f"echo '{CGR}i3 Modern Rice installed!{CNC}'" ]
    },
    { "id": "niri_wayland", "name": "Niri (Next-Gen Wayland)", "summary": "یک تجربه نسل بعدی با کامپوزیتور جدید و پویای Niri.", "description": "Niri یک کامپوزیتور Wayland مدرن با انیمیشن‌های روان و چینش ستونی پنجره‌هاست. این گزینه Niri را به همراه Waybar (نوار وضعیت) و Wofi (لانچر) با یک کانفیگ آماده نصب می‌کند.", "icon": "niri.png", "screenshot": "niri.png", "packages": "niri waybar wofi ttf-font-awesome",
        "post_install": [ f"echo '{CYE}Cloning Niri dotfiles...{CNC}'", "git clone --depth=1 https://github.com/sodiboo/niri-config /tmp/niri-dots", f"echo '{CYE}Backing up existing configs...{CNC}'", "mkdir -p ~/.RiceBackup", "mv ~/.config/niri ~/.RiceBackup/niri.bak || true", "mv ~/.config/waybar ~/.RiceBackup/waybar.bak || true", f"echo '{CYE}Installing new configs...{CNC}'", "cp -r /tmp/niri-dots/niri ~/.config/", "cp -r /tmp/niri-dots/waybar ~/.config/", "rm -rf /tmp/niri-dots", f"echo '{CGR}Niri Wayland environment is ready!{CNC}'" ]
    },
    { "id": "icewm_retro", "name": "IceWM (Retro-Futurist)", "summary": "سریع، سبک و با ظاهری نوستالژیک اما مدرن.", "description": "IceWM یکی از سبک‌ترین و سریع‌ترین مدیران پنجره است. این گزینه آن را به همراه یک پکیج از تم‌های زیبا نصب می‌کند و یک تم مدرن و تیره را به عنوان پیش‌فرض فعال می‌کند.", "icon": "icewm.png", "screenshot": "icewm.jpg", "packages": "icewm icewm-themes",
        "post_install": [ f"echo '{CYE}Setting a modern theme for IceWM...{CNC}'", "mkdir -p ~/.icewm", "echo 'Theme=\"icedesert/default.theme\"' > ~/.icewm/theme", f"echo '{CGR}IceWM is configured! Enjoy the speed!{CNC}'" ]
    },
]

STYLESHEET = """
QWidget { background-color: #282c34; color: #abb2bf; font-family: "Vazirmatn", "Tahoma", sans-serif; font-size: 11pt; }
QMainWindow { background-color: #21252b; }
QFrame#DesktopCard { background-color: #2c313a; border: 1px solid #3c424f; border-radius: 8px; }
QLabel#Title { font-size: 24pt; font-weight: bold; color: #e6e6e6; }
QLabel#SubTitle { font-size: 12pt; color: #7f8998; }
QLabel#CardTitle { font-size: 14pt; font-weight: bold; color: #e6e6e6; background-color: transparent; }
QLabel#CardSummary, QLabel#CardIcon { background-color: transparent; }
QLabel#DetailTitle { font-size: 20pt; font-weight: bold; color: #e6e6e6; }
QPushButton { background-color: #3e4451; border: none; border-radius: 5px; padding: 10px 20px; }
QPushButton:hover { background-color: #4a505e; }
QPushButton#InstallButton { background-color: #61afef; color: #21252b; font-weight: bold; padding: 12px 24px; }
QPushButton#BackButton { background: none; border: none; font-size: 18pt; padding: 5px; }
QTextEdit#LogView { background-color: #21252b; color: #c8ccd4; font-family: "Monospace"; border: 1px solid #3c424f; border-radius: 5px; }
QScrollArea { border: none; }
"""

class DesktopCard(QFrame):
    clicked = pyqtSignal()
    def __init__(self, desktop_info, parent=None):
        super().__init__(parent)
        self.setObjectName("DesktopCard"); self.setCursor(QCursor(Qt.PointingHandCursor))
        layout = QVBoxLayout(self); layout.setContentsMargins(15, 15, 15, 15); layout.setSpacing(10)
        icon_label = QLabel(); icon_label.setObjectName("CardIcon"); icon_label.setAlignment(Qt.AlignCenter); icon_label.setFixedSize(64, 64)
        icon_path = os.path.join("assets", "icons", desktop_info["icon"])
        if os.path.exists(icon_path): icon_label.setPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else: style = self.style(); icon_label.setPixmap(style.standardIcon(style.SP_DesktopIcon).pixmap(64, 64))
        title_label = QLabel(f'<p align="center" dir="rtl"><b>{desktop_info["name"]}</b></p>'); title_label.setObjectName("CardTitle"); title_label.setTextFormat(Qt.RichText)
        summary_label = QLabel(f'<p align="center" dir="rtl">{desktop_info["summary"]}</p>'); summary_label.setObjectName("CardSummary"); summary_label.setWordWrap(True); summary_label.setTextFormat(Qt.RichText)
        layout.addWidget(icon_label, alignment=Qt.AlignCenter); layout.addWidget(title_label); layout.addWidget(summary_label)
    def mousePressEvent(self, event): self.clicked.emit(); super().mousePressEvent(event)
    def enterEvent(self, event): self.setStyleSheet("QFrame#DesktopCard { background-color: #353b45; border: 1px solid #5c6370; }"); super().enterEvent(event)
    def leaveEvent(self, event): self.setStyleSheet(""); super().leaveEvent(event)

class InstallWorker(QObject):
    output_signal = pyqtSignal(str); finished_signal = pyqtSignal(bool)
    def __init__(self, commands, password):
        super().__init__(); self.commands = commands; self.password = password
    def run(self):
        for command in self.commands:
            self.output_signal.emit(f"\n$ {command}\n")
            final_command = command
            if command.strip().startswith("sudo"): final_command = f"echo '{self.password}' | sudo -S -p '' {command.strip()[4:].strip()}"
            try:
                process = subprocess.Popen(['sh', '-c', final_command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                for line in iter(process.stdout.readline, ''): self.output_signal.emit(line)
                process.stdout.close()
                if process.wait() != 0: self.finished_signal.emit(False); return
            except Exception as e: self.output_signal.emit(f"\n--- ERROR: {e} ---\n"); self.finished_signal.emit(False); return
        self.finished_signal.emit(True)

class MornixDeskKitApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mornix DeskKit for Arch Linux")
        self.setMinimumSize(950, 750)
        self.setStyleSheet(STYLESHEET)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.stack = QStackedWidget()
        self._create_header()
        self.main_layout.addWidget(self.header_frame)
        self.main_layout.addWidget(self.stack)
        self.stack.addWidget(self._create_selection_page())
        self.stack.addWidget(self._create_detail_page())
        self.stack.addWidget(self._create_install_page())

    def _create_header(self):
        self.header_frame = QFrame()
        self.header_frame.setFixedHeight(50)
        layout = QHBoxLayout(self.header_frame)
        layout.setContentsMargins(10, 0, 10, 0)
        self.back_button = QPushButton("→")
        self.back_button.setObjectName("BackButton")
        self.back_button.setFixedSize(40, 40)
        self.back_button.clicked.connect(self.go_to_selection_page)
        self.back_button.hide()
        self.header_title = QLabel("Mornix DeskKit")
        self.header_title.setAlignment(Qt.AlignCenter)
        self.header_title.setObjectName("Title")
        layout.addWidget(self.back_button)
        layout.addWidget(self.header_title)
        spacer = QWidget()
        spacer.setFixedSize(40,40)
        layout.addWidget(spacer)

    def _create_selection_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setAlignment(Qt.AlignTop)
        
        title = QLabel(f'<h1 align="center" dir="rtl">یک محیط کاری را انتخاب کنید</h1>')
        title.setObjectName("Title"); title.setTextFormat(Qt.RichText)
        
        subtitle = QLabel(f'<p align="center" dir="rtl">نصب کننده خودکار Ricing برای آرچ لینوکس</p>')
        subtitle.setObjectName("SubTitle"); subtitle.setTextFormat(Qt.RichText)
        
        layout.addWidget(title); layout.addWidget(subtitle); layout.addSpacing(30)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setSpacing(20)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        for i, desktop in enumerate(DESKTOPS):
            card = DesktopCard(desktop)
            card.clicked.connect(lambda d=desktop: self.go_to_detail_page(d))
            self.grid_layout.addWidget(card, i // 2, i % 2)
        
        return page

    def _create_detail_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(50, 20, 50, 30)
        layout.setAlignment(Qt.AlignTop)
        self.detail_screenshot = QLabel()
        self.detail_screenshot.setAlignment(Qt.AlignCenter)
        self.detail_screenshot.setMinimumHeight(350)
        self.detail_screenshot.setStyleSheet("border: 1px solid #3c424f; border-radius: 8px;")
        self.detail_title = QLabel()
        self.detail_title.setObjectName("DetailTitle"); self.detail_title.setAlignment(Qt.AlignCenter); self.detail_title.setTextFormat(Qt.RichText)
        self.detail_description = QLabel()
        self.detail_description.setObjectName("DetailDescription"); self.detail_description.setWordWrap(True); self.detail_description.setAlignment(Qt.AlignCenter); self.detail_description.setTextFormat(Qt.RichText)
        self.install_button = QPushButton()
        self.install_button.setObjectName("InstallButton"); self.install_button.setMinimumHeight(50)
        self.install_button.clicked.connect(self.start_installation_process)
        layout.addWidget(self.detail_screenshot); layout.addSpacing(20); layout.addWidget(self.detail_title); layout.addSpacing(10); layout.addWidget(self.detail_description); layout.addStretch(); layout.addWidget(self.install_button, alignment=Qt.AlignCenter)
        return page

    def go_to_detail_page(self, desktop):
        self.current_desktop = desktop
        self.detail_title.setText(f'<h2 align="center" dir="rtl">{desktop["name"]}</h2>')
        self.detail_description.setText(f'<p align="center" dir="rtl">{desktop["description"]}</p>')
        screenshot_path = os.path.join("assets", "screenshots", desktop["screenshot"])
        if os.path.exists(screenshot_path): self.detail_screenshot.setPixmap(QPixmap(screenshot_path).scaled(self.detail_screenshot.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else: self.detail_screenshot.setText(f'<p dir="rtl">پیش‌نمایش موجود نیست</p>')
        self.install_button.setEnabled(True)
        self.install_button.setText(f"نصب {desktop['name']}")
        self.back_button.show()
        self.stack.setCurrentIndex(1)

    def _create_install_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 20, 40, 20)
        title = QLabel(f'<h1 align="center" dir="rtl">در حال نصب...</h1>')
        title.setObjectName("Title"); title.setTextFormat(Qt.RichText)
        self.log_view = QTextEdit()
        self.log_view.setObjectName("LogView"); self.log_view.setReadOnly(True)
        layout.addWidget(title); layout.addSpacing(20); layout.addWidget(self.log_view)
        return page

    def go_to_selection_page(self):
        self.back_button.hide()
        self.stack.setCurrentIndex(0)

    def start_installation_process(self):
        password, ok = QInputDialog.getText(self, "نیاز به دسترسی مدیر", "لطفاً رمز عبور (sudo) خود را وارد کنید:", QLineEdit.Password)
        if not ok or not password: return
        if not self.validate_sudo_password(password):
            QMessageBox.critical(self, "خطا", "رمز عبور اشتباه است.")
            return
        self.go_to_install_page(password)

    def validate_sudo_password(self, password):
        return subprocess.run(['sudo', '-S', '-v'], input=password + '\n', text=True, capture_output=True).returncode == 0

    def go_to_install_page(self, password):
        self.back_button.setEnabled(False)
        self.stack.setCurrentIndex(2)
        self.log_view.clear()
        commands = []
        if self.current_desktop.get("packages"):
            commands.append(f"sudo pacman -S --noconfirm --needed {self.current_desktop['packages']}")
        if self.current_desktop.get("post_install"):
            commands.extend(self.current_desktop["post_install"])
        self.install_thread = QThread()
        self.install_worker = InstallWorker(commands, password)
        self.install_worker.moveToThread(self.install_thread)
        self.install_thread.started.connect(self.install_worker.run)
        self.install_worker.finished_signal.connect(self.on_installation_complete)
        self.install_worker.output_signal.connect(self.append_log)
        self.install_thread.start()

    def append_log(self, text):
        self.log_view.moveCursor(QTextCursor.End)
        self.log_view.insertPlainText(text)
        self.log_view.moveCursor(QTextCursor.End)
    
    def on_installation_complete(self, success):
        if success: self.append_log("\n\n✅ نصب با موفقیت به پایان رسید! لطفاً سیستم را ری‌استارت کنید.")
        else: self.append_log("\n\n❌ خطایی در حین نصب رخ داد! لطفاً لاگ‌ها را بررسی کنید.")
        self.back_button.setEnabled(True)
        self.install_thread.quit()
        self.install_thread.wait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Vazirmatn", 11))
    app.setLayoutDirection(Qt.RightToLeft)
    window = MornixDeskKitApp()
    window.show()
    sys.exit(app.exec_())
