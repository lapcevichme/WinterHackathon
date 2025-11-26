package com.lapcevichme.winterhackathon.domain.model

import androidx.compose.ui.graphics.Color

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
                val androidColor = android.graphics.Color.parseColor(colorHex)
                Color(androidColor)
            } catch (e: Exception) {
                Color(0xFF9E9E9E)
            }
        }
}