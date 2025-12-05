package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.POST

interface AuthApiService {
    @FormUrlEncoded
    @POST("v1/auth/login")
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String,
        @Field("scope") scope: String = "",
        @Field("grant_type") grantType: String = "password"
    ): TokenDto

    @POST("v1/auth/register")
    suspend fun register(
        @Body request: RegisterRequest
    ): TokenDto

    @POST("v1/auth/logout")
    suspend fun logout(): Any
}
@Serializable
data class TokenDto(
    @SerialName("access_token")
    val accessToken: String,

    @SerialName("refresh_token")
    val refreshToken: String,

    @SerialName("token_type")
    val tokenType: String = "bearer"
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

@Serializable
data class RegisterRequest(
    @SerialName("username")
    val username: String,
    @SerialName("password")
    val password: String,
    @SerialName("email")
    val email: String,
    @SerialName("display_name")
    val displayName: String
)