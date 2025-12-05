package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.remote.MainApiService
import com.lapcevichme.winterhackathon.domain.model.main.ActiveGame
import com.lapcevichme.winterhackathon.domain.model.main.DailyQuest
import com.lapcevichme.winterhackathon.domain.model.main.MainScreenData
import com.lapcevichme.winterhackathon.domain.model.main.UserSummary
import com.lapcevichme.winterhackathon.domain.repository.MainRepository
import javax.inject.Inject

class MainRepositoryImpl @Inject constructor(
    private val api: MainApiService
) : MainRepository {

    override suspend fun getMainScreenData(): MainScreenData {
        val response = api.getMainData()

        return MainScreenData(
            userSummary = UserSummary(
                id = response.userSummary.id,
                displayName = response.userSummary.displayName ?: "Игрок",
                department = "Отдел разработки",
                winStreak = 0,
                balance = response.userSummary.balance.amount
            ),
            activeGame = ActiveGame(
                name = response.activeGame.name,
                energyCost = response.activeGame.energyCost,
                isAvailable = response.activeGame.isAvailable
            ),
            quests = response.quests.map { dto ->
                DailyQuest(
                    id = dto.id,
                    title = dto.title,
                    currentProgress = dto.progress,
                    maxProgress = dto.maxProgress,
                    reward = dto.reward.amount,
                    isCompleted = dto.isCompleted
                )
            }
        )
    }
}