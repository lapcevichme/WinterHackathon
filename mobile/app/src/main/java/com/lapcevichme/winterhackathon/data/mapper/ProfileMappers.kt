package com.lapcevichme.winterhackathon.data.mapper

import com.lapcevichme.winterhackathon.data.remote.InventoryItemDto
import com.lapcevichme.winterhackathon.data.remote.UserProfileDto
import com.lapcevichme.winterhackathon.domain.model.casino.Prize
import com.lapcevichme.winterhackathon.domain.model.casino.PrizeType
import com.lapcevichme.winterhackathon.domain.model.profile.UserProfile

fun UserProfileDto.toDomain(): UserProfile {
    return UserProfile(
        id = id,
        username = username,
        displayName = displayName,
        department = department,
        avatarUrl = avatarUrl,
        level = level,
        xp = xp,
        maxXp = maxXp,
        inventory = inventory.map { it.toDomain() }
    )
}

fun InventoryItemDto.toDomain(): Prize {
    return Prize(
        id = id,
        name = name,
        type = mapPrizeType(type),
        amount = amount,
        emoji = emoji,
        colorHex = colorHex
    )
}

private fun mapPrizeType(typeString: String): PrizeType {
    return try {
        PrizeType.valueOf(typeString.uppercase())
    } catch (e: Exception) {
        PrizeType.TRASH
    }
}