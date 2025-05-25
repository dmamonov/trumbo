package onlinedb.function

import dev.langchain4j.data.message.SystemMessage
import dev.langchain4j.data.message.UserMessage
import dev.langchain4j.model.chat.request.ChatRequest
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
Your task is to extract all character names from the script. 
You should reply with complete list of characters in the markdown format. 
For each character you should specify all ways it has been references in the script. 

Example output:

```markdown
 - Bob, Bob Marney, Bob (Banana) Marney, Captain 
 - Alice, the gardener
 - Pinky (pig)
```
"""
                    ),
                    UserMessage(script)
                )
                .build()
        )
        return response.aiMessage().text()
    }


//
    val text = parseAliens1985().scenes.joinToString(separator = "\n") { it.toText() }
    println(listCharacters(text))
}