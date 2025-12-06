package com.lapcevichme.winterhackathon.presentation.team

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.domain.model.team.Team
import com.lapcevichme.winterhackathon.domain.usecase.GetTeamUseCase
import com.lapcevichme.winterhackathon.domain.usecase.JoinTeamUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class JoinTeamUiState(
    val isLoading: Boolean = false,
    val error: String? = null,
    val team: Team? = null,
    val joinSuccess: Boolean = false
)

@HiltViewModel
class JoinTeamViewModel @Inject constructor(
    private val getTeamUseCase: GetTeamUseCase,
    private val joinTeamUseCase: JoinTeamUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(JoinTeamUiState())
    val uiState: StateFlow<JoinTeamUiState> = _uiState.asStateFlow()

    fun loadTeam(teamId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            getTeamUseCase(teamId).fold(
                onSuccess = { team ->
                    _uiState.update { it.copy(isLoading = false, team = team) }
                },
                onFailure = { error ->
                    _uiState.update { it.copy(isLoading = false, error = error.message) }
                }
            )
        }
    }

    fun joinTeam(teamId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            joinTeamUseCase(teamId).fold(
                onSuccess = {
                    _uiState.update { it.copy(isLoading = false, joinSuccess = true) }
                },
                onFailure = { error ->
                    _uiState.update { it.copy(isLoading = false, error = error.message) }
                }
            )
        }
    }

    fun errorShown() {
        _uiState.update { it.copy(error = null) }
    }
}
