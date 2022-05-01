# Conventions
- Return a list of all possible interpretations 
- Store interpretations in blackboard
- Chop and finesse slots conventions runs first, stored result in blackboard to be used by others
- Some conventions depend on each other, probably should be run in a decision tree or something (layered finesse depends on finesse and bluff)
  - Conventions register their dependencies and as dependencies of each other 
  
# Interpretation
- Each turn, look back at the interpretations and filter them
  - Filtering could be cased on fix clues or cards that played between the turns
- Contradictions need to fork interpretations
  - For instance, if playing in a finesse does not result in playing the expected card, fork into layered finesse or bluff
  - Some interpretations take priority over others, finesse takes priority over simple play clue. If the player do not play, fork into ambiguous or simple play clue. 
  - A convention can register as a leaf or a root of another convention. When looking for an interpretation, try all roots, then iterate through the links until no leaf left.
  - If no leaf is found, log and assume error.

# Clue
- Store clues in blackboard
- Clues need to be resolved once it reached a leaf in the interpretation tree
