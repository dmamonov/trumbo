package onlinedb.function

import dev.langchain4j.data.message.SystemMessage
import dev.langchain4j.data.message.UserMessage
import dev.langchain4j.model.chat.request.ChatRequest
import dev.langchain4j.model.chat.request.ResponseFormat
import onlinedb.models.mistral
import onlinedb.models.openai
import onlinedb.scripts.Scene
import onlinedb.scripts.parseAliens1985

fun main() {
    val model = openai()

    fun listCharacters(script: String): String {
        val response = model.chat(
            ChatRequest.builder()
                .messages(
                    SystemMessage(
                        """
You are assisting a professional screenwriter.
You will be given an entire movie script.
Your task is to analyze it for cinematic conflict (tensions).

You must reply in the following JSON format:
 
```json
{
    "scenes": [
        {
            "scene": "...scene name...",
            "tensions": [
                {
                    "status": "ARISE" | "RESOLVED"
                    "conflict": "...brief conflict description..."
                },
                ...
            }
        },
        ...
        ...
        ...
    ]
}
```

You must cover each scene in order.
"""
                    ),
                    UserMessage(script)
                ).responseFormat(ResponseFormat.JSON)
                .build()
        )
        return response.aiMessage().text()
    }


//

    val script = parseAliens1985()
    script.scenes.forEach{ println(it.caption) }
    val text = script.scenes.joinToString(separator = "\n") { it.toText() }
    println(listCharacters(text))
}