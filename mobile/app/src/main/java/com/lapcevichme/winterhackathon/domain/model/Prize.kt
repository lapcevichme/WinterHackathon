package com.lapcevichme.winterhackathon.domain.model

import androidx.compose.ui.graphics.Color

data class Prize(
    val id: String,
    val name: String,
    val type: PrizeType,
    val amount: Int = 0,
    val emoji: String,
    val colorHex: Long
) {
    val color: Color get() = Color(colorHex)
}