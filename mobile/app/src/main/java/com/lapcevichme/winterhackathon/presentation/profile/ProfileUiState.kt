package com.lapcevichme.winterhackathon.presentation.profile

import com.lapcevichme.winterhackathon.domain.model.profile.InventoryItem
import com.lapcevichme.winterhackathon.domain.model.profile.UserProfile

data class ProfileUiState(
    val isLoading: Boolean = false,
    val profile: UserProfile? = null,
    val error: String? = null,
    val isRedeemLoading: Boolean = false,
    val selectedItem: InventoryItem? = null,
    val redeemToken: String? = null,
    val isLoggedOut: Boolean = false,
    val isEditDialogVisible: Boolean = false,
    val isAvatarUploading: Boolean = false
)