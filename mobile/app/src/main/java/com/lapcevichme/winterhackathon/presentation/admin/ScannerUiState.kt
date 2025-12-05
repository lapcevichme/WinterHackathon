package com.lapcevichme.winterhackathon.presentation.admin

import com.lapcevichme.winterhackathon.data.remote.AdminRedeemResponse

data class ScannerUiState(
    val isScanning: Boolean = true,
    val isLoading: Boolean = false,
    val successResponse: AdminRedeemResponse? = null,
    val error: String? = null
)