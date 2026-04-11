import frida
import sys
import subprocess

# 패키지명
PACKAGE_NAME = "com.wellbia.xigncode.sample" 

# 자바스크립트 로직
JS_CODE = """
Java.perform(function () {
    const moduleName = "libxigncode.so";
    let module = null;

    const dlopenPtr = Module.findExportByName(null, "android_dlopen_ext") || 
                     Module.findExportByName(null, "dlopen");

    Interceptor.attach(dlopenPtr, {
        onLeave: function (retval) {
            const target = Process.findModuleByName(moduleName);
            if (target && !module) {
                module = target;
                console.log("Loaded: " + module.base);
                
                // 인증 후킹
                Interceptor.attach(module.base.add(0x182ec), {
                    onEnter: function (args) {
                        console.log("--- Auth Data ---");
                        try {
                            // 데이터 추출
                            console.log("P2: " + Memory.readUtf8String(args[2]));
                            console.log("P3: " + Memory.readUtf8String(args[3]));
                        } catch(e) {
                            console.log("Data: Binary");
                        }
                    }
                });
            }
        }
    });
});
"""

def on_message(message, data):
    if message['type'] == 'send':
        print(f"[*] {message['payload']}")

def main():
    print("[*] Q-Analyzer Starting...")
    try:
        # ADB 설정
        subprocess.run(["adb", "forward", "tcp:27042", "tcp:27042"], shell=True)
        
        device = frida.get_usb_device()
        pid = device.spawn([PACKAGE_NAME])
        session = device.attach(pid)
        script = session.create_script(JS_CODE)
        script.on('message', on_message)
        script.load()
        device.resume(pid)
        print("[!] Running. Press Enter to Stop.")
        sys.stdin.read()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to Exit...")

if __name__ == "__main__":
    main()
