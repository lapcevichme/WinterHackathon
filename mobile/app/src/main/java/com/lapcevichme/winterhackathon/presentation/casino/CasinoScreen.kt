package com.lapcevichme.winterhackathon.presentation.casino

import android.view.SoundEffectConstants
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.platform.LocalView
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
import com.lapcevichme.winterhackathon.domain.model.casino.Prize
import kotlin.math.PI
import kotlin.math.sin
import kotlin.random.Random

@Composable
fun CasinoScreenRoot(
    viewModel: CasinoViewModel = hiltViewModel()
) {
    CasinoScreen(
        state = viewModel.uiState,
        onSpinClick = {
            viewModel.onSpinClicked()
        },
        onAnimationEnd = { viewModel.onAnimationFinished() }
    )
}

@Composable
fun CasinoScreen(
    state: CasinoUiState,
    onSpinClick: () -> Unit,
    onAnimationEnd: () -> Unit
) {
    val scope = rememberCoroutineScope()
    val listState = rememberLazyListState()

    // Звуки
    val haptic = LocalHapticFeedback.current
    val view = LocalView.current

    // Константы для анимации
    val configuration = LocalConfiguration.current
    val density = LocalDensity.current
    val screenWidthPx = with(density) { configuration.screenWidthDp.dp.toPx() }
    val itemWidthPx = with(density) { 100.dp.toPx() }

    // Анимация пульсации курсора
    val infiniteTransition = rememberInfiniteTransition(label = "cursor")
    val cursorAlpha by infiniteTransition.animateFloat(
        initialValue = 0.4f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(500),
            repeatMode = RepeatMode.Reverse
        ),
        label = "alpha"
    )

    LaunchedEffect(state.isSpinning) {
        if (state.isSpinning) {
            listState.scrollToItem(0)
            val winningItemCenter = (state.winningIndex * itemWidthPx) + (itemWidthPx / 2)
            val randomOffset = (itemWidthPx * 0.8f) * ((0..100).random() / 100f - 0.5f)
            val targetScrollPixels = winningItemCenter - (screenWidthPx / 2) - randomOffset

            val anim = Animatable(0f)
            var previousValue = 0f

            anim.animateTo(
                targetValue = targetScrollPixels,
                animationSpec = tween(
                    durationMillis = 5000,
                    easing = CubicBezierEasing(0.1f, 0.9f, 0.15f, 1f)
                )
            ) {
                val delta = value - previousValue
                listState.dispatchRawDelta(delta)

                // Звуки
                val currentItemCount = (value / itemWidthPx).toInt()
                val previousItemCount = (previousValue / itemWidthPx).toInt()

                if (currentItemCount != previousItemCount) {
                    // Щелчок!
                    haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                    view.playSoundEffect(SoundEffectConstants.CLICK)
                }
                previousValue = value
            }

            // Вибрация в конце
            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
            onAnimationEnd()
        }
    }

    Box(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.verticalGradient(
                        colors = listOf(
                            MaterialTheme.colorScheme.background,
                            MaterialTheme.colorScheme.secondaryContainer
                        )
                    )
                )
                .padding(vertical = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Header
            Card(
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                elevation = CardDefaults.cardElevation(8.dp)
            ) {
                Box(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "Баланс: ${state.balance} 🪙",
                        style = MaterialTheme.typography.headlineMedium,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
            }

            // Roulette
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(150.dp)
                        .background(MaterialTheme.colorScheme.tertiaryContainer)
                ) {
                    LazyRow(
                        state = listState,
                        userScrollEnabled = false,
                        modifier = Modifier.fillMaxSize(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        items(state.items) { item ->
                            RouletteItemCard(item)
                        }
                    }

                    // Cursor
                    Box(
                        modifier = Modifier
                            .width(4.dp)
                            .fillMaxHeight()
                            .background(MaterialTheme.colorScheme.primary.copy(alpha = if (state.isSpinning) cursorAlpha else 1f))
                            .align(Alignment.Center)
                    )

                    // Shadows
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(
                                Brush.horizontalGradient(
                                    0.0f to Color.Black.copy(alpha = 0.9f),
                                    0.15f to Color.Transparent,
                                    0.85f to Color.Transparent,
                                    1.0f to Color.Black.copy(alpha = 0.9f)
                                )
                            )
                    )
                }

                Spacer(modifier = Modifier.height(32.dp))

                // Result reveal
                AnimatedVisibility(
                    visible = state.lastWin != null,
                    enter = fadeIn() + scaleIn(initialScale = 0.5f) + expandVertically(),
                    exit = fadeOut() + shrinkVertically()
                ) {
                    state.lastWin?.let { win ->
                        Box(contentAlignment = Alignment.Center) {
                            // God Rays
                            Box(
                                modifier = Modifier
                                    .size(200.dp)
                                    .background(
                                        Brush.radialGradient(
                                            colors = listOf(
                                                win.color.copy(alpha = 0.5f),
                                                Color.Transparent
                                            )
                                        )
                                    )
                            )

                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text(
                                    text = "ВЫПАЛО:",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = Color.Gray,
                                    letterSpacing = 2.sp
                                )
                                Spacer(modifier = Modifier.height(8.dp))
                                Text(win.emoji, fontSize = 60.sp)
                                Text(
                                    text = win.name,
                                    style = MaterialTheme.typography.headlineMedium,
                                    color = win.color,
                                    modifier = Modifier.padding(top = 8.dp)
                                )
                            }
                        }
                    }
                }

                when {
                    state.isLoading -> {
                        Text(
                            "Заряжаем рулетку...",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f)
                        )
                    }

                    state.isSpinning -> {
                        Text(
                            "Удачи...",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.5f),
                            fontStyle = FontStyle.Italic
                        )
                    }

                    state.error != null -> {
                        Text(
                            "Ошибка: ${state.error}",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.error
                        )
                    }
                }
            }

            // Control button
            Button(
                onClick = onSpinClick,
                enabled = !state.isSpinning,
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.error,
                    disabledContainerColor = Color.Gray
                ),
                elevation = ButtonDefaults.buttonElevation(
                    defaultElevation = 8.dp,
                    pressedElevation = 2.dp
                ),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .height(60.dp)
            ) {
                Text(
                    text = if (state.isSpinning) "Крутим..." else "Крутить (10 🪙)",
                    style = MaterialTheme.typography.titleMedium
                )
            }
        }

        // Confetti
        if (state.lastWin != null) {
            ConfettiEffect()
        }
    }
}

