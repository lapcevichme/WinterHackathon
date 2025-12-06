package com.lapcevichme.winterhackathon.domain.repository

import com.lapcevichme.winterhackathon.domain.model.team.Team

interface TeamRepository {
    suspend fun getTeams(): Result<List<Team>>
    suspend fun joinTeam(teamId: String): Result<Team>
    suspend fun getTeam(teamId: String): Result<Team>
}
