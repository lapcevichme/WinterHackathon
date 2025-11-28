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
                LeaderboardEntry("1", 1, "IT Отдел", 154000, "24 сотрудника", Trend.UP),
                LeaderboardEntry("2", 2, "Продажи", 142050, "18 сотрудников", Trend.DOWN),
                LeaderboardEntry("3", 3, "HR", 98000, "5 сотрудников", Trend.STABLE),
                LeaderboardEntry("4", 4, "Маркетинг", 85000, "12 сотрудников", Trend.UP),
                LeaderboardEntry("5", 5, "Бухгалтерия", 42000, "8 сотрудников", Trend.DOWN),
            )
            LeaderboardType.PLAYERS -> listOf(
                LeaderboardEntry("p1", 1, "Егор Винник", 24500, "IT Отдел", Trend.UP),
                LeaderboardEntry("p2", 2, "Алексей Смирнов", 21000, "Продажи", Trend.STABLE),
                LeaderboardEntry("p3", 3, "Мария Иванова", 19500, "HR", Trend.UP),
                LeaderboardEntry("p4", 4, "Дмитрий Козлов", 18200, "IT Отдел", Trend.DOWN),
                LeaderboardEntry("p5", 5, "Анна Петрова", 15000, "Маркетинг", Trend.STABLE),
                LeaderboardEntry("p6", 6, "Сергей Волков", 12000, "Продажи", Trend.DOWN),
                LeaderboardEntry("p7", 7, "Елена Соколова", 11500, "Бухгалтерия", Trend.UP),
            )
        }
    }
}
