package onlinedb.function

import com.google.gson.Gson
import com.openai.models.ChatModel
import dev.langchain4j.data.message.SystemMessage
import dev.langchain4j.data.message.UserMessage
import dev.langchain4j.model.chat.ChatLanguageModel
import dev.langchain4j.model.chat.request.ChatRequest
import dev.langchain4j.model.chat.request.ResponseFormat
import dev.langchain4j.model.openaiofficial.OpenAiOfficialChatModel
import onlinedb.scripts.Scene
import onlinedb.scripts.parseAliens1985


enum class SceneCategory {
    continuity,
    progression,
    premise,
    theme,
    forestalling,
    finger_posts,
    preparation,
    anticlimax,
    complication,
    catastrophe,
    resolution,
    representation,
    crisis,
    antagonist,
    impressionism,
    adjustment,
    peripety,
    irony,
    attack,
    focus,
    suspense,
    action_recognition,
    balance,
    movement,
    orchestration,
    unity_of_opposites,
    static,
    jumping,
    transition,
    incident
}


fun classifyScene(model: ChatLanguageModel, scene: Scene): SceneCategory {
    data class CategoryResponse(val category: SceneCategory)

    val response = model.chat(
        ChatRequest.builder()
            .messages(
                SystemMessage(
                    "You are assisting a professional screenwriter.\n" +
                            "You task is to classify the following script scene to one of the following categories:\n" +
                            SceneCategory.values().joinToString(
                                separator = ", "
                            ) + ".\n" +
                            "You must return JSON structure {\"category\": \"...value...\"}."
                ),
                UserMessage(scene.toText())
            ).responseFormat(ResponseFormat.JSON)
            .build()
    )

    val gson = Gson()
    val json = gson.fromJson<CategoryResponse>(response.aiMessage().text(), CategoryResponse::class.java)
    return json.category
}


fun main() {
    val model: ChatLanguageModel = OpenAiOfficialChatModel.builder()
        .apiKey(System.getenv("OPENAI_API_KEY"))
        .modelName(ChatModel.GPT_4O_MINI)
        .build()


    parseAliens1985().scenes.subList(0,10).forEach {scene ->
        val category = classifyScene(model, scene)
        println("${scene.caption} = $category")
    }
}

/*
        Run1:
        ----------------------------------------------------------------------------
        FADE IN - suspense
        INT. NARCISSUS                                            2 - incident
        INT. HOSPITAL ROOM - TIGHT ON RIPLEY - GATEWAY STATION    3 - crisis
        EXT. PARK                                                 4 - crisis
        INT. CORRIDOR - GATEWAY                                   5 - preparation
        INT. CONFERENCE ROOM - ON RIPLEY - GATEWAY                6 - crisis
        INT. CORRIDOR                                             7 - null
        INT. CONFERENCE ROOM - TIGHT ON RIPLEY - LATER            8 - crisis
        INT. CORRIDOR                                             9 - complication
        EXT. ALIEN LANDSCAPE - DAY                               10 - representation


        Run2:
        ----------------------------------------------------------------------------
        FADE IN = suspense
        INT. NARCISSUS                                            2 = suspense
        INT. HOSPITAL ROOM - TIGHT ON RIPLEY - GATEWAY STATION    3 = crisis
        EXT. PARK                                                 4 = crisis
        INT. CORRIDOR - GATEWAY                                   5 = progression
        INT. CONFERENCE ROOM - ON RIPLEY - GATEWAY                6 = crisis
        INT. CORRIDOR                                             7 = continuity
        INT. CONFERENCE ROOM - TIGHT ON RIPLEY - LATER            8 = crisis
        INT. CORRIDOR                                             9 = complication
        EXT. ALIEN LANDSCAPE - DAY                               10 = null

        Run3:
        ----------------------------------------------------------------------------
        FADE IN = suspense
        INT. NARCISSUS                                            2 = progression
        INT. HOSPITAL ROOM - TIGHT ON RIPLEY - GATEWAY STATION    3 = crisis
        EXT. PARK                                                 4 = crisis
        INT. CORRIDOR - GATEWAY                                   5 = progression
        INT. CONFERENCE ROOM - ON RIPLEY - GATEWAY                6 = crisis
        INT. CORRIDOR                                             7 = null
        INT. CONFERENCE ROOM - TIGHT ON RIPLEY - LATER            8 = crisis
        INT. CORRIDOR                                             9 = complication
        EXT. ALIEN LANDSCAPE - DAY                               10 = representation
 */