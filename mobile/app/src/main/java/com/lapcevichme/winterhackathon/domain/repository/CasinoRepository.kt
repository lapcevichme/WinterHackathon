package com.lapcevichme.winterhackathon.domain.repository

import com.lapcevichme.winterhackathon.domain.model.casino.SpinResponse


interface CasinoRepository {
    suspend fun getUserBalance(): Int
    suspend fun spin(bet: Int): SpinResponse
}