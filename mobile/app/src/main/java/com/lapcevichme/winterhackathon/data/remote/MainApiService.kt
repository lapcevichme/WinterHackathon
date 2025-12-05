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
    @SerialName("active_game") val activeGame: ActiveGameDto?,
    @SerialName("quests") val quests: List<QuestDto>
)

@Serializable
data class UserSummaryDto(
    @SerialName("id") val id: String,
    @SerialName("display_name") val displayName: String,
    @SerialName("department") val department: String?,
    @SerialName("win_streak") val winStreak: Int? = 0,
    @SerialName("balance") val balance: Int? = 0,
    @SerialName("avatar_url") val avatarUrl: String? = null
)

@Serializable
data class ActiveGameDto(
    @SerialName("name") val name: String,
    @SerialName("id") val id: String? = null
)

@Serializable
data class QuestDto(
    @SerialName("id") val id: String,
    @SerialName("description") val description: String,
    @SerialName("current_progress") val currentProgress: Int,
    @SerialName("target_progress") val targetProgress: Int,
    @SerialName("reward_amount") val rewardAmount: Int,
    @SerialName("is_completed") val isCompleted: Boolean
)