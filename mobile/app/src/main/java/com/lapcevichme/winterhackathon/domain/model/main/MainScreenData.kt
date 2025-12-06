package com.lapcevichme.winterhackathon.domain.model.main

data class MainScreenData(
    val userSummary: UserSummary,
    val games: List<GameInfo>?
)