var ESP = {
    loop: function() {
        const base = Module.findBaseAddress(OFFSETS.G_LIB);
        if (!base) return;

        const playerListPtr = base.add(OFFSETS.ADDR_POSITION_BASE).readPointer();
        if (playerListPtr.isNull()) return;

        var enemyData = [];
        for (let i = 0; i < 50; i++) {
            let enemyPtr = playerListPtr.add(i * 0x8).readPointer();
            if (enemyPtr.isNull()) continue;

            let hp = enemyPtr.add(OFFSETS.OFF_HP).readInt();
            if (hp <= 0) continue;

            enemyData.push({
                x: enemyPtr.add(OFFSETS.OFF_X).readFloat(),
                y: enemyPtr.add(OFFSETS.OFF_Y).readFloat(),
                z: enemyPtr.add(OFFSETS.OFF_Z).readFloat(),
                hp: hp,
                name: enemyPtr.add(OFFSETS.OFF_NICKNAME).readUtf8String()
            });
        }
        send({ type: 'esp_data', data: enemyData });
    }
};
setInterval(ESP.loop, 16);
