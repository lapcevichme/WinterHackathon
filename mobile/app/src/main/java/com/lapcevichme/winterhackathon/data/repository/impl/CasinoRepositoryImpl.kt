package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.mapper.toDomain
import com.lapcevichme.winterhackathon.data.remote.CasinoApiService
import com.lapcevichme.winterhackathon.data.remote.SpinRequest
import com.lapcevichme.winterhackathon.domain.model.casino.SpinResponse
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository
import javax.inject.Inject

class CasinoRepositoryImpl @Inject constructor(
    private val api: CasinoApiService
) : CasinoRepository {

    override suspend fun getUserBalance(): Int {
        return api.getUserBalance().balance
    }

    override suspend fun spin(bet: Int): SpinResponse {
        val request = SpinRequest(bet = bet)
        val responseDto = api.spin(request)
        return responseDto.toDomain()
    }
}