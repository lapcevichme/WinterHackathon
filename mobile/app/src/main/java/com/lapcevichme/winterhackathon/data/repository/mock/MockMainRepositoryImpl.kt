package com.lapcevichme.winterhackathon.data.repository.mock

import com.lapcevichme.winterhackathon.domain.model.main.ActiveGame
import com.lapcevichme.winterhackathon.domain.model.main.DailyQuest
import com.lapcevichme.winterhackathon.domain.model.main.MainScreenData
import com.lapcevichme.winterhackathon.domain.model.main.UserSummary
import com.lapcevichme.winterhackathon.domain.repository.MainRepository
import kotlinx.coroutines.delay
import javax.inject.Inject

class MockMainRepositoryImpl @Inject constructor() : MainRepository {
    override suspend fun getMainScreenData(): MainScreenData {
        delay(800)

        return MainScreenData(
            userSummary = UserSummary(
                id = "1",
                displayName = "Егор Винник",
                department = "IT Отдел",
                winStreak = 3,
                balance = 1250
            ),
            activeGame = ActiveGame("Flappy Bird"),
            quests = listOf(
                DailyQuest("1", "Сыграть 3 матча", 1, 3, 50),
                DailyQuest("2", "Победить HR отдел", 0, 1, 100),
                DailyQuest("3", "Заработать 500 очков", 500, 500, 25, isCompleted = true)
            )
        )
    }
}
