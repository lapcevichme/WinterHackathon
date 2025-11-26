package com.lapcevichme.winterhackathon.ui.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.rememberNavController
import com.lapcevichme.winterhackathon.ui.theme.WinterHackathonTheme

@Composable
fun WinterHackathonApp() {
    WinterHackathonTheme {
        val navController = rememberNavController()

        Scaffold(
            containerColor = MaterialTheme.colorScheme.background,
            bottomBar = {
                AppBottomBar(navController = navController)
            }
        ) { innerPadding ->
            AppNavGraph(
                navController = navController,
                modifier = Modifier.padding(innerPadding)
            )
        }
    }
}