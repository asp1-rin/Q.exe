var Aimbot = {
    enabled: false,
    smooth: 0.5,      // 1.0이면 즉시 고정(자석), 0.1이면 매우 부드럽게 이동
    fovSize: 150,     // 에임 기준 반경(원 크기)
    
    tick: function() {
        if (!this.enabled) return;

        const base = Module.findBaseAddress(OFFSETS.G_LIB);
        const camPtr = base.add(OFFSETS.ADDR_CAMERA_BASE).readPointer();
        if (camPtr.isNull()) return;

        const enemies = ESP.getEnemyList();
        if (enemies.length === 0) return;

        // 현재 내 에임 각도 읽기
        let curYaw = camPtr.add(0x40).readFloat();
        let curPitch = camPtr.add(0x44).readFloat();

        let target = null;
        let minDistance = this.fovSize;

        enemies.forEach(en => {
            // W2S 연산이 되었다고 가정하거나 각도 차이로 FOV 계산
            // 여기서는 단순화하여 화면 중앙 기준 거리(FOV) 내 적 탐색
            let distToCrosshair = Math.sqrt(Math.pow(en.screenX - 960, 2) + Math.pow(en.screenY - 540, 2));

            if (distToCrosshair < minDistance) {
                minDistance = distToCrosshair;
                target = en;
            }
        });

        if (target) {
            // 타겟까지 필요한 목표 각도 계산 (Atan2 로직 필요)
            let targetYaw = target.calcYaw; 
            let targetPitch = target.calcPitch;

            // 부드러운 이동 (Smoothing) 로직
            let nextYaw = curYaw + (targetYaw - curYaw) * this.smooth;
            let nextPitch = curPitch + (targetPitch - curPitch) * this.smooth;

            camPtr.add(0x40).writeFloat(nextYaw);
            camPtr.add(0x44).writeFloat(nextPitch);
        }
    }
};

setInterval(() => {
    Aimbot.tick();
}, 10);

global.Aimbot = Aimbot;
