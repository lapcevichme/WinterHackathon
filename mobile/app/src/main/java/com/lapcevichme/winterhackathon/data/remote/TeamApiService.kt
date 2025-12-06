package com.lapcevichme.winterhackathon.data.remote

import com.lapcevichme.winterhackathon.domain.model.team.Team
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface TeamApiService {
    @GET("teams/")
    suspend fun getTeams(): List<Team>

    @POST("teams/join")
    suspend fun joinTeam(@Body teamJoinRequest: TeamJoinRequest): Team
}

@Serializable
data class TeamJoinRequest(
    val team_id: String
)
