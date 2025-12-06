package com.lapcevichme.winterhackathon.presentation.profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lapcevichme.winterhackathon.domain.model.profile.InventoryItem
import com.lapcevichme.winterhackathon.domain.repository.ProfileRepository
import com.lapcevichme.winterhackathon.domain.usecase.GenerateRedeemTokenUseCase
import com.lapcevichme.winterhackathon.domain.usecase.GetProfileUseCase
import com.lapcevichme.winterhackathon.domain.usecase.LogoutUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val getProfileUseCase: GetProfileUseCase,
    private val generateRedeemTokenUseCase: GenerateRedeemTokenUseCase,
    private val logoutUseCase: LogoutUseCase,
    private val profileRepository: ProfileRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    init {
        loadProfile()
    }

    fun refresh() {
        loadProfile()
    }

    private fun loadProfile() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val profile = getProfileUseCase()
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        profile = profile
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        error = "Не удалось загрузить профиль: ${e.message}"
                    )
                }
            }
        }
    }

    fun onRedeemItemClicked(item: InventoryItem) {
        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    selectedItem = item,
                    isRedeemLoading = true,
                    redeemToken = null
                )
            }

            try {
                val token = generateRedeemTokenUseCase(item.id)
                _uiState.update {
                    it.copy(
                        isRedeemLoading = false,
                        redeemToken = token
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isRedeemLoading = false,
                        selectedItem = null,
                        error = "Ошибка генерации QR: ${e.message}"
                    )
                }
            }
        }
    }

    fun onDismissRedeemDialog() {
        _uiState.update {
            it.copy(
                selectedItem = null,
                redeemToken = null,
                isRedeemLoading = false
            )
        }
    }

    fun logout() {
        viewModelScope.launch {
            try {
                logoutUseCase()
                _uiState.update { it.copy(isLoggedOut = true) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoggedOut = true) }
            }
        }
    }

    fun consumeLogoutEvent() {
        _uiState.update { it.copy(isLoggedOut = false) }
    }

    fun showEditDialog() {
        _uiState.update { it.copy(isEditDialogVisible = true) }
    }

    fun hideEditDialog() {
        _uiState.update { it.copy(isEditDialogVisible = false) }
    }

    fun updateDisplayName(newName: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, isEditDialogVisible = false) }
            try {
                val updatedProfile = profileRepository.updateProfile(displayName = newName, avatarUrl = null)
                _uiState.update {
                    it.copy(isLoading = false, profile = updatedProfile)
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(isLoading = false, error = "Ошибка обновления: ${e.message}")
                }
            }
        }
    }

    fun uploadAvatar(imageBytes: ByteArray) {
        viewModelScope.launch {
            _uiState.update { it.copy(isAvatarUploading = true) }
            try {
                val updatedProfile = profileRepository.uploadAvatar(imageBytes)
                _uiState.update {
                    it.copy(isAvatarUploading = false, profile = updatedProfile)
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isAvatarUploading = false,
                        error = "Ошибка загрузки фото: ${e.message}"
                    )
                }
            }
        }
    }
}