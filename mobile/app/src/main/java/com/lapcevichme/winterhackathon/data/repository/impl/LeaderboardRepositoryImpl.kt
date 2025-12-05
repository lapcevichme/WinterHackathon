package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.mapper.toDomain
import com.lapcevichme.winterhackathon.data.remote.LeaderboardApi
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardEntry
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardType
import com.lapcevichme.winterhackathon.domain.repository.LeaderboardRepository
import javax.inject.Inject

class LeaderboardRepositoryImpl @Inject constructor(
    private val api: LeaderboardApi
) : LeaderboardRepository {

    override suspend fun getLeaderboard(type: LeaderboardType): List<LeaderboardEntry> {
        return try {
            when (type) {
                LeaderboardType.DEPARTMENTS -> {
                    val response = api.getTeamLeaderboard()
                    response.leaders.mapIndexed { index, dto ->
                        dto.toDomain(rank = index + 1)
                    }
                }
                LeaderboardType.PLAYERS -> {
                    val response = api.getUserLeaderboard()
                    response.leaders.mapIndexed { index, dto ->
                        dto.toDomain(rank = index + 1)
                    }
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
            throw e
        }
    }
}