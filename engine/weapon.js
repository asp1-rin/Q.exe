var Weapon = {
    setNoRecoil: function(enable) {
        const addr = Module.findBaseAddress(OFFSETS.G_LIB).add(OFFSETS.WEAPON_RECOIL_PATCH);
        if (!addr) return;

        Memory.patchCode(addr, 4, code => {
            const writer = new Arm64Writer(code);
            if (enable) {
                writer.putBytes(hexToBytes("0040201E")); 
            } else {
                writer.putBytes(hexToBytes("F3031FA8")); // 원본 복구용 바이트 (예시)
            }
            writer.flush();
        });
    },

    setNoSpread: function(enable) {
        const addr = Module.findBaseAddress(OFFSETS.G_LIB).add(OFFSETS.WEAPON_SPREAD_PATCH);
        if (!addr) return;

        Memory.patchCode(addr, 4, code => {
            const writer = new Arm64Writer(code);
            if (enable) {
                writer.putBytes(hexToBytes("0040201E"));
            } else {
                writer.putBytes(hexToBytes("F3031FA8")); // 원본 복구용 바이트 (예시)
            }
            writer.flush();
        });
    }
};

function hexToBytes(hex) {
    var bytes = [];
    for (var c = 0; c < hex.length; c += 2)
        bytes.push(parseInt(hex.substr(c, 2), 16));
    return new Uint8Array(bytes);
}

// Q.py에서 호출할 수 있도록 전역 노출
global.Weapon = Weapon;
