package com.lapcevichme.winterhackathon.domain.model

data class SpinResult(
    val itemsChain: List<Prize>, // Готовая лента из 50 элементов
    val winningIndex: Int, // Индекс победителя с бэка
    val winPrize: Prize,
    val newBalance: Int
)