package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.Response
import retrofit2.http.GET

interface UserApiService {
    @GET("users/me/")
    suspend fun getUserMe(): Response<UserModel>
}

@Serializable
data class UserModel(
    @SerialName("id")
    val id: String,
    @SerialName("email")
    val email: String,
    @SerialName("username")
    val username: String?,
    @SerialName("display_name")
    val displayName: String?,
    @SerialName("role")
    val role: String,
    @SerialName("role_slugs")
    val roleSlugs: List<String>? = emptyList(),
    @SerialName("banned")
    val banned: Boolean
)