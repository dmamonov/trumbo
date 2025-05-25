package uk.co.trumbo.ui

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun Hierarchy() {
    Text("ALIENS")
    Text("Script")
    Text("Roles")
    Text("  > Ripley")
    Text("  > Jones")
    Text("  > ...")
}

@Composable
fun DoucumentTab() {

}



@Composable
fun Header() {

}

@Composable
fun MinimalDropdownMenu() {
    var expanded by remember { mutableStateOf(false) }
    Box(
        modifier = Modifier
            .padding(16.dp)
    ) {
        IconButton(onClick = { expanded = !expanded }) {
            Icon(Icons.Default.MoreVert, contentDescription = "More options")
        }
        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            DropdownMenuItem(
                content = { Text("Option 1") },
                onClick = { /* Do something... */ }
            )
            DropdownMenuItem(
                content = { Text("Option 2") },
                onClick = { /* Do something... */ }
            )
        }
    }
}

@Composable
fun Footer() {

}