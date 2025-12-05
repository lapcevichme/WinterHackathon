package com.lapcevichme.winterhackathon.presentation

import androidx.lifecycle.ViewModel
import com.lapcevichme.winterhackathon.domain.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject

@HiltViewModel
class MainViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {
    val isUserLoggedIn: Boolean = authRepository.isUserLoggedIn()
}