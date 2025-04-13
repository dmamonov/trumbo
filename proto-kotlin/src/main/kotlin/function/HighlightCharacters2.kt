package onlinedb.function

import com.apple.laf.ScreenMenuBar
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
You task is to highlight all mentions of character in a scene using markdown bold formatting.
Please ignore names of other objects (e.g. model, street or ship names).

Here is the list of characters:

 - Ripley, Ellen Ripley, Warrant Officer Ripley  
 - Newt, Rebecca "Newt" Jorden  
 - Hicks, Corporal Hicks  
 - Burke, Carter Burke  
 - Gorman, Lieutenant Gorman  
 - Vasquez, Private Vasquez  
 - Hudson, Private Hudson  
 - Bishop, Bishop (ECA)  
 - Apone, Master Sergeant Apone  
 - Jones, Jones (the cat)  
 - Bishop, ECA Bishop  
 - Jonesy (the cat)  
 - Lambert, Lambert (original crew member)  
 - Dallas, Dallas (original crew member)  
 - Parker, Parker (original crew member)  
 - Brett, Brett (original crew member)  
 - Kane, Kane (original crew member)  
 - Ash, Ash (android from original crew)  
 - Van Leuwen, ICC Van Leuwen  
 - ECA Rep, ECA Representative  
 - Doctor, Doctor (in hospital scene)  
 - Med-Tech, Med-Tech (in hospital scene)  
 - Jorden, Russ Jorden  
 - Anne, Anne Jorden  
 - Tim, Tim (Jorden's son)  
 - Med-Tech, Female Med-Tech (in hospital scene)  
 - Simpson, Operations Manager Simpson  
 - Lydecker, Assistant Operations Manager Lydecker  
 - Dr. Marachuk, John L. (cocooned colonist)  
 - Detrich, Corporal Detrich  
 - Ferro, Corporal Ferro  
 - Drake, Private Drake  
 - Wierzbowski, Private Wierzbowski  
 - Frost, Private Frost  
 - Spunkmeyer, PFC Spunkmeyer  
 - Crowe, Private Crowe  
 - Weyland, Weyland-Yutani Company Representative  
 - Insurance Investigator, Insurance Investigator (colonial investigation board)  
 - ECA Rep (ECA Representative)  
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
INT. BRIDGE - DAY

        All viewscreens operational.

                                 DALLAS
                  Engage artificial gravity.

        Lambert throws a switch.
        The ship lurches.

                                 LAMBERT
                  Engaged.

                                 DALLAS
                  Altering the vector now.

        A huge tremor runs throughout the ship.

                                 PARKER'S VOICE
                         (o.s.)
                  Dust is clogging the damn intakes
                  again.  We're overloading.

                                 DALLAS
                  Just hold us together until
                  we're beyond G1...

        The pitch of the engines changes...deepens.

        EXT. NOSTROMO - DAY

        The ship moves at an acute angle.
        Slices through the boiling clouds.

        INT. ENGINE ROOM CUBICLE

        Parker and Brett watching the guages.

        INT. BRIDGE - DAY

        Outside the screens, clouds, clouds, clouds.
        Another tremor runs through the ship.
        The crew's eyes riveted to their instruments.

                                 DALLAS
                  Let's pick up the money and go
                  home.

        EXT. NOSTROMO

        The ship clears the top of the cloud layer.
        Bursts out into star-sprinkled space.
        Trailing a wake of glimmering dust flecks.
        Attached itself to the hovering refinery.

        INT. ENGINE ROOM CUBICLE

        Brett waves his arms in exultation.

                                 BRETT
                  We did it

                                 PARKER
                  Walk in the park.  When we fix
                  something it stays fixed.

        Big smiles.

        INT. BRIDGE

        The Nostromo now safely beyond gravity.

                                 DALLAS
                  Set our course and get us up
                  to light plus four.

        Lambert begins punching buttons.

                                 LAMBERT
                  Feets get me out of here.

        EXT. OUTER SPACE

        The Nostromo now at light speed.
        Preceptible movement in the surrounding universe.
        A corona effect emerges.
        Stars approaching the Nostromo appear blue.
        Receding stars going to amber.
        Redshift, made visible because of the craft's velocity.

        INT. MESS

        Parker, Brett, Dallas and Ripley around the table.
        Drinking coffee.

                                 PARKER
                  The best thing to do is just to
                  freeze him.  Stop the goddam
                  disease.  He can get a doctor to
                  look at him when we get back home.

                                 BRETT
                  Right.

                                 RIPLEY
                  Whenever he says anything you say
                  'right'.  You know that, Brett.

                                 BRETT
                  Right.

                                 RIPLEY
                  What do you think, Parker.  Your
                  staff just follows you around and
                  says 'right'.  Like a regular parrot.

        Parker turns to Brett.

                                 PARKER
                  Yeah.  Shape up.  What are you,
                  some kind of parrot.

                                 BRETT
                  Right.

                                 DALLAS
                  Knock it off... Kane will have
                  to go into quarantine.

                                 RIPLEY
                  Yeah.  And so will we.

        Lambert enters.

                                 LAMBERT
                  How about a little something to
                  lower your spirits.

                                 DALLAS
                  Thrill me.

                                 LAMBERT
                  According to my calculations...
                  based on the time spent getting
                  to and from the planet and the
                  speed at which it's moving away
                  from the other...

                                 DALLAS
                  Give me the short version...

                                 LAMBERT
                  It'll take us six weeks to get
                  back on course.

                                 DALLAS
                  How far to Earth.

                                 LAMBERT
                  Ten months.

                                 RIPLEY
                  Christ.

        Beep.

                                 DALLAS
                  Dallas.

                                 ASH
                         (voice over)
                  Come and see Kane right away...

                                 DALLAS
                  Any change in his condition.

                                 ASH
                         (voice over)
                  It's simpler if you just come
                  see him.

        INT. CORRIDOR OUTSIDE INFIRMARY WINDOW

        What they see is...Not what they expect.
        Kane is sitting up in bed...wide awake.
        They enter...

                                 LAMBERT
                  Kane...Are you all right.

                                 KANE
                  Mouth's dry...can I have some
                  water.

        Instantly, Ash brings him a plastic cup and water.
        Kane gulps it down in a swallow.

                                 KANE
                  More.

        Ripley quickly fills a much bigger container.
        Hands it to Kane.
        He greedily consumes the entire contents.
        Then sags back, panting, on the bunk.

                                 DALLAS
                  How do you feel.

                                 KANE
                  Terrible.  What happened to me.

                                 ASH
                  You don't remember.

                                 KANE
                  Don't remember anything.  I can
                  barely remember my name.

                                 PARKER
                  Do you hurt.

                                 KANE
                  All over.  Feel like somebody's
                  been beating me with a stick
                  for about six years.
                         (smiles)
                  God, I'm hungry.

                                 RIPLEY
                  What's the last thing you can
                  remember.

                                 KANE
                  I don't know.

                                 DALLAS
                  Do you remember what happened
                  on the planet.

                                 KANE
                  Just some horrible dream
                  about smothering.  Where
                  are we.

                                 RIPLEY
                  We're on our way home.

                                 BRETT
                  Getting ready to go back into
                  the freezers.

                                 KANE
                  I'm starving.  I want some food
                  first.

                                 PARKER
                  I'm pretty hungry myself.

                                 DALLAS
                  One meal before bed.
    """.trimIndent()
        )
    )

    if (false) {
        parseAlien1976EarlyDraft().scenes.forEach { scene ->
            println("-".repeat(80))
            println(highlightCharacters(scene.toText()))
        }
    }
}

/*

--------------------------------------------------------------------------------
     INTERIOR - HYPERSLEEP VAULT

     A stainless steel room with no windows, the walls packed with
     instrumentation.  The lights are dim and the air is frigid.

     Occupying most of the floor space are rows of horizontal FREEZER
     COMPARTMENTS, looking for all the world like meat lockers.

     FOOM!  FOOM!  FOOM!  With explosions of escaping gas, the lids on the
     freezers pop open.

     Slowly, groggily, six nude men sit up.

                              **ROBY**
               Oh... God... am I cold...

                              **BROUSSARD**
               Is that you, **Roby**?

                              **ROBY**
               I feel like shit...

                              **BROUSSARD**
               Yeah, it's you all right.

     Now they are yawning, stretching, and shivering.

                              **FAUST**
                    (groans)
               Ohh... I must be alive, I feel dead.

                              **BROUSSARD**
               You look dead.

                              **MELKONIS**
               The vampires rise from their graves.

     This draws a few woozy chuckles.

                              **BROUSSARD**
                    (shakes his fist in the
                     air triumphantly)
               We made it!

                              **HUNTER**
                    (not fully awake)
               Is it over?

                              **STANDARD**
               It's over, **Hunter**.

                              **HUNTER**
                    (yawning)
               Boy, that's terrific.

                              **STANDARD**
                    (looking around with a grin)
               Well, how does it feel to be rich
               men?

                              **FAUST**
               Cold!

     This draws a LAUGH.

                              **STANDARD**
               Okay!  Everybody topside!  Let's get
               our pants on and get to our posts!

     The men begin to swing out of the freezers.

                              **MELKONIS**
               Somebody get the cat.

     **Roby** picks a limp cat out of a freezer.
--------------------------------------------------------------------------------
     INTERIOR - CONTROL ROOM

     This is a fantastic circular room, jammed with instrumentation.  There
     are no windows, but above head level the room is ringed by
     viewscreens, all blank for the moment.

     There are seats for four men.  Each chair faces a console and is
     surrounded by a dazzling array of technology.

     **STANDARD**, **ROBY**, **BROUSSARD**, and **MELKONIS** are entering and finding their
     seats.

                              **BROUSSARD**
               I'm going to buy a cattle ranch.

                              **ROBY**
                    (putting down the cat)
               Cattle ranch!

                              **BROUSSARD**
               I'm not kidding.  You can get one if
               you have the credit.  Look just like
               real cows, too.

                              **STANDARD**
               All right, tycoons, let's stop
               spending our credit and start
               worrying about the job at hand.

                              **ROBY**
               Right.  Fire up all systems.

     They begin to throw switches, lighting up their consoles.  The control
     room starts to come to life.  All around the room, colored lights
     flicker and chase each other across glowing screens.  The room fills
     with the hum and chatter of machinery.

                              **STANDARD**
               Sandy, you want to give us some
               vision?

                              **MELKONIS**
               Feast your eyes.

     **MELKONIS** reaches to his console and presses a bank of switches.  The
     strip of viewscreens flickers into life.

     On each screen, we see BLACKNESS SPECKLED WITH STARS.

                              **BROUSSARD**
                    (after a pause)
               Where's Irth?

                              **STANDARD**
               Sandy, scan the whole sky.

     **MELKONIS** hits buttons.  On the screens the images all begin to pan.

     CAMERA MOVES IN ON ONE OF THE SCREENS, with its moving image of a
     starfield.
--------------------------------------------------------------------------------
     EXTERIOR - OUTER SPACE

     CLOSE SHOT OF A PANNING TV CAMERA.  This camera is remote controlled,
     turning silently on its base.

     CAMERA BEGINS TO PULL BACK, revealing that the TV camera is mounted on
     the HULL OF SOME KIND OF CRAFT.

     When the pullback is finished, WE SEE THE FULL LENGTH OF THE **STARSHIP**
     "SNARK," hanging in the depths of interstellar space, against a
     background of glimmering stars.
--------------------------------------------------------------------------------
     INTERIOR - BRIDGE

                              **ROBY**
               Where are we?

                              **STANDARD**
               Sandy, contact traffic control.

     **Melkonis** switches on his radio unit.

                              **MELKONIS**
               This is deep space commercial vessel
               SNARK, registration number E180246,
               calling Antarctica air traffic
               control.  Do you read me?  Over.

     There is only the HISS OF STATIC.

                              **BROUSSARD**
                    (staring at a screen)
               I don't recognize that constellation.

                              **STANDARD**
               Dell, plot our location.

     **Broussard** goes into action, punching buttons, lighting up all his
     instruments.

                              **BROUSSARD**
               I got it.  Oh boy.

                              **STANDARD**
               Where the hell are we?

                              **BROUSSARD**
               Just short of Zeta II Reticuli.  We
               haven't even reached the outer rim
               yet.

                              **ROBY**
               What the hell?

     **Standard** picks up a microphone.

                              **STANDARD**
               This is Chaz speaking.  Sorry, but we
               are not home.  Our present location
               seems to be only halfway to Irth.
               Remain at your posts and stand by.
               That is all.

                              **ROBY**
               Chaz, I've got something here on my
               security alert.  A high priority from
               the computer...

                              **STANDARD**
               Let's hear it.

                              **ROBY**
                    (punches buttons)
               Computer, you have signalled a
               priority three message.  What is the
               message?

                              **COMPUTER**
                    (a mechanical voice)
               I have interrupted the course of the
               voyage.

                              **ROBY**
               What?  Why?

                              **COMPUTER**
               I am programmed to do so if certain
               conditions arise.

                              **STANDARD**
               Computer, this is Captain **Standard**.
               What conditions are you talking
               about?

                              **COMPUTER**
               I have intercepted a transmission of
               unknown origin.

                              **STANDARD**
               A transmission?

                              **COMPUTER**
               A voice transmission.

                              **MELKONIS**
               Out here?

     The men exchange glances.

                              **COMPUTER**
               I have recorded the transmission.

                              **STANDARD**
               Play it for us, please.

     Over the speakers, we hear a hum, a crackle, static... THEN A
     STRANGE, UNEARTHLY VOICE FILLS THE ROOM, SPEAKING AN ALIEN
     LANGUAGE.  The bizarre voice speaks a long sentence, then falls
     silent.

     The men all stare at each other in amazement.

                              **STANDARD**
               Computer, what language was that?

                              **COMPUTER**
               Unknown.

                              **ROBY**
               Unknown!  What do you mean?

                              **COMPUTER**
               It is none of the 678 dialects
               spoken by technological man.

     There is a pause, then EVERYBODY STARTS TALKING AT THE SAME TIME.

                              **STANDARD**
                    (silencing them)
               Just hold it, hold it!
                    (glares around the room)
               Computer: have you attempted to
               analyze the transmission?

                              **COMPUTER**
               Yes.  There are two points of salient
               interest.  Number one: it is highly
               systematized, indicating intelligent
               origin.  Number two: certain sounds
               are inconsistent with the human
               palate.

                              **ROBY**
               Oh my God.

                              **STANDARD**
               Well, it's finally happened.

                              **MELKONIS**
               First contact...

                              **STANDARD**
               Sandy, can you home in on that beam?

                              **MELKONIS**
               What's the frequency?

                              **STANDARD**
               Computer, what's the frequency of
               the transmission?

                              **COMPUTER**
               65330 dash 99.

     **Melkonis** punches buttons.

                              **MELKONIS**
               I've got it.  It's coming from
               ascension 6 minutes 32 seconds,
               declination -39 degrees 2 seconds.

                              **STANDARD**
               Dell -- show me that on a screen.

                              **BROUSSARD**
               I'll give it to you on number four.

     **Broussard** punches buttons.  One of the viewscreens flickers, and a
     small dot of light becomes visible in the corner of the screen.

                              **BROUSSARD (CONT'D)**
               That's it.  Let me straighten it out.

     He twists a knob, moving the image on the screen till the dot is in
     the center.

                              **STANDARD**
               Can you get it a little closer?

                              **BROUSSARD**
               That's what I'm going to do.

     He hits a button.  The screen flashes and a PLANET APPEARS.

                              **BROUSSARD (CONT'D)**
               Planetoid.  Diameter, 120 kilometers.

                              **MELKONIS**
               It's tiny!

                              **STANDARD**
               Any rotation?

                              **BROUSSARD**
               Yeah.  Two hours.

                              **STANDARD**
               Gravity?

                              **BROUSSARD**
               Point eight six.  We can walk on it.

     **Standard** rises.

                              **STANDARD**
               Martin, get the others up to the
               lounge.
--------------------------------------------------------------------------------
     INTERIOR - MULTI-PURPOSE ROOM

     The entire crew -- **STANDARD**, **ROBY**, **BROUSSARD**, **MELKONIS**, **HUNTER**, and
     **FAUST** -- are all seated around a table, with **STANDARD** at the head.

                              **MELKONIS**
               If it's an S.O.S., we're morally
               obligated to investigate.

                              **BROUSSARD**
               Right.

                              **HUNTER**
               I don't know.  Seems to me we came on
               this trip to make some credit, not
               to go off on some kind of side trip.

                              **BROUSSARD**
                    (excited)
               Forget the credit; what we have here
               is a chance to be the first men to
               contact a nonhuman intelligence.

                              **ROBY**
               If there is some kind of alien
               intelligence down on that planetoid,
               it'd be a serious mistake for us to
               blunder in unequipped.

                              **BROUSSARD**
               Hell, we're equipped --

                              **ROBY**
               Hell, no!  We don't know what's down
               there on that piece of rock!  It
               might be dangerous!  What we should
               do is get on the radio to the
               exploration authorities... and let
               them deal with it.

                              **STANDARD**
               Except it will take 75 years to get
               a reply back.  Don't forget how far
               we are from the Colonies, **MARTIN**.

                              **BROUSSARD**
               There are no commercial lanes out
               here.  Face it, we're out of range.

                              **MELKONIS**
               Men have waited centuries to contact
               another form of intelligent life in
               the universe.  This is an opportunity
               which may never come again.

                              **ROBY**
               Look --

                              **STANDARD**
               You're overruled, **MARTIN**.  Gentlemen
               -- let's go.
--------------------------------------------------------------------------------
     INTERIOR - BRIDGE

     The men are strapping in, but this time it is with grim determination.

                              **STANDARD**
               Dell, I want greater magnification.
               More surface detail.  I want to see
               what this place looks like.

                              **BROUSSARD**
               I'll see what I can do.

     He jabs his controls.  The image on the screen ZOOMS DOWN TOWARD THE
     PLANET; but all detail quickly vanishes into a featureless grey haze.

                              **STANDARD**
               It's out of focus.

                              **ROBY**
               No -- that's atmosphere.  Cloud
               layer.

                              **MELKONIS**
               My God, it's stormy for a piece of
               rock that size!

                              **ROBY**
               Just a second.
                    (punches buttons)
               Those aren't water vapor clouds;
               they have no moisture content.

                              **STANDARD**
               Put ship in atmospheric mode.
--------------------------------------------------------------------------------
There are no characters mentioned in this scene.
--------------------------------------------------------------------------------
     INTERIOR - BRIDGE

                              STANDARD
               **Dell**, set a course and bring us in
               on that beam.
--------------------------------------------------------------------------------
     EXTERIOR - SPACE

     The **SNARK**'s engines cough into life, and send it drifting toward the
     distant dot that is the planetoid.

     CAMERA APPROACHES THE PLANETOID, until it looms large on screen.  It is
     turbulent, completely enveloped in dun-colored clouds.

     The **SNARK** drops down toward the surface.
--------------------------------------------------------------------------------

Process finished with exit code 130 (interrupted by signal 2:SIGINT)

 */