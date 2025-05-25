package uk.co.trumbo.data2

typealias Lines = Int
typealias Rows = Int

data class Size(val lines: Lines, val rows: Rows)

sealed interface NodeContent {
    val side: Size get() = Size(0, 0)
}

sealed interface RowContent : NodeContent
data class StructureContent(val value: Unit = Unit) : RowContent

sealed interface LineContent : NodeContent

data class StringContent(val value: String) : LineContent
data class LineBreakContent(val value: Unit = Unit) : LineContent
data class FieldContent(val key: String, val value: String) : LineContent

interface Document {
    val root: DocumentNode
}

sealed interface DocumentNode {

}

sealed interface StructureNode: DocumentNode {
    val before: DocumentNode?
    val after: DocumentNode?
}

sealed interface VerticalNode: StructureNode
sealed interface HorizontalNode: StructureNode

sealed interface SemanticNode: DocumentNode
sealed interface NestedNode: SemanticNode
sealed interface SectionNode: SemanticNode
sealed interface HeadingNode: SemanticNode
sealed interface ParagraphNode: SemanticNode
sealed interface LineNode: SemanticNode
sealed interface CoverNode: SemanticNode






interface ContentNode: DocumentNode {
    val content: NodeContent
}
