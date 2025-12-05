package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface GameApi {
    @GET("game/start")
    suspend fun startGame(): GameStartResponseDto

    @POST("game/result")
    suspend fun sendGameResult(@Body body: GameResultRequestDto)
}


@Serializable
data class GameStartResponseDto(
    @SerialName("session") val sessionId: String,
    @SerialName("user_1") val user1Id: String,
    @SerialName("user_2") val user2Id: String
)

@Serializable
data class GameResultRequestDto(
    @SerialName("session_id") val sessionId: String,
    @SerialName("score") val score: Int,
    @SerialName("winner_id") val winnerId: Int
)