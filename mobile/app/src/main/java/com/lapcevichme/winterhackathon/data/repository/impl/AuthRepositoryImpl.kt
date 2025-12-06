package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.core.bus.AuthEvent
import com.lapcevichme.winterhackathon.core.bus.AuthEventBus
import com.lapcevichme.winterhackathon.core.manager.TokenManager
import com.lapcevichme.winterhackathon.data.remote.AuthApiService
import com.lapcevichme.winterhackathon.data.remote.LoginRequest
import com.lapcevichme.winterhackathon.data.remote.RegisterRequest
import com.lapcevichme.winterhackathon.data.remote.ValidationErrorResponse
import com.lapcevichme.winterhackathon.domain.repository.AuthRepository
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import retrofit2.HttpException
import javax.inject.Inject

class AuthRepositoryImpl @Inject constructor(
    private val api: AuthApiService,
    private val tokenManager: TokenManager,
    private val authEventBus: AuthEventBus
) : AuthRepository {

    private val json = Json { ignoreUnknownKeys = true }

    override suspend fun login(email: String, password: String): Result<Unit> {
        return try {
            val request = LoginRequest(email = email, password = password)
            val tokens = api.login(request)
            tokenManager.saveTokens(tokens.accessToken, tokens.refreshToken ?: "")
            Result.success(Unit)
        } catch (e: Exception) {
            e.printStackTrace()
            Result.failure(handleException(e))
        }
    }

    override suspend fun register(request: RegisterRequest): Result<Unit> {
        return try {
            val tokens = api.register(request)
            tokenManager.saveTokens(tokens.accessToken, tokens.refreshToken ?: "")
            Result.success(Unit)
        } catch (e: Exception) {
            e.printStackTrace()
            Result.failure(handleException(e))
        }
    }

    override suspend fun logout(): Result<Unit> {
        return try {
            try { api.logout() } catch (e: Exception) { e.printStackTrace() }
            tokenManager.clearTokens()
            runBlocking {
                authEventBus.postEvent(AuthEvent.LOGOUT)
            }
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override fun isUserLoggedIn(): Boolean {
        return !tokenManager.getAccessToken().isNullOrBlank()
    }

    private fun handleException(e: Exception): Exception {
        if (e is HttpException) {
            when (e.code()) {
                422 -> {
                    try {
                        val errorBody = e.response()?.errorBody()?.string()
                        if (errorBody != null) {
                            val validationError = json.decodeFromString<ValidationErrorResponse>(errorBody)
                            val errorMessage = validationError.detail?.joinToString("\n") {
                                val field = it.loc.lastOrNull() ?: "Поле"
                                "$field: ${it.msg}"
                            }
                            if (!errorMessage.isNullOrBlank()) {
                                return Exception(errorMessage)
                            }
                        }
                    } catch (parsingError: Exception) {
                        parsingError.printStackTrace()
                    }
                }
                in 500..599 -> {
                    return Exception("Сервер приуныл (Ошибка ${e.code()}). Скажи бэкендеру чекнуть логи.")
                }
                else -> {
                    return Exception("Ошибка сети: ${e.code()} ${e.message()}")
                }
            }
        }
        return e
    }
}