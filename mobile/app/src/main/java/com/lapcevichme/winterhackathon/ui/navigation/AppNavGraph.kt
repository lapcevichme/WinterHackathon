package com.lapcevichme.winterhackathon.ui.navigation

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable

@Composable
fun AppNavGraph(
    navController: NavHostController,
    modifier: Modifier = Modifier
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Home.route,
        modifier = modifier
    ) {
        composable(Screen.Home.route) { MainScreen() }
        composable(Screen.Leaderboard.route) { LeaderboardScreen() }
        composable(Screen.Casino.route) { CasinoScreen() }
        composable(Screen.Profile.route) { ProfileScreen() }
    }
}

@Composable
fun MainScreen() {
    Text("Main Screen")
}

@Composable
fun LeaderboardScreen() {
    Text("Leaderboard Screen")
}

@Composable
fun CasinoScreen() {
    Text("Casino Screen")
}

@Composable
fun ProfileScreen() {
    Text("Profile Screen")
}