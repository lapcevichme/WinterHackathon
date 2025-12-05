package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

interface AuthApiService {

    @POST("auth/login")
    suspend fun login(
        @Body request: LoginRequest,
        @Header("X-Client") client: String = "mobile"
    ): TokenDto

    @POST("auth/register")
    suspend fun register(
        @Body request: RegisterRequest,
        @Header("X-Client") client: String = "mobile"
    ): TokenDto

    @POST("auth/refresh")
    suspend fun refresh(
        @Header("Authorization") refreshToken: String
    ): TokenDto

    @POST("auth/logout")
    suspend fun logout(): Any
}

@Serializable
data class TokenDto(
    @SerialName("access_token")
    val accessToken: String,

    @SerialName("refresh_token")
    val refreshToken: String?,

    @SerialName("token_type")
    val tokenType: String = "bearer"
)

@Serializable
data class LoginRequest(
    @SerialName("email")
    val email: String,
    @SerialName("password")
    val password: String
)

@Serializable
data class RegisterRequest(
    @SerialName("email")
    val email: String,
    @SerialName("password")
    val password: String,
    @SerialName("username")
    val username: String? = null
)

@Serializable
data class ValidationErrorResponse(
    @SerialName("detail")
    val detail: List<ValidationErrorDetail>?
)

@Serializable
data class ValidationErrorDetail(
    @SerialName("loc")
    val loc: List<String>,
    @SerialName("msg")
    val msg: String,
    @SerialName("type")
    val type: String
)