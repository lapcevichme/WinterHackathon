package com.lapcevichme.winterhackathon.domain.model.casino

import androidx.compose.ui.graphics.Color
import androidx.core.graphics.toColorInt

data class Prize(
    val id: String,
    val name: String,
    val type: PrizeType,
    val amount: Int = 0,
    val emoji: String,
    val colorHex: String
) {
    val color: Color
        get() {
            return try {
                val androidColor = colorHex.toColorInt()
                Color(androidColor)
            } catch (e: Exception) {
                Color(0xFF9E9E9E)
            }
        }
}