label ask_difficulty:

  "Before we begin, how hard you want this to be?"

  menu: 
    "{b}Easy:{/b} Choose this if you just want to play for the plot and storyline":
      $ difficulty_multiplier = 0.7

    "{b}Normal:{/b} A balanced experience between gameplay and storyline":
      $ difficulty_multiplier = 1.0

    "{b}Hard:{/b} For those who want a bit more of a challenge":
      $ difficulty_multiplier = 1.3

    "{b}Extreme:{/b} I don't think you can handle this":
      $ difficulty_multiplier = 1.75

  $ current_difficulty = difficulty_multiplier

  return
