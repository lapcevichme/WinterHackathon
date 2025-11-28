package com.lapcevichme.winterhackathon.presentation.leaderboard

import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardEntry
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardType

data class LeaderboardUiState(
    val isLoading: Boolean = false,
    val leaderboard: List<LeaderboardEntry> = emptyList(),
    val selectedType: LeaderboardType = LeaderboardType.DEPARTMENTS,
    val error: String? = null
)