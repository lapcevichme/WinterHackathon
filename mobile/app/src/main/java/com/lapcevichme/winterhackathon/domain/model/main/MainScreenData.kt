package com.lapcevichme.winterhackathon.domain.model.main

data class MainScreenData(
    val userSummary: UserSummary,
    val activeGame: ActiveGame,
    val quests: List<DailyQuest>
)