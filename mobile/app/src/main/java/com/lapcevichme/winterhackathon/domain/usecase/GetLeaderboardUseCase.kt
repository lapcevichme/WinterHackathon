package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardEntry
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardType
import com.lapcevichme.winterhackathon.domain.repository.LeaderboardRepository
import javax.inject.Inject

class GetLeaderboardUseCase @Inject constructor(
    private val repository: LeaderboardRepository
) {
    suspend operator fun invoke(type: LeaderboardType): List<LeaderboardEntry> {
        return repository.getLeaderboard(type)
    }
}