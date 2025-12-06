package com.lapcevichme.winterhackathon.ui.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.lapcevichme.winterhackathon.presentation.MainViewModel
import com.lapcevichme.winterhackathon.ui.theme.WinterHackathonTheme

@Composable
fun WinterHackathonApp(
    viewModel: MainViewModel = hiltViewModel()
) {
    WinterHackathonTheme {
        val navController = rememberNavController()

        val navBackStackEntry by navController.currentBackStackEntryAsState()
        val currentRoute = navBackStackEntry?.destination?.route

        val bottomBarHiddenRoutes = listOf(
            Screen.Onboarding.route,
            Screen.Login.route,
            Screen.Game.route
        )

        val showBottomBar = currentRoute !in bottomBarHiddenRoutes

        LaunchedEffect(viewModel.isUserLoggedIn) {
            if (!viewModel.isUserLoggedIn && currentRoute !in bottomBarHiddenRoutes) {
                navController.navigate(Screen.Login.route) {
                    popUpTo(0) { inclusive = true }
                }
            }
        }

        LaunchedEffect(currentRoute) {
            if (currentRoute == Screen.Home.route) {
                viewModel.updateAuthState()
            }
        }

        Scaffold(
            containerColor = MaterialTheme.colorScheme.background,
            bottomBar = {
                if (showBottomBar) {
                    AppBottomBar(
                        navController = navController,
                        isAdmin = viewModel.isAdmin
                    )
                }
            }
        ) { innerPadding ->
            AppNavGraph(
                navController = navController,
                modifier = Modifier.padding(innerPadding),
                isLoggedIn = viewModel.isUserLoggedIn
            )
        }
    }
}