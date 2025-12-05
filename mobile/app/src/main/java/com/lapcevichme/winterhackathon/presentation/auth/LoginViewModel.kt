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
        nickname: String,
        password: String,
        email: String,
        displayName: String,
        departmentId: String?
    ) {
        val isLogin = _uiState.value.isLoginMode

        if (nickname.isBlank() || password.isBlank()) {
            _uiState.update { it.copy(error = "Заполните Логин и Пароль") }
            return
        }

        if (!isLogin) {
            if (email.isBlank() || displayName.isBlank()) {
                _uiState.update { it.copy(error = "Заполните Email и Имя") }
                return
            }
            if (departmentId == null) {
                _uiState.update { it.copy(error = "Выберите свой клан (отдел)") }
                return
            }
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            val result = if (isLogin) {
                authRepository.login(username = nickname, password = password)
            } else {
                val request = RegisterRequest(
                    username = nickname,
                    password = password,
                    email = email,
                    displayName = displayName
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