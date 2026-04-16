#ifndef OFFSET_H
#define OFFSET_H

#define G_LIB "libMyGame.so"
#define S_LIB "libxigncode.so"

#define ADDR_POSITION_BASE 0x7ABE28
#define ADDR_CASH_BASE     0x2D16FC
#define ADDR_CAMERA_BASE   0x8B26DC

#define OFFSET_GET_AIM_GAP 0x25B5268
#define OFFSET_SHAKE_CAMERA 0x28B6EB4
#define OFFSET_RECOIL_VALUE 0x25B51D0

#define WEAPON_RECOIL_PATCH 0x33BFAF0
#define WEAPON_SPREAD_PATCH 0x35ADC9C

#define OFF_HP         0x2C
#define OFF_MAXHP      0xEF4
#define OFF_NICKNAME   0x88
#define OFF_STATE      0x12C
#define OFF_X          0x190
#define OFF_Y          0x194
#define OFF_Z          0x198
#define OFF_SKILL_COOL 0xCC

#endif
