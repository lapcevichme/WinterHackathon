package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.data.remote.AdminRedeemResponse
import com.lapcevichme.winterhackathon.domain.repository.AdminRepository
import javax.inject.Inject

class RedeemPrizeUseCase @Inject constructor(
    private val repository: AdminRepository
) {
    suspend operator fun invoke(token: String): Result<AdminRedeemResponse> {
        if (token.isBlank()) return Result.failure(IllegalArgumentException("Token is empty"))
        return repository.redeemPrize(token)
    }
}