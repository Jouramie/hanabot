from bots.hanabot.conventions.basic.single_card_play_clue import SingleCardRankPlayClueConvention, SingleCardSuitPlayClueConvention
from bots.hanabot.conventions.convention import Conventions

basic = Conventions(
    {
        SingleCardSuitPlayClueConvention(),
        SingleCardRankPlayClueConvention(),
    }
)
