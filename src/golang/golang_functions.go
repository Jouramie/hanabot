package main

import (
   "C"
   "log"
   "math/rand"
)

//export helloWorld
func helloWorld(){
   log.Println("Hello World")
}

//export SetSeedInt
func SetSeedInt(seed int) {
	rand.Seed(seed)
}

//export GetRandomInt
func GetRandomInt(max int) {
	return rand.Intn(max)
}

func main(){

}

func (g *Game) InitDeck() {
	// Local variables
	variant := variants[g.Options.VariantName]

	// If a custom deck was provided along with the game options,
	// then we can simply add every card to the deck as specified
	if g.ExtraOptions.CustomDeck != nil &&
		len(g.ExtraOptions.CustomDeck) != 0 &&
		g.ExtraOptions.CustomSeed == "" { // Custom seeds override custom decks

		for _, card := range g.ExtraOptions.CustomDeck {
			g.Deck = append(g.Deck, NewCard(card.SuitIndex, card.Rank))
			g.CardIdentities = append(g.CardIdentities, &CardIdentity{
				SuitIndex: card.SuitIndex,
				Rank:      card.Rank,
			})
		}
		return
	}

	// Suits are represented as a slice of integers from 0 to the number of suits - 1
	// (e.g. [0, 1, 2, 3, 4] for a "No Variant" game)
	for suitIndex, suit := range variant.Suits {
		// Ranks are represented as a slice of integers
		// (e.g. [1, 2, 3, 4, 5] for a "No Variant" game)
		for _, rank := range variant.Ranks {
			amountToAdd := numCopiesOfCard(suit, rank, variant)

			for i := 0; i < amountToAdd; i++ {
				// Add the card to the deck
				g.Deck = append(g.Deck, NewCard(suitIndex, rank))
				g.CardIdentities = append(g.CardIdentities, &CardIdentity{
					SuitIndex: suitIndex,
					Rank:      rank,
				})
			}
		}
	}
}

// setSeed seeds the random number generator with a string
// Golang's "rand.Seed()" function takes an int64, so we need to convert a string to an int64
// We use the CRC64 hash function to do this
// Also note that seeding with negative numbers will not work
func setSeed(seed string) {
	// Remove the "legacy-x-" prefix from the seed, if it exists
	// (e.g. "legacy-1-", "legacy-2-", and so on)
	if strings.HasPrefix(seed, "legacy-") {
		seed = seed[len("legacy-x-"):]
	}
	crc64Table := crc64.MakeTable(crc64.ECMA)
	intSeed := crc64.Checksum([]byte(seed), crc64Table)
	SetSeedInt(int64(intSeed))
}

func (g *Game) ShuffleDeck() {
	// From: https://stackoverflow.com/questions/12264789/shuffle-array-in-go
	for i := range g.Deck {
		j := GetRandomInt(i + 1) // nolint: gosec
		g.Deck[i], g.Deck[j] = g.Deck[j], g.Deck[i]
		g.CardIdentities[i], g.CardIdentities[j] = g.CardIdentities[j], g.CardIdentities[i]
	}
}