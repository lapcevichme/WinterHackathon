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
        const val LEGENDARY = "#FFFFD700"
        const val EPIC = "#FFE91E63"
        const val RARE = "#FF2196F3"
        const val COMMON = "#FF9E9E9E"
    }
}