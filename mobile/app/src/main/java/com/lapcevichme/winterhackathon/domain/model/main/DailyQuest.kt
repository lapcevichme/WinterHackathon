package com.lapcevichme.winterhackathon.domain.model.main

data class DailyQuest(
    val id: String,
    val title: String,
    val currentProgress: Int,
    val maxProgress: Int,
    val reward: Int,
    val isCompleted: Boolean = false
)