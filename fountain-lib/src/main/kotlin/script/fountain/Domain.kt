package script.fountain

// see: https://fountain.io/syntax/

data class CoverPage(val title: String)

data class Scene(val heading: SceneHeading, val element: List<SceneElement>)


enum class SceneHeadingType {
    INT, EXT, INT_EXT, EST, CUSTOM
}

//can be escaped by "."
data class SceneHeading(val heading: String) {
    val type: SceneHeadingType = when {
        heading.startsWith("INT.") -> SceneHeadingType.INT
        heading.startsWith("EXT.") -> SceneHeadingType.EXT
        heading.startsWith("I/E.") -> SceneHeadingType.INT_EXT
        else -> SceneHeadingType.CUSTOM
    }

    override fun toString(): String = "\n$heading\n\n"
}

interface SceneElement

/**
 * Action, or scene description, is any paragraph that doesn’t meet criteria for another element
 * (e.g. Scene Heading, Character, Dialogue, etc.). Fountain respects your line-by-line decision
 * to single or double-space, taking every carriage return as intentional.
 *
 * Power User: You can force an Action element can by preceding it with an exclamation point !.
 *
 * Tabs and spaces are retained in Action elements, allowing writers to indent a line.
 * Tabs are converted to four spaces.
 *
 * Power User: You can force a Character element by preceding it with the “at” symbol @.
 *
 * ```
 * They drink long and well from the beers.
 *
 * And then there’s a long beat.
 * Longer than is funny.
 * Long enough to be depressing.
 *
 * The men look at each other.
 * ```
 *
 * ```
 * He opens the card. A simple little number inside of which is hand written:
 *
 *     Scott --
 *     Jacob Billups
 *     Palace Hotel, RM 412
 *     1:00 pm tomorrow
 *
 * Scott exasperatedly throws down the card on the table and picks up the phone, hitting speed dial #1…
 * ```
 */
data class Action(val lines: List<String>) : SceneElement {
    override fun toString(): String = "${lines.joinToString(separator = "\n")}\n"
}

/**
 *A Character element is any line entirely in uppercase,
 * with one empty line before it and without an empty line after it.
 *
 * If you want to indent a Character element with tabs or spaces, you can, but it is not necessary.
 *
 * “Character Extensions”–the parenthetical notations that follow a character name
 * on the same line–may be in uppercase or lowercase:
 *
 * ```
 * STEEL
 * The man’s a myth!
 * ```
 *
 * ```
 * MOM (O. S.)
 * Luke! Come down for supper!
 *
 * HANS (on the radio)
 * What was it you said?
 * ```
 *
 */
data class Character(val name: String) : SceneElement {
    override fun toString(): String = "\n$name\n"
}

/**
 * Parentheticals follow a Character or Dialogue element, and are wrapped in parentheses ().
 *
 * ```
 * STEEL
 * (starting the engine)
 * So much for retirement!
 * ```
 */
data class Parenthetical(val line: String) : SceneElement {
    override fun toString(): String = "($line)\n"
}

/**
 * Dialogue is any text following a Character or Parenthetical element.
 *
 * ```
 * SANBORN
 * A good ‘ole boy. You know, loves the Army, blood runs green. Country boy. Seems solid.
 * ```
 *
 * ```
 * DAN
 * Then let’s retire them.
 * _Permanently_.
 * ```
 *
 * Dual, or simultaneous, dialogue is expressed by adding a caret ^ after the second Character element.
 *
 * ```
 * BRICK
 * Screw retirement.
 *
 * STEEL ^
 * Screw retirement.
 * ```
 *
 * Any number of spaces between the Character name and the caret are acceptable,
 * and will be ignored. All that matters is that the caret is the last character on the line.
 */
data class Dialogue(val lines: List<String>, val isDual: Boolean = false) : SceneElement {
    override fun toString(): String = "${lines.joinToString(separator = "\n")}\n"
}

/**
 * You create a Lyric by starting with a line with a tilde ~.
 *
 * ```
 * ~Willy Wonka! Willy Wonka! The amazing chocolatier!
 * ~Willy Wonka! Willy Wonka! Everybody give a cheer!
 * ```
 *
 * Fountain will remove the ‘~’ and leave it up to the app to style the Lyric appropriately.
 * Lyrics are always forced. There is no “automatic” way to get them.
 */
data class Lyrics(val lines: List<String>) : SceneElement {
    override fun toString(): String = lines.joinToString(separator = "\n") + "\n"
}

/**
 * The requirements for Transition elements are:
 *
 * Uppercase
 * Preceded by and followed by an empty line
 * Ending in TO:
 *
 * ```
 * Jack begins to argue vociferously in Vietnamese (?), But mercifully we…
 *
 * CUT TO:
 *
 * EXT. BRICK’S POOL - DAY
 * ```
 *
 * Power user: You can force any line to be a transition by beginning it with a greater-than symbol >.
 *
 * ```
 * Brick and Steel regard one another. A job well done.
 *
 * >Burn to White.
 * ```
 *
 * Power user: If a line matches the rules for Transition,
 * but you want in interpreted as something else, you have two options:
 *
 * Precede it with a period to force a Scene Heading, or
 * Add one or more spaces after the colon to cause the line
 * to be interpreted as Action (since the line no longer ends with a colon).
 */
data class Transition(val line: String) : SceneElement {
    override fun toString(): String = "\n$line\n"
}

/**
 * Centered text constitutes an Action element, and is bracketed with greater/less-than:
 *
 * `>THE END<`
 *
 * Leading spaces are usually preserved in Action, but not for centered text,
 * so you can add spaces between the text and the >< if you like.
 *
 * `> THE END <`
 */
data class Centered(val line: String) : SceneElement {
    override fun toString(): String = "\n> $line\n"
}

interface Text {
    val text: String
}

data class Plain(override val text: String) : Text {
    override fun toString(): String = text
}

/**
 *Fountain follows Markdown’s rules for emphasis,
 * except that it reserves the use of underscores for underlining,
 * which is not interchangeable with italics in a screenplay.
 *
 * ```
 * *italics*
 * **bold**
 * ***bold italics***
 * _underline_
 * ```
 *
 * In this way the writer can mix and match and combine bold,
 * italics and underlining, as screenwriters often do.
 *
 * ```
 * From what seems like only INCHES AWAY. _Steel’s face FILLS the *Leupold Mark 4* scope_.
 * ```
 * If you need to use any of the emphasis syntaxes verbatim,
 * you escape the characters using the Markdown convention of a backslash:
 *
 * ```
 * Steel enters the code on the keypad: **\*9765\***
 * ```
 */
interface Emphasis : Text {
    val nested: Text
}

data class Bold(override val nested: Text) : Emphasis {

    override val text: String
        get() = nested.text

    override fun toString(): String = "**$text**"
}

data class Italic(override val nested: Text) : Emphasis {

    override val text: String
        get() = nested.text

    override fun toString(): String = "*$text*"
}

data class Underline(override val nested: Text) : Emphasis {

    override val text: String
        get() = nested.text

    override fun toString(): String = "_${text}_"
}