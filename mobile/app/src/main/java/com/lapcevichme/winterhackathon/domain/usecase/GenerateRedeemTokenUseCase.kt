package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.domain.repository.ProfileRepository
import javax.inject.Inject

class GenerateRedeemTokenUseCase @Inject constructor(
    private val repository: ProfileRepository
) {
    suspend operator fun invoke(itemId: String): String {
        return repository.generateRedeemToken(itemId)
    }
}