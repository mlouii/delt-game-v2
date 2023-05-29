label party:

    # scene hallway
    # with fade

    # show shahaan at left

    # show isiah at right

    # shahaan "Hey Isiah, you drink all of the everclear?"

    # shahaan "I was planning to make a jungle juice."

    # isiah "What's everclear? I don't drink. I'm a good SGA president."

    # isiah "Besides, everclear gets you really hungover the next day."

    # isiah "Not that I would know."

    # shahaan "Well if you don't drink, then how about you be the sober bro for tonight?"

    # isiah "..."

    # shahaan "Okay great! Silence is consent. We just need one more sober bro now."

    # isiah "Wait - this has got to be a joke right? You can't be serious."

    # isiah "You want ME to be the sober bro?"

    # "A voice echoes, coming from inside the walls."

    # talha "Isiah has been chosen as the sober bro."

    # talha "Failure to comply will result a 5 times X multiplier on your current fees."

    # talha "And a 10 times X multiplier on your future fees."

    # talha "You have been warned."

    # talha "You may also find a replacement for yourself."

    # shahaan "Well, I guess you're the sober bro then."

    # shahaan "I'll go find the other one."

    # hide shahaan
    # with moveoutleft

    # isiah "Bro, I'm already wayyy too sauced."

    # isiah "I don't know who you are, but can you take my place?"

    # y "Umm, I'm not sure if I can."

    # hide isiah
    # show isiah-money at right

    # isiah "I'll give you this."

    # isiah "And I'm SGA president, and I'm abusing my power to make you do this."

    # y "I guess I'll do it."

    # isiah "Thanks, you're the $hit."

    # hide isiah-money

    # scene bathroom
    # with fade

    # show shahaan at left
    # show erik at right
    # show mo at center

    # shahaan "What are you two doing in here?"

    # erik "Just inspecting each other's bodies."

    # mo "Yeah, we're just bros being bros."

    # erik "Mo's gained 10 pounds of lean muscle mass since last week."

    # erik "And his balls shrunk into raisins. Saw it with my own eyes."

    # mo "I'm natty, btw."

    # shahaan "Okay, I still need to find a sober bro."

    # erik "I'm not doing it."

    # erik "I hate doing sober bro almost as much as leg day."

    # mo "I'm also not doing it."

    # shahaan "Well, I guess I'll just have to find someone else."

    # shahaan "Because I'm not doing it either."

    # shahaan "I bet Logan could be the sober bro."

    # mo "As long as its not me."

    # shahaan "You think you can be the bartender tonight?"

    # mo "Yeah, I'll make sure everyone gets HAMMERED. EVERYONE."

    # talha "All-House begins in 5 minutes."

    # talha "X off opportunities are immediately available."

    # talha "You may now prepare for the event."

    # hide shahaan
    # with moveoutleft

    # hide erik
    # with moveoutright

    # hide mo
    # with moveoutright

    # y "Huh, I guess I'll follow Erik."

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
















            


















