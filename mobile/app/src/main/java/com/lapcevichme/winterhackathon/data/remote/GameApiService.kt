package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.Path

interface GameApiService {
    @POST("game/{game_id}/start")
    suspend fun startGame(@Path("game_id") gameId: String): GameStartResponse

    @POST("games/{game_id}/launch")
    suspend fun launchGame(@Path("game_id") gameId: String): GameLaunchResponse

    @POST("game/score")
    suspend fun sendScore(@Body body: GameScoreRequest): GameScoreResponse
}

@Serializable
data class GameLaunchResponse(
    @SerialName("launch_url") val launchUrl: String
)

@Serializable
data class GameStartResponse(
    @SerialName("session_id") val sessionId: String,
    @SerialName("energy_left") val energyLeft: Int
)

@Serializable
data class GameScoreRequest(
    @SerialName("session_id") val sessionId: String,
    @SerialName("score") val score: Int
)

@Serializable
data class GameScoreResponse(
    @SerialName("success") val success: Boolean,
    @SerialName("team_score_added") val teamScoreAdded: Int,
    @SerialName("total_team_score") val totalTeamScore: Int? = null
)
