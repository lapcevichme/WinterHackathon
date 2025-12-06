package com.lapcevichme.winterhackathon.presentation.team

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel

@Composable
fun JoinTeamScreen(
    teamId: String,
    onJoinSuccess: () -> Unit,
    onDismiss: () -> Unit,
    viewModel: JoinTeamViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current

    LaunchedEffect(teamId) {
        viewModel.loadTeam(teamId)
    }

    LaunchedEffect(uiState.joinSuccess) {
        if (uiState.joinSuccess) {
            Toast.makeText(context, "Вы успешно присоединились к команде!", Toast.LENGTH_SHORT).show()
            onJoinSuccess()
        }
    }

    LaunchedEffect(uiState.error) {
        uiState.error?.let {
            Toast.makeText(context, it, Toast.LENGTH_LONG).show()
            viewModel.errorShown()
            onDismiss()
        }
    }

    if (uiState.isLoading && uiState.team == null) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally
        ) {
            CircularProgressIndicator()
            Spacer(modifier = Modifier.height(8.dp))
            Text("Загружаем информацию о команде...")
        }
    } else if (uiState.team != null) {
        AlertDialog(
            onDismissRequest = onDismiss,
            title = { Text("Вступить в команду?") },
            text = { Text("Вы действительно хотите вступить в команду '${uiState.team!!.name}'?") },
            confirmButton = {
                Button(
                    onClick = { viewModel.joinTeam(teamId) },
                    enabled = !uiState.isLoading
                ) {
                    if (uiState.isLoading) {
                        CircularProgressIndicator(modifier = Modifier.width(24.dp))
                    } else {
                        Text("Вступить")
                    }
                }
            },
            dismissButton = {
                TextButton(onClick = onDismiss) {
                    Text("Отмена")
                }
            },
            modifier = Modifier
                .padding(16.dp)
                .background(
                    color = MaterialTheme.colorScheme.surface,
                    shape = RoundedCornerShape(16.dp)
                )
        )
    }
}
