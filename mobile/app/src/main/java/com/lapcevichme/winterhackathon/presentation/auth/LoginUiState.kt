package com.lapcevichme.winterhackathon.presentation.auth

data class LoginUiState(
    val isLoading: Boolean = false,
    val error: String? = null,
    val isSuccess: Boolean = false,
    val isLoginMode: Boolean = false
)