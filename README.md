bypass milkchoco libxigncode.so
____________________________________

bash
    
curl -v -k https://222.112.0.210:10443/ \
     -H "User-Agent: Xigncode/ZCWAVE" \
     -H "X-Xigncode-Token: [token]"
    
frida -U -f [hook.js] -l xigncode_hook.js
