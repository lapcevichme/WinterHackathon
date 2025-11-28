package com.lapcevichme.winterhackathon.domain.model.main

data class MainScreenData(
    val userSummary: UserSummary,
    val activeGameName: String,
    val quests: List<DailyQuest>
)