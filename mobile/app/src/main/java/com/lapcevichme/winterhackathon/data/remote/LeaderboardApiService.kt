package com.lapcevichme.winterhackathon.data.remote
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.GET

interface LeaderboardApi {
    @GET("/v1/user/leaderboard/team")
    suspend fun getTeamLeaderboard(): TeamLeaderboardResponseDto

    @GET("/v1/user/leaderboard/user")
    suspend fun getUserLeaderboard(): UserLeaderboardResponseDto
}

@Serializable
data class TeamLeaderboardResponseDto(
    @SerialName("leaders")
    val leaders: List<TeamLeaderboardEntryDto>
)

@Serializable
data class UserLeaderboardResponseDto(
    @SerialName("leaders")
    val leaders: List<UserLeaderboardEntryDto>
)

@Serializable
data class TeamLeaderboardEntryDto(
    @SerialName("username") val username: String,
    @SerialName("max_score") val maxScore: Int,
    @SerialName("amount") val amount: Int
)

@Serializable
data class UserLeaderboardEntryDto(
    @SerialName("id") val id: String? = null,
    @SerialName("username") val username: String,
    @SerialName("max_score") val maxScore: Int? = null,
    @SerialName("amount") val amount: Int? = null,
    @SerialName("department") val department: String? = null
)