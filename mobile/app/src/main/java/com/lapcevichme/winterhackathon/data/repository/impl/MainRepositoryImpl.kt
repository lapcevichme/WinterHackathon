//package com.lapcevichme.winterhackathon.data.repository.impl
//
//import com.lapcevichme.winterhackathon.data.remote.MainApiService
//import com.lapcevichme.winterhackathon.domain.model.main.ActiveGame
//import com.lapcevichme.winterhackathon.domain.model.main.DailyQuest
//import com.lapcevichme.winterhackathon.domain.model.main.MainScreenData
//import com.lapcevichme.winterhackathon.domain.model.main.UserSummary
//import com.lapcevichme.winterhackathon.domain.repository.MainRepository
//import javax.inject.Inject
//
//class MainRepositoryImpl @Inject constructor(
//    private val api: MainApiService
//) : MainRepository {
//
//    override suspend fun getMainScreenData(): MainScreenData {
//        val response = api.getMainData()
//
//        return MainScreenData(
//            userSummary = UserSummary(
//                id = response.userSummary.id,
//                displayName = response.userSummary.displayName,
//                department = response.userSummary.department ?: "Без отдела",
//                winStreak = response.userSummary.winStreak ?: 0,
//                balance = response.userSummary.balance ?: 0
//            ),
//            activeGame = response.activeGame?.let { ActiveGame(it.name) } ?: ActiveGame("Нет активной игры"),
//            quests = response.quests.map { dto ->
//                DailyQuest(
//                    id = dto.id,
//                    description = dto.description,
//                    currentProgress = dto.currentProgress,
//                    targetProgress = dto.targetProgress,
//                    reward = dto.rewardAmount,
//                    isCompleted = dto.isCompleted
//                )
//            }
//        )
//    }
//}