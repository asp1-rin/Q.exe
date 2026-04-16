import customtkinter as ctk
import frida
import threading
import os
import json

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ASP1RIN PRIVATE")
        self.geometry("400x400")
        ctk.set_appearance_mode("dark")

        self.label = ctk.CTkLabel(self, text="ASP1RIN PROJECT", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.pack(pady=10, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(self.status_frame, text="Status: Ready", text_color="gray")
        self.status_label.pack(pady=5)

        self.weapon_frame = ctk.CTkFrame(self)
        self.weapon_frame.pack(pady=10, padx=20, fill="x")

        self.recoil_var = ctk.BooleanVar(value=False)
        self.recoil_switch = ctk.CTkSwitch(self.weapon_frame, text="No Recoil", variable=self.recoil_var, command=self.toggle_weapon)
        self.recoil_switch.pack(side="left", padx=20, pady=10)

        self.spread_var = ctk.BooleanVar(value=False)
        self.spread_switch = ctk.CTkSwitch(self.weapon_frame, text="No Spread", variable=self.spread_var, command=self.toggle_weapon)
        self.spread_switch.pack(side="left", padx=20, pady=10)

        self.start_button = ctk.CTkButton(self, text="INJECT ENGINE", command=self.start_injection, height=50)
        self.start_button.pack(pady=20)

        self.session = None
        self.script = None

    def start_injection(self):
        self.start_button.configure(state="disabled")
        threading.Thread(target=self.run_frida, daemon=True).start()

    def run_frida(self):
        try:
            self.status_label.configure(text="Searching Device...", text_color="yellow")
            device = frida.get_usb_device()
            
            self.status_label.configure(text="Attaching Process...", text_color="orange")
            self.session = device.attach("com.gameparadiso.milkchoco")
            
            full_script = self.merge_scripts()
            self.script = self.session.create_script(full_script)
            self.script.on('message', self.on_message)
            self.script.load()
            
            self.status_label.configure(text="ENGINE INJECTED", text_color="cyan")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")
            self.start_button.configure(state="normal")

    def merge_scripts(self):
        scripts = ["offsets.js", "bypass.js", "weapon.js", "esp.js", "aimbot.js"]
        combined = ""
        base_path = "engine"
        for s in scripts:
            with open(os.path.join(base_path, s), "r", encoding='utf-8') as f:
                combined += f.read() + "\n"
        return combined

    def on_message(self, message, data):
        if message['type'] == 'send':
            payload = message['payload']
            if payload['type'] == 'esp':
                # Overlay Update Logic Here
                pass

    def toggle_weapon(self):
        if not self.script: return
        
        recoil = self.recoil_var.get()
        spread = self.spread_var.get()
        
        self.script.runtime.enqueue_job(f"Weapon.setNoRecoil({str(recoil).lower()})")
        self.script.runtime.enqueue_job(f"Weapon.setNoSpread({str(spread).lower()})")

if __name__ == "__main__":
    app = App()
    app.mainloop()
