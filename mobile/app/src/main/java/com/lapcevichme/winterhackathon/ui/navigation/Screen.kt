package com.lapcevichme.winterhackathon.ui.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.filled.Star
import androidx.compose.ui.graphics.vector.ImageVector

sealed class Screen(val route: String, val title: String, val icon: ImageVector) {
    object Home : Screen("home", "Арена", Icons.Filled.Home)
    object Leaderboard : Screen("leaderboard", "Топ", Icons.Filled.Star)
    object Casino : Screen("casino", "Казино", Icons.Filled.ShoppingCart)
    object Profile : Screen("profile", "Штаб", Icons.Filled.Person)
}