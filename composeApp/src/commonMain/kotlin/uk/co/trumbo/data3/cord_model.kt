package uk.co.trumbo.data3

sealed interface Content {
    val content: String
}

data class Text(override val content: String) : Content
data class Field(val key: String, val value: String) : Content {
    override val content: String = "$key: $value"
}

sealed class Node {
    abstract val size: Int
    val range: IntRange get() = 0..size
    abstract fun insert(index: Int, insertion: LeafNode): Node
    abstract fun delete(index: Int, length: Int): Node
}

class MetaNode(val semantic: String, val node: Node) : Node() {
    override val size: Int
        get() = node.size

    override fun insert(index: Int, insertion: LeafNode): Node {
        return MetaNode(semantic, node.insert(index, insertion))
    }

    override fun delete(index: Int, length: Int): Node {
        TODO("Not yet implemented")
    }
}

data object EmptyNode : Node() {
    override val size: Int
        get() = 0

    override fun insert(index: Int, insertion: LeafNode): Node {
        check(index == 0)
        return insertion
    }

    override fun delete(index: Int, length: Int): Node {
        check(index == 0)
        check(length == 0)
        return this
    }
}

class BranchNode(val left: Node, val right: Node) : Node() {
    override val size: Int
        get() = left.size + right.size

    override fun insert(index: Int, insertion: LeafNode): Node {
        return if (index in left.range) {
            BranchNode(left.insert(index, insertion), right)
        } else {
            BranchNode(left, right.insert(index - left.size, insertion))
        }
    }

    override fun delete(index: Int, length: Int): Node {
        return if (index in left.range) {
            BranchNode(left.delete(index, length), right)
        } else {
            BranchNode(left, right.delete(index - left.size, length))
        }
    }
}

sealed class LeafNode : Node() {
    abstract val content: String

    override val size: Int
        get() = content.length
}

data class TextNode(override val content: String) : LeafNode() {
    override fun insert(index: Int, insertion: LeafNode): Node {
        check(index in range)
        val left = TextNode(content.substring(0, index))
        val right = TextNode(content.substring(index))

        return if (left.size < right.size) {
            BranchNode(BranchNode(left, insertion), right)
        } else {
            BranchNode(left, BranchNode(insertion, right))
        }
    }

    override fun delete(index: Int, length: Int): Node {
        return TextNode(content.substring(0, index) + content.substring(index + length))
    }
}

data class FieldNode(val key: String, val value: String) : LeafNode() {
    override val content = "$key: $value"

    override fun insert(index: Int, insertion: LeafNode): Node {
        TODO("Not yet implemented")
    }

    override fun delete(index: Int, length: Int): Node {
        TODO("Not yet implemented")
    }
}


fun main() {

}