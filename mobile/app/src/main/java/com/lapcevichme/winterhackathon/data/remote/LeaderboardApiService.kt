package com.lapcevichme.winterhackathon.data.remote

import com.lapcevichme.winterhackathon.domain.model.leaderboard.LeaderboardType
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.GET
import retrofit2.http.Query

interface LeaderboardApiService {
    @GET("leaderboard")
    suspend fun getLeaderboard(@Query("type") type: LeaderboardType): List<LeaderboardEntryDto>
}

@Serializable
data class LeaderboardEntryDto(
    @SerialName("rank") val rank: Int,
    @SerialName("name") val name: String,
    @SerialName("score") val score: Int,
    @SerialName("trend") val trend: String
)
