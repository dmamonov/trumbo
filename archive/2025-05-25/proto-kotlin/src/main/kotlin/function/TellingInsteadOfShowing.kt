package onlinedb.function

import com.openai.models.ChatModel
import dev.langchain4j.data.message.SystemMessage
import dev.langchain4j.data.message.UserMessage
import dev.langchain4j.model.chat.ChatLanguageModel
import dev.langchain4j.model.chat.request.ChatRequest
import dev.langchain4j.model.openaiofficial.OpenAiOfficialChatModel
import onlinedb.scripts.Scene
import onlinedb.scripts.parseAlien1976EarlyDraft

fun inspectTelling(model: ChatLanguageModel, scene: Scene): String? {
    val response = model.chat(
        ChatRequest.builder()
            .messages(
                SystemMessage(
                    """
You are assisting a professional screenwriter.
Your task is to check if the following script scene for the typical design mistakes:

1. On-the-Nose Dialogue
Mistake: Characters say exactly what they’re feeling or thinking.

Example:

SARAH: I’m sad because you broke my heart and now I don’t trust anyone.

(Too obvious and unnatural.)

Fix: Show emotion through subtext, action, or metaphor.

SARAH: You know, I used to think people meant what they said. Silly me.

2. Too Much Exposition (a.k.a. "Info Dumping")
Mistake: Unnatural dialogue or narration that explains everything.

Example:

JOHN: As you know, Mom, I’m 25 years old, and I’ve been living in New York ever since Dad died in that car accident five years ago.

Fix: Reveal info organically, through conflict or context.

JOHN: I can't believe it's been five years... I still hear his voice every time I get behind the wheel.

3. Telling, Not Showing
Mistake: Describing emotions instead of letting the audience feel them.

Example (in action lines):

She is heartbroken and sad.

Fix:

She stares at the untouched coffee. Her hands tremble as she deletes his contact.

4. Flat Characters / No Arc
Mistake: Characters don’t grow or change throughout the story.

Example:
A hero who is fearless and good at everything from the start — and stays that way until the end.

Fix: Give them flaws, dilemmas, and emotional journeys.

5. Unclear or Weak Stakes
Mistake: The audience doesn’t know why the story matters.

Example:

"I have to win this race... just because."

Fix:

"If I lose this race, they shut down the track — and with it, Dad’s legacy dies."

6. Overwriting Action Lines
Mistake: Novels disguised as screenplays.

Example:

The golden sun dips below the horizon, casting long melancholic shadows as birds chirp wistfully in the distance, their wings cutting through the thick summer air like forgotten dreams.

Fix: Keep it visual and efficient.

The sun sets. A bird glides past. Stillness.

-----------------------------------------------
REPLY FORMAT IF THERE IS A PROBLEM:

**{scene name}***

Problem: {problem name}

Reference:
```
    {quote piece of the script depicting the problem}            
```

-----------------------------------------------
REPLY FORMAT IF THERE ARE NOT PROBLEMS:

OK

-----------------------------------------------

Please check this scene:
""".trim()
                ),
                UserMessage(scene.toText())
            )//.responseFormat(ResponseFormat.JSON)
            .build()
    )


    val result = response.aiMessage().text()
    return if (result.startsWith("OK")) {
        null
    } else {
        result
    }
}


fun main() {
    runWithOpenAi()
}

private fun runWithOpenAi() {
    val model: ChatLanguageModel = OpenAiOfficialChatModel.builder()
        .apiKey(System.getenv("OPENAI_API_KEY"))
        .modelName(ChatModel.GPT_4O_MINI)
        .build()

    parseAlien1976EarlyDraft().scenes.forEach {s ->
        println(s.caption)
    }
    parseAlien1976EarlyDraft().scenes.forEach { scene ->
        val inspection = inspectTelling(model, scene)
        if (inspection!=null) {
            println("-------------------------------------------------------")
            println("**${scene.caption}**\n$inspection")
        }

    }
}
