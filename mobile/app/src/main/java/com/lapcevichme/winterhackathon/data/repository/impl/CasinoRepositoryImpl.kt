package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.domain.model.SpinResponse
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository

class NetworkCasinoRepository(/* private val api: ApiService */) : CasinoRepository {
    override suspend fun getUserBalance(): Int {
        // return api.getBalance().amount
        return 0
    }

    override suspend fun spin(bet: Int): SpinResponse {
        // val response = api.spin(SpinRequest(bet))
        TODO("Когда Бэк сделают бахнуть retrofit")
    }
}
