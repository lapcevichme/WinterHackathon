package com.lapcevichme.winterhackathon.domain.repository

import com.lapcevichme.winterhackathon.data.remote.RegisterRequest

interface AuthRepository {
    suspend fun login(username: String, password: String): Result<Unit>
    suspend fun register(request: RegisterRequest): Result<Unit>
    suspend fun logout(): Result<Unit>
    fun isUserLoggedIn(): Boolean
}