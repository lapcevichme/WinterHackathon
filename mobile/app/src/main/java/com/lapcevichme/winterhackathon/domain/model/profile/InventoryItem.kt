package com.lapcevichme.winterhackathon.domain.model.profile

import com.lapcevichme.winterhackathon.domain.model.casino.PrizeType

data class InventoryItem(
    val id: String,
    val prizeId: String,
    val name: String,
    val type: PrizeType,
    val status: ItemStatus,
    val amount: Int,
    val emoji: String,
    val colorHex: String
)
