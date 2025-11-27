package com.lapcevichme.winterhackathon.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navDeepLink
import com.lapcevichme.winterhackathon.presentation.auth.LoginScreen
import com.lapcevichme.winterhackathon.presentation.casino.CasinoScreenRoot
import com.lapcevichme.winterhackathon.presentation.onboarding.OnboardingScreen

@Composable
fun AppNavGraph(
    navController: NavHostController,
    modifier: Modifier = Modifier,
    isLoggedIn: Boolean = false
) {
    val startDest = if (isLoggedIn) Screen.Home.route else Screen.Onboarding.route

    NavHost(
        navController = navController,
        startDestination = startDest,
        modifier = modifier
    ) {
        composable(Screen.Onboarding.route) { OnboardingScreen(navController) }

        composable(
            route = Screen.Login.route,
            deepLinks = listOf(
                navDeepLink {
                    uriPattern = "winterhack://join?team={teamId}"
                },
                navDeepLink {
                    // TODO: норм паттерн
                    uriPattern = "https://winterhack.com/join?team={teamId}"
                }
            )
        ) { backStackEntry ->
            val teamId = backStackEntry.arguments?.getString("teamId")

            LoginScreen(navController, preselectedTeamId = teamId)
        }

        composable(Screen.Home.route) { MainScreen(navController) }
        composable(Screen.Leaderboard.route) { LeaderboardScreen() }
        composable(Screen.Casino.route) { CasinoScreenRoot() }
        composable(Screen.Profile.route) { ProfileScreen() }
    }
}