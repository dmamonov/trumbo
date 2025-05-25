package onlinedb.function

import com.google.gson.Gson
import dev.langchain4j.data.message.SystemMessage
import dev.langchain4j.data.message.UserMessage
import dev.langchain4j.model.chat.request.ChatRequest
import onlinedb.models.mistral
import onlinedb.models.openai
import onlinedb.scripts.Scene
import onlinedb.scripts.parseAlien1976EarlyDraft
import onlinedb.scripts.parseAliens1985

fun main() {
    val model = openai()

    fun highlightCharacters(text: String): String {
        val response = model.chat(
            ChatRequest.builder()
                .messages(
                    SystemMessage(
                        """
You are assisting a professional screenwriter.

Here is the list of characters:

 - Primary name: Ripley. Also known as: Ellen Ripley, Warrant Officer Ripley  
 - Primary name: Newt. Also known as: Rebecca "Newt" Jorden  
 - Primary name: Hicks. Also known as: Corporal Hicks  
 - Primary name: Burke. Also known as: Carter Burke  
 - Primary name: Gorman. Also known as: Lieutenant Gorman  
 - Primary name: Vasquez. Also known as: Private Vasquez  
 - Primary name: Hudson. Also known as: Private Hudson  
 - Primary name: Bishop. Also known as: Bishop (ECA)  
 - Primary name: Apone. Also known as: Master Sergeant Apone  
 - Primary name: Jones. Also known as: Jones (the cat)  
 - Primary name: Bishop. Also known as: ECA Bishop  
 - Primary name: Jonesy. Also known as: (the cat)  
 - Primary name: Lambert. Also known as: Lambert (original crew member)  
 - Primary name: Dallas. Also known as: Dallas (original crew member)  
 - Primary name: Parker. Also known as: Parker (original crew member)  
 - Primary name: Brett. Also known as: Brett (original crew member)  
 - Primary name: Kane. Also known as: Kane (original crew member)  
 - Primary name: Ash. Also known as: Ash (android from original crew)  
 - Primary name: Van Leuwen. Also known as: ICC Van Leuwen  
 - Primary name: ECA Rep. Also known as: ECA Representative  
 - Primary name: Doctor. Also known as: Doctor (in hospital scene)  
 - Primary name: Med-Tech. Also known as: Med-Tech (in hospital scene)  
 - Primary name: Jorden. Also known as: Russ Jorden  
 - Primary name: Anne. Also known as: Anne Jorden  
 - Primary name: Tim. Also known as: Tim (Jorden's son)  
 - Primary name: Med-Tech. Also known as: Female Med-Tech (in hospital scene)  
 - Primary name: Simpson. Also known as: Operations Manager Simpson  
 - Primary name: Lydecker. Also known as: Assistant Operations Manager Lydecker  
 - Primary name: Dr. Marachuk. Also known as: John L. (cocooned colonist)  
 - Primary name: Detrich. Also known as: Corporal Detrich  
 - Primary name: Ferro. Also known as: Corporal Ferro  
 - Primary name: Drake. Also known as: Private Drake  
 - Primary name: Wierzbowski, Private Wierzbowski  
 - Primary name: Frost, Private Frost  
 - Primary name: Spunkmeyer. Also known as: PFC Spunkmeyer  
 - Primary name: Crowe. Also known as: Private Crowe  
 - Primary name: Weyland. Also known as: Weyland-Yutani Company Representative  
 - Primary name: Insurance Investigator. Also known as: Insurance Investigator (colonial investigation board)  
 - Primary name: ECA Rep (ECA Representative)  

You task is to highlight all mentions of this characters using markdown reference.

Example:
```input
    Hi Ferro!
    Where is ECA Bishop?
```

```output
    Hi [Ferro]!
    Where is [ECA Bishop](Bishop)?
```


 

"""
                    ),
                    UserMessage(text)
                )
                .build()
        )
        return response.aiMessage().text()
    }


    println(
        highlightCharacters(
            """
 Ripley's light falls on something amidst the debris...
        a FRAMED PHOTOGRAPH of Newt, dressed up and smiling,
        a ribbon in her hair.  In embossed gold letters
        underneath it says:

                      FIRST GRADE CITIZENSHIP AWARD
                              REBECCA JORDEN

        INT. OPERATIONS - ON NEWT - MANAGER'S OFFICE             73

        sitting huddles in a chair, arms around her knees.
        Looking at a point in space.

                                   GORMAN
                           (o.s.)
                    What's her name again?

                                   DIETRICH
                           (o.s.)
                    Rebecca.

        WIDER ANGLE  REVEALING Gorman sitting in front of her
        while Dietrich watches the readouts from a
        BIO-MONITORING CUFF wrapped around Newt's tiny arm.

    """.trimIndent()
        )
    )
}

/*


 */