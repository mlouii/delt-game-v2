label party:

    scene hallway
    with fade

    show shahaan at left

    show isiah at right

    shahaan "Hey Isiah, you drink all of the everclear?"

    shahaan "I was planning to make a jungle juice."

    isiah "What's everclear? I don't drink. I'm a good SGA president."

    isiah "Besides, everclear gets you really hungover the next day."

    isiah "Not that I would know."

    shahaan "Well if you don't drink, then how about you be the sober bro for tonight?"

    isiah "..."

    shahaan "Okay great! Silence is consent. We just need one more sober bro now."

    isiah "Wait - this has got to be a joke right? You can't be serious."

    isiah "You want ME to be the sober bro?"

    "A voice echoes, coming from inside the walls."

    talha "Isiah has been chosen as the sober bro."

    talha "Failure to comply will result a 5 times X multiplier on your current fees."

    talha "And a 10 times X multiplier on your future fees."

    talha "You have been warned."

    talha "You may also find a replacement for yourself."

    shahaan "Well, I guess you're the sober bro then."

    shahaan "I'll go find the other one."

    hide shahaan
    with moveoutleft

    isiah "Bro, I'm already wayyy too sauced."

    isiah "I don't know who you are, but can you take my place?"

    y "Umm, I'm not sure if I can."

    hide isiah
    show isiah-money at right

    isiah "I'll give you this."

    isiah "And I'm SGA president, and I'm abusing my power to make you do this."

    y "I guess I'll do it."

    isiah "Thanks, you're the $hit."

    hide isiah-money

    scene bathroom
    with fade

    show shahaan at left
    show erik at right
    show mo at center

    shahaan "What are you two doing in here?"

    erik "Just inspecting each other's bodies."

    mo "Yeah, we're just bros being bros."

    erik "Mo's gained 10 pounds of lean muscle mass since last week."

    erik "And his balls shrunk into raisins. Saw it with my own eyes."

    mo "I'm natty, btw."

    shahaan "Okay, I still need to find a sober bro."

    erik "I'm not doing it."

    erik "I hate doing sober bro almost as much as leg day."

    mo "I'm also not doing it."

    shahaan "Well, I guess I'll just have to find someone else."

    shahaan "Because I'm not doing it either."

    shahaan "I bet Logan could be the sober bro."

    mo "As long as its not me."

    shahaan "You think you can be the bartender tonight?"

    mo "Yeah, I'll make sure everyone gets HAMMERED. EVERYONE."

    talha "All-House begins in 5 minutes."

    talha "X off opportunities are immediately available."

    talha "You may now prepare for the event."

    hide shahaan
    with moveoutleft

    hide erik
    with moveoutright

    hide mo
    with moveoutright

    y "Huh, I guess I'll follow Erik."

    scene bar
    with fade

    show erik at left
    with moveinleft

    erik "We've made some changes to the bar room."

    erik "It's now a great place to get drunk."

    erik "Of course, we're still moving some stuff around."

    y "Why are you moving stuff around?"

    erik "We haven't been getting the turnout that we wanted."

    erik "So renovating things should help!"

    y "The ventilation isn't great in here."

    y "Maybe that's why people don't come here."

    erik "Ventilation makes you weak. You don't need it. Especially once you're drunk."

    y "I guess that makes sense."

    show zion at right
    with moveinright

    zion "Hey, so I just did some research on how to get a better turnout."

    zion "One of the most important things it to have a good ratio. Of guys and girls."

    zion "We need women to come to our parties."

    show mo at center
    with hpunch

    mo "I'm on it."

    mo "Although, there aren't enough HOT women on campus."

    hide mo

    erik "We can't just fix that."

    y "There has to be a way."

    y_nvl "Hey Mark, how do we get more attractive women into our party?"

    mark_nvl "In the fraternity of Delta Tau Delta, a man finds not just brothers, but the reflection of every version of his best self."

    mark_nvl "Even when the man disappears, the fraternity remains."

    y_nvl "I don't know what that means."

    mark_nvl "That is all I have to say."

    mark_nvl "You will find the answer within Delta Tau Delta."

    y "{i}What could Mark possibly mean? I have to think!{/i}"

    label choice:
        menu:
            "Pick the best option"
            "Hire strippers to join our party":
                y "I think I have an idea."

                y "We can hire strippers to join our party. Bronzeville strippers."

                y "They'll bring more people to our party."

                erik "Uhh, I don't really know about that one."

                erik "I feel like that's a little too far."

                erik "I'm not going to consider that."

                jump choice
            
            "Tell ASA Sorority to come through":
                y "I think I have an idea."

                y "We can tell ASA Sorority to come through. They're always down to party."

                y "It's also a sorority, so they'll bring more people to our party."

                erik "I don't know if that's a good idea."

                erik "They're not really our type of people. Kappa is better, anyways."

                erik "Have you heard of NASA? It stands for NO ASA."

                erik "I'm not going to consider that."

                jump choice

            "Genderbend the most breedable DELTS into the HOTTEST women":
                y "Genius just struck me."

                y "We have some of the most breedable MEN in our fraternity."

                y "Brotherhood doesn't discriminate."

                y "So why not have them switch up? It shouldn't be too hard."

                erik "Dude, you're actually a genius."

                erik "I'm going to consider that. In fact, I like that a lot."

    
    erik "You sir, just saved the party."

    mark_nvl "I'm glad to see you've found the answer."

    mark_nvl "But first, you must determine the most breedable DELTS."

    y "It's time to make some tough decisions."

    $ females = []
    $ males = []

    scene blank
    with fade

    show erik at left
    with moveinleft

    show mo at right
    with moveinright

    menu:
        "Who's more breedable?"

        "Erik":
            $ females.append("Erik")
            $ males.append("Mo")

        "Mo":
            $ females.append("Mo")
            $ males.append("Erik")

    hide erik 
    with moveoutleft

    hide mo
    with moveoutright

    show michael at left
    with moveinleft

    show brayden at right
    with moveinright

    menu:
        "Who's more breedable?"

        "Michael":
            $ females.append("Michael")
            $ males.append("Brayden")

        "Brayden":
            $ females.append("Brayden")
            $ males.append("Michael")

    hide michael
    with moveoutleft

    hide brayden
    with moveoutright

    show isiah at left
    with moveinleft

    show berto at right
    with moveinright

    menu:
        "Who's more breedable?"

        "Isiah":
            $ females.append("Isiah")
            $ males.append("Berto")

        "Berto":
            $ females.append("Berto")
            $ males.append("Isiah")

    hide isiah
    with moveoutleft

    hide berto
    with moveoutright

    show zion at left
    with moveinleft

    show luis at right
    with moveinright

    menu:
        "Who's more breedable?"

        "Zion":
            $ females.append("Zion")
            $ males.append("Luis")

        "Luis":
            $ females.append("Luis")
            $ males.append("Zion")

    hide zion
    with moveoutleft

    hide luis
    with moveoutright

    show logan at left
    with moveinleft

    show pranav at right
    with moveinright

    menu:
        "Who's more breedable?"

        "Logan":
            $ females.append("Logan")
            $ males.append("Pranav")

        "Pranav":
            show erik at center
            with hpunch
            
            erik "I don't think Pranav is breedable."
            
            erik "You're stupid."

            erik "Logan is the correct answer."

            $ females.append("Logan")
            $ males.append("Pranav")
            hide erik with dissolve

    hide logan
    with moveoutleft

    hide pranav
    with moveoutright

    scene bar
    with fade

    if "Erik" in females:
        show erik-female at left
        with moveinleft

        y "Oh my god, Erik, how did you turn into that?"

        erik "I just didn't take any creatine today."

        erik "I'm not going to lie, I'm kind of feeling it. I feel different."

        y "You look different."

        y "And why are your eyes blue now?"

        erik "Blond hair and blue eyes are coming back into style, baby!"

        y "I don't know about that one."

        erik "Check up on the others, would you?"

        hide erik-female
        with moveoutleft
    else:
        show erik-buff at left
        with moveinleft

        erik "I figured that we should all look our best, regardless any genderbending."

        y "Whoa, Erik... I like the new look."

        erik "Don't look down at my legs. They're still small."

        erik "Just look at my upper body. Got a quick pump in."

        y "Why are you so hot?"

        erik "Well, I'm a Delt. It's in my blood."

        erik "You've unlocked my true potential."

        erik "Isn't that what you wanted to do?"

        y "Yeah, but I didn't think it would work."

        erik "Anyways, I need to go mix up a protein shake."

        erik "Make sure everything is going well."

        hide erik-buff
        with moveoutleft

    show pledge-rack-night
    with fade

    if "Luis" in females:
        image luisfemaleglitch:
            "luis-female"
            pause 1
            glitch("luis-female")
            pause 0.4
            glitch("luis")
            pause 0.3
            "luis"
            pause 0.3
            glitch("luis")
            pause 0.1
            "luis-female"

        show luisfemaleglitch at right
        with moveinright

        y "Whoa, who's that cutie?"

        luis "Hehe, you'll never guess who it is."

        y "Is that you, Luis?"

        luis "Hehe, you got me."

        luis "Something was definitely in that blunt."

        luis "Got me feeling some type of way."

        hide luisfemaleglitch
        with moveoutright
    else:
        show zion-female at right
        with moveinright

        zion "Hey, there you are."

        y "Whoa, Zion, you look different."

        zion "It was your idea after all."

        zion "Fantastic judgement. This is exactly what I wanted."

        zion "We should go to the baseball game sometime."

        zion "I hope the kiss cam is on us."

        y "I don't know about that one."

        y "You're just a brother to me."

        hide zion-female
        with moveoutright

    if "isiah" in females:
        show isiah-female at left
        with moveinleft
    else:
        show isiah-buff at left
        with moveinleft

    isiah "Yo, thanks for... for takin' my sober bro shift."

    isiah "I'm havin' a... a great time, this... this is the best party ever."

    y "But the party hasn't even started yet."

    isiah "Pregaming is the... the best part of the party. I can drink... as much as I want."

    isiah "Also, can you... you take the back door? Here... here is the guest list."

    y "Sure, I'll take care of it. You take care of yourself, okay?"

    isiah "Yeah... I really need to use the toilet ... but I'll go ... go back to the PARTY!"

    scene back-door-open
    with fade

    y "I guess I just wait for guests to arrive."

    y "I wonder who's going to show up."

    show reagan at center
    with fade

    reagan "I hear there's a party deficit in there, and I've come to balance it out."

    show guests at left
    with moveinleft

    y "Hmm, I don't see your name on the list."

    hide guests
    with moveoutleft

    reagan "Seems I've hit a 'Berlin Wall' at the front door."

    hide reagan
    with dissolve

    show jenna at center
    with fade

    jenna "Is this party exclusive? Or can a girl like me join?"

    show guests at left
    with moveinleft

    y "You're not a Kappa, are you?"

    hide guests
    with moveoutleft

    jenna "I'm not a Kappa, but I think I'd be a great addition to the party."

    y "Sorry, no can do."

    jenna "That's unfortunate. I was really looking forward to it."

    hide jenna
    with dissolve

    show kappa at center
    with fade

    kappa "Let me in, I'm a Kappa."

    y "Wait, you look like you're 12."

    y "No way I'm letting you in."

    kappa "If you don't let me in, I'll tell my sisters."

    kappa "They'll be very upset."

    kappa "Now let me in. You're not a Kappa, so you don't get to decide."

    y "Fine, I guess I don't have a choice."

    hide kappa
    with moveoutright

    show shield-bearer-costume-2 at center
    with fade

    shield_girl "Hey again. Nice to see you."

    y "Wait, you're the opp from the u-farm."

    shield_girl "Yeah, so what?"

    shield_girl "I'm already dressed up for the party. I don't want any trouble."

    shield_girl "I have no intention of fighting you."

    shield_girl "Although, it would be a shame if I had to. I'm even stronger now."

    show oppasig at center
    with hpunch

    oppasig "Hey, you're supposed to be attacking the Delts."

    oppasig "Why aren't you doing anything, shield girl?"

    hide shield-bearer-costume-2
    show shield-bearer-costume-2 at center

    shield_girl "Shut up, boy. All you oppa sigs talk too much for how weak you are."

    shield_girl "Speak to me when you can bench 315."

    hide oppasig
    with fade

    y "Wait, you're not on the guest list though."

    y "I can't let you in."

    show pranav-buff at right
    with moveinright

    pranav "She's with me."

    y "Oh, okay. Good for you, Pranav."

    hide pranav-buff
    with moveoutright

    hide shield-bearer-costume-2 
    with moveoutright

    y "Looks like its all the guests for now."

    y "I think we need a bartender. I'll go look for Mo."

    scene hallway
    with fade

    show mo at center

    mo "I'm getting the drinks ready. Give me a minute, so I can change."

    hide mo 
    with moveoutright

    if "Mo" in females:
        show mo-female at center
        with moveinright

        y "Whoa! You're not just serving drinks, you're serving looks."

        mo "I'm cute, aren't I? I'd date me."

        mo "But I do have to get going. I'll see you later."

        hide mo-female
        with moveoutright
    else:
        show mo-buff at center
        with moveinright

        Mo "I've become the masculine ideal that I've always wanted to be."

        y "Oh hell no. This is not what I signed up for."

        mo "Do you not like what I'm cooking?"

        y "You look really bad. I'm sorry."

        mo "You don't understand. I'm pulling so many girls tonight with this look."

        y "Watch out, there's underage girls down there. Might want to put on some pants."

        hide mo-buff
        with moveoutright

    show colin at center
    with moveinleft

    colin "Hey, I'm Colin. You want a Smirnoff Ice?"

    y "No thanks, I'm good. I'm sober bro."

    colin "Just take it, maybe give it to someone else."

    y "Okay, I'll take it."

    colin "I've been drinking nonstop since 9am. I'm so drunk. I really want to stop."

    y "Why don't you stop?"

    colin "I made a bet as DAA. I drink as many drinks as people on academic probation."

    colin "I'm going to die. I'm going to die. I'm going to die."

    colin "This is punishment for my failure."

    colin "Although it's my kind of punishment."
    
    hide colin

    y "Hmm, I wonder who I should give this Ice to."

    show logan
    with moveinleft

    logan "Watch this."

    hide logan
    with hpunch

    show logan-female
    with hpunch

    y "What's a catgirl doing here?"

    y "I guess I'll give you a Smirnoff Ice."

    show offer-ice

    y "Here you go, catgirl. A treat."

    "Logan eyes the Smirnoff Ice, drooling."
    hide offer-ice
    hide logan-female
    show logan-female-2

    logan "Meow. I love Smirnoff Ice."

    logan "But I'm the sober bro. Nyan. I can't drink."

    logan "Hmmm, methinks that I can drink actually."

    logan "See, I'm no longer a bro. I'm a catgirl."

    logan "No such thing as a sober catgirl."

    "He takes the offer."

    logan "I can chug this Smirnoff Ice in 6 seconds."

    logan "Watch me."

    y "I'm good, I guess I'm the only sober bro here."

    y "I'll go downstairs and check on the party."

    scene bar
    with fade

    if "Mo" in females:
        show mo-female at center
    else:
        show mo-buff at center

    show bar-table at center

    mo "Who wants DRINKS? Guys you're not drinking enough."

    show kappa at left
    with moveinleft

    kappa "Me, give me something good for beginners. Something strong. I want to get buzzed."

    y "You're not actually going to give her a drink, are you?"

    mo "We've got everclear, vodka, and tequila shots."

    mo "Malibu rum as a chaser."

    mo "If you want to get buzzed, I'd recommend the everclear. Here you go."

    kappa "That sounds like it'll be good. I'll take it."

    "She downs the everclear shot."

    "She dies."

    "Her sorority sisters drag her back to Kappa."

    hide kappa

    show shield-bearer-costume-2 at right
    with moveinright

    shield_girl "She's a b1tch. I can tell. Watch out for girls like her."

    shield_girl "I know she's the type to snitch when she wakes up."

    shield_girl "B1tches like her are why I've got aggravated assault charges. They snitch too much."

    shield_girl "You guys have something nice together. Don't it get ruined."

    hide shield-bearer-costume-2
    with moveoutright

    if "Erik" in females:
        show erik-female at right
        with moveinright
    else:
        show erik-buff at right
        with moveinright

    erik "That scary girl is right. We should be careful. Go up and check the back door."

    erik "We need to make sure that it's locked. And watch for public safety."

    erik "I'll go check the front door."

    scene back-door

    y "Hmm, its pretty dark. Hard to see anything."

    y "Things look fine though. Nobody seems to be trying to get in."

    y "ERIK!! THE COAST IS CLEAR."

    y "I think we're good."

    play music scotts
    $ renpy.pause(6.25, hard=True)
    hide back-door
    show back-door-officer

    $ renpy.pause(3, hard=True)

    y "Oh no. PUBLIC SAFETY!!"

    y "I think they've even teamed up with the oppa sigs."

    if "Erik" in females:
        show erik-female at right
        with moveinright
    else:
        show erik-buff at right
        with moveinright

    erik "We're getting everyone upstairs NOW."

    erik "Man, I wish we had Anish here right now. He'd know what to do."

    erik "In the meantime, have a staring contest with the officer."

    erik "Maybe throw a fried chicken out the window. Perhaps he'll go after it."

    if "Erik" in females:
        hide erik-female
        with moveoutright
    else:
        hide erik-buff
        with moveoutright

    show logan-female at left
    with moveinleft

    show colin at right
    with moveinright

    colin "We need to prevent public safety from coming in."

    colin "We'll never get highest GPA on the quad if we get kicked off campus."

    logan "I'm throwing a Smirnoff Ice at him."

    logan "I'm going to throw it at his head."

    colin "Let's protect this house."

    $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "jacob", "pranav", "colin", "logan"]
    $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer", "kinetic", "officer", "van"]
    $ current_level = "level9"
    call game_and_select
    play music pushing_onwards

    scene back-door

    colin "Okay, we're safe for now."

    y "I'm going to check up on the people upstairs."

    scene hallway
    with fade

    show michael at center

    michael "What's going on? Are we surrounded by the enemy?"

    y "Yeah, we're surrounded by public safety. They're trying to get in."

    michael "Hold on, I need to transform into my true form."

    hide michael

    if "Michael" in females:
        show michael-female at center
        with fade
    else:
        show michael-buff at center
        with fade

    michael "I'm willing to make this my last stand."

    michael "We will never surrender."

    y "They're not going to kill us. They're just going to kick us off campus."

    michael "That's a fate worse than death."

    y "Well, they are pulling up in all their cars."

    y "Not sure how we're going to get out of this one."

    michael "AGM-114 Hellfire missiles. They penetrate 8 inches of armor."

    michael "Manufactered by Lockheed Martin. They've been taking out trucks like that since 1984."

    y "Uhh, I don't think we have any of those."

    y "Maybe you spend too much time playing Call of Duty."

    michael "I'm in the ROTC. I know what I'm talking about."

    michael "There's a reaper drone flying overhead at 50,000 feet. Time to call in air support."

    y "You're crazy. But I like it."

    michael "I'll be there when you need me."

    scene bathroom
    with fade

    show sweetheart at left
    
    show shield-bearer-costume-2 at right

    "The two girls are in the middle of a conversation."

    "They don't notice you yet."

    shield_girl "I'm so glad I got to meet you. I've heard so much about you."

    sweetheart "Yeah, if you ever want to know anything about becoming a sweetheart, just ask me."

    shield_girl "I didn't think it would, but this frat is starting to grow on me."

    shield_girl "Individually, the guys are still pretty worthless."
    
    shield_girl "{glitch}But when they come together, they become more than the sum of their parts.{/glitch}"

    sweetheart "Are you okay? You're talking a little strange."

    image shield glitched:
        glitch("shield-bearer-costume-2") # reliable slicing
        pause 0.1
        glitch("shield-bearer-costume-2") # reliable slicing
        pause 0.1
        glitch("shield-bearer-costume-2", offset=60, randomkey=None) # bigger and always-random slicing
        pause 0.2
        glitch("shield-bearer-costume-2") # reliable slicing
        pause 0.1
        "shield-bearer-costume-2"
        pause 0.5
        glitch("shield-bearer-costume-2", offset=60, randomkey=None) # bigger and always-random slicing
        pause 0.2
        glitch("shield-bearer-costume-2", offset=60, randomkey=None) # bigger and always-random slicing
        pause 0.1
        glitch("shield-bearer-costume-2", offset=60, randomkey=None) # bigger and always-random slicing
        pause 0.1
        "shield-bearer-costume-2"
        pause 0.4
        repeat

    image shield error:
        glitch("shield-bearer-costume-2") # reliable slicing
        pause 0.1
        glitch("shield-bearer-costume-2") # reliable slicing
        pause 0.1
        glitch("shield-bearer-costume-2-negative", offset=60, randomkey=None) # bigger and always-random slicing
        pause 0.2
        glitch("shield-bearer-costume-2-negative") # reliable slicing
        pause 0.1
        glitch("shield-bearer-costume-2")
        pause 0.5
        glitch("shield-bearer-costume-2", offset=60, randomkey=None) # bigger and always-random slicing
        pause 0.2
        glitch("shield-bearer-costume-2-negative", offset=60, randomkey=None) # bigger and always-random slicing
        pause 0.1
        glitch("shield-bearer-costume-2", offset=60, randomkey=None) # bigger and always-random slicing
        pause 0.1
        "shield-bearer-costume-2-negative"
        pause 0.2
        repeat

    image shield refactored:
        glitch("shield-bearer-costume-2") # reliable slicing
        pause 0.05
        glitch("shield-bearer-costume-2") # reliable slicing
        pause 0.05
        glitch("shield-bearer-costume-2") # reliable slicing
        pause 0.05
        glitch("shield-bearer-costume-2") # reliable slicing
        pause 0.05
        "gas-mask-shield-bearer"

    hide shield-bearer-costume-2
    show shield glitched at right

    shield_girl "{glitch=50} I don't want to hurt anyone {/glitch}"

    nvl clear

    mark_nvl "You're getting too close to them."

    mark_nvl "They aren't your friends."

    mark_nvl "You must destroy them."

    mark_nvl "You're an opp, remember?"

    y_nvl "Huh? What are you talking about?"

    mark_nvl "Oh, sorry."

    mark_nvl "Sent that to the wrong person."

    mark_nvl "{image=other/silly.png}"

    y_nvl "Oh, okay."

    y_nvl "We're currently surrounded by public safety."

    y_nvl "They're trying to get in."

    mark_nvl "Yeah, I know."

    mark_nvl "You'll figure it out."

    mark_nvl "You always do."

    hide shield glitched

    show gas-mask-shield-bearer at right

    shield_girl "Hey, sweetheart ... you've always been nice to me..."

    shield_girl "Don't come to the living room tonight."

    sweetheart "Wait, where are you going?"

    shield_girl "My actual friends are waiting for me outside."

    hide gas-mask-shield-bearer
    with hpunch

    y "Oh no, public safety and the opps are coming into the house."

    y "I need to find some backup."

    scene pledge-rack-night

    if "Berto" in females:
        show berto-female at left
    else:
        show berto-buff at left

    berto "Yo, I need your help."

    y "What's going on?"

    berto "Logan's blacking out again. I've put him on a bed here."

    berto "I need you to protect him."

    y "He's still chugging Smirnoff Ice? What do you mean he's blacking out?"

    berto "He's fully blacked out. He's not responding to anything. He still unconsciously drinks."

    berto "I don't know how this is possible."

    berto "But I need you to protect him."

    berto "That crazy girl with the red hair and black cap already tried to take him out."

    berto "She just dislocated his shoulder with a single punch."

    if "Michael" in females:
        show michael-female at right
        with moveinright
    else:
        show michael-buff at right
        with moveinright

    y "Okay, we'll protect him."

    michael "AFFIRMATIVE. SIR YES SIR!"

    michael "REAPER DRONE IS IN POSITION. READY TO ENGAGE."

    berto "Also, did someone $hit their pants? It certainly smells like it."

    $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "jacob", "pranav", "colin", "logan", "cobcannon"]
    $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer", "kinetic", "officer", "van", "mask_shield_bearer"]
    $ current_level = "level10"
    call game_and_select
    play music pushing_onwards

    scene hallway
    with fade

    show andrew at left
    with moveinleft

    andrew "What in the world is going on???? I'm sooooo confused."

    andrew "I was just in my room, doing my stuff."

    andrew "And all of a sudden, I hear a bunch of people screaming and yelling."

    y "Yeah, sorry. But public safety has us surrounded. We're in a lot of trouble."

    andrew "Oh, for heaven's sake. I'm not going to get in trouble for this, am I?"

    andrew "That's it. I'm booking a one-way ticket to Somalia."

    y "That's a strange choice."

    andrew "Well I watched a Youtube video of someone doing it."

    andrew "I feel like I could fit in with the locals. I don't stand out too much, do I?"

    y "Uhhhh"

    andrew "Great, I'm heading out."

    y "Wait, as you leave, don't forget to hit the griddy to distract the opps."

    andrew "Don't worry, I won't forget."

    y "Safe travels. Send me a postcard!"

    hide andrew 
    with moveoutleft

    "A few moments later ..."

    nvl clear

    nvl_narrator "Sienna has forcibly entered the group chat."

    sienna_nvl "I just hit and killed the guy that that was doing the griddy."

    sienna_nvl "A belated depledge, if you will."

    sienna_nvl "Every single one of you is going to be punished."

    sienna_nvl "I am justice."

    y_nvl "What the hell?"

    y_nvl "Sienna? Are you that shield girl?"

    sienna_nvl "I am not affiliated with that miserable, treacherous girl."

    sienna_nvl "My full name is"

    sienna_nvl "2018 Toyota Sienna LE 8 Passenger Van"

    sienna_nvl "Public Safety."

    y_nvl "Oh, okay."

    y_nvl "We'll continue to fight you."

    sienna_nvl "You won't survive this next assault."

    sienna_nvl "I'll see you in hell."

    y_nvl "Looking forward to it."

    $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "jacob", "pranav", "colin", "logan", "cobcannon", "andrew"]
    $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer", "kinetic", "officer", "van", "mask_shield_bearer"]
    $ current_level = "level11"
    call game_and_select
    play music pushing_onwards

    scene back-door-open
    with fade

    show officer

    officer "It's over, you guys."

    officer "We've been given a mandate that allows us to take control of this house."

    officer "You can't resist."

    hide officer
    with moveoutright

    "You hear a loud roar from the pledge rack."

    "It's Jacob"

    jacob "PUBLIC SAFETY, YOU'RE GOING DOWN."

    show shahaan at left
    with moveinleft

    shahaan "Hey, we need to restrain Jacob."

    shahaan "He's going to get himself life without parole."

    y "Yeah, he'll attack anyone that comes near him."

    scene pledge-rack-night
    with fade

    show jacob at right
    with vpunch

    jacob "ARE YOU PUBLIC SAFETY?"

    jacob "I'M GONNA PUT YOU IN THE GROUND."

    jacob "I love this fraternity so much..."

    jacob "Even if I have to go to jail for it..."

    jacob "I'm not letting this ship go down."

    if "Brayden" in females:
        show brayden-female at left
        with moveinleft

        brayden "With a body like this, I could make men cum so hard, they'd be paralyzed."

        brayden "And they wouldn't stop cumming, if we were on a ship, they'd all be cumming. Captain, crew, all of them."

        brayden "So the ship floods from the inside and capsizes and then goes down."

        brayden "You know Avatar, like the last airbender?"
        
        brayden "I'm Brayden, the last cumbender."

        y "Uh ..."

        jacob "..."

        y "Thanks for sharing."

        hide brayden-female
        with moveoutleft
    else:
        show brayden-buff at left
        with moveinleft

        brayden "Once I brought down a ship, it's a pretty sad story."

        brayden "So I was with this girl, and I made her squirt 40 times in 3 minutes."

        brayden "She was squirting like everywhere, laminar flow, 300 cubic meters per second"

        brayden "The ship was overflowing with squirt, then capsized and a lot of people drowned." 
        
        brayden "I feel really guilty, to this day."

        y "Oh, wow."

        jacob "Yeah, that's relatable."

        y "I'd love to hear more, but we're in the middle of something."

        hide brayden-buff
        with moveoutleft

    y "Anyways, Jacob. We can't let you do this."

    y "You can't fight the police."

    y "You don't want to suffer what Josh Silets went through."

    jacob "So what are you going to do?"

    jacob "Are you going to stop me?"

    y "I'm not letting any of them get near you."

    jacob "Well, if I see opps or public safety, I'm going to attack them."

    jacob "I'm going to attack them so hard."

    y "Then you won't see them. This is for your own good."

    scene hallway
    with fade

    "THEY'RE COMING UPSTAIRS!"

    show officer 
    with hpunch

    officer "Let me into the pledge rack!"

    y "I'm not going to let you anywhere near him."

    y "By any means necessary."

    $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "jacob", "pranav", "colin", "logan", "cobcannon", "andrew"]
    $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer", "kinetic", "officer", "van", "mask_shield_bearer"]
    $ current_level = "level12"
    call game_and_select
    play music pushing_onwards

    scene pledge-rack-night
    with fade

    show officer at left
    with moveinleft

    officer "You do know, we've already collected all the evidence we need."

    officer "You guys are getting kicked off campus. You'll never be able to come back."

    officer "We're already processing the paperwork. Just give up."

    officer "The provost is coming over right now."

    show shield-bearer-costume-2 at right
    with hpunch

    shield_girl "No he isn't."

    officer "What? Who are you to say that?"

    shield_girl "You know who I am."

    shield_girl "I'm Athena Cramb. Alan Cramb's daughter."

    shield_girl "This house is under my protection."

    officer "You do know what you're doing, right? You're going against HIM."

    hide shield-bearer-costume-2 
    show shield glitched at right

    shield_girl "{glitch=20}I don't care.{/glitch}"

    shield_girl "{glitch=30}Even if this is the last thing I ever do.{/glitch}"

    officer "You're going to regret this."

    hide shield glitched
    show shield error at right

    shield_girl_glitch "{glitch=50}There will be nothing left of me to regret.{/glitch}"

    shield_girl_glitch "{glitch=50}This house will NOT die.{/glitch}"

    hide shield error
    show shield-bearer-costume-2-outline at right

    $ renpy.pause(0.5, hard=True)

    hide shield-bearer-costume-2-outline

    mark_nvl "Sorry if you saw anything weird."

    officer "Well, I guess we can't do anything anymore."

    officer "We'll be back another time."

    officer "But we'll be back."

    hide officer 
    with moveoutleft

    show shield refactored at right

    refactored "Don't think she saved you."

    refactored "You'll be put in dire straits soon enough."

    hide shield refactored

    



    




























    
    





















    


























            


















