package com.lapcevichme.winterhackathon.presentation.main

import com.lapcevichme.winterhackathon.domain.model.main.MainScreenData

data class MainUiState(
    val isLoading: Boolean = false,
    val data: MainScreenData? = null,
    val error: String? = null
)