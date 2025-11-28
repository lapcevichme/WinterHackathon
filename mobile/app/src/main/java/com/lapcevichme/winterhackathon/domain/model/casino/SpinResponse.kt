package com.lapcevichme.winterhackathon.domain.model.casino

data class SpinResponse(
    val winner: Prize,
    val newBalance: Int
)