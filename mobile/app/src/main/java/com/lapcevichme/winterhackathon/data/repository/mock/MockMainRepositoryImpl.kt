package com.lapcevichme.winterhackathon.data.repository.mock

import com.lapcevichme.winterhackathon.domain.model.casino.Balance
import com.lapcevichme.winterhackathon.domain.model.main.EnergyState
import com.lapcevichme.winterhackathon.domain.model.main.GameInfo
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
                balance = Balance(1250, "❄️"),
                energy = EnergyState(3, 5, 3600)
            ),
            games = listOf(
                GameInfo("flappy-bird", "Flappy Bird", 1),
                GameInfo("snake", "Snake", 1)
            )
        )
    }
}
