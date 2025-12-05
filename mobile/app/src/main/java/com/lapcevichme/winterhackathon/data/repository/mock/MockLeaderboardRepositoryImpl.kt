package com.lapcevichme.winterhackathon.data.repository.mock

import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardEntry
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardType
import com.lapcevichme.winterhackathon.domain.model.leaderboard.Trend
import com.lapcevichme.winterhackathon.domain.repository.LeaderboardRepository
import kotlinx.coroutines.delay
import javax.inject.Inject

class MockLeaderboardRepositoryImpl @Inject constructor() : LeaderboardRepository {

    override suspend fun getLeaderboard(type: LeaderboardType): List<LeaderboardEntry> {
        delay(800)

        return when (type) {
            LeaderboardType.DEPARTMENTS -> listOf(
                LeaderboardEntry(1, "IT Отдел", 154000, Trend.UP),
                LeaderboardEntry(2, "Продажи", 142050, Trend.DOWN),
                LeaderboardEntry(3, "HR", 98000, Trend.SAME),
                LeaderboardEntry(4, "Маркетинг", 85000, Trend.UP),
                LeaderboardEntry(5, "Бухгалтерия", 42000, Trend.DOWN),
            )
            LeaderboardType.PLAYERS -> listOf(
                LeaderboardEntry(1, "Егор Винник", 24500, Trend.UP),
                LeaderboardEntry(2, "Алексей Смирнов", 21000, Trend.SAME),
                LeaderboardEntry(3, "Мария Иванова", 19500, Trend.UP),
                LeaderboardEntry(4, "Дмитрий Козлов", 18200, Trend.DOWN),
                LeaderboardEntry(5, "Анна Петрова", 15000, Trend.SAME),
                LeaderboardEntry(6, "Сергей Волков", 12000, Trend.DOWN),
                LeaderboardEntry(7, "Елена Соколова", 11500, Trend.UP),
            )
        }
    }
}
