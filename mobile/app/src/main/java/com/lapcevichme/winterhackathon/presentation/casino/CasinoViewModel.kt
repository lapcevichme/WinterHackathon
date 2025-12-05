package com.lapcevichme.winterhackathon.presentation.casino

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository
import com.lapcevichme.winterhackathon.domain.usecase.SpinRouletteUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject
import kotlin.collections.getOrNull

@HiltViewModel
class CasinoViewModel @Inject constructor(
    private val spinUseCase: SpinRouletteUseCase,
    private val repository: CasinoRepository
) : ViewModel() {

    var uiState by mutableStateOf(CasinoUiState())
        private set

    init {
        loadInitialData()
    }

    private fun loadInitialData() {
        viewModelScope.launch {
            try {
                val savedBalance = repository.getUserBalance()
                uiState = uiState.copy(balance = savedBalance)
            } catch (e: Exception) {
                uiState = uiState.copy(error = "Не удалось обновить баланс: ${e.message}")
            }
        }
    }

    fun onSpinClicked() {
        if (uiState.isSpinning || uiState.isLoading) return

        val bet = 10
        if (uiState.balance < bet) {
            uiState = uiState.copy(error = "Недостаточно средств")
            return
        }

        uiState = uiState.copy(isLoading = true, error = null, lastWin = null)

        viewModelScope.launch {
            val result = spinUseCase(bet)

            result.onSuccess { spinResult ->
                uiState = uiState.copy(
                    isLoading = false,
                    items = spinResult.itemsChain,
                    winningIndex = spinResult.winningIndex,
                    isSpinning = true
                )
            }.onFailure {
                uiState = uiState.copy(isLoading = false, error = it.message)
            }
        }
    }

    fun onAnimationFinished() {
        val winner = uiState.items.getOrNull(uiState.winningIndex)

        if (winner != null) {
            viewModelScope.launch {
                try {
                    val trueBalance = repository.getUserBalance()
                    uiState = uiState.copy(
                        balance = trueBalance,
                        lastWin = winner,
                        isSpinning = false
                    )
                } catch (e: Exception) {
                    uiState = uiState.copy(
                        lastWin = winner,
                        isSpinning = false,
                        error = "Сбой синхронизации баланса"
                    )
                }
            }
        }
    }
}