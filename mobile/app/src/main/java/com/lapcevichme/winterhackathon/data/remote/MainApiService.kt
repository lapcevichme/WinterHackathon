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
    @SerialName("active_game") val activeGame: ActiveGameDto,
    @SerialName("quests") val quests: List<QuestDto>
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
data class ActiveGameDto(
    @SerialName("name") val name: String,
    @SerialName("energy_cost") val energyCost: Int,
    @SerialName("is_available") val isAvailable: Boolean
)

@Serializable
data class QuestDto(
    @SerialName("id") val id: String,
    @SerialName("title") val title: String,
    @SerialName("progress") val progress: Int,
    @SerialName("max_progress") val maxProgress: Int,
    @SerialName("reward") val reward: BalanceDto,
    @SerialName("is_completed") val isCompleted: Boolean,
    @SerialName("is_claimed") val isClaimed: Boolean
)