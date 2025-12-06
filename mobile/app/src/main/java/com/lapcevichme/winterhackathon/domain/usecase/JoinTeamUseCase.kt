package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.domain.model.team.Team
import com.lapcevichme.winterhackathon.domain.repository.TeamRepository
import javax.inject.Inject

class JoinTeamUseCase @Inject constructor(
    private val teamRepository: TeamRepository
) {
    suspend operator fun invoke(teamId: String): Result<Team> {
        return teamRepository.joinTeam(teamId)
    }
}
