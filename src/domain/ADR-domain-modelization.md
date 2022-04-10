Aggregates
====

Clue and Card are in separated aggregates. 

## Global
- Suit
- Rank


## Clue

A Clue is given by a Player (or PlayerPosition) to another with a Suit or a Rank on a HandPosition.
ClueInterpretation contains
- Focus

The ClueInterpreter has a set of convention
- Conventions can be swapped for different levels or variants
- DecisionTree or something


## Card

A Card has a Suit and a Rank. 

The Deck contains Cards (and possibly variant information)

DeckGenerated based on a seed.

## Player
A Player has a Hand.

A PlayerHand contains PlayerCards. 
- PlayerCards = knownCard or ProbableCards + drawnTurn

## Stack


## GameState
- Stacks
- Players
- turnNumber
- History? (List of turn)
- clueCount
- bombCount

A Turn contains turnNumber + PlayerPosition + Action

Actions are 
- ClueAction
- PlayAction
- DiscardAction 
