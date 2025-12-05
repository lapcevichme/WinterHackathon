package com.lapcevichme.winterhackathon.data.mapper

import com.lapcevichme.winterhackathon.data.remote.TeamLeaderboardEntryDto
import com.lapcevichme.winterhackathon.data.remote.UserLeaderboardEntryDto
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardEntry
import com.lapcevichme.winterhackathon.domain.model.leaderboard.Trend


fun TeamLeaderboardEntryDto.toDomain(rank: Int): LeaderboardEntry {
    return LeaderboardEntry(
        id = this.username,
        rank = rank,
        name = this.username,
        score = this.maxScore,
        subLabel = "Баланс: ${this.amount}",
        trend = Trend.STABLE
    )
}

fun UserLeaderboardEntryDto.toDomain(rank: Int): LeaderboardEntry {
    return LeaderboardEntry(
        id = this.id ?: this.username,
        rank = rank,
        name = this.username,
        score = this.maxScore ?: 0,
        subLabel = this.department ?: "Игрок",
        trend = Trend.STABLE
    )
}