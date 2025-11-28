package com.lapcevichme.winterhackathon.presentation.profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.domain.model.casino.Prize
import com.lapcevichme.winterhackathon.domain.usecase.GenerateRedeemTokenUseCase
import com.lapcevichme.winterhackathon.domain.usecase.GetProfileUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject


@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val getProfileUseCase: GetProfileUseCase,
    private val generateRedeemTokenUseCase: GenerateRedeemTokenUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    init {
        loadProfile()
    }

    fun refresh() {
        loadProfile()
    }

    private fun loadProfile() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val profile = getProfileUseCase()
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        profile = profile
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        error = "Не удалось загрузить профиль: ${e.message}"
                    )
                }
            }
        }
    }

    fun onRedeemItemClicked(prize: Prize) {
        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    selectedPrize = prize,
                    isRedeemLoading = true,
                    redeemToken = null
                )
            }

            try {
                val token = generateRedeemTokenUseCase(prize.id)
                _uiState.update {
                    it.copy(
                        isRedeemLoading = false,
                        redeemToken = token
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isRedeemLoading = false,
                        selectedPrize = null,
                        error = "Ошибка генерации QR: ${e.message}"
                    )
                }
            }
        }
    }

    fun onDismissRedeemDialog() {
        _uiState.update {
            it.copy(
                selectedPrize = null,
                redeemToken = null,
                isRedeemLoading = false
            )
        }
    }
}