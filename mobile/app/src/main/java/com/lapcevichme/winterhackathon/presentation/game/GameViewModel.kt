package com.lapcevichme.winterhackathon.presentation.game

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.domain.usecase.SendScoreUseCase
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
    private val sendScoreUseCase: SendScoreUseCase
) : ViewModel() {

    private val _events = Channel<GameEvent>()
    val events = _events.receiveAsFlow()

    fun onScoreReceived(score: Int) {
        viewModelScope.launch {
            try {
                sendScoreUseCase(score)
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