package com.lapcevichme.winterhackathon.domain.repository

import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardEntry
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardType

interface LeaderboardRepository {
    suspend fun getLeaderboard(type: LeaderboardType): List<LeaderboardEntry>
}