package com.lapcevichme.winterhackathon.domain.model.profile

data class UserProfile(
    val id: String,
    val username: String?,
    val displayName: String?,
    val department: String?,
    val avatarUrl: String? = null,
    val level: Int = 1,
    val xp: Int = 0,
    val maxXp: Int = 100,
    val inventory: List<InventoryItem> = emptyList()
)
