package com.lapcevichme.winterhackathon.domain.model.leaderboard

data class LeaderboardEntry(
    val id: String,
    val rank: Int,
    val name: String,
    val score: Int,
    val subLabel: String, // Например, название отдела для игрока
    val trend: Trend = Trend.STABLE,
    val avatarUrl: String? = null
)