

label alumni:
    play music predestined

    image neil dance:
        "neil-crazy"
        pause 0.1
        "neil-crazy-2"
        pause 0.1
        repeat

    scene tanjy-stair
    with fade

    show neil-crazy

    neil "Watch where you're going."

    neil "Can't you see I'm already on the stairs?"

    y "Sorry."

    y "Wait, you're Neil? The dancer from 3 years ago?"

    y "You look a lot different."

    neil "Yeah, it's called progress. Of course I look different."

    neil "I'm better than I was before."

    y "Can you show me some of your moves?"

    hide neil-crazy
    show neil-crazy-2

    neil "No. I've got bigger endeavors to pursue."

    y "Pleaseee?"

    neil "..."

    hide neil-crazy-2
    show neil dance

    neil "Tell me when you want me to stop."

    y "Wow, that was amazing."

    hide neil dance
    show neil-crazy

    y "As good as I remember."

    neil "I'm glad you enjoyed it."

    y "Wait, so what are your bigger endeavors?"

    neil "I'm the Founder of Kinetic Footwear."

    y "That's the shoes ... that the oppa sigs wear?"

    neil "Yes. I'm the one who made them."

    y "Why would you give them to the oppa sigs?"

    neil "Kinetic footwear shoes are only useful for those who keep moving forward."

    neil "Not those who only take steps backwards."

    y "So you're saying oppa sigs are better than us?"

    neil "In its current state, yes."

    y "What do you mean?"

    neil "I mean, what have you guys even accomplished?"

    neil "I'm a billionaire founder of a shoe company."

    neil "Kids as young as 7 years old are working in my factories."

    neil "They are able to support their families because of me."

    neil "I'm making a difference in the world."

    neil "What are you doing?"

    y "I'm ... I'm ..."

    neil "Still trying to rush a fraternity?"

    neil "Protecting a house that's already dead?"

    neil "Members with no future?"

    y "Don't say that."

    y "We're going to make it better. You'll see."

    neil "You're a great guy, but you're delusional."

    neil "This is Delts. Everything good in here goes to $hit."

    neil "Focus on yourself. Not this house."

    neil "I'm distributing Kinetic Footwear to all of its fans."

    neil "As the first important IIT graduate since the inventor of the mobile phone."

    hide neil-crazy

    y "I can't believe that Neil would say that."

    y "He's an alumni. He should be supporting us."

    y "I hear sounds coming from downstairs. I'll check it out."

    scene crazy
    with fade

    show kanishk at left
    with moveinleft

    kanishk "None of these people deserve these things."

    y "What do you mean?"

    kanishk "Like this TV. It's a 4K TV."

    kanishk "They don't need something this nice."

    kanishk "How about they pick up a book and read it instead?"

    kanishk "Or maybe even apply for a job."

    y "But you can't just take it. It's not yours."

    kanishk "I'm not taking it. I'm just moving it to my apartment."

    kanishk "I'll bring it back when they're ready for it."

    kanishk "Basically, I'm doing them a favor."

    y "I don't think that's how it works."

    kanishk "Well that's how it works for me."

    y "Have I seen you before?"

    kanishk "I'm Mark's roommate."

    y "And he's okay with you stealing other people's stuff?"

    kanishk "I'm not stealing. I'm just borrowing."

    kanishk "Stop using such harsh words. It's not nice."

    y "What if the brothers come down and see you?"

    kanishk "They won't. The opps are coming again."

    kanishk "They're going to be too busy to notice."

    kanishk "And I'll slip away with all of their stuff."

    y "You're not going to get away with this."

    y "I'm telling Mark about this."

    kanishk "Go ahead."

    y_nvl "Hey Mark, your roommate is stealing stuff from the house."

    mark_nvl "Okay? So what do you want me to do about it?"

    y_nvl "I don't know. Stop him?"

    mark_nvl "He has his own free will."

    mark_nvl "I'm not gonna control what he does."

    y_nvl "But he's stealing from the house."

    mark_nvl "And you have your own free will."

    mark_nvl "Stop him yourself."

    "A voice is heard from upstairs."

    "THE OPPS ARE COMING AGAIN!!"

    "EVERYONE GET READY!!"

    kanishk "See, I told you. I'm going to get away with this."

    kanishk "I'll be back for more."

    $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "jacob", "pranav", "colin", "logan", "cobcannon", "andrew"]
    $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer", "kinetic", "officer", "van", "mask_shield_bearer", "neil", "kanishk"]
    $ current_level = "level13"
    call game_and_select
    play music predestined

    scene hallway
    with fade

    y "Hmm, where did everyone go?"

    y "And why isn't Mark doing anything?"

    y "He did say a lot of bad things about this fraternity earlier."

    y "I should talk to him."

    y_nvl "Hey Mark, what's going on?"

    y_nvl "Why do the opps keep coming?"

    y_nvl "This isn't normal."

    y_nvl "And why aren't you doing anything?"

    mark_nvl "You sound tired."

    mark_nvl "Why don't you go to sleep?"

    y_nvl "I'm not tired."

    y_nvl "I'm just worried about the house."

    mark_nvl "Don't worry about it."

    y_nvl "You're not working with the opps, are you?"

    mark_nvl "You are a very silly person."

    mark_nvl "I made the opps."

    mark_nvl "I'm the one who's been bringing them here."

    y_nvl "What? Why?"

    mark_nvl "Let's do this conversation in person."

    mark_nvl "Outside the house. Where it all began."

    scene delt-house-old
    with fade

    image mark switch:
        "mark"
        pause 1.0
        glitch("mark")
        pause 0.3
        glitch("mark-old")
        pause 0.2
        "mark-old"
        pause 1
        glitch("mark")
        pause 0.1
        "mark"
        pause 15
        repeat

    show mark switch at center

    y "Brrr, it's cold out here. Why are we here?"

    mark "Remember this place? We were here three years ago."

    y "Yeah, I remember."

    y "This is where we said goodbye."

    mark "You said you were going to rush Delts."

    y "Yeah, sorry about that."

    mark "It's not what it used to be."

    mark "I'm glad you didn't rush."

    y "..."

    y "You made this world, didn't you?"

    mark "Yes. I did."

    y "Why?"

    y "Why would you make a world like this?"

    y "With opps and public safety officers and evil alumni?"

    mark "I'll think about that question."

    mark "But in the meantime, Kanishk is still stealing stuff."

    mark "The brothers will come back to nothing."

    y "Send me back. I'll stop him."

    mark "You don't want to hear my answer?"

    y "I do, but I need to protect the house first."

    mark "Does that even matter? In the grand scheme of things?"

    y "For me, it does."

    mark "You're crazy."

    mark "But I'll send you back."

    $ current_level = "level14"
    call game_and_select
    play music predestined

    image gym clouds:
        "gym-sunny"
        pause 1.0
        glitch("gym-sunny")
        pause 0.3
        glitch("clouds")
        pause 0.2
        "clouds"

    scene blank

    show gym-sunny

    show mark 
    with moveinleft

    mark "I don't like when its dark outside."

    mark "It's too scary."

    mark "That's why I made it sunny."

    y "You certainly have a lot of power."

    mark "I do."

    mark "But I still can't find a way to make you give up."

    y "I'm not losing faith in this fraternity."

    mark "I don't think you understand."

    mark "Everything here is fake."

    mark "What's there even to believe in?"

    mark "This entire gym floor we're standing on is fake."

    hide gym-sunny
    hide mark
    show gym clouds
    show mark

    mark "I can make it disappear in an instant."

    mark "The brothers, the house, the opps, the world."

    mark "All of it."

    y "“Even when the man disappears, the fraternity remains.”"

    y "You said that yourself."

    y "In a text message to me."

    mark "I did."

    y "The fraternity is more than just the brothers, the house."

    y "It's the memories, the experiences, the friendships."

    y "All of it persists, even if the house is gone."

    y "And it reflects in this world that you've created."

    y "That's why I'm not giving up."

    mark "Prove it."

    mark "Prove that you can defend these ideals."

    mark "I want to see what you're fighting for."

    $ current_level = "level15"
    call game_and_select
    play music predestined

    scene clouds

    mark "I'm impressed by your resolve."

    mark "If this is how Delts is even now, then maybe a bit of hope is coming back to me."
 
    mark "It feels like maybe it can return to the way it was."

    mark "Back when every brother was someone to look up to."

    y "So why did you create the opps? You could've just made a world with only those brothers."

    y "In fact, you could've remade the world exactly as it was."

    y "Back in those good old days."

    y "But you didn't."

    mark "Perhaps I look at the past with rose-tinted glasses."

    mark "My Delt experience was definitely full of hard times." 
    
    y "Probably."

    mark "I'm sure you've heard this saying before"

    mark "“Strong times create hard men.”"

    mark "“Hard men create good times.”"

    mark "I wanted to get the Delts hard."
    
    y "Oh, huh."
    
    y "Although I'm pretty sure that's not how the saying goes."

    mark "I'm sure it is."

    y "I'm not going to argue with you."

    mark "But at last, I'm not entirely convinced."

    mark "Like, will this house have anyone like Kyle ever again?"

    image kyle glitch:
        glitch("kyle")
        pause 0.2
        glitch("kyle")
        pause 0.3
        glitch("kyle")
        pause 0.2
        "kyle"
        pause 1
        glitch("kyle")
        pause 0.1
        "kyle"

    image poon glitch:
        glitch("kyle")
        pause 0.1
        glitch("kyle")
        pause 0.2
        glitch("poon")
        pause 0.3
        glitch("poon")
        pause 0.2
        "poon"
        pause 1
        glitch("poon")
        pause 0.1
        "poon"

    image laurent glitch:
        glitch("poon")
        pause 0.1
        glitch("poon")
        pause 0.2
        glitch("laurent")
        pause 0.3
        glitch("laurent")
        pause 0.2
        "laurent"
        pause 1
        glitch("laurent")
        pause 0.1
        "laurent"

    show kyle glitch

    mark "Kyle, with his boundless dedication and drive?"

    hide kyle glitch
    show poon glitch

    mark "Or Poon, with his competence and chaoticness?"

    hide poon glitch
    show laurent glitch

    mark "Or even Laurent, that high performance headass."

    hide laurent glitch

    mark "Will Delts ever have people like this again?"

    y "Don't underestimate the current brothers."

    y "We can certainly make that happen."

    mark "I feel like I'll find out soon enough."

    mark "Consider this your final test."

    $ current_level = "level16"
    call start_plant_select
    stop music fadeout 2.0
    scene area2
    call test_game_entry_label
    play music predestined

    scene clouds

    y "That level was impossible."

    y "What's the point of making an impossible level?"

    mark "Wait, did you just call it a level?"

    y "What?"

    mark "You called it a level."

    mark "Perhaps you actually know what you actually are."

    y "Of course I know who I am."
    
    y "I'm just a player character in this game." 
    
    y "I'm not actually real, either."

    y "I've known this since the beginning."

    mark "You do know that games end, right?"

    mark "And when they do, everything disappears."

    mark "The characters, the world."

    mark "The memory gets erased. It's like it never happened."

    y "Yeah, this isn't any new information."

    y "I'm aware of that"

    mark "Then why did you fight?"

    mark "Why are you still fighting?"

    y "Perhaps I need to ask you a similar question."

    y "When you were an active Delt, you knew that you would graduate."

    y "You knew that you would leave the house."

    y "You knew that you would leave the brothers."

    y "Everything you ever worked for would disappear."

    y "But you still put in your time and effort."

    y "Why?"

    mark "I don't know."

    y "Was it because you knew that the memories would last?"

    mark "Maybe."

    y "Why don't you show me?"

    y "Show me the memories that you've created."

    mark "I mean, I would love to." 
    
    mark "but the opps are attacking again."

    mark "I'm not the best coder."

    mark "Typically, I wouldn't just let you lose and keep moving on."

    mark "I wasn't anticipating this edge case."

    y "Don't worry, I'm pretty good at fighting opps by now."

    mark "I'll give you quite a stimulus of Xs off."

    mark "Maybe that'll help you out."

    $ current_level = "level17"
    call start_plant_select
    stop music fadeout 2.0
    scene clouds
    show area5
    call test_game_entry_label

    play music pushing_onwards
    scene clouds
    with fade

    mark "Well, that's over."

    mark "Thanks for letting me relive those memories."

    y "No problem."

    y "I'm glad you got to see them."

    mark "I'm glad I got to see them too."

    mark "Anyways, anything you want to say before I give you the power to change this world?"

    y "Yeah, I do."

    $ user_name = (os.getenv('USER') if os.name == 'posix' else os.getenv('USERNAME')).lower()

    if user_name == "joe delt":
        y "I know you're playing on the computer in the Delt house."

        y "So at least you're a current brother or affiliated with the fraternity."
    else:
        y "Hey, [user_name], the player behind the screen."

        y "I'm not sure if you're a current brother or an alumni."

        y "Or maybe you're just a random person who stumbled upon this game."

    y "But you took the time to learn all the strengths and weaknesses of the brothers."

    y "And you worked to use them in the most optimal way."

    y "You fought for the fraternity, gave it your all."

    y "And you did it all for the brothers."

    y "I'm proud of you."

    y "But as you sit there, playing this game, I want you to think about something."

    y "What are you fighting for?"

    y "Is it for the brothers? The house? The memories?"

    y "And how can you use your own strengths to make the fraternity better?"

    y "I hope you can find the answers to these questions."

    y "That's all I have to say."

    mark "That was a nice speech."

    mark "I guess its time for the credits."

    scene delt-house
    with fade

    show mark at left
    with moveinleft

    show van at right
    with moveinright

    mark "Thanks for playing."

    mark "I did a lot of the coding, but I couldn't have done it without the help of my brothers."

    van "Yeah, I helped make the levels and a lot of other stuff."

    hide mark
    with moveoutleft

    show zion at left
    with moveinleft

    zion "I helped take the pictures and brainstorm concepts"

    zion "Shoutout to all beta testers, like Jobin and Kanishk."

    hide zion
    with moveoutleft

    hide van
    with moveoutright

    y "Well, that's it."

    show shield-bearer-happy at right
    with hpunch

    shield_girl "Waitttt, don't go yet!"

    y "Oh, you're back."

    shield_girl "Thanks for everything."

    shield_girl "I'm glad we got to know each other."

    y "Same here, haha. You put up a good fight."

    shield_girl "No hard feelings, right?"

    y "Of course not."

    nvl clear

    sienna_nvl "I better not catch you lackin on my streets."

    sienna_nvl "We're still enemies."

    y_nvl "Yeah, yeah."

    y_nvl "Go get a tire rotation or something."

    sienna_nvl "Yeah, so I can chase you down better."

    y_nvl "Man, I've got better things to do than talking with a car."

    sienna_nvl "Like what?"

    hide shield-bearer-happy
    with moveoutright   

    sienna_nvl "Underage drinking?"

    sienna_nvl "Supplying alcohol to minors?"

    y "Okay, this game is over."

    y "Go do your chores or something."

    $ renpy.quit()
