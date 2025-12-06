package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.remote.MainApiService
import com.lapcevichme.winterhackathon.domain.model.casino.Balance
import com.lapcevichme.winterhackathon.domain.model.main.EnergyState
import com.lapcevichme.winterhackathon.domain.model.main.GameInfo
import com.lapcevichme.winterhackathon.domain.model.main.MainScreenData
import com.lapcevichme.winterhackathon.domain.model.main.UserSummary
import com.lapcevichme.winterhackathon.domain.repository.MainRepository
import javax.inject.Inject

class MainRepositoryImpl @Inject constructor(
    private val api: MainApiService
) : MainRepository {

    override suspend fun getMainScreenData(): MainScreenData {
        val response = api.getMainData()

        return MainScreenData(
            userSummary = UserSummary(
                id = response.userSummary.id,
                displayName = response.userSummary.displayName,
                balance = Balance(
                    amount = response.userSummary.balance.amount,
                    currencySymbol = response.userSummary.balance.currencySymbol
                ),
                energy = EnergyState(
                    current = response.userSummary.energy.current,
                    max = response.userSummary.energy.max,
                    nextRefillInSeconds = response.userSummary.energy.nextRefillInSeconds
                )
            ),
            games = response.games?.map { game ->
                GameInfo(
                    slug = game.slug,
                    name = game.name,
                    energyCost = game.energyCost
                )
            }
        )
    }
}