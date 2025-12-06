package com.lapcevichme.winterhackathon.presentation.game

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.view.ViewGroup
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.viewinterop.AndroidView
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import kotlinx.coroutines.flow.collectLatest

@SuppressLint("SetJavaScriptEnabled", "JavascriptInterface")
@Composable
fun GameScreen(
    navController: NavController,
    viewModel: GameViewModel = hiltViewModel()
) {
    val context = LocalContext.current
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        viewModel.events.collectLatest { event ->
            when (event) {
                is GameEvent.ShowScoreToast -> {
                    Toast.makeText(context, event.message, Toast.LENGTH_SHORT).show()
                }
                is GameEvent.CloseGame -> {
                    navController.popBackStack()
                }
            }
        }
    }

    val webInterface = remember {
        object {
            @JavascriptInterface
            fun sendScore(score: Int) {
                viewModel.onScoreReceived(score)
            }

            @JavascriptInterface
            fun closeGame() {
                viewModel.onCloseRequested()
            }
        }
    }

    AndroidView(
        factory = { ctx ->
            WebView(ctx).apply {
                layoutParams = ViewGroup.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.MATCH_PARENT
                )

                settings.apply {
                    javaScriptEnabled = true
                    domStorageEnabled = true
                    allowFileAccess = true
                    // For local development
                    WebView.setWebContentsDebuggingEnabled(true)
                }

                webViewClient = WebViewClient()

                addJavascriptInterface(webInterface, "AndroidGame")
            }
        },
        update = { webView ->
            uiState.url?.let { url ->
                webView.loadUrl(url)
            }
        }
    )
}
