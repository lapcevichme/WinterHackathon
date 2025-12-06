package com.lapcevichme.winterhackathon.presentation.game

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.domain.usecase.SendScoreUseCase
import com.lapcevichme.winterhackathon.domain.usecase.StartGameUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.receiveAsFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class GameEvent {
    data class ShowScoreToast(val message: String) : GameEvent()
    data object CloseGame : GameEvent()
}

@HiltViewModel
class GameViewModel @Inject constructor(
    private val startGameUseCase: StartGameUseCase,
    private val sendScoreUseCase: SendScoreUseCase,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _events = Channel<GameEvent>()
    val events = _events.receiveAsFlow()

    private var sessionId: String? = null

    init {
        val gameId: String = savedStateHandle.get<String>("gameId")!!
        onGameStarted(gameId)
    }

    private fun onGameStarted(gameId: String) {
        viewModelScope.launch {
            try {
                sessionId = startGameUseCase(gameId)
            } catch (e: Exception) {
                _events.send(GameEvent.ShowScoreToast("Ошибка начала игры: ${e.message}"))
                _events.send(GameEvent.CloseGame)
            }
        }
    }

    fun onScoreReceived(score: Int) {
        viewModelScope.launch {
            try {
                val currentSessionId = sessionId
                if (currentSessionId == null) {
                    _events.send(GameEvent.ShowScoreToast("Ошибка: сессия не найдена"))
                    return@launch
                }
                sendScoreUseCase(currentSessionId, score)
                _events.send(GameEvent.ShowScoreToast("Очки получены: $score"))
            } catch (e: Exception) {
                _events.send(GameEvent.ShowScoreToast("Ошибка сохранения: ${e.message}"))
            }
        }
    }

    fun onCloseRequested() {
        viewModelScope.launch {
            _events.send(GameEvent.CloseGame)
        }
    }
}