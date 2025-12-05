package com.lapcevichme.winterhackathon.presentation

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.core.manager.TokenManager
import com.lapcevichme.winterhackathon.domain.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class MainViewModel @Inject constructor(
    private val tokenManager: TokenManager,
    private val userRepository: UserRepository
) : ViewModel() {

    var isUserLoggedIn by mutableStateOf(false)
        private set

    var isAdmin by mutableStateOf(false)
        private set

    init {
        updateAuthState()
    }

    // Делаем метод публичным, чтобы дергать его из UI при навигации
    fun updateAuthState() {
        val token = tokenManager.getAccessToken()
        if (!token.isNullOrBlank()) {
            isUserLoggedIn = true
            fetchUserRole()
        } else {
            isUserLoggedIn = false
            isAdmin = false
        }
    }

    private fun fetchUserRole() {
        viewModelScope.launch {
            userRepository.getUserMe()
                .onSuccess { user ->
                    isAdmin = user.role == "admin" || user.roleSlugs?.contains("admin") == true
                }
                .onFailure {
                    // Если токен есть, но профиль не грузится - считаем что не админ,
                    // но флаг логина не сбрасываем (пусть обработчики ошибок решают)
                    isAdmin = false
                }
        }
    }
}