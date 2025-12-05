package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.remote.AdminApiService
import com.lapcevichme.winterhackathon.data.remote.AdminRedeemRequest
import com.lapcevichme.winterhackathon.data.remote.AdminRedeemResponse
import com.lapcevichme.winterhackathon.domain.repository.AdminRepository
import javax.inject.Inject

class AdminRepositoryImpl @Inject constructor(
    private val api: AdminApiService
) : AdminRepository {
    override suspend fun redeemPrize(token: String): Result<AdminRedeemResponse> {
        return try {
            val response = api.redeemPrize(AdminRedeemRequest(token))
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Error: ${response.code()} ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}