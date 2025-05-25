package uk.co.trumbo

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CutCornerShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.Button
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.material.Text
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
import com.mohamedrejeb.richeditor.model.rememberRichTextState
import org.jetbrains.compose.resources.painterResource
import org.jetbrains.compose.ui.tooling.preview.Preview

import trumbo.composeapp.generated.resources.Res
import trumbo.composeapp.generated.resources.compose_multiplatform

private val snippet = """

                            ZOOTOPIA




                           Written by

                    Jared Bush & Phil Johnston




                                                                     Story by
                                                     Byron Howard, Rich Moore,
                                      Jared Bush, Jim Reardon, Josie Trinidad,
                                                Phil Johnston and Jennifer Lee



   IN BLACK --

   We hear the feral, primeval sounds of a jungle at night. A
   timpani bangs an ominous beat.

   FADE IN ON:


   A JUNGLE - NIGHT

   A BUNNY nervously walks through the dark, foreboding forest,
   frightened by every shadow and moving leaf.

                    YOUNG JUDY (V.O.)
          Fear. Treachery. Bloodlust!
          Thousands of years ago, these were
          the forces that ruled our world. A
          world where prey were scared of
          predators. And predators had an
          uncontrollable biological urge to
          maim and maul and...

   The timpani crescendos. A JAGUAR leaps out of the shadows,
   attacks the bunny, who screams--

                                                  CUT TO:


   INSIDE A BARN - A JUNGLE (SET) - NIGHT

   The action continues-- as imagined by an amateur stage
   production.

                    YOUNG JUDY
          Blood, blood, blood!

   Reams of red papier m�ch� entrails ooze from the bunny. And
   when those run out-- projectile ketchup.

   Reveal: These are ANIMAL KID ACTORS. The bunny, JUDY HOPPS,
   10, is our hero. And this is her play being staged. A banner
   reads: CARROT DAYS TALENT SHOW!

                       YOUNG JUDY (CONT'D)
          And death.

   The CROWD looks on, confused. The music goes discordant as
   BOBBY CATMULL, a bobcat, bangs a drum.

                    YOUNG JUDY (CONT'D)
          Back then, the world was divided in
          two. Vicious predator or Meek prey.
                                                           2.


TWO BOXES drop down, labeled VICIOUS PREDATOR and MEEK PREY.
The PREDATOR box lands on the jaguar. The MEEK PREY box lands
on Judy. Her entrails get stuck outside the box. She drags
them underneath with her.

                    YOUNG JUDY (O.S.) (CONT'D)
          But over time, we evolved, and
          moved beyond our primitive savage
          ways.

A YOUNG SHEEP wearing a white muumuu and a cardboard rainbow            
        """.trimIndent()

@Composable
fun App1() {

    MaterialTheme {
//        val state = rememberRichTextState()
//        state.toggleSpanStyle(SpanStyle(fontWeight = FontWeight.Bold))

        Column(Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
            Surface(
                color = Color.LightGray,
                border = BorderStroke(2.dp, Color.White),
                shape = RoundedCornerShape(8.dp),
            ) {
                Column(
                    Modifier.fillMaxWidth()
                ) {
                    Text("Hello \uD83D\uDE80\uD83D\uDE80\uD83D\uDE80")
                }
            }
            LogPointerEvents()
            UppercaseTextField()
        }
    }
}

@Composable
fun LogPointerEvents(filter: PointerEventType? = null) {
    var log by remember { mutableStateOf("") }
    Column {
        Text(log)
        Box(
            Modifier
                .size(250.dp)
                .background(Color.Red)
                .pointerInput(filter) {
                    awaitPointerEventScope {
                        while (true) {
                            val event = awaitPointerEvent()
                            // handle pointer event
                            if (filter == null || event.type == filter) {
                                log = "${event.type}, ${event.changes.first().position}"
                            }
                        }
                    }
                }
        )
    }
}


class CapitalizeVisualTransformation : VisualTransformation {
    override fun filter(text: AnnotatedString): TransformedText {
        val transformed = buildAnnotatedString {
            text.forEach { char ->
                withStyle(
                    style = if (char.isUpperCase())
                        SpanStyle(fontWeight = FontWeight.Bold)
                    else
                        SpanStyle(fontWeight = FontWeight.Normal)
                ) {
                    append(char)
                }
            }
        }

        val offsetMap = object : OffsetMapping {
            override fun originalToTransformed(offset: Int) = offset
            override fun transformedToOriginal(offset: Int) = offset
        }

        return TransformedText(transformed, offsetMap)
    }
}


@Composable
fun UppercaseTextField() {
    var text by remember { mutableStateOf("Fade In:\nWritten by\nJared Bush & Phil Johnston") }

    BasicTextField(
        value = text,
        onValueChange = { text = it },
        visualTransformation = CapitalizeVisualTransformation(),
        textStyle = TextStyle(
            fontSize = 18.sp,
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.Bold, // Apply one bold style to all
            lineHeight = 22.sp
        ),
        modifier = Modifier
            .fillMaxWidth()
            .background(color = Color.White)
            .padding(16.dp)
    )
}