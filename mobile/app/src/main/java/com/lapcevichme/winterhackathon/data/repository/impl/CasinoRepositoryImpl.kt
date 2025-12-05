package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.mapper.toDomain
import com.lapcevichme.winterhackathon.data.remote.CasinoApiService
import com.lapcevichme.winterhackathon.data.remote.SpinRequest
import com.lapcevichme.winterhackathon.data.remote.ValidationErrorResponse
import com.lapcevichme.winterhackathon.domain.model.casino.SpinResponse
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository
import kotlinx.serialization.json.Json
import retrofit2.HttpException
import javax.inject.Inject

class CasinoRepositoryImpl @Inject constructor(
    private val api: CasinoApiService
) : CasinoRepository {

    private val json = Json { ignoreUnknownKeys = true }

    override suspend fun getUserBalance(): Int {
        return try {
            api.getUserBalance().balance
        } catch (e: Exception) {
            throw handleException(e)
        }
    }

    override suspend fun spin(bet: Int): SpinResponse {
        return try {
            val request = SpinRequest(bet = bet)
            val responseDto = api.spin(request)
            responseDto.toDomain()
        } catch (e: Exception) {
            throw handleException(e)
        }
    }

    private fun handleException(e: Exception): Exception {
        if (e is HttpException) {
            when (e.code()) {
                400, 422 -> {
                    try {
                        val errorBody = e.response()?.errorBody()?.string()
                        if (errorBody != null) {
                            return if (errorBody.contains("\"detail\"")) {
                                val validationError = json.decodeFromString<ValidationErrorResponse>(errorBody)
                                val errorMessage = validationError.detail?.joinToString("\n") {
                                    it.msg
                                } ?: "Ошибка валидации"
                                Exception(errorMessage)
                            } else {
                                Exception(errorBody)
                            }
                        }
                    } catch (parsingError: Exception) {
                        parsingError.printStackTrace()
                        return Exception("Ошибка казино: ${e.code()}")
                    }
                }
                401 -> return Exception("Нужна авторизация")
                in 500..599 -> {
                    return Exception("Казино закрыто на переучет (Ошибка сервера ${e.code()})")
                }
                else -> {
                    return Exception("Ошибка сети: ${e.code()} ${e.message()}")
                }
            }
        }
        return e
    }
}