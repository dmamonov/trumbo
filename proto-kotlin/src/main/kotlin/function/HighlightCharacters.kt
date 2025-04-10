package onlinedb.function

import com.apple.laf.ScreenMenuBar
import com.google.gson.Gson
import dev.langchain4j.data.message.SystemMessage
import dev.langchain4j.data.message.UserMessage
import dev.langchain4j.model.chat.request.ChatRequest
import onlinedb.models.mistral
import onlinedb.models.openai
import onlinedb.scripts.Scene
import onlinedb.scripts.parseAliens1985

fun main() {
    val model = openai()

    fun highlightCharacters(scene: Scene): String {
        val response = model.chat(
            ChatRequest.builder()
                .messages(
                    SystemMessage(
                        """
You are assisting a professional screenwriter.
You task is to highlight all mentions of character in a stage using markdown formatting: **character**.
Please ignore other named objets (e.g. model, street or ship names).
"""
                    ),
                    UserMessage(scene.toText())
                )
                .build()
        )
        return response.aiMessage().text()
    }


    parseAliens1985().scenes.subList(0, 10).forEach { scene ->
        println("-".repeat(80))
        println(highlightCharacters(scene))
    }
}