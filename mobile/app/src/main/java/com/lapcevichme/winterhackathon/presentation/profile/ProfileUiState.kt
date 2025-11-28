package com.lapcevichme.winterhackathon.presentation.profile

import com.lapcevichme.winterhackathon.domain.model.profile.UserProfile

data class ProfileUiState(
    val isLoading: Boolean = false,
    val profile: UserProfile? = null,
    val error: String? = null
)
