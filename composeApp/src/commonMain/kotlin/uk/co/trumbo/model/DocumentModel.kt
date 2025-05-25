package uk.co.trumbo.model


//Hierarchy Model


//Document Model

interface Document {
    val blocks: List<Block>
}


data class Location(val offset: Int) {
    init {
        check(offset >= 0)
    }
}

data class Steps(val count: Int) {
    init {
        check(count >= 0)
    }
}

interface Block {
    val contentSteps: Int
    val contentWidth: Int

    fun delete(location: Location, steps: Steps): Block

    fun insert(location: Location, block: Block): Block
}

object Empty : Block {
    override val contentSteps: Int = 0
    override val contentWidth: Int = 0

    override fun delete(location: Location, steps: Steps): Block {
        check(location.offset == 0)
        check(steps.count == 0)
        return this
    }

    override fun insert(location: Location, block: Block): Block {
        check(location.offset == 0)
        return block
    }
}

interface Content : Block {
    val content: String
}

data class Branch(
    val left: Block,
    val right: Block,
) : Block {
    override val contentSteps: Int
        get() = left.contentSteps + right.contentSteps
    override val contentWidth: Int
        get() = left.contentWidth + right.contentWidth

    override fun delete(location: Location, steps: Steps): Block {
        check(location.offset == 0)
        check(steps.count == 0)
        return this
    }

    override fun insert(location: Location, block: Block): Block {
        check(location.offset == 0)
        return block
    }
}


private fun isAllSingleWidth(text: String): Boolean {
    //return text.codePoints().allMatch { codePoint ->
    //    val width = UCharacter.getIntPropertyValue(codePoint, UProperty.EAST_ASIAN_WIDTH)
    //    width == UCharacter.EastAsianWidth.NEUTRAL || width == UCharacter.EastAsianWidth.NARROW
    //}
    return true
}

private fun textToBlock(text: String): Block {
    if (text.length == 0) {
        return Empty
    } else {
        return Text(text)
    }
}

data class Text(
    override val content: String,
) : Content {
    init {
        require(isAllSingleWidth(content)) { "Content must not contain emoji symbols" }
    }

    override val contentSteps: Int
        get() = content.length
    override val contentWidth: Int
        get() = content.length

    override fun delete(location: Location, steps: Steps): Block {
        check(location.offset + steps.count < content.length)
        TODO()
    }

    override fun insert(location: Location, block: Block): Block {
        TODO()
    }
}

data class Emoji(
    val codePoint: Int
) : Content {
    override val contentSteps: Int
        get() = 1
    override val contentWidth: Int
        get() = 2

    override val content: String
        get() = ""

    override fun delete(location: Location, steps: Steps): Block {
        check(location.offset == 0)
        if (steps.count == 0) {
            return this
        }
        check(steps.count == 1)
        return Empty
    }

    override fun insert(location: Location, block: Block): Block {
        TODO()
    }
}

interface Line : Content {

}

interface Variable : Content {
    val property: String
    val value: String
}

interface Meta : Block {
    val content: Content
}


fun main() {
    println("Hello")
}


//Object Model






