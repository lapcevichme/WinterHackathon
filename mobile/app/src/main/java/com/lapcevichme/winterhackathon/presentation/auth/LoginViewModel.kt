package com.lapcevichme.winterhackathon.presentation.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.data.remote.RegisterRequest
import com.lapcevichme.winterhackathon.domain.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class LoginViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(LoginUiState())
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()

    fun toggleMode() {
        _uiState.update { it.copy(isLoginMode = !it.isLoginMode, error = null) }
    }

    fun submit(
        username: String,
        password: String,
        email: String,
        displayName: String,
        departmentId: String?
    ) {
        val isLogin = _uiState.value.isLoginMode

        if (email.isBlank() || password.isBlank()) {
            _uiState.update { it.copy(error = "Email и пароль обязательны") }
            return
        }

        if (!isLogin) {
            // Для регистрации нужен еще username (как минимум)
            if (username.isBlank()) {
                _uiState.update { it.copy(error = "Укажите Username") }
                return
            }
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            val result = if (isLogin) {
                authRepository.login(email = email, password = password)
            } else {
                val request = RegisterRequest(
                    email = email,
                    password = password,
                    username = username
                    // displayName и departmentId
                )
                authRepository.register(request)
            }

            result.fold(
                onSuccess = {
                    _uiState.update { it.copy(isLoading = false, isSuccess = true) }
                },
                onFailure = { error ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = error.message ?: "Ошибка соединения с сервером"
                        )
                    }
                }
            )
        }
    }

    fun errorShown() {
        _uiState.update { it.copy(error = null) }
    }
}