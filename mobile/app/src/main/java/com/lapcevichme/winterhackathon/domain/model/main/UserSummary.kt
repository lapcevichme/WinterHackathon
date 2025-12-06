package com.lapcevichme.winterhackathon.domain.model.main

import com.lapcevichme.winterhackathon.domain.model.casino.Balance

data class UserSummary(
    val id: String,
    val displayName: String?,
    val balance: Balance,
    val energy: EnergyState
)