package com.lapcevichme.winterhackathon.domain.model.main

data class UserSummary(
    val id: String,
    val displayName: String,
    val department: String,
    val winStreak: Int,
    val balance: Int
)