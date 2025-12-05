package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.mapper.toDomain
import com.lapcevichme.winterhackathon.data.remote.LeaderboardApiService
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardEntry
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardType
import com.lapcevichme.winterhackathon.domain.repository.LeaderboardRepository
import javax.inject.Inject

class LeaderboardRepositoryImpl @Inject constructor(
    private val api: LeaderboardApiService
) : LeaderboardRepository {

    override suspend fun getLeaderboard(type: LeaderboardType): List<LeaderboardEntry> {
        return try {
            val response = api.getLeaderboard(type)
            response.map { it.toDomain() }
        } catch (e: Exception) {
            e.printStackTrace()
            throw e
        }
    }
}