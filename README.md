# ASP1RIN PRIVATE PROJECT

This repository contains both the PC version (EXE) and the Mobile version (LUA) of the ASP1RIN PRIVATE tool.

## ASP1RIN PRIVATE PC (EXE)
A powerful tool designed for the MilkChoco PC environment, focusing on stability and advanced feature injection.

### Features
* **Security Bypass**: Built-in logic to handle game security software.
* **Advanced Injection**: Seamlessly injects recoil and spread control via Frida.
* **Local Authentication**: Secure access for authorized users.

### Requirements
* **Windows 10/11** (64-bit)
* **Frida-tools** installed on the system
* **USB Debugging** enabled on the target device
* **MilkChoco** installed on the connected device

### How to Use
1. Connect your mobile device or emulator to your PC via USB.
2. Ensure ADB is authorized and the device is recognized.
3. Run `Q.exe` as Administrator.
4. Enter your ID in the login field.
5. Click the "LOGIN & START" button.
6. Keep the tool running while playing the game.

### Technical Notes
* The tool requires `libMyGame.so` to be loaded before injection.
* To force close the application, use Task Manager or run: `taskkill /f /im Q.exe`.

## Disclaimer
This software is provided for educational and research purposes only. The developer assumes no liability for account bans or any legal issues arising from the use of this tool. Use it at your own risk.

## Credits
* Developed by **@asp1-rin**
