package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.domain.model.profile.UserProfile
import com.lapcevichme.winterhackathon.domain.repository.ProfileRepository
import javax.inject.Inject

class GetProfileUseCase @Inject constructor(
    private val repository: ProfileRepository
) {
    suspend operator fun invoke(): UserProfile {
        return repository.getMyProfile()
    }
}