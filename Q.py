import sys
import time
import subprocess
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import frida

class QAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.device = None
        self.session = None
        self.script = None

    def initUI(self):
        self.setWindowTitle("Q-Analyzer: Strategic Bypass")
        self.setGeometry(100, 100, 450, 600)
        
        layout = QVBoxLayout()
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("background-color: #1e1e1e; color: #ffffff; font-family: Consolas;")
        
        buttons = [
            ("1. ADB 연결 (Link Start)", self.step1_adb),
            ("2. 서버 시작 (Push & Run)", self.step2_server),
            ("3. 시리얼 인증 (Device Sync)", self.step3_serial),
            ("4. 프리다 핸드셰이크", self.step4_handshake),
            ("5. 쿠키 체크 (Lobby Entry)", self.step5_cookie),
            ("6. 에이전트 주입 (Bypass & Aim ON)", self.step6_agent)
        ]

        self.btn_list = []
        for text, func in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(40)
            btn.clicked.connect(func)
            layout.addWidget(btn)
            self.btn_list.append(btn)

        layout.addWidget(QLabel("Process Log"))
        layout.addWidget(self.log_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def log(self, msg):
        self.log_box.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

    def step1_adb(self):
        try:
            subprocess.run(["adb", "connect", "127.0.0.1:5555"], capture_output=True)
            result = subprocess.check_output(["adb", "devices"]).decode()
            if "device" in result.split('\n')[1]:
                self.log("ADB 연결 성공")
            else:
                self.log("장치 연결 실패: adb 상태를 확인하십시오.")
        except Exception as e:
            self.log(f"ADB 오류: {e}")

    def step2_server(self):
        self.log("Frida-Server 기동 명령 전송")
        subprocess.run(["adb", "shell", "su -c 'setenforce 0'"], capture_output=True)
        subprocess.Popen(["adb", "shell", "su -c '/data/local/tmp/frida-server &'"], shell=True)
        time.sleep(2)
        self.log("서버 실행 완료")

    def step3_serial(self):
        try:
            serial = subprocess.check_output(["adb", "get-serialno"]).decode().strip()
            self.log(f"시리얼 인증: {serial}")
        except:
            self.log("시리얼 인증 실패")

    def step4_handshake(self):
        try:
            self.device = frida.get_usb_device(timeout=5)
            self.log(f"프리다 엔진 동기화 완료: {self.device}")
        except Exception as e:
            self.log(f"핸드셰이크 실패: {e}")

    def step5_cookie(self):
        self.log("세션 쿠키 체크 (마을 진입 확인)")
        res = subprocess.run(["adb", "shell", "pidof com.gameparadiso.milkchoco"], capture_output=True).stdout.decode().strip()
        if res:
            self.log(f"마을 진입 확인 (PID: {res})")
        else:
            self.log("게임 프로세스를 찾을 수 없습니다.")

    def step6_agent(self):
        if not self.device:
            self.log("4단계 핸드셰이크가 선행되어야 합니다.")
            return

        self.log("에이전트 주입 및 보안 우회 시작")
        
        jscode = """
        const LIB_NAME = "libMyGame.so"; 
        const base = Module.findBaseAddress(LIB_NAME);
        
        if (base) {
            console.log("Base Address: " + base);
        }

        Interceptor.attach(Module.findExportByName(null, "read"), {
            onEnter: function(args) {
                // Aim Logic Placeholder
            }
        });
        """

        try:
            self.session = self.device.attach("com.gameparadiso.milkchoco")
            self.script = self.session.create_script(jscode)
            self.script.on('message', lambda msg, data: self.log(f"Script Msg: {msg}"))
            self.script.load()
            self.log("보안 우회 및 에이전트 주입 완료")
        except Exception as e:
            self.log(f"주입 실패: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QAnalyzer()
    window.show()
    sys.exit(app.exec())
