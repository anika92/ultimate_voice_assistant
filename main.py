import os
import threading
import customtkinter as ctk
import speech_recognition as sr

# Set up ultra-modern CustomTkinter appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class UltimateVoiceAssistant(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window - Fully Resizable & Maximizable
        self.title("Ultimate Voice Assistant — Windows 64-bit")
        self.geometry("800x850")
        self.minsize(700, 750)
        self.resizable(True, True)

        self.is_listening = False
        self.all_apps = {}
        self.audio_apps = {}
        self.browser_apps = {}
        self.system_tools = {}

        # State tracking: "IDLE", "WAITING_FOR_AUDIO", "WAITING_FOR_BROWSER"
        self.current_state = "IDLE"

        # --- UI Layout Design ---
        self.create_header()
        self.create_control_panel()
        self.create_features_dashboard()
        self.create_activity_log()

        # Scan system shortcuts and settings in background on startup
        threading.Thread(target=self.init_system_scanner, daemon=True).start()

    def create_header(self):
        """Creates a sleek modern header and status indicator."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(25, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="🎙️ Ultimate Voice Control Hub",
            font=ctk.CTkFont(family="Segoe UI Variable", size=24, weight="bold")
        )
        title_label.pack(side="left")

        # Status Badge (Pill style)
        self.status_badge = ctk.CTkFrame(header_frame, fg_color="#18181b", corner_radius=18, height=36, border_width=1,
                                         border_color="#27272a")
        self.status_badge.pack(side="right", padx=5)

        self.status_dot = ctk.CTkLabel(self.status_badge, text="●", text_color="#3b82f6", font=("Segoe UI", 16))
        self.status_dot.pack(side="left", padx=(12, 2))

        self.status_text = ctk.CTkLabel(self.status_badge, text="Initializing...", text_color="#a1a1aa",
                                        font=("Segoe UI Variable", 12, "bold"))
        self.status_text.pack(side="right", padx=(0, 14))

    def create_control_panel(self):
        """Creates the main activation button card."""
        panel = ctk.CTkFrame(self, fg_color="#18181b", corner_radius=16, border_width=1, border_color="#27272a")
        panel.pack(fill="x", padx=30, pady=10)

        self.toggle_btn = ctk.CTkButton(
            panel,
            text="Start Listening",
            font=ctk.CTkFont(family="Segoe UI Variable", size=15, weight="bold"),
            fg_color="#2563eb", hover_color="#1d4ed8",
            height=52, corner_radius=12,
            command=self.toggle_listening,
            state="disabled"
        )
        self.toggle_btn.pack(fill="x", padx=20, pady=20)

    def create_features_dashboard(self):
        """Creates a clean unified dashboard preview showing what you can control."""
        dashboard_card = ctk.CTkFrame(self, fg_color="#18181b", corner_radius=16, border_width=1,
                                      border_color="#27272a")
        dashboard_card.pack(fill="x", padx=30, pady=5)

        header_text = ctk.CTkLabel(
            dashboard_card,
            text="⚡ Voice Capabilities & Quick Shortcuts Ready",
            font=ctk.CTkFont(family="Segoe UI Variable", size=13, weight="bold"),
            text_color="#38bdf8"
        )
        header_text.pack(anchor="w", padx=20, pady=(14, 4))

        self.info_box = ctk.CTkTextbox(
            dashboard_card,
            height=85,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color="#09090b", text_color="#a1a1aa",
            corner_radius=10, border_width=1, border_color="#27272a"
        )
        self.info_box.pack(fill="x", padx=20, pady=(0, 16))

        capabilities_text = (
            "• Say 'Audio Player' or 'Browser' -> Suggests all installed options dynamically\n"
            "• Say 'Screenshot' -> Displays Windows shortcut keys instantly\n"
            "• Say any app/tool: 'pg admin', 'Chrome', 'KMPlayer', 'Disk Management', 'Display Settings'"
        )
        self.info_box.insert("end", capabilities_text)
        self.info_box.configure(state="disabled")

    def create_activity_log(self):
        """Creates the live activity log output box."""
        log_frame = ctk.CTkFrame(self, fg_color="transparent")
        log_frame.pack(fill="both", expand=True, padx=30, pady=(10, 25))

        log_label = ctk.CTkLabel(log_frame, text="Live Activity & Voice Feed",
                                 font=ctk.CTkFont(family="Segoe UI Variable", size=13, weight="bold"))
        log_label.pack(anchor="w", pady=(0, 6))

        self.log_box = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(family="Consolas", size=11), fg_color="#18181b",
                                      text_color="#e4e4e7", corner_radius=16, border_width=1, border_color="#27272a")
        self.log_box.pack(fill="both", expand=True)
        self.log_box.configure(state="disabled")

    def log(self, message):
        """Thread-safe logging helper."""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def init_system_scanner(self):
        """Deep indexes Windows applications, subfolders, browsers, and tools."""
        self.log("🔍 Deep indexing all applications, subfolders & tools...")

        # 1. Windows System Settings & Management Tools
        self.system_tools = {
            "display settings": "ms-settings:display",
            "display": "ms-settings:display",
            "sound settings": "ms-settings:sound",
            "audio settings": "ms-settings:sound",
            "sound": "ms-settings:sound",
            "disk management": "diskmgmt.msc",
            "device partitioning": "diskmgmt.msc",
            "partition": "diskmgmt.msc",
            "device manager": "devmgmt.msc",
            "control panel": "control",
            "network settings": "ms-settings:network",
            "wifi settings": "ms-settings:network-wifi",
            "bluetooth settings": "ms-settings:bluetooth",
            "bluetooth": "ms-settings:bluetooth",
            "windows update": "ms-settings:windowsupdate",
            "storage settings": "ms-settings:storagesense"
        }

        # 2. Known Browser paths fallback
        known_browsers = {
            "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "microsoft edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "brave": os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe")
        }
        for name, path in known_browsers.items():
            if os.path.exists(path):
                self.browser_apps[name] = path
                self.all_apps[name] = path

        # 3. Comprehensive Start Menu Recursive Walk
        search_paths = [
            os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu',
                         'Programs'),
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
        ]

        audio_keywords = ["audio", "player", "music", "kmplayer", "vlc", "winamp", "spotify", "media", "gom", "itunes",
                          "aimp"]
        browser_keywords = ["browser", "chrome", "firefox", "edge", "brave", "opera", "vivaldi", "safari"]

        app_count = 0
        for base_path in search_paths:
            if os.path.exists(base_path):
                for root, dirs, files in os.walk(base_path):
                    for file in files:
                        if file.lower().endswith('.lnk'):
                            clean_name = file[:-4].lower().strip()
                            full_path = os.path.join(root, file)

                            self.all_apps[clean_name] = full_path
                            no_space_name = clean_name.replace(" ", "")
                            if no_space_name != clean_name:
                                self.all_apps[no_space_name] = full_path

                            app_count += 1

                            if any(kw in clean_name for kw in audio_keywords):
                                self.audio_apps[clean_name] = full_path

                            if any(kw in clean_name for kw in browser_keywords):
                                self.browser_apps[clean_name] = full_path

        self.log(
            f"✅ Deep Scan Complete! Indexed {app_count} apps ({len(self.audio_apps)} audio, {len(self.browser_apps)} browsers).")
        self.status_text.configure(text="Idle / Ready")
        self.status_dot.configure(text_color="#22c55e")
        self.toggle_btn.configure(state="normal")

    def toggle_listening(self):
        """Starts or stops the background listening thread."""
        if not self.is_listening:
            self.is_listening = True
            self.current_state = "IDLE"
            self.toggle_btn.configure(text="Stop Listening", fg_color="#ef4444", hover_color="#dc2626")
            self.status_dot.configure(text_color="#ef4444")
            self.status_text.configure(text="Listening...")

            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.reset_ui_state()
            self.log("🛑 Voice session manually stopped.")

    def listen_loop(self):
        """Continuously listens and manages states for category suggestions vs direct commands."""
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True

        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    self.log("\n🎤 [Listening... Speak command]")
                    recognizer.adjust_for_ambient_noise(source, duration=0.8)

                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)

                    if not self.is_listening:
                        break

                    self.log("⚙️ Processing speech...")
                    command = recognizer.recognize_google(audio).lower().strip()
                    self.log(f"🗣️ You said: '{command}'")

                    if "exit" in command or "quit" in command:
                        self.log("👋 Exit command recognized.")
                        self.is_listening = False
                        self.after(0, self.reset_ui_state)
                        break

                    # --- STATE MACHINE HANDLING ---
                    if self.current_state == "IDLE":
                        if "screenshot" in command or "screen shot" in command:
                            self.show_screenshot_shortcuts()
                        elif any(kw in command for kw in ["audio", "music", "media player", "player"]):
                            self.current_state = "WAITING_FOR_AUDIO"
                            self.suggest_audio_players()
                        elif any(kw in command for kw in ["browser", "web", "internet"]):
                            self.current_state = "WAITING_FOR_BROWSER"
                            self.suggest_browsers()
                        else:
                            self.try_direct_launch(command)

                    elif self.current_state == "WAITING_FOR_AUDIO":
                        launched = self.match_and_launch(command, self.audio_apps, "Audio Player")
                        if not launched:
                            self.try_direct_launch(command)

                    elif self.current_state == "WAITING_FOR_BROWSER":
                        launched = self.match_and_launch(command, self.browser_apps, "Web Browser")
                        if not launched:
                            self.try_direct_launch(command)

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                self.log("❓ Could not understand audio clearly. Speak clearly.")
            except sr.RequestError as e:
                self.log(f"⚠️ Speech service error: {e}")
            except Exception as e:
                self.log(f"⚠️ Error: {e}")

    def show_screenshot_shortcuts(self):
        """Displays Windows screenshot shortcuts in the log and stops listening."""
        self.log("\n📸 === WINDOWS SCREENSHOT SHORTCUTS ===")
        self.log("   • [Win + Shift + S] : Open Snipping Tool (Select area & copy to clipboard)")
        self.log("   • [Win + PrtScn]    : Save full screen directly to Pictures > Screenshots")
        self.log("   • [PrtScn]          : Copy full screen to clipboard")
        self.log("✨ Shortcut guide displayed successfully!")

        # Stop listening after delivering the helpful info
        self.is_listening = False
        self.after(0, self.reset_ui_state)

    def suggest_audio_players(self):
        self.log("\n🎧 === SUGGESTED AUDIO PLAYERS ===")
        if self.audio_apps:
            for name in self.audio_apps.keys():
                self.log(f"   • {name.title()}")
        else:
            self.log("   • (No audio apps found)")
        self.log("👉 Say the name of the player:")
        self.status_text.configure(text="Say Audio App Name...")

    def suggest_browsers(self):
        self.log("\n🌐 === SUGGESTED WEB BROWSERS ===")
        if self.browser_apps:
            for name in self.browser_apps.keys():
                self.log(f"   • {name.title()}")
        else:
            self.log("   • (Chrome, Edge, Firefox)")
        self.log("👉 Say the name of the browser:")
        self.status_text.configure(text="Say Browser Name...")

    def match_and_launch(self, command, target_dict, category_label):
        cmd_clean = command.replace(" ", "")
        for name, path in target_dict.items():
            name_clean = name.replace(" ", "")
            if command in name or name in command or cmd_clean in name_clean or name_clean in cmd_clean:
                self.log(f"🚀 Launching {category_label}: '{name.title()}'")
                try:
                    os.startfile(path)
                    self.log(f"✨ Successfully opened '{name.title()}'!")
                    self.is_listening = False
                    self.after(0, self.reset_ui_state)
                    return True
                except Exception as e:
                    self.log(f"❌ Failed to launch: {e}")
                    return True
        return False

    def try_direct_launch(self, command):
        cmd_clean = command.replace(" ", "")

        # Check System Tools
        for name, target in self.system_tools.items():
            name_clean = name.replace(" ", "")
            if command in name or name in command or cmd_clean in name_clean or name_clean in cmd_clean:
                self.log(f"⚙️ Opening Windows Tool: '{name.title()}'")
                try:
                    os.startfile(target)
                    self.log(f"✨ Successfully opened '{name.title()}'!")
                    self.is_listening = False
                    self.after(0, self.reset_ui_state)
                    return
                except Exception as e:
                    self.log(f"❌ Failed to open tool: {e}")
                    return

        # Check Apps
        for name, path in self.all_apps.items():
            name_clean = name.replace(" ", "")
            if command in name or name in command or cmd_clean in name_clean or name_clean in cmd_clean:
                self.log(f"🚀 Launching App: '{name.title()}'")
                try:
                    os.startfile(path)
                    self.log(f"✨ Successfully opened '{name.title()}'!")
                    self.is_listening = False
                    self.after(0, self.reset_ui_state)
                    return
                except Exception as e:
                    self.log(f"❌ Failed to launch: {e}")
                    return

        self.log(
            f"🔍 No match found for '{command}'. Try saying 'Audio Player', 'Browser', 'Screenshot', or an app name.")

    def reset_ui_state(self):
        """Resets the UI back to idle mode."""
        self.current_state = "IDLE"
        self.toggle_btn.configure(text="Start Listening", fg_color="#2563eb", hover_color="#1d4ed8")
        self.status_dot.configure(text_color="#22c55e")
        self.status_text.configure(text="Idle / Ready")


if __name__ == "__main__":
    app = UltimateVoiceAssistant()
    app.mainloop()