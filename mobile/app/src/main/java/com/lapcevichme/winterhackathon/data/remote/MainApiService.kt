package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.GET

interface MainApiService {
    @GET("main")
    suspend fun getMainData(): MainResponseDto
}

@Serializable
data class MainResponseDto(
    @SerialName("user_summary") val userSummary: UserSummaryDto,
    @SerialName("games") val games: List<GameInfoDto>? = null
)

@Serializable
data class UserSummaryDto(
    @SerialName("id") val id: String,
    @SerialName("display_name") val displayName: String?,
    @SerialName("balance") val balance: BalanceDto,
    @SerialName("energy") val energy: EnergyStateDto
)

@Serializable
data class EnergyStateDto(
    @SerialName("current") val current: Int,
    @SerialName("max") val max: Int,
    @SerialName("next_refill_in_seconds") val nextRefillInSeconds: Int
)

@Serializable
data class GameInfoDto(
    @SerialName("slug") val slug: String,
    @SerialName("name") val name: String,
    @SerialName("energy_cost") val energyCost: Int
)