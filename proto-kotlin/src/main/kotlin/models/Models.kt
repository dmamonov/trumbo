package onlinedb.models

import com.openai.models.ChatModel
import dev.langchain4j.model.chat.ChatLanguageModel
import dev.langchain4j.model.mistralai.MistralAiChatModel
import dev.langchain4j.model.mistralai.MistralAiChatModelName
import dev.langchain4j.model.openaiofficial.OpenAiOfficialChatModel

fun mistral() = MistralAiChatModel.builder()
    .apiKey(System.getenv("MISTRAL_AI_API_KEY"))
    .modelName(MistralAiChatModelName.MISTRAL_LARGE_LATEST)
    .build()


fun openai() = OpenAiOfficialChatModel.builder()
    .apiKey(System.getenv("OPENAI_API_KEY"))
    .modelName(ChatModel.GPT_4O_MINI)
    .build()