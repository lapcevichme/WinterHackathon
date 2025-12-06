package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.remote.TeamApiService
import com.lapcevichme.winterhackathon.data.remote.TeamJoinRequest
import com.lapcevichme.winterhackathon.domain.model.team.Team
import com.lapcevichme.winterhackathon.domain.repository.TeamRepository
import javax.inject.Inject

class TeamRepositoryImpl @Inject constructor(
    private val api: TeamApiService
) : TeamRepository {
    override suspend fun getTeams(): Result<List<Team>> {
        return try {
            Result.success(api.getTeams())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun joinTeam(teamId: String): Result<Team> {
        return try {
            Result.success(api.joinTeam(TeamJoinRequest(team_id = teamId)))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun getTeam(teamId: String): Result<Team> {
        return try {
            val teams = api.getTeams()
            val team = teams.firstOrNull { it.id == teamId }
            if (team != null) {
                Result.success(team)
            } else {
                Result.failure(Exception("Team not found"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
