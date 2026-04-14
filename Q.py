import customtkinter as ctk
import frida
import requests
import sys
import threading
import os

AUTH_SERVER = "http://dc.wrd.kr:26471/auth"
PACKAGE_NAME = "com.gameparadiso.milkchoco"
LIB_NAME = "libMyGame.so"
ICON_PATH = "icon/Q.ico"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ASP1RIN PRIVATE")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)

        self.label = ctk.CTkLabel(self, text="ASP1RIN PRIVATE TOOL", font=("Roboto", 20))
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter ID")
        self.entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="LOGIN & START", command=self.start_process)
        self.button.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Status: Waiting", text_color="gray")
        self.status_label.pack(pady=10)

    def start_process(self):
        user_id = self.entry.get().strip()
        if not user_id:
            self.status_label.configure(text="Status: Please enter ID", text_color="red")
            return
        
        threading.Thread(target=self.run_logic, args=(user_id,), daemon=True).start()

    def run_logic(self, user_id):
        try:
            self.status_label.configure(text="Status: Authenticating...", text_color="yellow")
            res = requests.post(AUTH_SERVER, json={"id": user_id}, timeout=10)
            data = res.json()

            if not data.get("ok"):
                self.status_label.configure(text=f"Status: {data.get('msg')}", text_color="red")
                return

            grade = data.get("grade")
            self.status_label.configure(text=f"Status: Access Granted ({grade})", text_color="green")
            
            device = frida.get_usb_device()
            pid = device.spawn([PACKAGE_NAME])
            session = device.attach(pid)
            
            script = session.create_script(self.get_js(grade))
            script.load()
            device.resume(pid)
            
            self.status_label.configure(text="Status: Inject Success", text_color="cyan")
        except Exception as e:
            self.status_label.configure(text="Status: Connection Error", text_color="red")

    def get_js(self, grade):
        return f"""
        Java.perform(() => {{
            const X = Java.use("com.wellbia.xigncode.XigncodeClientSystem");
            X["initialize"].implementation = function (a, b, c, d, e) {{
                return 0;
            }};
        }});
        const G = "{grade}";
        const L = "{LIB_NAME}";
        function apply() {{
            if (G === "A") {{
                var r = Module.findExportByName(L, "_ZN6Recoil11ShakeCameraERKf");
                if (r) {{ Interceptor.attach(r, {{ onEnter: function(a) {{ a[1] = ptr(0); }} }}); }}
                var s = Module.findExportByName(L, "_ZN6Spread19GetAimGapByCurStateEv");
                if (s) {{ Interceptor.replace(s, new NativeCallback(function() {{ return 0.0; }}, 'float', [])); }}
            }}
        }}
        var t = setInterval(function() {{
            if (Module.findBaseAddress(L)) {{ clearInterval(t); apply(); }}
        }}, 500);
        """

if __name__ == "__main__":
    app = App()
    app.mainloop()
