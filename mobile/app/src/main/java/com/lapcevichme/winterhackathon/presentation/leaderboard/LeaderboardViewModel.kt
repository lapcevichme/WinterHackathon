package com.lapcevichme.winterhackathon.presentation.leaderboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardType
import com.lapcevichme.winterhackathon.domain.usecase.GetLeaderboardUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class LeaderboardViewModel @Inject constructor(
    private val getLeaderboardUseCase: GetLeaderboardUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(LeaderboardUiState())
    val uiState: StateFlow<LeaderboardUiState> = _uiState.asStateFlow()

    init {
        loadLeaderboard(LeaderboardType.DEPARTMENTS)
    }

    fun onTypeChanged(type: LeaderboardType) {
        if (_uiState.value.selectedType == type) return

        _uiState.update { it.copy(selectedType = type) }
        loadLeaderboard(type)
    }

    private fun loadLeaderboard(type: LeaderboardType) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val data = getLeaderboardUseCase(type)
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        leaderboard = data
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        error = "Не удалось загрузить данные: ${e.message}"
                    )
                }
            }
        }
    }
}