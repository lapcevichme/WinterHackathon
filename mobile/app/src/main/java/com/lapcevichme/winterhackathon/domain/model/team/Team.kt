package com.lapcevichme.winterhackathon.domain.model.team

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class Team(
    val id: String,
    val name: String,
    val score: Long,
    @SerialName("max_score")
    val maxScore: Long
)
