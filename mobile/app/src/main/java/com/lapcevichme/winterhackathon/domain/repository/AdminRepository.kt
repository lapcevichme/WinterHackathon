package com.lapcevichme.winterhackathon.domain.repository

import com.lapcevichme.winterhackathon.data.remote.AdminRedeemResponse

interface AdminRepository {
    suspend fun redeemPrize(token: String): Result<AdminRedeemResponse>
}