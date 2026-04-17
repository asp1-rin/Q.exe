import tkinter as tk

class GameOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")
        self.root.config(bg="black")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.fov_radius = 150

    def draw_esp(self, enemies):
        self.canvas.delete("all")
        cx, cy = self.root.winfo_screenwidth()//2, self.root.winfo_screenheight()//2
        
        # FOV 원 그리기
        self.canvas.create_oval(cx-self.fov_radius, cy-self.fov_radius, 
                                cx+self.fov_radius, cy+self.fov_radius, outline="cyan")

        for en in enemies:
            # 실제로는 여기서 W2S 변환 로직이 필요함 (가상 좌표 예시)
            sx, sy = en['x'] * 10 + cx, en['y'] * 10 + cy 
            
            # 적 박스 및 정보
            self.canvas.create_rectangle(sx-20, sy-40, sx+20, sy+10, outline="red", width=2)
            self.canvas.create_text(sx, sy-55, text=f"{en['name']} [{en['hp']}]", fill="white")

    def update_overlay(self):
        self.root.update()
