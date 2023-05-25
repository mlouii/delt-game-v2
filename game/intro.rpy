label intro:

  play music pushing_onwards

  # go up to the house and reminisce

  $ playerName = "You"
  $ y = Character(playerName, color="#376e3a")
  $ MCName = playerName
  $ y_nvl = Character(playerName, kind=nvl, image="nighten", callback=Phone_SendSound)

  # scene dining-sunny
  # with fade

  # y "It's been a while since I was last here... it looks familiar but a little different"

  # y "I remember how everyone came and talked to me... they were so nice."

  # y "Maybe I should walk around and find someone. Will anyone even remember who I am?"

  # y "Probably not... I've been gone for so long."

  # y "I guess I should go and find someone to talk to. Let's see whats behind me."

  # scene mail-room
  # with fade

  # y "So this is where the brothers get their packages and stuff... "
  
  # y "I don't want to snoop around too much. Might look like im stealing stuff."

  # y "But its funny, how they call this the “Male Room”."
  
  # y  "Isn't this a fraternity? I guess it makes sense."

  # y "I think I hear someone talking... what are they saying?"

  # y "They're saying that ... their “Huge Package”... “Came”... in the “Male”??"

  # y "I don't know what they're talking about, but it sounds like they're having fun."

  # y "I don't want to interrupt them, so I'll just leave them alone."

  # scene living-room-sunny
  # with fade

  # y "This is the living room. It's definitely changed a lot since I was last here."

  # y "It was a lot busier back then, but now it's just... empty."
  
  # y  "Then again, it was rush week when I was here."

  # y "Perhaps the old man is still here." 
  
  # y "I don't really want to check though, he's probably still mad at me."

  # y "I'll just leave him alone."

  # y "Lets see whats in the library."

  # scene library
  # with fade

  # y "This is the library. It's a bit messier than I remember."

  # y "Although I mostly just remember talking to the chapter president that time."
  
  # y "I remember the calves, I don't actually remember his name or face."

  # y "Why was I even looking at his calves? I don't know. They were just there."

  # y "What's written on the whiteboard? It looks interesting, maybe I should take a look."

  # scene whiteboard
  # with zoomin

  # y "This wasn't quite what I was expecting. It looked a bit different from far away."

  # y "Maybe its a free body diagram? I don't know, I cheated on all my physics tests."
  
  # y "That was back during covid."

  # y "If it wasn't for covid, I would've been able to stay here. I wouldn't have had to leave."

  # y "I wonder what would've happened if I stayed. Would I have been a good brother?"

  # y "I don't know. But that's the past."

  # y "Moving onwards, we strive for a life of excellence."

  # y "I want to make this fraternity a shining beacon on this campus."

  # scene library
  # with zoominout

  # y "I should probably leave before someone sees me."

  # show mark at right
  # with vpunch

  # mark "Who the hell are you? Snooping around, muttering to yourself."

  # mark "Messing up my peace and quiet. I was in my zone."

  # y "Wait, where did you come from? I didn't see you here."

  # # change to use curse words later on
  # mark "I was $hitting in ladies head. You know, the bathroom here."

  # mark "Where I $hit."

  # y "But I didn't even hear any noise coming from there!"

  # mark "What do you want me to do?" 
  
  # mark "Start moaning?"
  
  # mark "I can do that if you want." 

  # y "No, I mean, I didn't hear a flush"

  # mark "I don't flush. Save water. Save the planet."

  # mark "Let's move somewhere else. Stank up the place."

  # scene kitchen-sunny
  # with fade

  # show mark at right
  # with moveinright

  # mark "So, who are you? You were talking about how you wanted to make this place better."

  # mark "You want to rush, don't you? Introduce yourself."

  # $ playerName = renpy.input("Enter a name if you want")
  # $ playerName = playerName.strip()
  # $ y = Character(playerName, color="#376e3a")
  # $ MCName = playerName

  # while not playerName:
  #   mark "Ain't gonna continue until you tell me your name."
  #   $ playerName = renpy.input("Enter a name if you want")
  #   $ playerName = playerName.strip()
  #   $ MCName = playerName
  #   $ y = Character(playerName, color="#376e3a")

  # y "I'm [playerName]. I was at a rush event three years ago."

  # mark "Oh, I think I remember you. You said you were going to rush, but you never did."

  # mark "We spent so much time talking to you"

  # mark "I spent so much time writing the script"

  # y "I'm sorry, but virtual delts wasn't a thing. I couldn't rush."

  # mark "Okay, now let's get down to business."

  # mark "I'm going to ask you a question, and you're going to answer it."

  # y "Uhhhh- My GPA is 3.5, I'm a junior."

  # mark "Wow, you prepared for this. I'm impressed."

  # mark "But that's not even that good. I'm sigma cum loud. That's not even a 4.0"

  # y "I guess I'm not that good. I'm sorry."

  # mark "No, its actually way better than I expected. I thought you were going to say 2.5."

  # mark "Like all the others..."

  # mark "You know, I'm starting to lose faith in this fraternity."

  # mark "Like, look at this kitchen. It's a mess."

  # mark "And it's not even my mess this time."

  # y "I'm sorry, maybe if I rushed back then, I could've helped."

  # y "Is there any way I can help turn this fraternity around?"

  # mark "It's up to you. I don't really care. I'm just here to steal food."

  # mark "Maybe talk to other people. I'm sure they'll be more fun than me."

  # show shahaan at left
  # with moveinleft

  # shahaan "Hey, I'm Shahaan. You must be the new guy."

  # shahaan "Anyways, Mark, I'm heading out to get some alcohol"

  # shahaan "Can you make sure nothing happens while I'm gone?"

  # mark "What about the house manager? Isn't he supposed to do that?"

  # shahaan "Oh, Talha?" 
  
  # shahaan "He's..."

  # shahaan "no longer with us..."

  # mark "What do you mean? Did we kick him out?"

  # shahaan "His side project had some ... complications."

  # mark "Huh, so that's why the house is so dirty."

  # shahaan "Uh... yeah!"
  
  # shahaan "I guess."
  
  # shahaan "Anyways, I'm heading out."

  # shahaan "And put a shirt on, Mark. You're scaring the new guy."

  # shahaan "It's against the bylaws. You know that."

  # mark "Oh hell no."

  # shahaan "Well, I'm out. See you guys later."

  # hide shahaan
  # with moveoutleft

  # mark "I hate the bylaws. I'm leaving too."

  # mark "I'm going to go back to the bathroom."

  # mark "Don't follow me. Don't bother me under any circumstances."

  # mark "I need to finish what I started."

  # hide mark
  # with moveoutright

  # y "Well, that was interesting."

  # play sound doorbell

  # y "Oh, someone's at the front door."

  # y "I should let them in."

  # scene front-door
  # with fade

  # show berto
  # with moveinright

  # berto "Thanks for letting me in."

  # berto "Some people robbed me and took my keys."

  # berto "They beat my a$$."

  # berto "HARD."

  # berto "Although I kinda liked it."

  # scene dining-sunny
  # with fade

  # show berto at right
  # with moveinright

  # y "Wait where was that?"

  # berto "I was coming home from a White Sox game. We lost. IM MAD!!"

  # berto "Then the opps came out of nowhere."

  # berto "They done stripped me naked"

  # berto "Finessed my jersey, took my keys and my phone"

  # berto "And then they beat my a$$."

  # berto "I'm mostly mad about the game."

  # y "I'm sorry to hear that."

  # y "Would you like to go to the IIT Student Health and Wellness Center?"

  # berto "No. I want to fight some opps."

  # play sound egg

  # berto "..."

  # berto "Someone threw eggs at our house!"

  # play sound doorbell

  # y "Huh, someone's at the front door again"

  # berto "I'm going to go get them."

  # y "I'll come with you."

  # scene front-door
  # with fade

  # play music death

  # show oppasig
  # with hpunch

  # oppasig "DELTA TAU DELTA WE ARE PISSING ON YOUR WALL"

  # oppasig "WE ARE DRY HUMPING YOUR WALL"

  # oppasig "WE ARE LACTATING ON YOUR WALL"

  # oppasig "COME OUT AND WE'LL CREAMPIE YOU"

  # oppasig "WE ARE THE OPPA SIGS"

  # berto "Shut the f*ck up, dumba$$."

  # y "Why are you wearing a crop top?"

  # oppasig "Freshmen LOVE my ABS."

  # oppasig "I'm ALPHA SIGMA PHI, and I LOVE FRESHMEN"

  # oppasig "I'm going to beat your a$$."

  # oppasig "Just like how we beat your friend's a$$."

  # oppasig "See you around, DELT."

  # hide oppasig

  # stop music fadeout 4.0
  # play music pushing_onwards

  scene mail-room
  with fade

  show berto
  with zoomin

  berto "They are so annoying."

  berto "They don't know I've been practicing my fastpitch."

  y "Wait, I just got a notification on my phone."

  berto "Me too. Let me check my phone."

  nvl_narrator "Mark has changed the background picture"

  mark_nvl "Hey, have you seen Berto?"

  mark_nvl "He isn't answering"

  mark_nvl "Im still $hitting, btw"

  y_nvl "He's right here"

  y_nvl "He got robbed and beaten up"

  mark_nvl "Anyways, have you seen this guy?"

  mark_nvl "{image=../minigame/images/zombies/basic/basic.png}"

  mark_nvl "sorry for android"

  y_nvl "Yeah, I just saw him"

  y_nvl "He just threw an egg at us"

  mark_nvl "The opps are out here"

  mark_nvl "Preparing for an all out assault"

  y_nvl "What do you mean?"

  mark_nvl "It's up to you to stop them"

  mark_nvl "Get the brothers to help you"

  mark_nvl "I've got bigger things to worry about"

  mark_nvl "Good luck"

  y "The opps are coming."

  y "Are you listening?"

  berto "Bro... I'm done checking my phone..."
  
  berto "I just got 10,000 Xs today."

  berto "I already owe the house 2.3 Million dollars."

  berto "Ever since Talha became house manager, I've had to sell everything I own."

  berto "I'm going to have to sell my body soon."

  berto "Its gotten worse, as now he's uploaded his consciousness to the house."

  berto "The Talha-bot 9000 ... I need to pray for Xs off. Negative Xs."

  y "Maybe helping defend the house will help you get some Xs off."

  berto "I hope so."

  y "The massive assault is coming. Will you help me?"

  berto "Of course."

  berto "The opps are going to pay."

  y "Let's go."

  mark_nvl "Hey, by the way, theres something special coming up"

  mark_nvl "You won't be able to save, load, or go back"

  mark_nvl "Also, don't resize the window, or try to exit out"

  mark_nvl "It'll restart the current game"

  mark_nvl "Just a heads up"

  mark_nvl "Good luck"

  $ plants = ["peashooter", "sunflower"]
  $ seen_zombies = ["basic"]
  $ current_level = "level1"
  call game_and_select

  scene mail-room

  show berto
  with zoomin

  berto "That was fun."

  return











































