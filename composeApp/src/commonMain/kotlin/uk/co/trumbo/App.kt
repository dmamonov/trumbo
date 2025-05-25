package uk.co.trumbo

import androidx.compose.animation.core.Spring
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Phone
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.PointerEventType
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.*
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import org.jetbrains.compose.ui.tooling.preview.Preview
import uk.co.trumbo.ui.MinimalDropdownMenu

@Composable
@Preview
fun App() {
    var presses by remember { mutableIntStateOf(0) }
    MaterialTheme {
        Scaffold(
            topBar = {
                TopAppBar(
                ){
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(56.dp)
                    ) {
                        IconButton(
                            onClick = {  },
                            modifier = Modifier.align(Alignment.CenterStart)
                        ) {
                            Icon(Icons.Default.Menu, contentDescription = "Menu")
                        }

                        Text(
                            text = "Alien / 1976 / First Draft",
                            style = MaterialTheme.typography.h6,
                            modifier = Modifier.align(Alignment.Center)
                        )

                        IconButton(
                            onClick = {  },
                            modifier = Modifier.align(Alignment.CenterEnd)
                        ) {
                            Icon(Icons.Default.MoreVert, contentDescription = "More")
                        }
                    }
                }
            },
            bottomBar = { BottomAppBar { MinimalDropdownMenu() } },
            floatingActionButton = {
                FloatingActionButton(onClick = { presses++ }) {
                    Icon(Icons.Default.Add, contentDescription = "Add")
                }
            }
        ) { innerPadding ->
            Row(){
                TreeScreen()
                Column(
                    modifier = Modifier
                        .padding(innerPadding),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                ) {
                    Text(
                        modifier = Modifier.padding(8.dp),
                        text =
                            """
                    This is an example of a scaffold. It uses the Scaffold composable's parameters to create a screen with a simple top app bar, bottom app bar, and floating action button.

                    It also contains some basic inner content, such as this text.

                    You have pressed the floating action button $presses times.
                """.trimIndent(),
                    )
                }
            }

        }
    }
}


@Composable
fun ArtistCardColumn() {
    Column {
        Text("Alfred Sisley")
        Text("3 minutes ago")
    }
}

data class TreeNode(
    val name: String,
    val children: List<TreeNode> = emptyList()
)

@Composable
fun TreeNodeView(node: TreeNode, level: Int = 0) {
    var expanded by remember { mutableStateOf(false) }

    Column(modifier = Modifier.padding(start = (level * 16).dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            if (node.children.isNotEmpty()) {
                IconButton(onClick = { expanded = !expanded }) {
                    Icon(
                        imageVector = if (expanded) Icons.Default.Menu else Icons.Default.Add,
                        contentDescription = "Toggle"
                    )
                }
            } else {
                Spacer(modifier = Modifier.size(40.dp)) // aligns text
            }
            Text(node.name)
        }

        if (expanded) {
            node.children.forEach {
                TreeNodeView(it, level + 1)
            }
        }
    }
}


val sampleTree = TreeNode("Root", listOf(
    TreeNode("Folder A", listOf(TreeNode("File A1"), TreeNode("File A2"))),
    TreeNode("Folder B"),
    TreeNode("File C")
))

@Composable
fun TreeScreen() {
    TreeNodeView(sampleTree)
}
