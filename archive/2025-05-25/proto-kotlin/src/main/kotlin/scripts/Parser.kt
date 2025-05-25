package onlinedb.scripts

import java.io.File
import kotlin.io.path.readLines


sealed class Block(private val prefix: String) {
    abstract val lines: List<String>

    fun toText(): String = lines.joinToString(separator = "\n")

    override fun toString(): String {
        return "-".repeat(80) + "\n" + lines.joinToString(separator = "\n") { "$prefix$it" }
    }
}

class CoverPage(override val lines: List<String>) : Block("COVER: ")
class Title(override val lines: List<String>) : Block("TITLE: ")
class Scene(override val lines: List<String>) : Block("") {
    val caption: String = lines[0]
}

class TheEnd(override val lines: List<String>) : Block("END: ")

class Script(
    val cover: CoverPage,
    val title: Title,
    val scenes: List<Scene>,
    val theEnd: TheEnd
)


fun parseScript(scriptFile: File): Script {
    val lines = scriptFile.toPath().readLines(Charsets.UTF_8)

    val coverLines = mutableListOf<String>()
    val titleLines = mutableListOf<String>()
    val sceneList = mutableListOf<Scene>()
    var sceneLines = mutableListOf<String>()
    val theEndLines = mutableListOf<String>()

    var inScript = false
    var inScene = false
    var offScript = false

    fun appendSceneIfPresent() {
        if (sceneLines.size > 0) {
            sceneList.add(Scene(listOf(*sceneLines.toTypedArray())))
            sceneLines = mutableListOf()
        }

    }

    lines.forEach { line ->
        if (false) {
            println("$inScript/$inScene/$offScript = ${line.trim()}")
        }
        if (!inScript) {
            if (line.startsWith("----")) inScript = true
            coverLines.add(line)
        } else {
            if (line.trim() == "THE END") offScript = true
            if (!offScript) {
                if (line.trim().startsWith("FADE IN")) inScene = true
                if (!inScene) {
                    titleLines.add(line)
                } else {
                    if (line.trim().startsWith("INT") || line.trim().startsWith("EXT")) {
                        appendSceneIfPresent()
                    }
                    sceneLines.add(line)
                }
            } else {
                theEndLines.add(line)
            }

        }
    }
    appendSceneIfPresent()

    return Script(
        CoverPage(coverLines),
        Title(titleLines),
        sceneList,
        TheEnd(theEndLines)
    )
}

fun parseAliens1985() = parseScript(File("scripts/aliens1985.txt"))

fun parseAlien1976EarlyDraft() = parseScript(File("scripts/alien1976_early_draft.txt"))


fun main() {
    val script = parseAliens1985()

    println(script.cover)
    println(script.title)
    println("Scenes: ${script.scenes.size}")
    script.scenes.subList(0, minOf(10, script.scenes.size)).forEach { println(it) }
    println(script.theEnd)
}



