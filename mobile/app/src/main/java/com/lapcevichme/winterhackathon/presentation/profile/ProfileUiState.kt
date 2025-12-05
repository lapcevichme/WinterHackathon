package com.lapcevichme.winterhackathon.presentation.profile

import com.lapcevichme.winterhackathon.domain.model.casino.Prize
import com.lapcevichme.winterhackathon.domain.model.profile.UserProfile

data class ProfileUiState(
    val isLoading: Boolean = false,
    val profile: UserProfile? = null,
    val error: String? = null,
    val isRedeemLoading: Boolean = false,
    val selectedPrize: Prize? = null,
    val redeemToken: String? = null,
    val isLoggedOut: Boolean = false
)