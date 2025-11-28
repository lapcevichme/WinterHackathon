package com.lapcevichme.winterhackathon.presentation.profile

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun ProfileScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(20.dp))
        Box(
            modifier = Modifier.size(100.dp).clip(CircleShape).background(Color.Gray),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Filled.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(50.dp))
        }
        Spacer(modifier = Modifier.height(16.dp))
        Text("Егор Винник", color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.headlineMedium)
        Text("IT Отдел", color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.titleMedium)

        Spacer(modifier = Modifier.height(32.dp))

        Text("МОЙ ЛУТ", color = Color.Gray, style = MaterialTheme.typography.labelSmall, modifier = Modifier.align(Alignment.Start))
        Spacer(modifier = Modifier.height(8.dp))

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            LootItem("🧤", MaterialTheme.colorScheme.error)
            LootItem("💩", Color.Gray)
            LootItem("🐉", MaterialTheme.colorScheme.primary)
        }
    }
}

@Composable
fun LootItem(emoji: String, color: Color) {
    Box(
        modifier = Modifier
            .size(80.dp)
            .background(color.copy(alpha = 0.2f), RoundedCornerShape(8.dp))
            .border(1.dp, color, RoundedCornerShape(8.dp)),
        contentAlignment = Alignment.Center
    ) {
        Text(emoji, fontSize = 32.sp)
    }
}