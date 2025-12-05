package com.lapcevichme.winterhackathon.domain.model.leaderboard

data class LeaderboardEntry(
    val rank: Int,
    val name: String,
    val score: Int,
    val trend: Trend = Trend.SAME
)