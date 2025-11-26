package com.lapcevichme.winterhackathon.presentation.casino

import com.lapcevichme.winterhackathon.domain.model.Prize

data class CasinoUiState(
    val balance: Int = 0,
    val items: List<Prize> = emptyList(),
    val isSpinning: Boolean = false,
    val isLoading: Boolean = false,
    val lastWin: Prize? = null,
    val winningIndex: Int = 40,
    val error: String? = null
)