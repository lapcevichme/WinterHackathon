package com.lapcevichme.winterhackathon.presentation.admin

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.domain.usecase.RedeemPrizeUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject


@HiltViewModel
class AdminScannerViewModel @Inject constructor(
    private val redeemPrizeUseCase: RedeemPrizeUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(ScannerUiState())
    val uiState = _uiState.asStateFlow()

    private var isProcessing = false

    fun onCodeScanned(code: String) {
        if (isProcessing) return
        isProcessing = true

        _uiState.update {
            it.copy(isLoading = true, isScanning = false, error = null)
        }

        viewModelScope.launch {
            redeemPrizeUseCase(code)
                .onSuccess { response ->
                    _uiState.update {
                        it.copy(isLoading = false, successResponse = response)
                    }
                }
                .onFailure { error ->
                    _uiState.update {
                        it.copy(isLoading = false, error = error.message ?: "Unknown error")
                    }
                }
        }
    }

    fun resetScanner() {
        isProcessing = false
        _uiState.update { ScannerUiState(isScanning = true) }
    }
}