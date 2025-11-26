package com.lapcevichme.winterhackathon.core.config

object CasinoConfig {
    // Настройки рулетки
    const val TOTAL_ITEMS_IN_STRIP = 50
    const val WINNING_INDEX = 40

    // Шансы выпадения
    const val CHANCE_LEGENDARY = 2  // 0..1
    const val CHANCE_EPIC = 10      // 2..9
    const val CHANCE_RARE = 40      // 10..39
    // 40..100 Common/Trash

    // Цвета редкости
    object Colors {
        const val LEGENDARY = 0xFFFFD700
        const val EPIC = 0xFFE91E63
        const val RARE = 0xFF2196F3
        const val COMMON = 0xFF9E9E9E
    }
}