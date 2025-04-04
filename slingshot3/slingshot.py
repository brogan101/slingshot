import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, Toplevel
import customtkinter as ctk
import psutil
import time
import threading
import queue
import logging
import json
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor
import tools
import custom_tools  # Added for custom tool integration
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configure logging
logging.basicConfig(filename='slingshot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Feature icons and descriptions (unchanged)
FEATURE_ICONS = {
    "Generate Key": "🔑",
    "Encrypt File": "🔐",
    "Decrypt File": "🔓",
    "Hash File": "📊",
    "AV Status": "🛡️",
    "Firewall Manager": "🔥",
    "Startup Items": "🚀",
    "Process Manager": "⚠️",
    "OTP Generator": "🔢",
    "Shred File": "🗑️",
    "Vuln Scan": "🔍",
    "Password Manager": "💪",
    "Harden Sys": "🛠️",
    "Phishing Detector": "🎣",
    "Malware Scanner": "🦠",
    "BitLocker Status": "🔒",
    "Secure Boot Check": "✅",
    "Audit Policy Viewer": "📋",
    "USB Lockdown": "🔌",
    "Resource Monitor": "📈",
    "System Info": "ℹ️",
    "Clear Temp Files": "🧹",
    "List Users": "👥",
    "Check Disk Health": "💿",
    "List Environment Vars": "🌍",
    "File Permissions Viewer": "🔐",
    "Registry Manager": "📂",
    "Shortcut Creator": "🔗",
    "Recycle Bin Manager": "♻️",
    "File Integrity Checker": "✔️",
    "Text Encoder/Decoder": "📝",
    "Screen Capture Tool": "📸",
    "PDF Merger": "📄",
    "Startup Optimizer": "⚡",
    "Folder Sync": "🔄",
    "Network Monitor": "🌐",
    "Backup Manager": "💾",
    "System Control": "🔄",
    "DNS Cache Cleaner": "🧹",
    "Driver Manager": "🚗",
    "Boot Manager": "🥾",
    "Sys Info Export": "📤",
    "BIOS Info": "🖥️",
    "Remote Desktop Toggle": "🖥️",
    "Power Plan Manager": "⚡",
    "Command History": "📜",
    "Group Policy Viewer": "📋",
    "Task Kill By Name": "❌",
    "Windows Feature Manager": "🛠️",
    "Multi-Monitor Config": "🖥️",
    "Event Log Manager": "📅",
    "Memory Leak Detector": "🕳️",
    "Real-Time Alerts": "🔔",
    "Service Monitor": "🖥️",
    "Scheduled Task Manager": "⏳",
    "Process Heatmap": "🌡️",
    "Network Latency Graph": "📉",
    "Network Intrusion Detection": "🕵️",
    "User Activity Logger": "👤",
    "Keylogger Detector": "⌨️",
    "Password Policy Enforcer": "🔒",
    "Secure File Transfer": "📤",
    "CPU Temperature Monitor": "🌡️",
    "Event Log Analyzer": "📊",
    "Disk I/O Monitor": "💾",
    "System Uptime Tracker": "⏳",
    "Alert Scheduler": "⏰",
    "Duplicate File Finder": "📂",
    "File Recovery Tool": "🔄",
    "System Tray Manager": "🖥️",
    "Clipboard Manager": "📋",
    "Batch File Renamer": "✏️",
    "Port Scanner": "🔎",
    "Wi-Fi Analyzer": "📶",
    "DNS Resolver": "🌐",
    "Packet Sniffer": "📡",
    "Bandwidth Limiter": "📏",
    "Backup Verifier": "✔️",
    "Backup Scheduler": "⏰",
    "Differential Backup Tool": "🔄",
    "Backup Encryption Key Manager": "🔑",
    "Cloud Backup Uploader": "☁️",
    "System Restore Point Creator": "🔙",
    "Event Log Cleaner": "🧹",
    "Driver Verifier": "🚦",
    "System File Checker": "🛠️",
    "Performance Benchmark": "🏁",
    "Remote Assistance Tool": "🖥️",
    "User Account Manager": "👥",
    "System Diagnostic Report": "📈",
    "Service Dependency Viewer": "🔗",
    "Hardware Inventory Tool": "🖥️",
    "Process Injection Detector": "🕵️‍♂️",
    "Kernel Driver Enumerator": "🚨",
    "Shadow Copy Manager": "📌",
    "Memory Forensics Lite": "🧠",
    "Privilege Escalation Checker": "🔝",
    "Network Connection Anomaly Detector": "🚨🌐",
    "File System Anomaly Scanner": "📁🔍",
    "Service Behavior Profiler": "🖥️📊",
    "Registry Anomaly Detector": "📂🚨",
    "Thread Stack Analyzer": "🧵",
    "Secure Boot Policy Editor": "🔐✅",
    "Process Hollowing Detector": "👻",
    "Network Packet Entropy Analyzer": "📡🔍",
    "System Call Tracer": "📞",
    "Dynamic DNS Resolver Monitor": "🌐⏳",
    "Browser Password Extractor": "🌐🔑",
    "Windows Credential Manager Extractor": "🖥️🔑",
    "Unified Password Aggregator": "📋🔑",
    "Sniff Browser Activity": "📡👀",
    "Sublist3r": "🌐🔍",
    "crt.sh": "📜🔍",
    "Censys": "🔎🌍",
    "Slack Notify": "📢"
}

FEATURE_DESCRIPTIONS = {
    f"{FEATURE_ICONS.get(key, '')} {key}" if FEATURE_ICONS.get(key) else key: desc
    for key, desc in {
        "Sniff Browser Activity": "Monitor browser login traffic.",
        "Generate Key": "Create encryption key.",
        "Encrypt File": "Secure file with key.",
        "Decrypt File": "Unlock encrypted file.",
        "Hash File": "Calculate file hash.",
        "AV Status": "Check antivirus status.",
        "Firewall Manager": "Control firewall settings.",
        "Startup Items": "View startup programs.",
        "Process Manager": "Manage active processes.",
        "OTP Generator": "Generate one-time codes.",
        "Shred File": "Securely delete file.",
        "Vuln Scan": "Scan for vulnerabilities.",
        "Password Manager": "Handle password tasks.",
        "Harden Sys": "Enhance system security.",
        "Phishing Detector": "Spot phishing attempts.",
        "Malware Scanner": "Detect malware.",
        "BitLocker Status": "Check encryption status.",
        "Secure Boot Check": "Verify Secure Boot.",
        "Audit Policy Viewer": "View audit settings.",
        "USB Lockdown": "Block USB access.",
        "Resource Monitor": "Track system usage.",
        "System Info": "Show system details.",
        "Clear Temp Files": "Remove temp files.",
        "List Users": "List system users.",
        "Check Disk Health": "Assess disk condition.",
        "List Environment Vars": "Show env variables.",
        "File Permissions Viewer": "View file perms.",
        "Registry Manager": "Edit system registry.",
        "Shortcut Creator": "Make app shortcuts.",
        "Recycle Bin Manager": "Handle recycle bin.",
        "File Integrity Checker": "Verify file integrity.",
        "Text Encoder/Decoder": "Encode/decode text.",
        "Screen Capture Tool": "Take screenshots.",
        "PDF Merger": "Combine PDF files.",
        "Startup Optimizer": "Speed up startup.",
        "Folder Sync": "Sync folder contents.",
        "Network Monitor": "Watch network activity.",
        "Backup Manager": "Manage backups.",
        "System Control": "Control system state.",
        "DNS Cache Cleaner": "Clear DNS cache.",
        "Driver Manager": "Handle device drivers.",
        "Boot Manager": "Adjust boot settings.",
        "Sys Info Export": "Export system info.",
        "BIOS Info": "Show BIOS details.",
        "Remote Desktop Toggle": "Toggle remote access.",
        "Power Plan Manager": "Manage power plans.",
        "Command History": "View past commands.",
        "Group Policy Viewer": "Show group policies.",
        "Task Kill By Name": "End task by name.",
        "Windows Feature Manager": "Control Windows features.",
        "Multi-Monitor Config": "Set up monitors.",
        "Event Log Manager": "Manage event logs.",
        "Memory Leak Detector": "Find memory leaks.",
        "Real-Time Alerts": "Set system alerts.",
        "Service Monitor": "Monitor services.",
        "Scheduled Task Manager": "Manage scheduled tasks.",
        "Process Heatmap": "Visualize process activity.",
        "Network Latency Graph": "Graph network latency.",
        "Network Intrusion Detection": "Detect network threats.",
        "User Activity Logger": "Log user actions.",
        "Keylogger Detector": "Find keyloggers.",
        "Password Policy Enforcer": "Set password rules.",
        "Secure File Transfer": "Transfer files securely.",
        "CPU Temperature Monitor": "Track CPU temp.",
        "Event Log Analyzer": "Analyze event logs.",
        "Disk I/O Monitor": "Monitor disk I/O.",
        "System Uptime Tracker": "Track uptime.",
        "Alert Scheduler": "Schedule system alerts.",
        "Duplicate File Finder": "Find duplicate files.",
        "File Recovery Tool": "Recover deleted files.",
        "System Tray Manager": "Manage tray apps.",
        "Clipboard Manager": "Handle clipboard history.",
        "Batch File Renamer": "Rename files in bulk.",
        "Port Scanner": "Scan open ports.",
        "Wi-Fi Analyzer": "Analyze Wi-Fi networks.",
        "DNS Resolver": "Resolve DNS names.",
        "Packet Sniffer": "Capture network packets.",
        "Bandwidth Limiter": "Limit app bandwidth.",
        "Backup Verifier": "Check backup integrity.",
        "Backup Scheduler": "Schedule backups.",
        "Differential Backup Tool": "Create differential backups.",
        "Backup Encryption Key Manager": "Manage backup keys.",
        "Cloud Backup Uploader": "Upload to cloud.",
        "System Restore Point Creator": "Create restore points.",
        "Event Log Cleaner": "Clear event logs.",
        "Driver Verifier": "Verify driver integrity.",
        "System File Checker": "Fix system files.",
        "Performance Benchmark": "Test system performance.",
        "Remote Assistance Tool": "Start remote assistance.",
        "User Account Manager": "Manage user accounts.",
        "System Diagnostic Report": "Generate diagnostic report.",
        "Service Dependency Viewer": "View service dependencies.",
        "Hardware Inventory Tool": "List hardware components.",
        "Process Injection Detector": "Detect process injections.",
        "Kernel Driver Enumerator": "List kernel drivers.",
        "Shadow Copy Manager": "Manage shadow copies.",
        "Memory Forensics Lite": "Scan memory for clues.",
        "Privilege Escalation Checker": "Check privilege risks.",
        "Network Connection Anomaly Detector": "Spot network anomalies.",
        "File System Anomaly Scanner": "Detect filesystem issues.",
        "Service Behavior Profiler": "Profile service behavior.",
        "Registry Anomaly Detector": "Monitor registry changes.",
        "Thread Stack Analyzer": "Analyze thread issues.",
        "Secure Boot Policy Editor": "Edit Secure Boot.",
        "Process Hollowing Detector": "Detect hollowed processes.",
        "Network Packet Entropy Analyzer": "Analyze packet entropy.",
        "System Call Tracer": "Trace system calls.",
        "Dynamic DNS Resolver Monitor": "Monitor DNS changes.",
        "Browser Password Extractor": "Extract browser passwords.",
        "Windows Credential Manager Extractor": "Pull system credentials.",
        "Unified Password Aggregator": "Aggregate all passwords.",
        "Sublist3r": "Enumerate subdomains using Sublist3r.",
        "crt.sh": "Query crt.sh for subdomain certificates.",
        "Censys": "Search Censys for subdomain data.",
        "Slack Notify": "Send notifications to Slack."
    }.items()
}

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, background="#2a2a2a", foreground="white", relief="solid", borderwidth=1, font=("Segoe UI", 10))
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class SlingShot:
    def __init__(self, root):
        self.root = root
        self.root.title("SlingShot IT Security Toolkit")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.root.configure(bg="#1f1f1f")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.command_history_log = []
        self.scheduled_tasks = []
        self.passwords_db = {}
        self.totp_secrets = {}
        self.custom_tools = {}  # Persistent storage for custom tools by category

        self.favorites = [None] * 6
        self.theme = "Dark"
        self.update_check_interval = 3600
        self.log_level = "INFO"
        self.language = "English"
        self.default_timeout = 10
        self.font_size = 12
        self.show_welcome = True
        self.default_tab = "Security"
        self.load_config()

        logger.setLevel(getattr(logging, self.log_level, logging.INFO))
        ctk.set_appearance_mode(self.theme.lower())

        self.log_queue = queue.Queue()
        self.task_queue = queue.Queue()
        self.output_history = []
        self.log_paused = False
        self.current_tasks = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.running = True

        self.analytics_data = {'cpu': [], 'mem': [], 'disk': [], 'times': []}
        self.lock = threading.Lock()

        self.progress_value = 0
        self.progress_running = False
        self.current_tool_name = None
        self.task_start_time = None
        self.task_timeout = None

        try:
            self.setup_gui()
            # Load custom tools after GUI setup
            import os
            import json
            import importlib
            tools_dir = "custom_tools"
            if not os.path.exists(os.path.join(tools_dir, "__init__.py")):
                with open(os.path.join(tools_dir, "__init__.py"), "w") as f:
                    f.write("")
                logger.info("Created __init__.py in custom_tools directory")
            metadata_file = os.path.join(tools_dir, "custom_tools.json")
            if os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                custom_tools_file = "custom_tools.py"
                if not os.path.exists(custom_tools_file):
                    with open(custom_tools_file, "w") as f:
                        f.write("# Custom tools dynamically added\nSCRIPT_REGISTRY = {}\n")
                with open(custom_tools_file, "r") as f:
                    existing_content = f.read()
                with open(custom_tools_file, "w") as f:
                    f.write("# Custom tools dynamically added\n")
                    f.write("SCRIPT_REGISTRY = {}\n")
                    for name, info in metadata.items():
                        safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in name.lower())
                        script_type = info.get("type", "python")  # Default to python for older entries
                        registry_line = f"SCRIPT_REGISTRY['{safe_name}'] = {{'type': '{script_type}', 'path': r'{info['file']}'}}\n"
                        f.write(registry_line)
                        # Add to self.custom_tools
                        category = info["category"]
                        if category not in self.custom_tools:
                            self.custom_tools[category] = []
                        if name not in self.custom_tools[category]:
                            self.custom_tools[category].append(name)
                        self.add_custom_tool(name, info["category"], script_type, info["file"])
                importlib.reload(custom_tools)
                logger.info("Custom tools loaded with SCRIPT_REGISTRY")
            logger.info("GUI setup completed successfully")
        except Exception as e:
            logger.error(f"Failed to setup GUI: {str(e)}")
            raise

        self.start_background_tasks()
        if self.show_welcome:
            self.show_welcome_screen()

    def create_new_tool(self):
        popup = Toplevel(self.root)
        popup.title("Create New Tool")
        popup.configure(bg="#1f1f1f")
        popup.transient(self.root)
        popup.grab_set()

        main_frame = ctk.CTkFrame(popup, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="Tool Name:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ctk.CTkEntry(main_frame, placeholder_text="Enter tool name", width=200)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(main_frame, text="Category:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        categories = list(self.get_categories().keys())
        category_var = tk.StringVar(value=categories[0])
        category_dropdown = ctk.CTkOptionMenu(main_frame, values=categories, variable=category_var, width=200)
        category_dropdown.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(main_frame, text="Script Type:", font=("Segoe UI", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        script_type_var = tk.StringVar(value="Batch")  # Default to Batch
        script_type_dropdown = ctk.CTkOptionMenu(main_frame, values=["Batch", "PowerShell"], variable=script_type_var, width=200)
        script_type_dropdown.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(main_frame, text="Script:", font=("Segoe UI", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        script_text = ctk.CTkTextbox(main_frame, width=400, height=300, font=("Segoe UI", 12))
        script_text.grid(row=3, column=1, padx=5, pady=5)

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        save_btn = ctk.CTkButton(btn_frame, text="Save", 
                                command=lambda: self.save_new_tool(name_entry.get(), category_var.get(), script_text.get("1.0", "end-1c"), script_type_var.get(), popup), 
                                fg_color="#28a745")
        save_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy, fg_color="#dc3545")
        cancel_btn.pack(side="right", padx=5)

        popup.update_idletasks()
        popup.geometry("500x500")  # Adjusted for extra dropdown
        logger.info("New Tool popup created with script type selection")

    def save_new_tool(self, name, category, script, script_type, popup):
        logger.info(f"Attempting to save new tool: Name={name}, Category={category}, Script length={len(script)}, Type={script_type}")
        if not name or not script.strip():
            messagebox.showerror("Error", "Tool name and script are required.", parent=popup)
            logger.warning("Save aborted: Empty name or script")
            return
        
        try:
            import os
            import json
            import importlib
            
            tools_dir = "custom_tools"
            if not os.path.exists(tools_dir):
                os.makedirs(tools_dir)
                logger.info(f"Created directory: {tools_dir}")
            if not os.path.exists(os.path.join(tools_dir, "__init__.py")):
                with open(os.path.join(tools_dir, "__init__.py"), "w") as f:
                    f.write("")
                logger.info("Created __init__.py in custom_tools directory")
            
            safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in name.lower())
            ext = ".bat" if script_type == "Batch" else ".ps1"
            script_file = os.path.join(tools_dir, f"{safe_name}{ext}")
            
            with open(script_file, "w") as f:
                f.write(script)  # Write script as-is
            logger.info(f"Saved {script_type} script to: {script_file}")
            
            custom_tools_file = "custom_tools.py"
            if not os.path.exists(custom_tools_file):
                with open(custom_tools_file, "w") as f:
                    f.write("# Custom tools dynamically added\nSCRIPT_REGISTRY = {}\n")
                logger.info(f"Created {custom_tools_file}")
            
            with open(custom_tools_file, "r") as f:
                content = f.read()
            if "SCRIPT_REGISTRY" not in content:
                with open(custom_tools_file, "w") as f:
                    f.write("# Custom tools dynamically added\nSCRIPT_REGISTRY = {}\n")
            with open(custom_tools_file, "r") as f:
                lines = f.readlines()
            with open(custom_tools_file, "w") as f:
                for line in lines:
                    if not line.startswith("SCRIPT_REGISTRY"):
                        f.write(line)
                registry_line = f"SCRIPT_REGISTRY['{safe_name}'] = {{'type': '{script_type.lower()}', 'path': r'{script_file}'}}\n"
                f.write(registry_line)
            logger.info(f"Updated SCRIPT_REGISTRY in {custom_tools_file}")
            
            metadata_file = os.path.join(tools_dir, "custom_tools.json")
            metadata = {}
            if os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
            
            metadata[name] = {"category": category, "file": script_file, "type": script_type.lower()}
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=4)
            logger.info(f"Updated metadata in {metadata_file}")
            
            importlib.reload(custom_tools)
            logger.info("Reloaded custom_tools module")
            
            self.add_custom_tool(name, category, script_type.lower(), script_file)
            self.log_queue.put(f"New {script_type} tool '{name}' added to {category}")
            popup.destroy()
            logger.info(f"New {script_type} tool '{name}' successfully added and popup closed")
        except Exception as e:
            error_msg = f"Failed to save tool '{name}': {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("Error", error_msg, parent=popup)

    def add_custom_tool(self, name, category, script_type, script_path):
        logger.info(f"Adding custom tool: Name={name}, Category={category}, Type={script_type}, Path={script_path}")
        def tool_method(self):
            safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in name.lower())
            if script_type == "batch":
                cmd = f'cmd.exe /c "{script_path}"'
                result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
                output = result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
                self.show_output_popup(output, name)
            elif script_type == "powershell":
                cmd = f'powershell.exe -File "{script_path}"'
                result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
                output = result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
                self.show_output_popup(output, name)
            else:  # Python tools
                self.queue_task(lambda: getattr(custom_tools, f"run_{safe_name}")(), self.default_timeout, name)
                return
        
        setattr(self.__class__, name.lower().replace(" ", "_"), tool_method)
        
        # Add to self.custom_tools
        if category not in self.custom_tools:
            self.custom_tools[category] = []
        if name not in self.custom_tools[category]:
            self.custom_tools[category].append(name)
            logger.info(f"Added '{name}' to custom_tools category '{category}'")
        
        FEATURE_ICONS[name] = "🛠️"
        FEATURE_DESCRIPTIONS[f"🛠️ {name}"] = f"Custom {script_type} script."
        
        self.reset_tab_buttons()
        self.add_buttons_to_tabs()
        self.notebook.update_idletasks()  # Force GUI refresh
        logger.info(f"GUI updated with new {script_type} tool '{name}'")

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                loaded_favorites = config.get("favorites", [None] * 6)
                self.favorites = loaded_favorites + [None] * (6 - len(loaded_favorites)) if len(loaded_favorites) < 6 else loaded_favorites[:6]
                self.theme = config.get("theme", "Dark")
                self.update_check_interval = config.get("update_check_interval", 3600)
                self.log_level = config.get("log_level", "INFO")
                self.language = config.get("language", "English")
                self.default_timeout = config.get("default_timeout", 10)
                self.font_size = config.get("font_size", 12)
                self.show_welcome = config.get("show_welcome", True)
                self.default_tab = config.get("default_tab", "Security")
            logger.info("Configuration loaded successfully")
        except FileNotFoundError:
            self.save_config()
            logger.info("No config file found, created new config")
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")

    def save_config(self):
        config = {
            "favorites": self.favorites,
            "theme": self.theme,
            "update_check_interval": self.update_check_interval,
            "log_level": self.log_level,
            "language": self.language,
            "default_timeout": self.default_timeout,
            "font_size": self.font_size,
            "show_welcome": self.show_welcome,
            "default_tab": self.default_tab
        }
        try:
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def export_output(self, output):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Export Output")
        if file_path:
            with open(file_path, "w") as f:
                f.write(output)
            self.log_queue.put(f"Output exported to {file_path}")
        else:
            self.log_queue.put("Export cancelled.")

    def start_progress(self, tool_name, timeout):
        self.progress_running = True
        self.progress_value = 0
        self.current_tool_name = tool_name
        self.task_start_time = time.time()
        self.task_timeout = timeout
        self.update_progress()

    def update_progress(self):
        if self.progress_running:
            if self.task_start_time and self.task_timeout:
                elapsed = time.time() - self.task_start_time
                self.progress_value = min((elapsed / self.task_timeout) * 100, 100)
            else:
                self.progress_value = (self.progress_value + 1) % 100
            self.progress_bar.set(self.progress_value / 100)
            self.progress_label.configure(text=f"Running: {self.current_tool_name} - {self.progress_value:.1f}%")
            self.root.after(50, self.update_progress)
        else:
            self.progress_label.configure(text="")

    def stop_progress(self):
        self.progress_running = False
        self.progress_value = 0
        self.current_tool_name = None
        self.task_start_time = None
        self.task_timeout = None
        self.progress_bar.set(0)
        self.progress_label.configure(text="")

    def queue_task(self, task_func, timeout, task_name):
        def task_wrapper():
            try:
                self.start_progress(task_name, timeout)
                result = task_func()
                if isinstance(result, tuple):  # Handle tools returning state updates
                    output, state = result
                    if "totp_secrets" in task_name.lower():
                        self.totp_secrets = state
                    elif "password_manager" in task_name.lower():
                        self.passwords_db = state
                    elif "scheduled_task_manager" in task_name.lower():
                        self.scheduled_tasks = state
                else:
                    output = result
                self.log_queue.put(f"Task '{task_name}' completed: {output}")
                logger.info(f"Task '{task_name}' completed: {output}")
                self.show_output_popup(str(output), task_name)
            except Exception as e:
                error_msg = f"Task '{task_name}' failed: {str(e)}"
                self.log_queue.put(error_msg)
                logger.error(error_msg)
                self.show_output_popup(error_msg, task_name)
            finally:
                if task_name in self.current_tasks:
                    del self.current_tasks[task_name]
                self.stop_progress()

        self.current_tasks[task_name] = True
        self.task_queue.put((task_wrapper, timeout))
        threading.Thread(target=self.process_task_queue, daemon=True).start()

    def process_task_queue(self):
        while not self.task_queue.empty() and self.running:
            try:
                task_func, timeout = self.task_queue.get(timeout=1)
                future = self.executor.submit(task_func)
                future.result(timeout=timeout)
            except queue.Empty:
                break
            except Exception as e:
                self.log_queue.put(f"Task execution failed: {e}")
                logger.error(f"Task execution failed: {e}")
            finally:
                self.task_queue.task_done()

    def update_log_display(self):
        while self.running:
            try:
                message = self.log_queue.get_nowait()
                if not self.log_paused:
                    self.log_display.configure(state="normal")
                    self.log_display.insert("end", message + "\n")
                    self.log_display.see("end")
                    self.log_display.configure(state="disabled")
                self.output_history.append(message)
            except queue.Empty:
                pass
            time.sleep(0.1)

    def clear_log(self):
        self.log_display.configure(state="normal")
        self.log_display.delete("1.0", "end")
        self.log_display.configure(state="disabled")
        self.output_history.clear()
        self.log_queue.put("Log cleared.")

    def pause_log(self):
        self.log_paused = not self.log_paused
        self.pause_btn.configure(text="▶ Resume" if self.log_paused else "⏸ Pause")
        if not self.log_paused:
            self.log_display.configure(state="normal")
            for message in self.output_history[-100:]:
                self.log_display.insert("end", message + "\n")
            self.log_display.see("end")
            self.log_display.configure(state="disabled")

    def export_logs(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Export Logs")
        if file_path:
            with open(file_path, "w") as f:
                f.write("\n".join(self.output_history))
            self.log_queue.put(f"Logs exported to {file_path}")

    def run_custom_command(self):
        command = self.command_entry.get()
        if command:
            try:
                result = tools.run_command(command, self.command_history_log, timeout=self.default_timeout)
                output = f"Command '{command}' output:\n{result}"
                self.show_output_popup(output, "Custom Command")
            except Exception as e:
                self.show_output_popup(f"Command '{command}' failed: {e}", "Custom Command")
        else:
            self.show_output_popup("No command entered.", "Custom Command")

    def open_cmd(self):
        subprocess.run("start cmd", shell=True)
        self.log_queue.put("Opened Command Prompt.")

    def open_powershell(self):
        subprocess.run("start powershell", shell=True)
        self.log_queue.put("Opened PowerShell.")

    def add_to_favorites(self, feature):
        for i in range(len(self.favorites)):
            if self.favorites[i] is None:
                self.favorites[i] = feature
                self.update_favorites_display()
                self.save_config()
                self.log_queue.put(f"Added '{feature}' to favorites at slot {i+1}.")
                return
        self.log_queue.put("Favorites list is full. Remove an item first.")

    def remove_from_favorites(self, idx):
        if self.favorites[idx]:
            feature = self.favorites[idx]
            self.favorites[idx] = None
            self.update_favorites_display()
            self.save_config()
            self.log_queue.put(f"Removed '{feature}' from favorites at slot {idx+1}.")

    def run_favorite(self, idx):
        feature = self.favorites[idx]
        if feature:
            self.run_feature(feature)

    def update_favorites_display(self):
        try:
            for widget in self.favorites_grid.winfo_children():
                widget.destroy()
            for i in range(3):
                for j in range(2):
                    idx = i * 2 + j
                    text = self.favorites[idx] if idx < len(self.favorites) and self.favorites[idx] else "Empty"
                    btn = ctk.CTkButton(self.favorites_grid, text=text, width=50, height=30,
                                      font=("Segoe UI", self.font_size, "bold"),
                                      fg_color="#007bff" if text != "Empty" else "#6c757d",
                                      command=lambda idx=idx: self.run_favorite(idx) if self.favorites[idx] else None)
                    btn.grid(row=i, column=j, padx=2, pady=2, sticky="ew")
                    btn.bind("<Button-3>", lambda e, idx=idx: self.remove_from_favorites(idx))
                    if text != "Empty":
                        ToolTip(btn, FEATURE_DESCRIPTIONS.get(f"{FEATURE_ICONS.get(text, '')} {text}", "Run this favorite"))
            logger.info("Favorites display updated successfully")
        except Exception as e:
            logger.error(f"Failed to update favorites display: {str(e)}")

    def edit_favorites_popup(self):
        popup = Toplevel(self.root)
        popup.title("Edit Favorites")
        popup.configure(bg="#1f1f1f")
        popup.transient(self.root)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Edit Favorites", font=("Segoe UI", 16, "bold")).pack(pady=10)

        entries_frame = ctk.CTkFrame(popup, fg_color="#2a2a2a")
        entries_frame.pack(fill="both", expand=True, padx=10, pady=5)

        all_features = []
        for category, features in self.get_categories().items():
            all_features.extend(features)
        all_features.sort()

        self.fav_vars = [tk.StringVar(value=self.favorites[i] if self.favorites[i] else "Empty") for i in range(6)]

        for i in range(6):
            row = i // 2
            col = i % 2
            frame = ctk.CTkFrame(entries_frame, fg_color="transparent")
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            ctk.CTkLabel(frame, text=f"Slot {i+1}:", font=("Segoe UI", 12)).pack(side="left", padx=5)
            dropdown = ctk.CTkOptionMenu(frame, values=["Empty"] + all_features, variable=self.fav_vars[i], width=100)
            dropdown.pack(side="left", fill="x", expand=True)

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        save_btn = ctk.CTkButton(btn_frame, text="Save", command=lambda: self.save_favorites_from_popup(popup), fg_color="#28a745")
        save_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy, fg_color="#dc3545")
        cancel_btn.pack(side="right", padx=5)

        popup.update_idletasks()
        width = max(400, entries_frame.winfo_reqwidth() + 40)
        height = max(300, entries_frame.winfo_reqheight() + 100)
        popup.geometry(f"{width}x{height}")

    def save_favorites_from_popup(self, popup):
        for i in range(6):
            value = self.fav_vars[i].get()
            self.favorites[i] = value if value != "Empty" else None
        self.update_favorites_display()
        self.save_config()
        self.log_queue.put("Favorites updated from popup.")
        popup.destroy()

    def search_filter(self, event=None):
        search_term = self.search_entry.get().lower()
        current_tab = self.notebook.get()  # Fixed: Use get() instead of select()
        
        if not search_term:
            self.reset_tab_buttons()
            return

        categories = self.get_categories()
        all_features = []
        for category, features in categories.items():
            all_features.extend([(category, feature) for feature in features])

        filtered_features = [(cat, feat) for cat, feat in all_features if search_term in feat.lower()]

        # Clear current tab content
        tab = self.notebook.tab(current_tab)
        for widget in tab.winfo_children():
            widget.destroy()

        if not filtered_features:
            frame = ctk.CTkFrame(tab, fg_color="#1f1f1f")
            frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            ctk.CTkLabel(frame, text="No matching features found.", font=("Segoe UI", 14)).pack(pady=20)
            return

        # Create scrollable frame for search results
        frame = ctk.CTkScrollableFrame(tab, fg_color="#1f1f1f")
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        for idx, (category, feature) in enumerate(filtered_features):
            btn_text = f"{FEATURE_ICONS.get(feature, '')} {feature} ({category})"
            btn = ctk.CTkButton(frame, text=btn_text,
                                command=lambda f=feature: self.run_feature(f),
                                width=200, height=30, font=("Segoe UI", self.font_size-2), fg_color="#007bff")
            btn.grid(row=idx, column=0, padx=2, pady=2, sticky="ew")
            btn.bind("<Button-3>", lambda e, t=feature: self.add_to_favorites(t))
            ToolTip(btn, FEATURE_DESCRIPTIONS.get(f"{FEATURE_ICONS.get(feature, '')} {feature}", ""))

    def reset_tab_buttons(self):
        for tab_name in self.notebook._tab_dict.keys():
            for widget in self.notebook.tab(tab_name).winfo_children():
                widget.destroy()
        self.add_buttons_to_tabs()

    def open_settings(self):
        settings_window = Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.configure(bg="#1f1f1f")
        settings_window.transient(self.root)
        settings_window.grab_set()

        ctk.CTkLabel(settings_window, text="Settings", font=("Segoe UI", 16, "bold")).pack(pady=10)

        settings_frame = ctk.CTkFrame(settings_window, fg_color="#2a2a2a")
        settings_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(settings_frame, text="Theme:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        theme_var = tk.StringVar(value=self.theme)
        ctk.CTkOptionMenu(settings_frame, values=["Light", "Dark"], variable=theme_var).pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Update Check Interval (seconds):", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        update_interval_entry = ctk.CTkEntry(settings_frame)
        update_interval_entry.insert(0, str(self.update_check_interval))
        update_interval_entry.pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Log Level:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        log_level_var = tk.StringVar(value=self.log_level)
        ctk.CTkOptionMenu(settings_frame, values=["DEBUG", "INFO", "WARNING", "ERROR"], variable=log_level_var).pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Language:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        language_var = tk.StringVar(value=self.language)
        ctk.CTkOptionMenu(settings_frame, values=["English", "Spanish", "French"], variable=language_var).pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Default Timeout (seconds):", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        timeout_entry = ctk.CTkEntry(settings_frame)
        timeout_entry.insert(0, str(self.default_timeout))
        timeout_entry.pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Font Size:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        font_size_entry = ctk.CTkEntry(settings_frame)
        font_size_entry.insert(0, str(self.font_size))
        font_size_entry.pack(fill="x", padx=5, pady=2)

        show_welcome_var = tk.BooleanVar(value=self.show_welcome)
        ctk.CTkCheckBox(settings_frame, text="Show Welcome Screen", variable=show_welcome_var).pack(anchor="w", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Default Tab:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        default_tab_var = tk.StringVar(value=self.default_tab)
        ctk.CTkOptionMenu(settings_frame, values=["Security", "Monitoring", "Utility", "Network", "Backup", "Advanced", "IT Support"], variable=default_tab_var).pack(fill="x", padx=5, pady=2)

        def save_settings():
            self.theme = theme_var.get()
            self.update_check_interval = int(update_interval_entry.get())
            self.log_level = log_level_var.get()
            self.language = language_var.get()
            self.default_timeout = int(timeout_entry.get())
            self.font_size = int(font_size_entry.get())
            self.show_welcome = show_welcome_var.get()
            self.default_tab = default_tab_var.get()
            ctk.set_appearance_mode(self.theme.lower())
            logger.setLevel(getattr(logging, self.log_level, logging.INFO))
            self.save_config()
            self.update_favorites_display()
            self.log_queue.put("Settings updated.")
            settings_window.destroy()

        btn_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        save_btn = ctk.CTkButton(btn_frame, text="Save", command=save_settings, fg_color="#28a745")
        save_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=settings_window.destroy, fg_color="#dc3545")
        cancel_btn.pack(side="right", padx=5)

        settings_window.update_idletasks()
        width = max(400, settings_frame.winfo_reqwidth() + 40)
        height = max(500, settings_frame.winfo_reqheight() + 100)
        settings_window.geometry(f"{width}x{height}")

    def show_welcome_screen(self):
        welcome_window = Toplevel(self.root)
        welcome_window.title("Welcome to SlingShot")
        welcome_window.configure(bg="#1f1f1f")
        welcome_window.transient(self.root)
        welcome_window.grab_set()

        ctk.CTkLabel(welcome_window, text="Welcome to SlingShot IT Security Toolkit", font=("Segoe UI", 18, "bold")).pack(pady=20)
        ctk.CTkLabel(welcome_window, text="Your all-in-one solution for IT security and system management.", font=("Segoe UI", 14), wraplength=400).pack(pady=10)
        ctk.CTkLabel(welcome_window, text="Features:\n- Security Tools\n- System Monitoring\n- Network Utilities\n- Backup Solutions\n- Advanced IT Support", font=("Segoe UI", 12), justify="left").pack(pady=10, anchor="w", padx=20)
        ctk.CTkButton(welcome_window, text="Get Started", command=welcome_window.destroy, fg_color="#28a745").pack(pady=20)

        welcome_window.update_idletasks()
        width = max(500, welcome_window.winfo_reqwidth() + 40)
        height = max(400, welcome_window.winfo_reqheight() + 40)
        welcome_window.geometry(f"{width}x{height}")

    def check_scheduled_tasks(self):
        while self.running:
            current_time = datetime.now()
            for task in self.scheduled_tasks[:]:
                if task["time"] <= current_time:
                    self.queue_task(task["func"], task["timeout"], task["name"])
                    if task["recurring"]:
                        task["time"] = current_time + timedelta(seconds=task["interval"])
                    else:
                        self.scheduled_tasks.remove(task)
            time.sleep(1)

    def collect_analytics(self):
        while self.running:
            try:
                with self.lock:
                    cpu = psutil.cpu_percent(interval=1)
                    mem = psutil.virtual_memory().percent
                    disk = psutil.disk_usage('/').percent
                    self.analytics_data['cpu'].append(cpu)
                    self.analytics_data['mem'].append(mem)
                    self.analytics_data['disk'].append(disk)
                    self.analytics_data['times'].append(time.time())
                    if len(self.analytics_data['cpu']) > 60:
                        self.analytics_data['cpu'].pop(0)
                        self.analytics_data['mem'].pop(0)
                        self.analytics_data['disk'].pop(0)
                        self.analytics_data['times'].pop(0)
                self.root.event_generate("<<UpdateAnalytics>>", when="tail")
            except tk.TclError:
                break
            time.sleep(1)

    def update_analytics_plot(self, event=None):
        try:
            with self.lock:
                times = [t - self.analytics_data['times'][0] for t in self.analytics_data['times']]
                cpu = self.analytics_data['cpu']
                mem = self.analytics_data['mem']
                disk = self.analytics_data['disk']

            self.ax.clear()
            self.ax.plot(times, cpu, label='CPU (%)', color='red')
            self.ax.plot(times, mem, label='Memory (%)', color='blue')
            self.ax.plot(times, disk, label='Disk (%)', color='green')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Usage (%)')
            self.ax.set_title('System Resource Usage')
            self.ax.legend()
            self.ax.grid(True)
            self.canvas.draw()
        except tk.TclError:
            pass

    def update_health_periodically(self):
        while self.running:
            try:
                self.log_queue.put("System health check placeholder (check_system_health not implemented)")
            except Exception as e:
                self.log_queue.put(f"System health check failed: {e}")
            time.sleep(300)

    def kill_program(self):
        self.running = False
        
        tools.terminate_subprocesses()
        
        while not self.task_queue.empty():
            try:
                self.task_queue.get_nowait()
                self.task_queue.task_done()
            except queue.Empty:
                break
        
        while not self.log_queue.empty():
            try:
                self.log_queue.get_nowait()
            except queue.Empty:
                break
        
        self.executor.shutdown(wait=False)
        
        try:
            self.root.quit()
            self.root.destroy()
        except tk.TclError:
            pass
        
        logger.info("Application fully terminated.")
        os._exit(0)

    def get_categories(self):
        categories = {
            "Security": [
                "Generate Key", "Encrypt File", "Decrypt File", "Hash File", "Shred File",
                "Password Manager", "OTP Generator", "BitLocker Status", "Secure Boot Check",
                "Harden Sys", "AV Status", "Malware Scanner", "Phishing Detector",
                "Firewall Manager", "USB Lockdown", "Password Policy Enforcer", "Secure File Transfer",
                "Vuln Scan", "Audit Policy Viewer"
            ],
            "Monitoring": [
                "Resource Monitor", "Service Monitor", "Real-Time Alerts", "CPU Temperature Monitor",
                "Network Latency Graph", "Event Log Analyzer", "Disk I/O Monitor",
                "System Uptime Tracker", "Alert Scheduler", "Network Connection Anomaly Detector",
                "File System Anomaly Scanner", "Service Behavior Profiler", "Registry Anomaly Detector",
                "Network Intrusion Detection", "User Activity Logger", "Process Heatmap"
            ],
            "Utility": [
                "System Info", "Clear Temp Files", "List Users", "Check Disk Health",
                "List Environment Vars", "File Permissions Viewer", "Registry Manager",
                "Shortcut Creator", "Recycle Bin Manager", "File Integrity Checker",
                "Text Encoder/Decoder", "Screen Capture Tool", "PDF Merger", "Folder Sync",
                "Duplicate File Finder", "System Tray Manager", "Clipboard Manager", "Batch File Renamer"
            ],
            "Network": [
                "Network Monitor", "Port Scanner", "Wi-Fi Analyzer", "DNS Resolver", "Packet Sniffer",
                "Bandwidth Limiter", "Sniff Browser Activity", "Dynamic DNS Resolver Monitor",
                "Network Packet Entropy Analyzer"
            ],
            "Backup": [
                "Backup Manager", "Backup Verifier", "Backup Scheduler", "Differential Backup Tool",
                "Backup Encryption Key Manager", "Cloud Backup Uploader", "Shadow Copy Manager",
                "File Recovery Tool", "System Restore Point Creator"
            ],
            "Advanced": [
                "Process Manager", "Process Injection Detector", "Process Hollowing Detector",
                "Memory Leak Detector", "Memory Forensics Lite", "Kernel Driver Enumerator",
                "Thread Stack Analyzer", "Privilege Escalation Checker", "Keylogger Detector",
                "Task Kill By Name", "System Call Tracer", "Secure Boot Policy Editor",
                "System Control", "DNS Cache Cleaner", "Driver Manager", "Boot Manager",
                "Sys Info Export", "BIOS Info", "Remote Desktop Toggle", "Power Plan Manager",
                "Command History", "Group Policy Viewer", "Windows Feature Manager",
                "Multi-Monitor Config", "Event Log Cleaner", "Driver Verifier", "System File Checker",
                "Performance Benchmark", "Startup Items", "Startup Optimizer"
            ],
            "IT Support": [
                "Remote Assistance Tool", "User Account Manager", "System Diagnostic Report",
                "Service Dependency Viewer", "Hardware Inventory Tool", "Scheduled Task Manager",
                "Event Log Manager"
            ],
            "Reconnaissance": [
                "Sublist3r", "crt.sh", "Censys", "Slack Notify"
            ]
        }
        # Merge with custom tools
        for category, tools_list in self.custom_tools.items():
            if category in categories:
                categories[category].extend([tool for tool in tools_list if tool not in categories[category]])
            else:
                categories[category] = tools_list
        logger.info(f"Categories retrieved: {list(categories.keys())}")
        return categories

    def setup_gui(self):
        logger.info("Starting GUI setup")
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        logger.info("Grid configured")

        top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        top_frame.grid_columnconfigure(1, weight=1)
        logger.info("Top frame created")

        manage_tools_btn = ctk.CTkButton(top_frame, text="Manage Tools", command=self.manage_tools, width=80, fg_color="#28a745", hover_color="#218838")
        manage_tools_btn.grid(row=0, column=0, padx=5, pady=5)

        self.search_entry = ctk.CTkEntry(top_frame, placeholder_text="Search all tools...", width=150)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.search_filter)
        logger.info("Search entry added")

        self.progress_bar = ctk.CTkProgressBar(top_frame, width=150)
        self.progress_bar.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.progress_bar.set(0)
        self.progress_label = ctk.CTkLabel(top_frame, text="", font=("Segoe UI", 12))
        self.progress_label.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        logger.info("Progress bar and label added")

        self.command_entry = ctk.CTkEntry(top_frame, placeholder_text="Run command...", width=150)
        self.command_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        run_btn = ctk.CTkButton(top_frame, text="Run", command=self.run_custom_command, width=80, fg_color="#28a745", hover_color="#218838")
        run_btn.grid(row=0, column=5, padx=5, pady=5)
        cmd_btn = ctk.CTkButton(top_frame, text="CMD", command=self.open_cmd, width=80, fg_color="#c0c0c0", hover_color="#a9a9a9", text_color="black")
        cmd_btn.grid(row=0, column=6, padx=5, pady=5)
        powershell_btn = ctk.CTkButton(top_frame, text="PowerShell", command=self.open_powershell, width=80)
        powershell_btn.grid(row=0, column=7, padx=5, pady=5)
        kill_btn = ctk.CTkButton(top_frame, text="Kill", command=self.kill_program, width=80, fg_color="#dc3545", hover_color="#c82333")
        kill_btn.grid(row=0, column=8, padx=5, pady=5)
        settings_btn = ctk.CTkButton(top_frame, text="⚙️ Settings", command=self.open_settings, width=80)
        settings_btn.grid(row=0, column=9, padx=5, pady=5)
        logger.info("Command entry and buttons added, with Manage Tools button")

        self.left_frame = ctk.CTkFrame(self.root, width=250, fg_color="#2a2a2a")
        self.left_frame.grid(row=1, column=0, sticky="nsew", padx=(5, 0), pady=5)
        self.left_frame.grid_propagate(False)
        logger.info("Left frame created")

        favorites_frame = ctk.CTkFrame(self.left_frame, fg_color="#1f1f1f", corner_radius=10)
        favorites_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame = ctk.CTkFrame(favorites_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(header_frame, text="⭐ FAVORITES", font=("Segoe UI", 14, "bold")).pack(side="left", padx=5)
        edit_fav_btn = ctk.CTkButton(header_frame, text="✏️", command=self.edit_favorites_popup, width=30)
        edit_fav_btn.pack(side="right", padx=5)
        self.favorites_grid = ctk.CTkFrame(favorites_frame, fg_color="transparent")
        self.favorites_grid.pack(fill="both", expand=True, padx=5, pady=5)
        self.update_favorites_display()
        logger.info("Favorites frame added")

        logs_frame = ctk.CTkFrame(self.left_frame, fg_color="#444444", corner_radius=10)
        logs_frame.pack(fill="both", expand=True, padx=10, pady=5)
        logs_frame.grid_rowconfigure(1, weight=1)
        logs_frame.grid_columnconfigure(0, weight=1)

        log_label = ctk.CTkLabel(logs_frame, text="📜 LIVE LOGS", font=("Segoe UI", 14, "bold"))
        log_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        self.log_display = ctk.CTkTextbox(logs_frame, wrap="word", font=("Segoe UI", self.font_size), fg_color="#333333", state="disabled")
        self.log_display.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

        scrollbar = ctk.CTkScrollbar(logs_frame, command=self.log_display.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.log_display.configure(yscrollcommand=scrollbar.set)

        btn_frame = ctk.CTkFrame(logs_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        clear_btn = ctk.CTkButton(btn_frame, text="🗑️Clear", command=self.clear_log, width=80, fg_color="#ffc107", hover_color="#e0a800")
        clear_btn.grid(row=0, column=0, padx=2)
        self.pause_btn = ctk.CTkButton(btn_frame, text="⏸ Pause", command=self.pause_log, width=80)
        self.pause_btn.grid(row=0, column=1, padx=2)
        export_btn = ctk.CTkButton(btn_frame, text="💾 Export", command=self.export_logs, width=80)
        export_btn.grid(row=0, column=2, padx=2)
        logger.info("Logs frame added")

        self.main_frame = ctk.CTkFrame(self.root, fg_color="#1f1f1f")
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        logger.info("Main frame created")

        self.notebook = ctk.CTkTabview(self.main_frame, width=800, height=600, fg_color="#1f1f1f")
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        self.tab_colors = {
            "Security": "#ff4d4d",
            "Monitoring": "#4da8ff",
            "Utility": "#ffcc00",
            "Network": "#00cc66",
            "Backup": "#cc00ff",
            "Advanced": "#ff8000",
            "IT Support": "#ff66b3",
            "Reconnaissance": "#66b3ff"
        }
        logger.info("Tabview created")

        categories = self.get_categories()
        for tab_name in categories.keys():
            self.notebook.add(tab_name)
            self.notebook.tab(tab_name).grid_rowconfigure(0, weight=1)
            self.notebook.tab(tab_name).grid_columnconfigure(0, weight=1)
            self.notebook._tab_dict[tab_name].configure(fg_color="#1f1f1f")
            if tab_name in self.tab_colors:
                self.notebook._segmented_button._buttons_dict[tab_name].configure(fg_color=self.tab_colors[tab_name])
            else:
                logger.warning(f"No color defined for tab: {tab_name}")
                self.notebook._segmented_button._buttons_dict[tab_name].configure(fg_color="#2a2a2a")
        logger.info(f"Tabs added: {list(categories.keys())}")

        self.add_buttons_to_tabs()

        try:
            self.notebook.set(self.default_tab)
            logger.info(f"Set default tab to {self.default_tab}")
        except ValueError:
            logger.warning(f"Tab '{self.default_tab}' not found, falling back to 'Security'")
            self.notebook.set("Security")

        self.root.bind("<<UpdateAnalytics>>", self.update_analytics_plot)

    def manage_tools(self):
        popup = Toplevel(self.root)
        popup.title("Manage Tools")
        popup.configure(bg="#1f1f1f")
        popup.transient(self.root)
        popup.grab_set()

        # Create a scrollable frame for the entire popup
        main_frame = ctk.CTkScrollableFrame(popup, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        notebook = ctk.CTkTabview(main_frame, fg_color="#2a2a2a")
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Add Tool Tab
        add_tab = notebook.add("Add Tool")
        self._create_new_tool_popup(add_tab, popup)

        # Remove Tool Tab
        remove_tab = notebook.add("Remove Tool")
        self._remove_custom_tool_popup(remove_tab, popup)

        # Calculate size based on content
        popup.update_idletasks()
        width = min(max(500, main_frame.winfo_reqwidth() + 40), 1000)  # Dynamic width with max 1000
        height = min(600, main_frame.winfo_reqheight() + 40)  # Dynamic height with max 600
        popup.geometry(f"{width}x{height}")
        popup.minsize(400, 300)
        logger.info(f"Manage Tools popup created with dynamic sizing: {width}x{height}")

    def _create_new_tool_popup(self, parent, popup):
        main_frame = ctk.CTkFrame(parent, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="Tool Name:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ctk.CTkEntry(main_frame, placeholder_text="Enter tool name", width=200)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(main_frame, text="Category:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        categories = list(self.get_categories().keys())
        category_var = tk.StringVar(value=categories[0])
        category_dropdown = ctk.CTkOptionMenu(main_frame, values=categories, variable=category_var, width=200)
        category_dropdown.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(main_frame, text="Script Type:", font=("Segoe UI", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        script_type_var = tk.StringVar(value="Batch")
        script_type_dropdown = ctk.CTkOptionMenu(main_frame, values=["Batch", "PowerShell"], variable=script_type_var, width=200)
        script_type_dropdown.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(main_frame, text="Script:", font=("Segoe UI", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        script_text = ctk.CTkTextbox(main_frame, width=400, height=300, font=("Segoe UI", 12))
        script_text.grid(row=3, column=1, padx=5, pady=5)

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        save_btn = ctk.CTkButton(btn_frame, text="Save", 
                                 command=lambda: self.save_new_tool(name_entry.get(), category_var.get(), script_text.get("1.0", "end-1c"), script_type_var.get(), popup), 
                                 fg_color="#28a745")
        save_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy, fg_color="#dc3545")
        cancel_btn.pack(side="right", padx=5)

    def _remove_custom_tool_popup(self, parent, popup):
        all_tools = []
        for category, tools_list in self.custom_tools.items():
            all_tools.extend([(tool, category) for tool in tools_list])
        
        main_frame = ctk.CTkFrame(parent, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if not all_tools:
            ctk.CTkLabel(main_frame, text="No custom tools available to remove.", font=("Segoe UI", 12)).pack(pady=20)
            return

        ctk.CTkLabel(main_frame, text="Select Tool to Remove:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tool_options = [f"{tool} ({category})" for tool, category in all_tools]
        tool_var = tk.StringVar(value=tool_options[0] if tool_options else "")
        tool_dropdown = ctk.CTkOptionMenu(main_frame, values=tool_options, variable=tool_var, width=200)
        tool_dropdown.grid(row=0, column=1, padx=5, pady=5)

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        remove_btn = ctk.CTkButton(btn_frame, text="Remove", 
                                   command=lambda: self._execute_remove_tool(tool_var.get().split(" (")[0], all_tools, popup), 
                                   fg_color="#dc3545")
        remove_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy, fg_color="#6c757d")
        cancel_btn.pack(side="right", padx=5)

    def save_new_tool(self, name, category, script, script_type, popup):
        logger.info(f"Attempting to save new tool: Name={name}, Category={category}, Script length={len(script)}, Type={script_type}")
        if not name or not script.strip():
            messagebox.showerror("Error", "Tool name and script are required.", parent=popup)
            logger.warning("Save aborted: Empty name or script")
            return
        
        try:
            import os
            import json
            import importlib
            
            tools_dir = "custom_tools"
            if not os.path.exists(tools_dir):
                os.makedirs(tools_dir)
                logger.info(f"Created directory: {tools_dir}")
            if not os.path.exists(os.path.join(tools_dir, "__init__.py")):
                with open(os.path.join(tools_dir, "__init__.py"), "w") as f:
                    f.write("")
                logger.info("Created __init__.py in custom_tools directory")
            
            safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in name.lower())
            ext = ".bat" if script_type == "Batch" else ".ps1"
            script_file = os.path.join(tools_dir, f"{safe_name}{ext}")
            
            with open(script_file, "w") as f:
                f.write(script)
            logger.info(f"Saved {script_type} script to: {script_file}")
            
            custom_tools_file = "custom_tools.py"
            if not os.path.exists(custom_tools_file):
                with open(custom_tools_file, "w") as f:
                    f.write("# Custom tools dynamically added\nSCRIPT_REGISTRY = {}\n")
                logger.info(f"Created {custom_tools_file}")
            
            with open(custom_tools_file, "r") as f:
                content = f.read()
            if "SCRIPT_REGISTRY" not in content:
                with open(custom_tools_file, "w") as f:
                    f.write("# Custom tools dynamically added\nSCRIPT_REGISTRY = {}\n")
            with open(custom_tools_file, "r") as f:
                lines = f.readlines()
            with open(custom_tools_file, "w") as f:
                for line in lines:
                    if not line.startswith("SCRIPT_REGISTRY"):
                        f.write(line)
                registry_line = f"SCRIPT_REGISTRY['{safe_name}'] = {{'type': '{script_type.lower()}', 'path': r'{script_file}'}}\n"
                f.write(registry_line)
            logger.info(f"Updated SCRIPT_REGISTRY in {custom_tools_file}")
            
            metadata_file = os.path.join(tools_dir, "custom_tools.json")
            metadata = {}
            if os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
            
            metadata[name] = {"category": category, "file": script_file, "type": script_type.lower()}
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=4)
            logger.info(f"Updated metadata in {metadata_file}")
            
            importlib.reload(custom_tools)
            logger.info("Reloaded custom_tools module")
            
            self.add_custom_tool(name, category, script_type.lower(), script_file)
            self.log_queue.put(f"New {script_type} tool '{name}' added to {category}")
            popup.destroy()
            logger.info(f"New {script_type} tool '{name}' successfully added and popup closed")
        except Exception as e:
            error_msg = f"Failed to save tool '{name}': {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("Error", error_msg, parent=popup)

    def _execute_remove_tool(self, tool_name, all_tools, popup):
        try:
            import os
            import json
            import importlib

            category = next(cat for t, cat in all_tools if t == tool_name)

            metadata_file = os.path.join("custom_tools", "custom_tools.json")
            with open(metadata_file, "r") as f:
                metadata = json.load(f)

            script_file = metadata[tool_name]["file"]
            if os.path.exists(script_file):
                os.remove(script_file)
                logger.info(f"Deleted script file: {script_file}")

            del metadata[tool_name]
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=4)
            logger.info(f"Removed '{tool_name}' from {metadata_file}")

            custom_tools_file = "custom_tools.py"
            with open(custom_tools_file, "r") as f:
                lines = f.readlines()
            with open(custom_tools_file, "w") as f:
                safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in tool_name.lower())
                for line in lines:
                    if safe_name not in line:
                        f.write(line)
            importlib.reload(custom_tools)
            logger.info(f"Removed '{tool_name}' from {custom_tools_file} and reloaded module")

            self.custom_tools[category].remove(tool_name)
            if not self.custom_tools[category]:
                del self.custom_tools[category]
            logger.info(f"Removed '{tool_name}' from self.custom_tools")

            self.reset_tab_buttons()
            self.add_buttons_to_tabs()
            self.notebook.update_idletasks()
            self.log_queue.put(f"Tool '{tool_name}' removed successfully")
            popup.destroy()
        except Exception as e:
            error_msg = f"Failed to remove tool '{tool_name}': {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("Error", error_msg, parent=popup)

    def open_settings(self):
        settings_window = Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.configure(bg="#1f1f1f")
        settings_window.transient(self.root)
        settings_window.grab_set()

        # Create a scrollable frame for the settings content
        main_frame = ctk.CTkScrollableFrame(settings_window, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="Settings", font=("Segoe UI", 16, "bold")).pack(pady=10)

        settings_frame = ctk.CTkFrame(main_frame, fg_color="#2a2a2a")
        settings_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(settings_frame, text="Theme:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        theme_var = tk.StringVar(value=self.theme)
        ctk.CTkOptionMenu(settings_frame, values=["Light", "Dark"], variable=theme_var).pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Update Check Interval (seconds):", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        update_interval_entry = ctk.CTkEntry(settings_frame)
        update_interval_entry.insert(0, str(self.update_check_interval))
        update_interval_entry.pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Log Level:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        log_level_var = tk.StringVar(value=self.log_level)
        ctk.CTkOptionMenu(settings_frame, values=["DEBUG", "INFO", "WARNING", "ERROR"], variable=log_level_var).pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Language:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        language_var = tk.StringVar(value=self.language)
        ctk.CTkOptionMenu(settings_frame, values=["English", "Spanish", "French"], variable=language_var).pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Default Timeout (seconds):", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        timeout_entry = ctk.CTkEntry(settings_frame)
        timeout_entry.insert(0, str(self.default_timeout))
        timeout_entry.pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Font Size:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        font_size_entry = ctk.CTkEntry(settings_frame)
        font_size_entry.insert(0, str(self.font_size))
        font_size_entry.pack(fill="x", padx=5, pady=2)

        show_welcome_var = tk.BooleanVar(value=self.show_welcome)
        ctk.CTkCheckBox(settings_frame, text="Show Welcome Screen", variable=show_welcome_var).pack(anchor="w", padx=5, pady=2)

        ctk.CTkLabel(settings_frame, text="Default Tab:", font=("Segoe UI", 12)).pack(anchor="w", padx=5, pady=2)
        default_tab_var = tk.StringVar(value=self.default_tab)
        ctk.CTkOptionMenu(settings_frame, values=["Security", "Monitoring", "Utility", "Network", "Backup", "Advanced", "IT Support"], variable=default_tab_var).pack(fill="x", padx=5, pady=2)

        def save_settings():
            self.theme = theme_var.get()
            self.update_check_interval = int(update_interval_entry.get())
            self.log_level = log_level_var.get()
            self.language = language_var.get()
            self.default_timeout = int(timeout_entry.get())
            self.font_size = int(font_size_entry.get())
            self.show_welcome = show_welcome_var.get()
            self.default_tab = default_tab_var.get()
            ctk.set_appearance_mode(self.theme.lower())
            logger.setLevel(getattr(logging, self.log_level, logging.INFO))
            self.save_config()
            self.update_favorites_display()
            self.log_queue.put("Settings updated.")
            settings_window.destroy()

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        save_btn = ctk.CTkButton(btn_frame, text="Save", command=save_settings, fg_color="#28a745")
        save_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=settings_window.destroy, fg_color="#dc3545")
        cancel_btn.pack(side="right", padx=5)

        # Calculate size based on content
        settings_window.update_idletasks()
        width = min(max(400, main_frame.winfo_reqwidth() + 40), 1000)
        height = min(600, main_frame.winfo_reqheight() + 40)
        settings_window.geometry(f"{width}x{height}")
        settings_window.minsize(400, 300)
        logger.info(f"Settings popup created with dynamic sizing: {width}x{height}")

    def show_welcome_screen(self):
        welcome_window = Toplevel(self.root)
        welcome_window.title("Welcome to SlingShot")
        welcome_window.configure(bg="#1f1f1f")
        welcome_window.transient(self.root)
        welcome_window.grab_set()

        # Create a scrollable frame for the welcome content
        main_frame = ctk.CTkScrollableFrame(welcome_window, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="Welcome to SlingShot IT Security Toolkit", font=("Segoe UI", 18, "bold")).pack(pady=20)
        ctk.CTkLabel(main_frame, text="Your all-in-one solution for IT security and system management.", font=("Segoe UI", 14), wraplength=400).pack(pady=10)
        ctk.CTkLabel(main_frame, text="Features:\n- Security Tools\n- System Monitoring\n- Network Utilities\n- Backup Solutions\n- Advanced IT Support", font=("Segoe UI", 12), justify="left").pack(pady=10, anchor="w", padx=20)
        ctk.CTkButton(main_frame, text="Get Started", command=welcome_window.destroy, fg_color="#28a745").pack(pady=20)

        # Calculate size based on content
        welcome_window.update_idletasks()
        width = min(max(500, main_frame.winfo_reqwidth() + 40), 1000)
        height = min(600, main_frame.winfo_reqheight() + 40)
        welcome_window.geometry(f"{width}x{height}")
        welcome_window.minsize(400, 300)
        logger.info(f"Welcome Screen popup created with dynamic sizing: {width}x{height}")

    def check_scheduled_tasks(self):
        while self.running:
            current_time = datetime.now()
            for task in self.scheduled_tasks[:]:
                if task["time"] <= current_time:
                    self.queue_task(task["func"], task["timeout"], task["name"])
                    if task["recurring"]:
                        task["time"] = current_time + timedelta(seconds=task["interval"])
                    else:
                        self.scheduled_tasks.remove(task)
            time.sleep(1)

    def collect_analytics(self):
        while self.running:
            try:
                with self.lock:
                    cpu = psutil.cpu_percent(interval=1)
                    mem = psutil.virtual_memory().percent
                    disk = psutil.disk_usage('/').percent
                    self.analytics_data['cpu'].append(cpu)
                    self.analytics_data['mem'].append(mem)
                    self.analytics_data['disk'].append(disk)
                    self.analytics_data['times'].append(time.time())
                    if len(self.analytics_data['cpu']) > 60:
                        self.analytics_data['cpu'].pop(0)
                        self.analytics_data['mem'].pop(0)
                        self.analytics_data['disk'].pop(0)
                        self.analytics_data['times'].pop(0)
                self.root.event_generate("<<UpdateAnalytics>>", when="tail")
            except tk.TclError:
                break
            time.sleep(1)

    def update_analytics_plot(self, event=None):
        try:
            with self.lock:
                times = [t - self.analytics_data['times'][0] for t in self.analytics_data['times']]
                cpu = self.analytics_data['cpu']
                mem = self.analytics_data['mem']
                disk = self.analytics_data['disk']

            self.ax.clear()
            self.ax.plot(times, cpu, label='CPU (%)', color='red')
            self.ax.plot(times, mem, label='Memory (%)', color='blue')
            self.ax.plot(times, disk, label='Disk (%)', color='green')
            self.ax.set_xlabel('Time (s)', color='white')
            self.ax.set_ylabel('Usage (%)', color='white')
            self.ax.set_title('System Resource Usage', color='white')
            self.ax.legend(facecolor='#2a2a2a', edgecolor='white', labelcolor='white')
            self.ax.grid(True, color='gray', linestyle='--', alpha=0.7)
            self.ax.set_facecolor('#333333')
            self.ax.tick_params(colors='white')
            self.canvas.figure.set_facecolor('#2a2a2a')
            self.canvas.figure.subplots_adjust(bottom=0.2)  # Add padding to the bottom to prevent cutoff
            self.canvas.draw()
        except tk.TclError:
            pass

    def update_health_periodically(self):
        while self.running:
            try:
                self.log_queue.put("System health check placeholder (check_system_health not implemented)")
            except Exception as e:
                self.log_queue.put(f"System health check failed: {e}")
            time.sleep(300)

    def kill_program(self):
        self.running = False
        
        tools.terminate_subprocesses()
        
        while not self.task_queue.empty():
            try:
                self.task_queue.get_nowait()
                self.task_queue.task_done()
            except queue.Empty:
                break
        
        while not self.log_queue.empty():
            try:
                self.log_queue.get_nowait()
            except queue.Empty:
                break
        
        self.executor.shutdown(wait=False)
        
        try:
            self.root.quit()
            self.root.destroy()
        except tk.TclError:
            pass
        
        logger.info("Application fully terminated.")
        os._exit(0)

    def get_categories(self):
        categories = {
            "Security": [
                "Generate Key", "Encrypt File", "Decrypt File", "Hash File", "Shred File",
                "Password Manager", "OTP Generator", "BitLocker Status", "Secure Boot Check",
                "Harden Sys", "AV Status", "Malware Scanner", "Phishing Detector",
                "Firewall Manager", "USB Lockdown", "Password Policy Enforcer", "Secure File Transfer",
                "Vuln Scan", "Audit Policy Viewer"
            ],
            "Monitoring": [
                "Resource Monitor", "Service Monitor", "Real-Time Alerts", "CPU Temperature Monitor",
                "Network Latency Graph", "Event Log Analyzer", "Disk I/O Monitor",
                "System Uptime Tracker", "Alert Scheduler", "Network Connection Anomaly Detector",
                "File System Anomaly Scanner", "Service Behavior Profiler", "Registry Anomaly Detector",
                "Network Intrusion Detection", "User Activity Logger", "Process Heatmap"
            ],
            "Utility": [
                "System Info", "Clear Temp Files", "List Users", "Check Disk Health",
                "List Environment Vars", "File Permissions Viewer", "Registry Manager",
                "Shortcut Creator", "Recycle Bin Manager", "File Integrity Checker",
                "Text Encoder/Decoder", "Screen Capture Tool", "PDF Merger", "Folder Sync",
                "Duplicate File Finder", "System Tray Manager", "Clipboard Manager", "Batch File Renamer"
            ],
            "Network": [
                "Network Monitor", "Port Scanner", "Wi-Fi Analyzer", "DNS Resolver", "Packet Sniffer",
                "Bandwidth Limiter", "Sniff Browser Activity", "Dynamic DNS Resolver Monitor",
                "Network Packet Entropy Analyzer"
            ],
            "Backup": [
                "Backup Manager", "Backup Verifier", "Backup Scheduler", "Differential Backup Tool",
                "Backup Encryption Key Manager", "Cloud Backup Uploader", "Shadow Copy Manager",
                "File Recovery Tool", "System Restore Point Creator"
            ],
            "Advanced": [
                "Process Manager", "Process Injection Detector", "Process Hollowing Detector",
                "Memory Leak Detector", "Memory Forensics Lite", "Kernel Driver Enumerator",
                "Thread Stack Analyzer", "Privilege Escalation Checker", "Keylogger Detector",
                "Task Kill By Name", "System Call Tracer", "Secure Boot Policy Editor",
                "System Control", "DNS Cache Cleaner", "Driver Manager", "Boot Manager",
                "Sys Info Export", "BIOS Info", "Remote Desktop Toggle", "Power Plan Manager",
                "Command History", "Group Policy Viewer", "Windows Feature Manager",
                "Multi-Monitor Config", "Event Log Cleaner", "Driver Verifier", "System File Checker",
                "Performance Benchmark", "Startup Items", "Startup Optimizer"
            ],
            "IT Support": [
                "Remote Assistance Tool", "User Account Manager", "System Diagnostic Report",
                "Service Dependency Viewer", "Hardware Inventory Tool", "Scheduled Task Manager",
                "Event Log Manager"
            ],
            "Reconnaissance": [
                "Sublist3r", "crt.sh", "Censys", "Slack Notify"
            ]
        }
        # Merge with custom tools
        for category, tools_list in self.custom_tools.items():
            if category in categories:
                categories[category].extend([tool for tool in tools_list if tool not in categories[category]])
            else:
                categories[category] = tools_list
        logger.info(f"Categories retrieved: {list(categories.keys())}")
        return categories

    def edit_favorites_popup(self):
        popup = Toplevel(self.root)
        popup.title("Edit Favorites")
        popup.configure(bg="#1f1f1f")
        popup.transient(self.root)
        popup.grab_set()

        # Create a scrollable frame for the favorites content
        main_frame = ctk.CTkScrollableFrame(popup, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="Edit Favorites", font=("Segoe UI", 16, "bold")).pack(pady=10)

        entries_frame = ctk.CTkFrame(main_frame, fg_color="#2a2a2a")
        entries_frame.pack(fill="both", expand=True, padx=10, pady=5)

        all_features = []
        for category, features in self.get_categories().items():
            all_features.extend(features)
        all_features.sort()

        self.fav_vars = [tk.StringVar(value=self.favorites[i] if self.favorites[i] else "Empty") for i in range(6)]

        for i in range(6):
            row = i // 2
            col = i % 2
            frame = ctk.CTkFrame(entries_frame, fg_color="transparent")
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            ctk.CTkLabel(frame, text=f"Slot {i+1}:", font=("Segoe UI", 12)).pack(side="left", padx=5)
            dropdown = ctk.CTkOptionMenu(frame, values=["Empty"] + all_features, variable=self.fav_vars[i], width=100)
            dropdown.pack(side="left", fill="x", expand=True)

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        save_btn = ctk.CTkButton(btn_frame, text="Save", command=lambda: self.save_favorites_from_popup(popup), fg_color="#28a745")
        save_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy, fg_color="#dc3545")
        cancel_btn.pack(side="right", padx=5)

        # Calculate size based on content
        popup.update_idletasks()
        width = min(max(400, main_frame.winfo_reqwidth() + 40), 1000)
        height = min(600, main_frame.winfo_reqheight() + 40)
        popup.geometry(f"{width}x{height}")
        popup.minsize(400, 300)
        logger.info(f"Edit Favorites popup created with dynamic sizing: {width}x{height}")

    def save_favorites_from_popup(self, popup):
        for i in range(6):
            value = self.fav_vars[i].get()
            self.favorites[i] = value if value != "Empty" else None
        self.update_favorites_display()
        self.save_config()
        self.log_queue.put("Favorites updated from popup.")
        popup.destroy()

    def search_filter(self, event=None):
        search_term = self.search_entry.get().lower()
        current_tab = self.notebook.get()
        
        if not search_term:
            self.reset_tab_buttons()
            return

        categories = self.get_categories()
        all_features = []
        for category, features in categories.items():
            all_features.extend([(category, feature) for feature in features])

        filtered_features = [(cat, feat) for cat, feat in all_features if search_term in feat.lower()]

        tab = self.notebook.tab(current_tab)
        for widget in tab.winfo_children():
            widget.destroy()

        if not filtered_features:
            frame = ctk.CTkFrame(tab, fg_color="#1f1f1f")
            frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            ctk.CTkLabel(frame, text="No matching features found.", font=("Segoe UI", 14)).pack(pady=20)
            return

        frame = ctk.CTkScrollableFrame(tab, fg_color="#1f1f1f")
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        for idx, (category, feature) in enumerate(filtered_features):
            btn_text = f"{FEATURE_ICONS.get(feature, '')} {feature} ({category})"
            btn = ctk.CTkButton(frame, text=btn_text,
                                command=lambda f=feature: self.run_feature(f),
                                width=200, height=30, font=("Segoe UI", self.font_size-2), fg_color="#007bff")
            btn.grid(row=idx, column=0, padx=2, pady=2, sticky="ew")
            btn.bind("<Button-3>", lambda e, t=feature: self.add_to_favorites(t))
            ToolTip(btn, FEATURE_DESCRIPTIONS.get(f"{FEATURE_ICONS.get(feature, '')} {feature}", ""))

    def reset_tab_buttons(self):
        for tab_name in self.notebook._tab_dict.keys():
            for widget in self.notebook.tab(tab_name).winfo_children():
                widget.destroy()
        self.add_buttons_to_tabs()

    def show_output_popup(self, output, title):
        popup = Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="#1f1f1f")
        popup.transient(self.root)
        popup.grab_set()

        # Create a scrollable frame for the output content
        main_frame = ctk.CTkScrollableFrame(popup, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        inner_frame = ctk.CTkFrame(main_frame, fg_color="#2a2a2a")
        inner_frame.pack(fill="both", expand=True)

        inner_frame.grid_rowconfigure(0, weight=1)
        inner_frame.grid_rowconfigure(1, weight=0)
        inner_frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(1, weight=0)

        lines = output.splitlines()
        num_lines = len(lines)
        max_line_length = max(len(line) for line in lines) if lines else 1

        char_width = 8
        char_height = 20
        text_width = min(max(max_line_length * char_width, 600), 1000)
        text_height = min(max(num_lines * char_height, 400), 600)

        text_area = ctk.CTkTextbox(
            inner_frame,
            wrap="word",
            font=("Segoe UI", self.font_size),
            fg_color="#333333",
            width=text_width,
            height=text_height
        )
        text_area.insert("1.0", output)
        text_area.configure(state="disabled")
        text_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 0))

        scrollbar = ctk.CTkScrollbar(inner_frame, command=text_area.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text_area.configure(yscrollcommand=scrollbar.set)

        btn_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        export_btn = ctk.CTkButton(btn_frame, text="Export", command=lambda: self.export_output(output), fg_color="#28a745")
        export_btn.grid(row=0, column=0, sticky="e", padx=5)

        close_btn = ctk.CTkButton(btn_frame, text="Close", command=popup.destroy, fg_color="#dc3545")
        close_btn.grid(row=0, column=1, sticky="w", padx=5)

        # Calculate size based on content
        popup.update_idletasks()
        total_width = min(max(text_width + scrollbar.winfo_reqwidth() + 40, 400), 1000)
        total_height = min(600, text_height + btn_frame.winfo_reqheight() + 50)
        popup.geometry(f"{total_width}x{total_height}")
        popup.minsize(400, 300)
        logger.info(f"Output popup created with dynamic sizing: {total_width}x{total_height}")

    def add_buttons_to_tabs(self):
        try:
            categories = self.get_categories()
            logger.info("Adding buttons to tabs")
            for tab_name, features in categories.items():
                logger.info(f"Processing tab: {tab_name}")
                tab = self.notebook.tab(tab_name)
                frame = ctk.CTkFrame(tab, fg_color="#1f1f1f")
                frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

                if tab_name == "Monitoring":
                    tab.grid_rowconfigure(0, weight=0)
                    tab.grid_rowconfigure(1, weight=1)
                    tab.grid_columnconfigure(0, weight=1)
                    
                    num_tools = len(features)
                    columns_per_row = 4  
                    num_rows = (num_tools + columns_per_row - 1) // columns_per_row
                    
                    button_frame = ctk.CTkFrame(frame, fg_color="#1f1f1f")
                    button_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
                    
                    for i in range(num_rows):
                        button_frame.grid_rowconfigure(i, weight=1)
                    for j in range(columns_per_row):
                        button_frame.grid_columnconfigure(j, weight=1)
                    
                    for idx, feature in enumerate(features):
                        row = idx // columns_per_row
                        col = idx % columns_per_row
                        icon = FEATURE_ICONS.get(feature, '')
                        btn_text = f"{icon} {feature}" if icon else feature
                        logger.info(f"Creating button for {feature} with text: {btn_text}")
                        btn = ctk.CTkButton(
                            button_frame,
                            text=btn_text,
                            command=lambda f=feature: self.run_feature(f),
                            width=200,
                            height=30,
                            font=("Segoe UI Emoji", self.font_size-2),
                            fg_color="#007bff"
                        )
                        btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
                        btn.bind("<Button-3>", lambda e, t=feature: self.add_to_favorites(t))
                        ToolTip(btn, FEATURE_DESCRIPTIONS.get(f"{FEATURE_ICONS.get(feature, '')} {feature}", ""))
                    logger.info(f"Added {num_tools} buttons to Monitoring tab")
                    
                    # Add a bordered frame for the plot with adjusted size
                    plot_border_frame = ctk.CTkFrame(frame, fg_color="#2a2a2a", border_color="#007bff", border_width=2)
                    plot_border_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
                    plot_border_frame.grid_rowconfigure(0, weight=1)
                    plot_border_frame.grid_columnconfigure(0, weight=1)

                    # Increase figure size to ensure labels fit
                    self.canvas = FigureCanvasTkAgg(plt.figure(figsize=(6, 5)), master=plot_border_frame)
                    self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
                    self.ax = self.canvas.figure.add_subplot(111)
                    logger.info("Added plot area to Monitoring tab with border and adjusted size")
                else:
                    num_tools = len(features)
                    columns_per_row = 4
                    num_rows = (num_tools + columns_per_row - 1) // columns_per_row
                    
                    grid_frame = ctk.CTkFrame(frame, fg_color="#1f1f1f")
                    grid_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
                    
                    for i in range(num_rows):
                        grid_frame.grid_rowconfigure(i, weight=1)
                    for j in range(columns_per_row):
                        grid_frame.grid_columnconfigure(j, weight=1)
                    
                    for idx, feature in enumerate(features):
                        row = idx // columns_per_row
                        col = idx % columns_per_row
                        icon = FEATURE_ICONS.get(feature, '')
                        btn_text = f"{icon} {feature}" if icon else feature
                        logger.info(f"Creating button for {feature} with text: {btn_text}")
                        btn = ctk.CTkButton(
                            grid_frame,
                            text=btn_text,
                            command=lambda f=feature: self.run_feature(f),
                            width=200,
                            height=30,
                            font=("Segoe UI Emoji", self.font_size-2),
                            fg_color="#007bff"
                        )
                        btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
                        btn.bind("<Button-3>", lambda e, t=feature: self.add_to_favorites(t))
                        ToolTip(btn, FEATURE_DESCRIPTIONS.get(f"{FEATURE_ICONS.get(feature, '')} {feature}", ""))
                    logger.info(f"Added {num_tools} buttons to {tab_name} tab")
        except Exception as e:
            logger.error(f"Failed to add buttons to tabs: {str(e)}")
            raise

    def add_buttons_to_tabs(self):
        try:
            categories = self.get_categories()
            logger.info("Adding buttons to tabs")
            for tab_name, features in categories.items():
                logger.info(f"Processing tab: {tab_name}")
                tab = self.notebook.tab(tab_name)
                frame = ctk.CTkFrame(tab, fg_color="#1f1f1f")
                frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

                if tab_name == "Monitoring":
                    tab.grid_rowconfigure(0, weight=0)
                    tab.grid_rowconfigure(1, weight=1)
                    tab.grid_columnconfigure(0, weight=1)
                    
                    num_tools = len(features)
                    columns_per_row = 4  
                    num_rows = (num_tools + columns_per_row - 1) // columns_per_row
                    
                    button_frame = ctk.CTkFrame(frame, fg_color="#1f1f1f")
                    button_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
                    
                    for i in range(num_rows):
                        button_frame.grid_rowconfigure(i, weight=1)
                    for j in range(columns_per_row):
                        button_frame.grid_columnconfigure(j, weight=1)
                    
                    for idx, feature in enumerate(features):
                        row = idx // columns_per_row
                        col = idx % columns_per_row
                        icon = FEATURE_ICONS.get(feature, '')
                        btn_text = f"{icon} {feature}" if icon else feature
                        logger.info(f"Creating button for {feature} with text: {btn_text}")
                        btn = ctk.CTkButton(
                            button_frame,
                            text=btn_text,
                            command=lambda f=feature: self.run_feature(f),
                            width=200,
                            height=30,
                            font=("Segoe UI Emoji", self.font_size-2),
                            fg_color="#007bff"
                        )
                        btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
                        btn.bind("<Button-3>", lambda e, t=feature: self.add_to_favorites(t))
                        ToolTip(btn, FEATURE_DESCRIPTIONS.get(f"{FEATURE_ICONS.get(feature, '')} {feature}", ""))
                    logger.info(f"Added {num_tools} buttons to Monitoring tab")
                    
                    plot_frame = ctk.CTkFrame(frame, fg_color="#1f1f1f")
                    plot_frame.grid(row=1, column=0, sticky="n", padx=5, pady=5)
                    plot_frame.grid_rowconfigure(0, weight=1)
                    plot_frame.grid_columnconfigure(0, weight=1)
                    self.canvas = FigureCanvasTkAgg(plt.figure(figsize=(5, 4)), master=plot_frame)
                    self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
                    self.ax = self.canvas.figure.add_subplot(111)
                    logger.info("Added plot area to Monitoring tab")
                else:
                    num_tools = len(features)
                    columns_per_row = 4
                    num_rows = (num_tools + columns_per_row - 1) // columns_per_row
                    
                    grid_frame = ctk.CTkFrame(frame, fg_color="#1f1f1f")
                    grid_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
                    
                    for i in range(num_rows):
                        grid_frame.grid_rowconfigure(i, weight=1)
                    for j in range(columns_per_row):
                        grid_frame.grid_columnconfigure(j, weight=1)
                    
                    for idx, feature in enumerate(features):
                        row = idx // columns_per_row
                        col = idx % columns_per_row
                        icon = FEATURE_ICONS.get(feature, '')
                        btn_text = f"{icon} {feature}" if icon else feature
                        logger.info(f"Creating button for {feature} with text: {btn_text}")
                        btn = ctk.CTkButton(
                            grid_frame,
                            text=btn_text,
                            command=lambda f=feature: self.run_feature(f),
                            width=200,
                            height=30,
                            font=("Segoe UI Emoji", self.font_size-2),
                            fg_color="#007bff"
                        )
                        btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
                        btn.bind("<Button-3>", lambda e, t=feature: self.add_to_favorites(t))
                        ToolTip(btn, FEATURE_DESCRIPTIONS.get(f"{FEATURE_ICONS.get(feature, '')} {feature}", ""))
                    logger.info(f"Added {num_tools} buttons to {tab_name} tab")
        except Exception as e:
            logger.error(f"Failed to add buttons to tabs: {str(e)}")
            raise

    def start_background_tasks(self):
        if self.running:
            threading.Thread(target=self.update_log_display, daemon=True).start()
            threading.Thread(target=self.check_scheduled_tasks, daemon=True).start()
            threading.Thread(target=self.collect_analytics, daemon=True).start()
            threading.Thread(target=self.update_health_periodically, daemon=True).start()
        logger.info("Background tasks started")

    def run_feature(self, feature):
        method_name = feature.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
        method = getattr(self, method_name, None)
        if method:
            method()
        else:
            self.show_output_popup(f"Feature {feature} not implemented.", feature)

    def show_output_popup(self, output, title):
        popup = Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="#1f1f1f")
        popup.transient(self.root)
        popup.grab_set()

        main_frame = ctk.CTkFrame(popup, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)

        lines = output.splitlines()
        num_lines = len(lines)
        max_line_length = max(len(line) for line in lines) if lines else 1

        char_width = 8
        char_height = 20
        text_width = min(max(max_line_length * char_width, 600), 1000)
        text_height = min(max(num_lines * char_height, 400), 600)

        text_area = ctk.CTkTextbox(
            main_frame,
            wrap="word",
            font=("Segoe UI", self.font_size),
            fg_color="#333333",
            width=text_width,
            height=text_height
        )
        text_area.insert("1.0", output)
        text_area.configure(state="disabled")
        text_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 0))

        scrollbar = ctk.CTkScrollbar(main_frame, command=text_area.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text_area.configure(yscrollcommand=scrollbar.set)

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        export_btn = ctk.CTkButton(btn_frame, text="Export", command=lambda: self.export_output(output), fg_color="#28a745")
        export_btn.grid(row=0, column=0, sticky="e", padx=5)

        close_btn = ctk.CTkButton(btn_frame, text="Close", command=popup.destroy, fg_color="#dc3545")
        close_btn.grid(row=0, column=1, sticky="w", padx=5)

        popup.update_idletasks()
        total_width = text_width + scrollbar.winfo_reqwidth() + 40
        total_height = text_height + btn_frame.winfo_reqheight() + 50
        popup.geometry(f"{total_width}x{total_height}")
        popup.resizable(False, False)

    def generate_key(self):
        save_to_file = messagebox.askyesno("Generate Key", "Do you want to save the key to a file?")
        file_path = None
        password = None
        if save_to_file:
            file_path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key files", "*.key")])
            if file_path:
                password = simpledialog.askstring("Password", "Enter a password to encrypt the key:", show="*")
                if not password:
                    self.show_output_popup("Password required to save key.", "Generate Key")
                    return
        self.queue_task(lambda: tools.generate_key(save_to_file, file_path, password), self.default_timeout, "Generate Key")

    def encrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Encrypt")
        if not file_path:
            self.show_output_popup("No file selected.", "Encrypt File")
            return
        key = simpledialog.askstring("Encrypt File", "Enter encryption key:")
        if not key:
            self.show_output_popup("Key required.", "Encrypt File")
            return
        algorithm = simpledialog.askstring("Encrypt File", "Choose algorithm (fernet/aes):", initialvalue="fernet")
        password = None
        if algorithm == "aes":
            password = simpledialog.askstring("Password", "Enter a password for AES encryption:", show="*")
        self.queue_task(lambda: tools.encrypt_file(file_path, key.encode(), algorithm, password), self.default_timeout, "Encrypt File")

    def sniff_browser_activity(self):
        self.queue_task(tools.sniff_browser_activity, self.default_timeout, "Sniff Browser Activity")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Decrypt")
        if not file_path:
            self.show_output_popup("No file selected.", "Decrypt File")
            return
        key = simpledialog.askstring("Decrypt File", "Enter decryption key:")
        if not key:
            self.show_output_popup("Key required.", "Decrypt File")
            return
        algorithm = simpledialog.askstring("Decrypt File", "Choose algorithm (fernet/aes):", initialvalue="fernet")
        password = None
        if algorithm == "aes":
            password = simpledialog.askstring("Password", "Enter the password for AES decryption:", show="*")
        self.queue_task(lambda: tools.decrypt_file(file_path, key.encode(), algorithm, password), self.default_timeout, "Decrypt File")

    def hash_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Hash")
        if not file_path:
            self.show_output_popup("No file selected.", "Hash File")
            return
        algorithms = simpledialog.askstring("Hash File", "Enter hash algorithms (comma-separated, e.g., md5,sha1,sha256):", initialvalue="md5,sha1,sha256")
        algorithms = [algo.strip() for algo in algorithms.split(",")]
        compare_hash = {}
        if messagebox.askyesno("Hash File", "Compare with a known hash?"):
            for algo in algorithms:
                hash_value = simpledialog.askstring("Hash File", f"Enter known {algo} hash (or leave blank):")
                if hash_value:
                    compare_hash[algo.lower()] = hash_value
        self.queue_task(lambda: tools.hash_file(file_path, algorithms, compare_hash), self.default_timeout, "Hash File")

    def av_status(self):
        initiate_scan = messagebox.askyesno("AV Status", "Initiate a quick scan?")
        self.queue_task(lambda: tools.check_antivirus_status(self.command_history_log, initiate_scan), self.default_timeout, "AV Status")

    def firewall_manager(self):
        action = simpledialog.askstring("Firewall Manager", "Toggle (t), List Rules (l), or Add Rule (a)?")
        if action == "t":
            toggle_state = simpledialog.askstring("Firewall Manager", "Turn firewall on or off? (on/off)")
            self.queue_task(lambda: tools.toggle_firewall(self.command_history_log, toggle_state), self.default_timeout, "Firewall Manager")
        elif action == "l":
            filter_by = simpledialog.askstring("Firewall Manager", "Filter rules by keyword (or Enter for all):")
            self.queue_task(lambda: tools.list_firewall_rules(self.command_history_log, filter_by), self.default_timeout, "Firewall Manager")
        elif action == "a":
            name = simpledialog.askstring("Firewall Manager", "Enter rule name:")
            port = simpledialog.askstring("Firewall Manager", "Enter port to block:")
            self.queue_task(lambda: tools.add_firewall_rule(self.command_history_log, name, port), self.default_timeout, "Firewall Manager")

    def startup_items(self):
        disable_item = simpledialog.askstring("Startup Items", "Enter item to disable (or Enter to list):")
        self.queue_task(lambda: tools.list_startup_items(self.command_history_log, disable_item), self.default_timeout, "Startup Items")

    def process_manager(self):
        action = simpledialog.askstring("Process Manager", "List All (a), Suspicious (s), or Kill (k)?")
        if action == "a":
            sort_by = simpledialog.askstring("Process Manager", "Sort by (cpu/memory/name):", initialvalue="cpu")
            filter_by = simpledialog.askstring("Process Manager", "Filter by name (or Enter for all):")
            self.queue_task(lambda: tools.show_processes(sort_by, filter_by), self.default_timeout, "Process Manager")
        elif action == "s":
            self.queue_task(tools.check_suspicious_processes, self.default_timeout, "Process Manager")
        elif action == "k":
            task_name = simpledialog.askstring("Kill Process", "Enter process name:")
            confirm = messagebox.askyesno("Kill Process", f"Kill task '{task_name}'?")
            self.queue_task(lambda: tools.kill_task_by_name(task_name, self.command_history_log, confirm), self.default_timeout, "Process Manager")

    def otp_generator(self):
        account_name = simpledialog.askstring("OTP Generator", "Enter account name (default: current user):")
        self.queue_task(lambda: tools.generate_otp(self.totp_secrets, account_name), self.default_timeout, "OTP Generator")

    def shred_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Shred")
        if not file_path:
            self.show_output_popup("No file selected.", "Shred File")
            return
        method = simpledialog.askstring("Shred File", "Method (standard/dod):", initialvalue="standard")
        passes = simpledialog.askinteger("Shred File", "Number of passes:", initialvalue=3, minvalue=1)
        self.queue_task(lambda: tools.shred_file(file_path, method, passes), self.default_timeout, "Shred File")

    def vuln_scan(self):
        self.queue_task(lambda: tools.vuln_scan(self.command_history_log), self.default_timeout, "Vuln Scan")

    def password_manager(self):
        action = simpledialog.askstring("Password Manager", "Generate (g), Strength (s), Sync (y)?")
        if action == "g":
            length = simpledialog.askinteger("Password Length", "Enter length:", initialvalue=12, minvalue=8)
            category = simpledialog.askstring("Category", "Enter category (or Enter for General):")
            name = simpledialog.askstring("Name", "Enter name (or Enter for default):")
            self.queue_task(lambda: tools.password_manager("generate", length, self.passwords_db, category, name), self.default_timeout, "Password Manager")
        elif action == "s":
            password = simpledialog.askstring("Password", "Enter password to check:")
            self.queue_task(lambda: tools.password_manager("strength", password=password), self.default_timeout, "Password Manager")
        elif action == "y":
            password = simpledialog.askstring("Password", "Enter database password:", show="*")
            sub_action = simpledialog.askstring("Sync", "Save (s), Load (l), or Search (r)?")
            search_term = simpledialog.askstring("Search", "Enter search term (if Search):") if sub_action == "r" else None
            self.queue_task(lambda: tools.password_manager("sync", passwords_db=self.passwords_db, password=password, search_term=search_term), self.default_timeout, "Password Manager")

    def harden_sys(self):
        self.queue_task(lambda: tools.harden_system(self.command_history_log), self.default_timeout, "Harden Sys")

    def phishing_detector(self):
        url = simpledialog.askstring("Phishing Detector", "Enter URL:")
        self.queue_task(lambda: tools.phishing_detector(url), self.default_timeout, "Phishing Detector")

    def malware_scanner(self):
        self.queue_task(lambda: tools.malware_scanner(self.command_history_log), self.default_timeout, "Malware Scanner")

    def bitlocker_status(self):
        enable_drive = simpledialog.askstring("BitLocker", "Enter drive to enable (or Enter to check):")
        self.queue_task(lambda: tools.check_bitlocker_status(self.command_history_log, enable_drive), self.default_timeout, "BitLocker Status")

    def secure_boot_check(self):
        self.queue_task(lambda: tools.check_secure_boot(self.command_history_log), self.default_timeout, "Secure Boot Check")

    def audit_policy_viewer(self):
        modify_category = simpledialog.askstring("Audit Policy", "Enter category to modify (or Enter to view):")
        success = messagebox.askyesno("Audit Success", "Audit success?") if modify_category else False
        failure = messagebox.askyesno("Audit Failure", "Audit failure?") if modify_category else False
        self.queue_task(lambda: tools.view_audit_policy(self.command_history_log, modify_category, success, failure), self.default_timeout, "Audit Policy Viewer")

    def usb_lockdown(self):
        enable = messagebox.askyesno("USB Lockdown", "Enable USB lockdown? (No to disable)")
        self.queue_task(lambda: tools.usb_lockdown(self.command_history_log, enable), self.default_timeout, "USB Lockdown")

    def network_intrusion_detection(self):
        duration = simpledialog.askinteger("Duration", "Enter monitoring duration (seconds):", initialvalue=10)
        self.queue_task(lambda: tools.network_intrusion_detection(duration), duration, "Network Intrusion Detection")

    def user_activity_logger(self):
        duration = simpledialog.askinteger("Duration", "Enter logging duration (seconds):", initialvalue=10)
        self.queue_task(lambda: tools.user_activity_logger(duration), duration, "User Activity Logger")

    def keylogger_detector(self):
        self.queue_task(tools.keylogger_detector, self.default_timeout, "Keylogger Detector")

    def password_policy_enforcer(self):
        min_length = simpledialog.askinteger("Min Length", "Enter minimum password length:", initialvalue=14)
        max_age = simpledialog.askinteger("Max Age", "Enter maximum password age (days):", initialvalue=90)
        self.queue_task(lambda: tools.password_policy_enforcer(min_length, max_age), self.default_timeout, "Password Policy Enforcer")

    def secure_file_transfer(self):
        file_path = filedialog.askopenfilename(title="Select File")
        host = simpledialog.askstring("Host", "Enter destination host:")
        username = simpledialog.askstring("Username", "Enter username:")
        password = simpledialog.askstring("Password", "Enter password:", show="*")
        destination_path = simpledialog.askstring("Destination", "Enter destination path:")
        self.queue_task(lambda: tools.secure_file_transfer(file_path, host, username, password, destination_path), self.default_timeout, "Secure File Transfer")

    # Monitoring Tools
    def resource_monitor(self):
        log_to_file = messagebox.askyesno("Log", "Log to file?")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt") if log_to_file else None
        self.queue_task(lambda: tools.resource_monitor(log_to_file, file_path), self.default_timeout, "Resource Monitor")

    def service_monitor(self):
        self.queue_task(lambda: tools.monitor_services(self.command_history_log), self.default_timeout, "Service Monitor")

    def memory_leak_detector(self):
        self.queue_task(tools.memory_leak_detector, self.default_timeout, "Memory Leak Detector")

    def real_time_alerts(self):
        view_history = messagebox.askyesno("History", "View alert history?")
        self.queue_task(lambda: tools.real_time_alerts(view_history), self.default_timeout, "Real-Time Alerts")

    def process_heatmap(self):
        self.queue_task(tools.process_heatmap, self.default_timeout, "Process Heatmap")

    def network_latency_graph(self):
        host = simpledialog.askstring("Host", "Enter host to ping:", initialvalue="8.8.8.8")
        duration = simpledialog.askinteger("Duration", "Enter duration (seconds):", initialvalue=10)
        self.queue_task(lambda: tools.network_latency_graph(self.command_history_log, host, duration), duration, "Network Latency Graph")

    def cpu_temperature_monitor(self):
        duration = simpledialog.askinteger("Duration", "Enter monitoring duration (seconds):", initialvalue=10)
        self.queue_task(lambda: tools.cpu_temperature_monitor(duration), duration, "CPU Temperature Monitor")

    def event_log_analyzer(self):
        event_id = simpledialog.askinteger("Event ID", "Enter Event ID:", initialvalue=1000)
        duration = simpledialog.askinteger("Duration", "Enter analysis duration (seconds):", initialvalue=10)
        self.queue_task(lambda: tools.event_log_analyzer(event_id, duration), duration, "Event Log Analyzer")

    def disk_io_monitor(self):
        duration = simpledialog.askinteger("Duration", "Enter monitoring duration (seconds):", initialvalue=10)
        self.queue_task(lambda: tools.disk_io_monitor(duration), duration, "Disk I/O Monitor")

    def system_uptime_tracker(self):
        self.queue_task(tools.system_uptime_tracker, self.default_timeout, "System Uptime Tracker")

    def alert_scheduler(self):
        condition = simpledialog.askstring("Condition", "Enter condition (e.g., cpu>90):", initialvalue="cpu>90")
        duration = simpledialog.askinteger("Duration", "Enter total duration (seconds):", initialvalue=300)
        interval = simpledialog.askinteger("Interval", "Enter check interval (seconds):", initialvalue=60)
        self.queue_task(lambda: tools.alert_scheduler(condition, duration, interval), duration, "Alert Scheduler")

    # Utility Tools
    def system_info(self):
        detailed = messagebox.askyesno("Detailed", "Include detailed info?")
        include_bios = messagebox.askyesno("BIOS", "Include BIOS info?")
        self.queue_task(lambda: tools.get_system_info(self.command_history_log, include_bios=include_bios, detailed=detailed), self.default_timeout, "System Info")

    def clear_temp_files(self):
        proceed = messagebox.askyesno("Proceed", "Delete temp files?")
        self.queue_task(lambda: tools.clear_temp_files(self.command_history_log, proceed), self.default_timeout, "Clear Temp Files")

    def list_users(self):
        self.queue_task(lambda: tools.list_users(self.command_history_log), self.default_timeout, "List Users")

    def check_disk_health(self):
        self.queue_task(lambda: tools.check_disk_health(self.command_history_log), self.default_timeout, "Check Disk Health")

    def list_environment_vars(self):
        search_term = simpledialog.askstring("Search", "Enter search term (or Enter for all):")
        edit_key = simpledialog.askstring("Edit Key", "Enter variable to edit (or Enter to skip):")
        edit_value = simpledialog.askstring("Edit Value", "Enter new value:") if edit_key else None
        self.queue_task(lambda: tools.list_environment_vars(self.command_history_log, search_term, edit_key, edit_value), self.default_timeout, "List Environment Vars")

    def file_permissions_viewer(self):
        file_path = filedialog.askopenfilename(title="Select File/Folder")
        self.queue_task(lambda: tools.file_permissions_viewer(self.command_history_log, file_path), self.default_timeout, "File Permissions Viewer")

    def registry_manager(self):
        action = simpledialog.askstring("Action", "Edit (e) or Backup (b)?")
        if action == "e":
            self.queue_task(lambda: tools.open_registry_editor(self.command_history_log), self.default_timeout, "Registry Manager")
        elif action == "b":
            self.queue_task(lambda: tools.registry_backup(self.command_history_log), self.default_timeout, "Registry Manager")

    def shortcut_creator(self):
        target = filedialog.askopenfilename(title="Select Target")
        shortcut_path = filedialog.asksaveasfilename(defaultextension=".lnk", filetypes=[("Shortcut files", "*.lnk")])
        self.queue_task(lambda: tools.shortcut_creator(self.command_history_log, target, shortcut_path), self.default_timeout, "Shortcut Creator")

    def recycle_bin_manager(self):
        action = simpledialog.askstring("Action", "List (l), Restore (r), or Empty (e)?")
        item_name = simpledialog.askstring("Item", "Enter filename to restore:") if action == "r" else None
        self.queue_task(lambda: tools.manage_recycle_bin(self.command_history_log, action, item_name), self.default_timeout, "Recycle Bin Manager")

    def file_integrity_checker(self):
        file_path = filedialog.askopenfilename(title="Select File")
        monitor_duration = simpledialog.askinteger("Monitor", "Enter monitoring duration (seconds, or 0 for none):", initialvalue=0)
        self.queue_task(lambda: tools.file_integrity_checker(self.command_history_log, file_path, monitor_duration or None), self.default_timeout, "File Integrity Checker")

    def text_encoder_decoder(self):
        text = simpledialog.askstring("Text", "Enter text:")
        method = simpledialog.askstring("Method", "Base64 (b), Decode (bd), URL (u), Decode (ud), Hex (h), Decode (hd), Encrypt (e), Decrypt (d):")
        method_map = {"b": "base64", "bd": "base64_decode", "u": "url", "ud": "url_decode", "h": "hex", "hd": "hex_decode", "e": "encrypt", "d": "decrypt"}
        password = simpledialog.askstring("Password", "Enter password (for encrypt/decrypt):", show="*") if method in ["e", "d"] else None
        copy = messagebox.askyesno("Clipboard", "Copy result?")
        self.queue_task(lambda: tools.text_encoder_decoder(text, method_map.get(method, "base64"), password, copy), self.default_timeout, "Text Encoder/Decoder")

    def screen_capture_tool(self):
        region = "full" if simpledialog.askstring("Region", "Full (f) or Region (r)?", initialvalue="f") == "f" else (100, 100, 300, 200)
        annotation = simpledialog.askstring("Annotation", "Enter annotation text (or Enter for none):")
        save_format = "jpg" if simpledialog.askstring("Format", "PNG (p) or JPEG (j)?", initialvalue="p") == "j" else "png"
        self.queue_task(lambda: tools.screen_capture_tool(region, annotation, save_format), self.default_timeout, "Screen Capture Tool")

    def pdf_merger(self):
        files = filedialog.askopenfilenames(title="Select PDFs", filetypes=[("PDF files", "*.pdf")])
        order = [int(i) for i in simpledialog.askstring("Order", "Enter new order (e.g., 2,1,0):").split(",")] if messagebox.askyesno("Reorder", "Reorder files?") else None
        page_ranges = {file: simpledialog.askstring("Range", f"Pages for {file} (e.g., 1-3):") for file in files} if messagebox.askyesno("Pages", "Select pages?") else {}
        self.queue_task(lambda: tools.pdf_merger(files, order, page_ranges), self.default_timeout, "PDF Merger")

    def startup_optimizer(self):
        disable_item = simpledialog.askstring("Disable", "Enter item to disable (or Enter to analyze):")
        self.queue_task(lambda: tools.optimize_startup(self.command_history_log, disable_item), self.default_timeout, "Startup Optimizer")

    def folder_sync(self):
        src = filedialog.askdirectory(title="Source Folder")
        dst = filedialog.askdirectory(title="Destination Folder")
        selective = messagebox.askyesno("Selective", "Selective sync?")
        pattern = simpledialog.askstring("Pattern", "Enter file pattern (e.g., *.txt):") if selective else None
        self.queue_task(lambda: tools.folder_sync(src, dst, selective, pattern), self.default_timeout, "Folder Sync")

    def duplicate_file_finder(self):
        directory = filedialog.askdirectory(title="Select Directory")
        self.queue_task(lambda: tools.duplicate_file_finder(directory), self.default_timeout, "Duplicate File Finder")

    def file_recovery_tool(self):
        drive_letter = simpledialog.askstring("Drive", "Enter drive letter (e.g., C:):")
        self.queue_task(lambda: tools.file_recovery_tool(drive_letter), self.default_timeout, "File Recovery Tool")

    def system_tray_manager(self):
        action = simpledialog.askstring("Action", "List (l) or Disable (d)?")
        process_name = simpledialog.askstring("Process", "Enter process name to disable:") if action == "d" else None
        self.queue_task(lambda: tools.system_tray_manager(action, process_name), self.default_timeout, "System Tray Manager")

    def clipboard_manager(self):
        action = simpledialog.askstring("Action", "List (l), Add (a), or Recall (r)?")
        index = simpledialog.askinteger("Index", "Enter index to recall:", minvalue=0) if action == "r" else None
        self.queue_task(lambda: tools.clipboard_manager(action, index), self.default_timeout, "Clipboard Manager")

    def batch_file_renamer(self):
        directory = filedialog.askdirectory(title="Select Directory")
        pattern = simpledialog.askstring("Pattern", "Enter file pattern (e.g., *.txt):")
        prefix = simpledialog.askstring("Prefix", "Enter prefix (or Enter for none):")
        start_number = simpledialog.askinteger("Start", "Enter starting number:", initialvalue=1)
        self.queue_task(lambda: tools.batch_file_renamer(directory, pattern, prefix, start_number), self.default_timeout, "Batch File Renamer")

    # Network Tools
    def network_monitor(self):
        action = simpledialog.askstring("Action", "Connections (c), Traffic (t), Latency (l)?")
        if action == "c":
            filter_by = simpledialog.askstring("Filter", "Filter by protocol/port:")
            self.queue_task(lambda: tools.list_network_connections(self.command_history_log, filter_by), self.default_timeout, "Network Monitor")
        elif action == "t":
            self.queue_task(tools.monitor_network_traffic, self.default_timeout, "Network Monitor")
        elif action == "l":
            self.network_latency_graph()

    def port_scanner(self):
        host = simpledialog.askstring("Host", "Enter host:")
        ports = [int(p) for p in simpledialog.askstring("Ports", "Enter ports (comma-separated, or Enter for defaults):").split(",")] if simpledialog.askstring("Ports", "Enter ports?") else None
        self.queue_task(lambda: tools.port_scanner(host, ports), self.default_timeout, "Port Scanner")

    def wi_fi_analyzer(self):
        self.queue_task(tools.wifi_analyzer, self.default_timeout, "Wi-Fi Analyzer")

    def dns_resolver(self):
        domain = simpledialog.askstring("Domain", "Enter domain:")
        self.queue_task(lambda: tools.dns_resolver(domain), self.default_timeout, "DNS Resolver")

    def packet_sniffer(self):
        count = simpledialog.askinteger("Count", "Enter number of packets:", initialvalue=10)
        self.queue_task(lambda: tools.packet_sniffer(count), self.default_timeout, "Packet Sniffer")

    def bandwidth_limiter(self):
        process_name = simpledialog.askstring("Process", "Enter process name:")
        limit_mb = simpledialog.askfloat("Limit", "Enter bandwidth limit (MB/s):", initialvalue=1.0)
        self.queue_task(lambda: tools.bandwidth_limiter(process_name, limit_mb), self.default_timeout, "Bandwidth Limiter")

    # Backup Tools
    def backup_manager(self):
        action = simpledialog.askstring("Action", "Backup (b), Restore (r), Encrypt Backup (e)?")
        source = filedialog.askdirectory(title="Source") if action in ["b", "e"] else filedialog.askopenfilename(title="Backup File") if action == "r" else None
        destination = filedialog.askdirectory(title="Destination")
        encrypt = action == "e"
        incremental = messagebox.askyesno("Incremental", "Incremental backup?") if action in ["b", "e"] else False
        self.queue_task(lambda: tools.backup_manager(action if action != "e" else "backup", source, destination, encrypt, self.command_history_log, incremental), self.default_timeout, "Backup Manager")

    def backup_verifier(self):
        backup_path = filedialog.askopenfilename(title="Select Backup")
        self.queue_task(lambda: tools.backup_verifier(backup_path), self.default_timeout, "Backup Verifier")

    def backup_scheduler(self):
        source = filedialog.askdirectory(title="Source")
        destination = filedialog.askdirectory(title="Destination")
        interval = simpledialog.askinteger("Interval", "Enter interval (seconds):")
        encrypt = messagebox.askyesno("Encrypt", "Encrypt backup?")
        self.queue_task(lambda: tools.backup_scheduler(source, destination, interval, encrypt), self.default_timeout, "Backup Scheduler")

    def differential_backup_tool(self):
        source = filedialog.askdirectory(title="Source")
        destination = filedialog.askdirectory(title="Destination")
        full_backup_path = filedialog.askopenfilename(title="Full Backup")
        encrypt = messagebox.askyesno("Encrypt", "Encrypt backup?")
        self.queue_task(lambda: tools.differential_backup(source, destination, full_backup_path, encrypt), self.default_timeout, "Differential Backup Tool")

    def backup_encryption_key_manager(self):
        action = simpledialog.askstring("Action", "Store (s) or Retrieve (r)?")
        key = simpledialog.askstring("Key", "Enter key:")
        password = simpledialog.askstring("Password", "Enter password:", show="*")
        self.queue_task(lambda: tools.backup_encryption_key_manager(action, key, password), self.default_timeout, "Backup Encryption Key Manager")

    def cloud_backup_uploader(self):
        backup_path = filedialog.askopenfilename(title="Select Backup")
        destination = simpledialog.askstring("Destination", "Enter cloud destination:", initialvalue="google_drive")
        self.queue_task(lambda: tools.cloud_backup_uploader(backup_path, destination), self.default_timeout, "Cloud Backup Uploader")

    # Advanced Tools
    def system_control(self):
        action = simpledialog.askstring("Action", "Restart (r), Shutdown (s), Lock (l)?")
        if action in ["r", "s"]:
            delay = simpledialog.askinteger("Delay", "Enter delay (seconds):", initialvalue=0)
            confirm = messagebox.askyesno("Confirm", f"{action.capitalize()} in {delay} seconds?")
            self.queue_task(lambda: (tools.restart_system if action == "r" else tools.shutdown_system)(self.command_history_log, delay, confirm), self.default_timeout, "System Control")
        elif action == "l":
            self.queue_task(lambda: tools.lock_workstation(self.command_history_log), self.default_timeout, "System Control")

    def dns_cache_cleaner(self):
        clear = messagebox.askyesno("Clear", "Clear DNS cache?")
        self.queue_task(lambda: tools.clear_dns_cache(self.command_history_log, clear), self.default_timeout, "DNS Cache Cleaner")

    def driver_manager(self):
        open_manager = messagebox.askyesno("Open", "Open Device Manager?")
        self.queue_task(lambda: tools.driver_mgr(self.command_history_log, open_manager), self.default_timeout, "Driver Manager")

    def boot_manager(self):
        timeout = simpledialog.askinteger("Timeout", "Enter boot timeout (seconds, or Enter to view):", minvalue=0) if messagebox.askyesno("Set Timeout", "Set boot timeout?") else None
        self.queue_task(lambda: tools.boot_mgr(self.command_history_log, timeout), self.default_timeout, "Boot Manager")

    def sys_info_export(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        self.queue_task(lambda: tools.get_system_info(self.command_history_log, export=True, file_path=file_path), self.default_timeout, "Sys Info Export")

    def bios_info(self):
        self.queue_task(lambda: tools.get_system_info(self.command_history_log, include_bios=True), self.default_timeout, "BIOS Info")

    def remote_desktop_toggle(self):
        toggle_state = simpledialog.askstring("Toggle", "On or Off? (on/off)")
        self.queue_task(lambda: tools.toggle_remote_desktop(self.command_history_log, toggle_state), self.default_timeout, "Remote Desktop Toggle")

    def power_plan_manager(self):
        switch_plan = simpledialog.askstring("Plan", "Enter plan GUID (or Enter to list):") if messagebox.askyesno("Switch", "Switch power plan?") else None
        self.queue_task(lambda: tools.power_plan_manager(self.command_history_log, switch_plan), self.default_timeout, "Power Plan Manager")

    def command_history(self):
        self.show_output_popup("\n".join(self.command_history_log[-10:]) or "No history.", "Command History")

    def group_policy_viewer(self):
        self.queue_task(lambda: tools.view_group_policy(self.command_history_log), self.default_timeout, "Group Policy Viewer")

    def task_kill_by_name(self):
        task_name = simpledialog.askstring("Task", "Enter task name:")
        confirm = messagebox.askyesno("Confirm", f"Kill '{task_name}'?")
        self.queue_task(lambda: tools.kill_task_by_name(task_name, self.command_history_log, confirm), self.default_timeout, "Task Kill By Name")

    def windows_feature_manager(self):
        feature = simpledialog.askstring("Feature", "Enter feature name:") if messagebox.askyesno("Manage", "Enable/disable feature?") else None
        enable = messagebox.askyesno("Enable", "Enable feature?") if feature else True
        self.queue_task(lambda: tools.windows_feature_manager(self.command_history_log, feature, enable), self.default_timeout, "Windows Feature Manager")

    def multi_monitor_config(self):
        open_settings = messagebox.askyesno("Settings", "Open display settings?")
        self.queue_task(lambda: tools.multi_monitor_config(self.command_history_log, open_settings), self.default_timeout, "Multi-Monitor Config")

    def system_restore_point_creator(self):
        description = simpledialog.askstring("Description", "Enter restore point description:")
        self.queue_task(lambda: tools.system_restore_point_creator(description), self.default_timeout, "System Restore Point Creator")

    def event_log_cleaner(self):
        log_type = simpledialog.askstring("Log Type", "Enter log type (e.g., System):", initialvalue="System")
        self.queue_task(lambda: tools.event_log_cleaner(log_type), self.default_timeout, "Event Log Cleaner")

    def driver_verifier(self):
        action = simpledialog.askstring("Action", "Start (s) or Stop (t)?")
        self.queue_task(lambda: tools.driver_verifier("start" if action == "s" else "stop"), self.default_timeout, "Driver Verifier")

    def system_file_checker(self):
        self.queue_task(tools.system_file_checker, self.default_timeout, "System File Checker")

    def performance_benchmark(self):
        self.queue_task(tools.performance_benchmark, self.default_timeout, "Performance Benchmark")

    # IT Support Tools
    def event_log_manager(self):
        action = simpledialog.askstring("Action", "View (v), Monitor (m), Export (e)?")
        filter_by = simpledialog.askstring("Filter", "Enter keyword (or Enter for all):") if action in ["v", "m"] else None
        monitor_duration = simpledialog.askinteger("Duration", "Enter monitoring duration (seconds):") if action == "m" else None
        file_path = filedialog.asksaveasfilename(defaultextension=".txt") if action == "e" else None
        self.queue_task(lambda: tools.manage_logs("events", action if action != "v" else "view", file_path, self.command_history_log, filter_by, monitor_duration), self.default_timeout if action != "m" else monitor_duration, "Event Log Manager")

    def scheduled_task_manager(self):
        action = simpledialog.askstring("Action", "Add (a), List (l), Delay (d)?")
        if action == "a":
            task_name = simpledialog.askstring("Name", "Enter task name:")
            interval = simpledialog.askinteger("Interval", "Enter interval (seconds):")
            task_type = simpledialog.askstring("Type", "Clear Temp (c), Resource Monitor (r), Custom Command (cmd)?")
            custom_command = simpledialog.askstring("Command", "Enter custom command:") if task_type == "cmd" else None
            self.queue_task(lambda: tools.recurring_tasks(self.scheduled_tasks, task_name, interval, task_type, custom_command), self.default_timeout, "Scheduled Task Manager")
        elif action == "l":
            self.show_output_popup("\n".join([f"{t['name']}: Next run at {t['time']}" for t in self.scheduled_tasks]) or "No tasks.", "Scheduled Task Manager")
        elif action == "d":
            task_name = simpledialog.askstring("Name", "Enter task name:")
            delay = simpledialog.askinteger("Delay", "Enter delay (seconds):")
            self.queue_task(lambda: tools.delay_task(self.scheduled_tasks, task_name, delay), self.default_timeout, "Scheduled Task Manager")

    def remote_assistance_tool(self):
        self.queue_task(tools.remote_assistance_tool, self.default_timeout, "Remote Assistance Tool")

    def user_account_manager(self):
        action = simpledialog.askstring("Action", "Add (a), Remove (r), Modify (m)?")
        username = simpledialog.askstring("Username", "Enter username:")
        password = simpledialog.askstring("Password", "Enter password:", show="*") if action in ["a", "m"] else None
        self.queue_task(lambda: tools.user_account_manager(action, username, password), self.default_timeout, "User Account Manager")

    def system_diagnostic_report(self):
        self.queue_task(tools.system_diagnostic_report, self.default_timeout, "System Diagnostic Report")

    def service_dependency_viewer(self):
        service_name = simpledialog.askstring("Service", "Enter service name:")
        self.queue_task(lambda: tools.service_dependency_viewer(service_name), self.default_timeout, "Service Dependency Viewer")

    def hardware_inventory_tool(self):
        self.queue_task(tools.hardware_inventory_tool, self.default_timeout, "Hardware Inventory Tool")

    # Additional Advanced Tools
    def process_injection_detector(self):
        self.queue_task(tools.process_injection_detector, self.default_timeout, "Process Injection Detector")

    def kernel_driver_enumerator(self):
        self.queue_task(tools.kernel_driver_enumerator, self.default_timeout, "Kernel Driver Enumerator")

    def shadow_copy_manager(self):
        self.queue_task(tools.shadow_copy_manager, self.default_timeout, "Shadow Copy Manager")

    def memory_forensics_lite(self):
        self.queue_task(tools.memory_forensics_lite, self.default_timeout, "Memory Forensics Lite")

    def privilege_escalation_checker(self):
        self.queue_task(tools.privilege_escalation_checker, self.default_timeout, "Privilege Escalation Checker")

    def network_connection_anomaly_detector(self):
        self.queue_task(tools.network_connection_anomaly_detector, self.default_timeout, "Network Connection Anomaly Detector")

    def file_system_anomaly_scanner(self):
        self.queue_task(tools.file_system_anomaly_scanner, self.default_timeout, "File System Anomaly Scanner")

    def service_behavior_profiler(self):
        self.queue_task(tools.service_behavior_profiler, self.default_timeout, "Service Behavior Profiler")

    def registry_anomaly_detector(self):
        self.queue_task(tools.registry_anomaly_detector, self.default_timeout, "Registry Anomaly Detector")

    def thread_stack_analyzer(self):
        self.queue_task(tools.thread_stack_analyzer, self.default_timeout, "Thread Stack Analyzer")

    def secure_boot_policy_editor(self):
        self.queue_task(tools.secure_boot_policy_editor, self.default_timeout, "Secure Boot Policy Editor")

    def process_hollowing_detector(self):
        self.queue_task(tools.process_hollowing_detector, self.default_timeout, "Process Hollowing Detector")

    def network_packet_entropy_analyzer(self):
        self.queue_task(tools.network_packet_entropy_analyzer, self.default_timeout, "Network Packet Entropy Analyzer")

    def system_call_tracer(self):
        self.queue_task(tools.system_call_tracer, self.default_timeout, "System Call Tracer")

    def dynamic_dns_resolver_monitor(self):
        self.queue_task(tools.dynamic_dns_resolver_monitor, self.default_timeout, "Dynamic DNS Resolver Monitor")

    # Password Extraction Tools
    def browser_password_extractor(self):
        try:
            root = tk.Tk()
            root.withdraw()
            browsers_input = simpledialog.askstring(
                "Browsers",
                "Select browsers (comma-separated: chrome, firefox, edge, ie) or leave blank for all:",
                initialvalue="chrome,firefox,edge,ie",
                parent=root
            )
            root.destroy()
            if browsers_input is None:
                self.show_output_popup("Browser selection cancelled.", "Browser Password Extractor")
                return
            browsers = [b.strip().lower() for b in browsers_input.split(",")] if browsers_input else ["chrome", "firefox", "edge", "ie"]
            self.queue_task(lambda: tools.browser_password_extractor(browsers), self.default_timeout, "Browser Password Extractor")
        except Exception as e:
            self.show_output_popup(f"Error: {str(e)}", "Browser Password Extractor")

    def windows_credential_manager_extractor(self):
        self.queue_task(tools.windows_credential_manager_extractor, self.default_timeout, "Windows Credential Manager Extractor")

    def unified_password_aggregator(self):
        try:
            root = tk.Tk()
            root.withdraw()
            category = simpledialog.askstring(
                "Category",
                "Categorize by (website, application, source):",
                initialvalue="website",
                parent=root
            )
            root.destroy()
            if not category:
                category = "website"
            category = category.lower()
            self.queue_task(lambda: tools.unified_password_aggregator(category), self.default_timeout, "Unified Password Aggregator")
        except Exception as e:
            self.show_output_popup(f"Error: {str(e)}", "Unified Password Aggregator")

    # Reconnaissance and OSINT Tools
    def sublist3r(self):
        try:
            domain = simpledialog.askstring("Sublist3r", "Enter domain to enumerate subdomains:")
            if not domain:
                self.show_output_popup("No domain provided.", "Sublist3r")
                return
            bruteforce = messagebox.askyesno("Bruteforce", "Enable bruteforce?")
            self.queue_task(lambda: tools.run_sublist3r(domain, bruteforce), self.default_timeout, "Sublist3r")
        except Exception as e:
            self.show_output_popup(f"Error: {str(e)}", "Sublist3r")

    def crt_sh(self):
        domain = simpledialog.askstring("crt.sh", "Enter domain to query crt.sh:")
        if not domain:
            self.show_output_popup("No domain provided.", "crt.sh")
            return
        self.queue_task(lambda: tools.query_crt_sh(domain), self.default_timeout, "crt.sh")

    def censys(self):
        domain = simpledialog.askstring("Censys", "Enter domain to query Censys:")
        api_id = simpledialog.askstring("Censys", "Enter Censys API ID:")
        api_secret = simpledialog.askstring("Censys", "Enter Censys API Secret:", show="*")
        if not all([domain, api_id, api_secret]):
            self.show_output_popup("Domain, API ID, and Secret are required.", "Censys")
            return
        self.queue_task(lambda: tools.query_censys(domain, api_id, api_secret), self.default_timeout, "Censys")

    def slack_notify(self):
        message = simpledialog.askstring("Slack Notify", "Enter message to send to Slack:")
        channel = simpledialog.askstring("Slack Notify", "Enter Slack channel (e.g., #general):")
        token = simpledialog.askstring("Slack Notify", "Enter Slack Bot Token:", show="*")
        if not all([message, channel, token]):
            self.show_output_popup("Message, channel, and token are required.", "Slack Notify")
            return
        self.queue_task(lambda: tools.send_slack_notification(message, channel, token), self.default_timeout, "Slack Notify")

    # New Tool Removal Method
    def remove_custom_tool(self):
        # Get list of custom tools
        all_tools = []
        for category, tools_list in self.custom_tools.items():
            all_tools.extend([(tool, category) for tool in tools_list])
        
        if not all_tools:
            messagebox.showinfo("Remove Tool", "No custom tools available to remove.")
            return

        # Create popup to select tool
        popup = Toplevel(self.root)
        popup.title("Remove Custom Tool")
        popup.configure(bg="#1f1f1f")
        popup.transient(self.root)
        popup.grab_set()

        main_frame = ctk.CTkFrame(popup, fg_color="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="Select Tool to Remove:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tool_options = [f"{tool} ({category})" for tool, category in all_tools]
        tool_var = tk.StringVar(value=tool_options[0] if tool_options else "")
        tool_dropdown = ctk.CTkOptionMenu(main_frame, values=tool_options, variable=tool_var, width=200)
        tool_dropdown.grid(row=0, column=1, padx=5, pady=5)

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        remove_btn = ctk.CTkButton(btn_frame, text="Remove", 
                                   command=lambda: self._execute_remove_tool(tool_var.get().split(" (")[0], all_tools, popup), 
                                   fg_color="#dc3545")
        remove_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy, fg_color="#6c757d")
        cancel_btn.pack(side="right", padx=5)

        popup.update_idletasks()
        popup.geometry("400x150")
        logger.info("Remove Tool popup created")

    def _execute_remove_tool(self, tool_name, all_tools, popup):
        try:
            import os
            import json
            import importlib

            # Find category
            category = next(cat for t, cat in all_tools if t == tool_name)

            # Load metadata
            metadata_file = os.path.join("custom_tools", "custom_tools.json")
            with open(metadata_file, "r") as f:
                metadata = json.load(f)

            # Get script file path and remove it
            script_file = metadata[tool_name]["file"]
            if os.path.exists(script_file):
                os.remove(script_file)
                logger.info(f"Deleted script file: {script_file}")

            # Remove from metadata
            del metadata[tool_name]
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=4)
            logger.info(f"Removed '{tool_name}' from {metadata_file}")

            # Update custom_tools.py
            custom_tools_file = "custom_tools.py"
            with open(custom_tools_file, "r") as f:
                lines = f.readlines()
            with open(custom_tools_file, "w") as f:
                safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in tool_name.lower())
                for line in lines:
                    if safe_name not in line:
                        f.write(line)
            importlib.reload(custom_tools)
            logger.info(f"Removed '{tool_name}' from {custom_tools_file} and reloaded module")

            # Remove from self.custom_tools
            self.custom_tools[category].remove(tool_name)
            if not self.custom_tools[category]:
                del self.custom_tools[category]
            logger.info(f"Removed '{tool_name}' from self.custom_tools")

            # Refresh GUI
            self.reset_tab_buttons()
            self.add_buttons_to_tabs()
            self.notebook.update_idletasks()
            self.log_queue.put(f"Tool '{tool_name}' removed successfully")
            popup.destroy()
        except Exception as e:
            error_msg = f"Failed to remove tool '{tool_name}': {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("Error", error_msg, parent=popup)

# Main function outside the class
def main():
    root = ctk.CTk()
    app = SlingShot(root)
    root.protocol("WM_DELETE_WINDOW", app.kill_program)
    root.mainloop()

if __name__ == "__main__":
    main()