@Composable
fun ConfettiEffect() {
    val particles = remember {
        List(50) {
            ConfettiParticle(
                x = Random.nextFloat(),
                y = Random.nextFloat() * 0.5f,
                color = Color(Random.nextLong(0xFF000000, 0xFFFFFFFF)),
                speed = Random.nextFloat() * 10f + 5f,
                angle = Random.nextFloat() * 2 * PI.toFloat()
            )
        }
    }

    // Анимация времени
    val infiniteTransition = rememberInfiniteTransition(label = "confetti")
    val time by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "time"
    )

    Canvas(modifier = Modifier.fillMaxSize()) {
        val width = size.width
        val height = size.height

        particles.forEachIndexed { index, particle ->
            val animatedProgress = (time + index * 0.1f) % 1f

            val currentY = -100f + (height + 200f) * animatedProgress // Падают сверху вниз
            val currentX =
                (particle.x * width) + (sin(animatedProgress * 10f + index) * 50f) // Качаются

            drawCircle(
                color = particle.color,
                radius = 10f,
                center = Offset(currentX, currentY)
            )
        }
    }
}

data class ConfettiParticle(
    val x: Float,
    val y: Float,
    val color: Color,
    val speed: Float,
    val angle: Float
)

@Composable
fun RouletteItemCard(prize: Prize) {
    Card(
        modifier = Modifier
            .width(100.dp)
            .height(130.dp)
            .padding(4.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        border = BorderStroke(2.dp, prize.color.copy(alpha = 0.6f))
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.verticalGradient(
                        colors = listOf(Color.Transparent, prize.color.copy(alpha = 0.1f))
                    )
                )
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(4.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text(text = prize.emoji, fontSize = 32.sp)
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = prize.name,
                    style = MaterialTheme.typography.labelSmall,
                    color = Color.White,
                    textAlign = TextAlign.Center,
                    lineHeight = 12.sp,
                    maxLines = 2
                )
            }
        }
    }
}