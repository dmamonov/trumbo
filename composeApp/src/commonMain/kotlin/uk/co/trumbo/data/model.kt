package uk.co.trumbo.data

import androidx.compose.ui.text.LinkAnnotation


//everything is a document,
//everything is an object,
//everything has a type,
//types are collections,
//documents are sequences.

//Q: What is the underlying data model? Document+Storage?
//Q: Should we use relational model somewhere?
//Q: Is there root object? - Project.
//Q: Should projects be connected?
//Q: How to access other objects otherwise?

//Q: User profile page
//Q: Project profile page
//Q: Stream/chat pages?

//Q: Document is also a sequence.

//Q: How to display document properties that are not visual?

//Q: What about incorporating views into docs?


interface Field {

}

interface Document {
    val first: StartBlock
}


interface Block {
    val next: Block?
}

interface StartBlock : Block

interface CollectionBlock {
    val first: StartBlock
}

interface ContentBlock {

}

sealed interface Value {
    val length: Int
}

interface StringValue : Value {}
interface LineBreakValue : Value {}
interface FieldValue : Value {}

interface TextBlock : ContentBlock {
    val sequence: List<Value>
}

data class URL(val ref: String)

interface MediaBlock : ContentBlock {
    val contentUrl: LinkAnnotation.Url
}

interface ImageBlock : MediaBlock {

}

interface VideoBlock : MediaBlock {

}

interface AudioBlock : MediaBlock {

}


fun main() {
    println("Hello")
}
