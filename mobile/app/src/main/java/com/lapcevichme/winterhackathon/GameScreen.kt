package com.lapcevichme.winterhackathon

import android.annotation.SuppressLint
import android.view.ViewGroup
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.viewinterop.AndroidView

@SuppressLint("SetJavaScriptEnabled", "JavascriptInterface")
@Composable
fun GameScreen(
    onCloseGame: () -> Unit
) {
    val context = LocalContext.current

    val webInterface = remember {
        object {
            @JavascriptInterface
            fun sendScore(score: Int) {
                android.os.Handler(android.os.Looper.getMainLooper()).post {
                    Toast.makeText(context, "Очки получены: $score", Toast.LENGTH_SHORT).show()
                }
            }

            @JavascriptInterface
            fun closeGame() {
                android.os.Handler(android.os.Looper.getMainLooper()).post {
                    onCloseGame()
                }
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
                }

                webViewClient = WebViewClient()

                addJavascriptInterface(webInterface, "AndroidGame")

                loadUrl("https://lapcevichme.github.io/WinterHackathon/")
            }
        },
        update = { webView ->
        }
    )
}
