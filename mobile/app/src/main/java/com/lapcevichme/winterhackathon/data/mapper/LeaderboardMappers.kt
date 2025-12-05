package com.lapcevichme.winterhackathon.data.mapper

import com.lapcevichme.winterhackathon.data.remote.LeaderboardEntryDto
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardEntry
import com.lapcevichme.winterhackathon.domain.model.leaderboard.Trend

fun LeaderboardEntryDto.toDomain(): LeaderboardEntry {
    return LeaderboardEntry(
        rank = rank,
        name = name,
        score = score,
        trend = try {
            Trend.valueOf(trend.uppercase())
        } catch (e: Exception) {
            Trend.SAME
        }
    )
}
