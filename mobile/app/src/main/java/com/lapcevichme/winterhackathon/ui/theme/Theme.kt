package com.lapcevichme.winterhackathon.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = AccentYellow,
    onPrimary = Color.Black,
    background = CyberDark,
    onBackground = Color.White,
    surface = SurfaceDark,
    onSurface = Color.White,
    surfaceVariant = ItemCardBg,
    onSurfaceVariant = Color.White,
    error = ActionRed,
    onError = Color.White,
    secondaryContainer = DeepNav,
    onSecondaryContainer = Color.White,
    tertiaryContainer = CyberBlack
)

@Composable
fun WinterHackathonTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = DarkColorScheme,
        typography = AppTypography,
        content = content
    )
}