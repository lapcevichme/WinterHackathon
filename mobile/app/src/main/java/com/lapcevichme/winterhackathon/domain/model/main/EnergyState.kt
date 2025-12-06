package com.lapcevichme.winterhackathon.domain.model.main

data class EnergyState(
    val current: Int,
    val max: Int,
    val nextRefillInSeconds: Int
)
