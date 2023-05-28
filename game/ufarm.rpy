
label ufarm:

  # scene penthouse

  # y "That was such a great nap."

  # y "I feel so refreshed."

  # nvl_narrator "Shahaan has been added to the chat"

  # shahaan_nvl "Hey you should pull up"

  # shahaan_nvl "You want to smoke?"

  # y_nvl "I don't want smoke with nobody"

  # y_nvl "I have no enemies"

  # shahaan_nvl "Well, you should pull up anyways"

  # y_nvl "I'm on my way"

  # scene front-door-2
  # with fade

  # y "hmm, door is locked this time."

  # y "Is it usually locked? Maybe they need good security for this party."

  # y_nvl "Hey, I'm locked out. Can you let me in?"

  # shahaan_nvl "Brayden will come get you"

  # nvl clear

  # scene front-door-3
  # with fade


  # show brayden
  # with moveinleft

  # brayden "Hey, you're here!"

  # y "Damn, you've got some good style."

  # brayden "Thanks, it comes naturally."

  # brayden "You look good too."

  # y "Thanks, I try."

  # brayden "You here for the party?"

  # y "Yeah! Is it happening right now?"

  # brayden "Not yet, we've got to do something else first."

  # y "What's that?"

  # brayden "Smoke."

  # y "Oh, I don't smoke."

  # "A voice calls out to Brayden from inside the house."

  # brayden "They want me to investigate the u-farm. For opps."

  # brayden "You want to come?"

  # y "Sure, I'm down."

  # y "I've done some gardening before. I grew an onion once."

  # scene ufarm-table-sunset
  # with fade

  # show brayden at left
  # with moveinleft

  # y "So when do we start cultivating?"

  # play sound smoker_planted

  # hide brayden
  # show brayden-boof at left

  # brayden "I know you don't smoke, but take a moment to appreciate this."

  # brayden "Aint this the nicest boof you've ever seen?"

  # brayden "The finest strain of indica, wrapped up flawlessly."

  # brayden "I'm gonna be so chill."

  # y "I'm not sure if I'm ready for this."

  # "Brayden takes a hit from the boof."

  # brayden "Oh my god, I'm so high."

  # brayden "I'm chill as heck right now."

  # hide brayden-boof
  # show brayden-chill at left

  # y "Wow."

  # y "You're so chill."

  # show oppasig at right
  # with moveinright

  # brayden "Hey, are you opps?"

  # oppasig "Yeah, I'm opp"

  # oppasig "Should have turned off your snap map"

  # oppasig "We gonna smoke you now"

  # mark_nvl "Hey, just a heads up"

  # mark_nvl "You're not in the house anymore, so there are less X off opportunities"

  # mark_nvl "Keep that in mind"

  # $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter"]
  # $ seen_zombies = ["basic", "dog", "conehead", "buckethead"]
  # $ current_level = "level5"
  # call game_and_select
  # play music pushing_onwards

  # show ufarm-back2-sunset
  # with fade

  # show brayden-chill at left
  # with moveinleft

  # brayden "Let's go back to the house."

  # brayden "We can tell the others that the u-farm is safe."

  # hide brayden-chill

  # y "Hmm, theres this random girl here."

  # y "I hope we arent causing her any trouble."

  # scene hallway
  # with fade

  # show luis at center
  
  # show pranav at right

  # "Some people are talking in the hallway."

  # show brayden at left
  # with moveinleft

  # brayden "Cleared out the u-farm."

  # brayden "No opps."

  # luis "Great, I've packed a boof."

  # luis "Let's smoke. In peace."

  # brayden "I already smoked, so I'll go play some genshin."

  # hide brayden
  # with moveoutleft

  # pranav "Gimme a second, I need to go to the bathroom."

  # pranav "Don't start without me."

  # hide pranav
  # with moveoutright

  # luis "Meet us there!"

  # scene ufarm-back-sunset
  # with fade

  # show luis at left
  # with moveinright

  # luis "Isn't the sunset beautiful?"

  # luis "I've always loved the way the sun looks when it's setting."

  # luis "It's like the sun is saying goodbye."

  # luis "But it's not sad."

  # luis "It's just a reminder that the sun will come back tomorrow."

  # luis "And it will be just as beautiful."

  # luis "Anyways, I'm Luis."

  # y "Hey, nice to meet you!"

  # luis "Just making sure, you're fine with me smoking right?"

  # y "Yeah, I'm fine with it."

  # y "What are you smoking?"

  # luis "Nothing too crazy. A small joint."

  # luis "I'm not trying to get too high."

  # hide luis

  # show luis-boof at left

  # luis "See, it's not too big."

  # "He takes a hit from the boof."

  # hide luis-boof

  # show luis-faded at left

  # luis "It's not too strong, but I'm kinda feeling it."

  # y "That absolutely reeks."

  # y "The smell is so strong, the entire u-farm stank."

  # y "I think Im getting high just from being around you."

  # luis "Actually, I'm feeling it too."

  # hide luis-faded

  # show luis-faded-2 at left

  # luis "I'm so faded."

  # y "We are absolutely so faded."

  # show shield-girl2 at right
  # with hpunch

  # hide luis-faded-2

  # show luis at left

  # arg "So I can't even enjoy a game of Hennessy pong in peace? Nasty smell."

  # y "Uh, what's that?"

  # arg "Hennessy X.O. It's cognac."

  # arg "Oh, you're probably too broke to know what that is."

  # arg "But anyways, It's beer pong, but better."

  # y "That sounds like a lot of alcohol."

  # arg "If you can't handle multiple cups of 40 percent ABV, you're actually a b1tch."

  # arg "So, are you going to stop that smoking?"

  # arg "Or should I throw a table at you?"

  # luis "Mann, I'm so faded."

  # luis "I can't even think straight."

  # luis "You want to take a hit, girl? This boof is straight gas."

  # arg "..."

  # hide luis
  # show luis-boof at left

  # luis "..."

  # arg "I hate people like you."

  # y "Yo, what do you mean by that?"

  # hide luis-boof
  # show luis at left

  # mark_nvl "That girl is with the opps."

  # mark_nvl "And she just said that to Luis."

  # mark_nvl "Definitely racially motivated."

  # y_nvl "She's just upset that Luis is smoking."

  # mark_nvl "Damn, you pussy?"

  # mark_nvl "I wouldn't let that slide, if I were you."

  # mark_nvl "You should probably do something."

  # arg_r "May God have mercy on my enemies, because I won't."

  # $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom"]
  # $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer"]
  # $ current_level = "level6"
  # call game_and_select
  # play music pushing_onwards

  # show ufarm-back2-sunset
  # with fade

  # "A voice comes from the distance. It's powerful."

  # "Is she giving you any trouble, Luis?"

  # show jacob at right
  # with hpunch

  # hide shield-girl2

  # show luis at left

  # luis "Jacob! You're back! You've been gone for so long."

  # jacob "Thanks, I'm out on parole."

  # jacob "It's crazy in there."

  # jacob "I became the most feared man in the prison."

  # jacob "Don't drop the soap around me, they said. One person didn't listen."

  # jacob "He said he wasn't scared of me."

  # jacob "But one day, the soap slipped out of his hands."

  # jacob "He bent down to pick it up."

  # y "Oh no."

  # jacob "And I bent down too."

  # jacob "And I picked it up for him."

  # jacob "'Here you go, buddy.', I said to him."

  # y "Wow, you're a really nice guy."

  # jacob "Then I hit him with a German suplex."

  # jacob "They extended my sentence for that."

  # y "Oh."

  # y "What did you do to get in there?"

  # jacob "Trespassing."

  # jacob "Sox Stadium. At night. Josh Silets brought me there. We got arrested together."

  # y "Oh, that's not too bad. Trepassing is a misdemeanor."

  # jacob "Josh Silets was such a good friend. The world will never be the same without him."

  # y "Wait, what happened to him?"

  # jacob "He got the death penalty."

  # y "What?!"

  # y "For trespassing?!"

  # jacob "Anish was his defense attorney. You probably wouldn't know him."

  # jacob "But he has a way with words."

  # jacob "The judge was so moved by Anish's speech, he started crying."

  # jacob "The more he spoke, the harsher the sentence got."

  # jacob "Somehow, it went from community service to the death penalty."

  # y "That's crazy."

  # jacob "But the feds had a hard time finding a way to kill him."

  # jacob "They tried everything."

  # jacob "Shooting him didn't work. He got a pump in at the gym before his execution so he was fine."

  # jacob "They tried to poison him, but he's taken so many drugs that he's immune to everything."

  # jacob "Injecting alcohol into his bloodstream didn't work either. ABV went up to 100 percent. He was fine."

  # y "So how did they kill him?"

  # jacob "They screenshotted his NFTs."

  # jacob "Then he exploded."

  # y "Oh."

  # jacob "Anyways, you got anyone I can wrestle?"

  # jacob "I've been itching for a fight."

  # y "That girl over there looks like she wants to fight."

  # y "Let's go."

  # $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "jacob"]
  # $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer"]
  # $ current_level = "level7"
  # call game_and_select
  # play music pushing_onwards

  scene ufarm-table-sunset
  with fade

  show shield-girl2 at right
  with fade

  shield_girl "Damn, yall got hands."

  shield_girl "But I swear, if I had a gas mask on, I would've won."

  shield_girl "I'm much stronger when I can actually breathe."

  show pranav at left
  with moveinleft

  pranav "Damn girl, you look super goooood."

  pranav "Wyd?"

  pranav "I got a lot of money."

  pranav "And a nicotine addiction."

  shield_girl "Wow thanks, you're super ugly."

  shield_girl "And I'm already rich."

  pranav "You should see me after a haircut. And a workout."

  pranav "Except I don't workout. At least not my body."

  pranav "I do lung workouts. I can smoke a pack in 10 minutes."

  pranav "I'm a beast."

  shield_girl "Yeah, I can tell."

  shield_girl "You stink. It physically hurts me to be around you."

  shield_girl "Once I get my gas mask, I'm killing you."

  hide shield-girl2
  with moveoutright

  y "Damn, she's mean."

  y "I don't know what's her problem."

  pranav "Yo, I think she's into me."

  pranav "Look at her eyes. She wants me. She's gonna be mine by the end of the night."

  pranav "Also, did you guys start smoking yet?"

  y "Uhh, yeah. We smoked all of it."

  show kinetic at right
  with moveinright

  leather "Hey, how do you like my fit?"

  y "It's pretty stylish."

  y "But why were you just pacing around? You were walking back and forth for like hours."

  leather "I was charging my phone for the first hour."

  leather "These shoes are Kinetic Footwear. They charge your phone when you walk."

  kinetic "Now my phone is at 185 percent."

  kinetic "All the leftover energy goes straight into your brain."

  kinetic "You know, if we had these shoes, we could've won tug of war. Thats the power of Kinetic Footwear."

  y "Wow, that's pretty cool. I want a pair."

  kinetic "You'll have to talk to the Founder."

  y "But, who are you anyways?"

  kinetic "I'm her boyfriend."

  kinetic "I'm also an oppa sig. Been living there for a while now."

  pranav "I'm gonna take your girl. Just watch."

  a_oppasig "I'm gonna take your life. I'm disintegrating you."

  a_oppasig "Wasn't planning to fight today, but I guess I have to."

  mark_nvl "You can't use all the brothers in one scene."

  mark_nvl "Unfortunately, you can only use seven at a time."

  mark_nvl "So, who do you want to use?"

  $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "jacob", "pranav"]
  $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer", "kinetic"]
  $ current_level = "level8"
  call game_and_select
  play music pushing_onwards








































  


























  



  






  




