package com.lapcevichme.winterhackathon

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.ui.graphics.toArgb
import com.lapcevichme.winterhackathon.ui.navigation.WinterHackathonApp
import com.lapcevichme.winterhackathon.ui.theme.CyberDark
import com.lapcevichme.winterhackathon.ui.theme.DeepNav

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(
                scrim = CyberDark.toArgb()
            ),
            navigationBarStyle = SystemBarStyle.dark(
                scrim = DeepNav.toArgb()
            )
        )
        setContent {
            WinterHackathonApp()
        }
    }
}
