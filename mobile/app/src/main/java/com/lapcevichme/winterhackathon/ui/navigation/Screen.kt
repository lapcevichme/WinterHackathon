package com.lapcevichme.winterhackathon.ui.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.Gamepad
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.QrCodeScanner
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.filled.Star
import androidx.compose.ui.graphics.vector.ImageVector

sealed class Screen(val route: String, val title: String, val icon: ImageVector) {
    object Onboarding : Screen("onboarding", "Intro", Icons.Default.Info)
    object Login : Screen("login", "Login", Icons.Default.AccountCircle)
    object Home : Screen("home", "Арена", Icons.Filled.Home)
    object Leaderboard : Screen("leaderboard", "Топ", Icons.Filled.Star)
    data object AdminScanner : Screen("admin_scanner", "Scan", Icons.Default.QrCodeScanner)
    object Casino : Screen("casino", "Казино", Icons.Filled.ShoppingCart)
    object Profile : Screen("profile", "Штаб", Icons.Filled.Person)
    object Game : Screen("game", "Игра", Icons.Filled.Gamepad)

}