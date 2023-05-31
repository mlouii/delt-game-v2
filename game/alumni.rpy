

label alumni:
    # play music predestined

    # image neil dance:
    #     "neil-crazy"
    #     pause 0.1
    #     "neil-crazy-2"
    #     pause 0.1
    #     repeat

    # scene tanjy-stair
    # with fade

    # show neil-crazy

    # neil "Watch where you're going."

    # neil "Can't you see I'm already on the stairs?"

    # y "Sorry."

    # y "Wait, you're Neil? The dancer from 3 years ago?"

    # y "You look a lot different."

    # neil "Yeah, it's called progress. Of course I look different."

    # neil "I'm better than I was before."

    # y "Can you show me some of your moves?"

    # hide neil-crazy
    # show neil-crazy-2

    # neil "No. I've got bigger endeavors to pursue."

    # y "Pleaseee?"

    # neil "..."

    # hide neil-crazy-2
    # show neil dance

    # neil "Tell me when you want me to stop."

    # y "Wow, that was amazing."

    # hide neil dance
    # show neil-crazy

    # y "As good as I remember."

    # neil "I'm glad you enjoyed it."

    # y "Wait, so what are your bigger endeavors?"

    # neil "I'm the Founder of Kinetic Footwear."

    # y "That's the shoes ... that the oppa sigs wear?"

    # neil "Yes. I'm the one who made them."

    # y "Why would you give them to the oppa sigs?"

    # neil "Kinetic footwear shoes are only useful for those who keep moving forward."

    # neil "Not those who only take steps backwards."

    # y "So you're saying oppa sigs are better than us?"

    # neil "In its current state, yes."

    # y "What do you mean?"

    # neil "I mean, what have you guys even accomplished?"

    # neil "I'm a billionaire founder of a shoe company."

    # neil "Kids as young as 7 years old are working in my factories."

    # neil "They are able to support their families because of me."

    # neil "I'm making a difference in the world."

    # neil "What are you doing?"

    # y "I'm ... I'm ..."

    # neil "Still trying to rush a fraternity?"

    # neil "Protecting a house that's already dead?"

    # neil "Members with no future?"

    # y "Don't say that."

    # y "We're going to make it better. You'll see."

    # neil "You're a great guy, but you're delusional."

    # neil "This is Delts. Everything good in here goes to $hit."

    # neil "Focus on yourself. Not this house."

    # neil "I'm distributing Kinetic Footwear to all of its fans."

    # neil "As first important IIT graduate since the inventor of the mobile phone."

    # hide neil-crazy

    # y "I can't believe that Neil would say that."

    # y "He's an alumni. He should be supporting us."

    # y "I hear sounds coming from downstairs. I'll check it out."

    # scene crazy
    # with fade

    # show kanishk at left
    # with moveinleft

    # kanishk "None of these people deserve these things."

    # y "What do you mean?"

    # kanishk "Like this TV. It's a 4K TV."

    # kanishk "They don't need something this nice."

    # kanishk "How about they pick up a book and read it instead?"

    # kanishk "Or maybe even apply for a job."

    # y "But you can't just take it. It's not yours."

    # kanishk "I'm not taking it. I'm just moving it to my apartment."

    # kanishk "I'll bring it back when they're ready for it."

    # kanishk "Basically, I'm doing them a favor."

    # y "I don't think that's how it works."

    # kanishk "Well that's how it works for me."

    # y "Have I seen you before?"

    # kanishk "I'm Mark's roommate."

    # y "And he's okay with you stealing other people's stuff?"

    # kanishk "I'm not stealing. I'm just borrowing."

    # kanishk "Stop using such harsh words. It's not nice."

    # y "What if the brothers come down and see you?"

    # kanishk "They won't. The opps are coming again."

    # kanishk "They're going to be too busy to notice."

    # kanishk "And I'll slip away with all of their stuff."

    # y "You're not going to get away with this."

    # y "I'm telling Mark about this."

    # kanishk "Go ahead."

    # y_nvl "Hey Mark, your roommate is stealing stuff from the house."

    # mark_nvl "Okay? So what do you want me to do about it?"

    # y_nvl "I don't know. Stop him?"

    # mark_nvl "He has his own free will."

    # mark_nvl "I'm not gonna control what he does."

    # y_nvl "But he's stealing from the house."

    # mark_nvl "And you have your own free will."

    # mark_nvl "Stop him yourself."

    # "A voice is heard from upstairs."

    # "THE OPPS ARE COMING AGAIN!!"

    # "EVERYONE GET READY!!"

    # kanishk "See, I told you. I'm going to get away with this."

    # kanishk "I'll be back for more."

    # $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "jacob", "pranav", "colin", "logan", "cobcannon", "andrew"]
    # $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer", "kinetic", "officer", "van", "mask_shield_bearer", "neil", "kanishk"]
    # $ current_level = "level13"
    # call game_and_select
    # play music predestined

    # scene hallway
    # with fade

    # y "Hmm, where did everyone go?"

    # y "And why isn't Mark doing anything?"

    # y "He did say a lot of bad things about this fraternity earlier."

    # y "I should talk to him."

    # y_nvl "Hey Mark, what's going on?"

    # y_nvl "Why do the opps keep coming?"

    # y_nvl "This isn't normal."

    # y_nvl "And why aren't you doing anything?"

    # mark_nvl "You sound tired."

    # mark_nvl "Why don't you go to sleep?"

    # y_nvl "I'm not tired."

    # y_nvl "I'm just worried about the house."

    # mark_nvl "Don't worry about it."

    # y_nvl "You're not working with the opps, are you?"

    # mark_nvl "You are a very silly person."

    # mark_nvl "I made the opps."

    # mark_nvl "I'm the one who's been bringing them here."

    # y_nvl "What? Why?"

    # mark_nvl "Let's do this conversation in person."

    # mark_nvl "Outside the house. Where it all began."

    # scene delt-house-old
    # with fade

    # image mark switch:
    #     "mark"
    #     pause 1.0
    #     glitch("mark")
    #     pause 0.3
    #     glitch("mark-old")
    #     pause 0.2
    #     "mark-old"
    #     pause 1
    #     glitch("mark")
    #     pause 0.1
    #     "mark"
    #     pause 15
    #     repeat

    # show mark switch at center

    # y "Brrr, it's cold out here. Why are we here?"

    # mark "Remember this place? We were here three years ago."

    # y "Yeah, I remember."

    # y "This is where we said goodbye."

    # mark "You said you were going to rush Delts."

    # y "Yeah, sorry about that."

    # mark "It's not what it used to be."

    # mark "I'm glad you didn't rush."

    # y "..."

    # y "You made this world, didn't you?"

    # mark "Yes. I did."

    # y "Why?"

    # y "Why would you make a world like this?"

    # y "With opps and public safety officers and evil alumni?"

    # mark "I'll think about that question."

    # mark "But in the meantime, Kanishk is still stealing stuff."

    # mark "The brothers will come back to nothing."

    # y "Send me back. I'll stop him."

    # mark "You don't want to hear my answer?"

    # y "I do, but I need to protect the house first."

    # mark "Does that even matter? In the grand scheme of things?"

    # y "For me, it does."

    # mark "You're crazy."

    # mark "But I'll send you back."

    # $ current_level = "level14"
    # call game_and_select
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

    y "That's all persists, even if the house is gone."

    y "And all of it reflects in this world that you've created."

    y "That's why I'm not giving up."

    mark "Prove it."

    mark "Prove that you can defend these ideals."

    mark "I want to see what you're fighting for."

    # $ current_level = "level15"
    # call game_and_select
    # play music predestined

    scene clouds

    show mark

    mark "I'm impressed."

    mark "But I'm not convinced yet."

    mark "Defend your ideals again. If you can, I'll give you the power to change this world."

    mark "If you can't, I'll destroy it."

    # $ current_level = "level16"
    # call game_and_select
    # play music predestined

    scene clouds

    y "That level was impossible."

    y "I can't do this anymore."

    mark "Wait, why did you call it a level?"

    y "What?"

    mark "You called it a level."

    mark "Perhaps you actually know what you actually are."

    y "Of course I know who I am. I'm a player character in this game."

    y "I've known this since the beginning."

    mark "You do know that games end, right?"

    mark "And when they do, everything disappears."

    mark "The characters, the world."

    mark "The memory gets erased. It's like it never happened."

    y "Yeah, this isn't any new information."

    y "I'm aware of that"

    mark "Then why are you still fighting?"

    y "Perhaps I need to ask you a similar question."

    y "When you were a Delt, you knew that you would graduate."

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

    if is_testing:
        scene clouds
        show area5
        $ current_level = "level90"
        $ chosen_plants = ["peashooter", "sunflower", "wallnut", "repeater", "cobcannon"]
        call test_game_entry_label from _call_test_game_entry_label_1

    # $ current_level = "level17"
    # call game_and_select
    # play music predestined

    play music pushing_onwards
    scene clouds
    with fade

    mark "Well, that's over."

    mark "Thanks for letting me relive those memories."

    y "No problem."

    y "I'm glad you got to see them."

    mark "I'm glad I got to see them too."

    mark "Anything you want to say before I give you the power to change this world?"

    y "Yeah, I do."

    $ user_name = (os.getenv('USER') if os.name == 'posix' else os.getenv('USERNAME')).lower()

    if user_name == "joe delt":
        y "I know you're playing on the computer in the Delt house."

        y "So at least you're a current brother or affiliated with the fraternity."
    else:
        y "Hey, [user_name]."

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

    zion "I helped take the pictures and early concepts."

    zion "Shoutout to all beta testers, like Jobin and Kanishk."

    hide zion
    with moveoutleft

    hide van
    with moveoutright

    y "Well, that's it."

    y "Go do your chores or something."

    $ renpy.quit()
