from bots.hanabot.conventions.basic.five_save import FiveSave
from bots.hanabot.conventions.basic.prompt import Prompt
from bots.hanabot.conventions.basic.single_card_play_clue import SingleCardPlayClue
from bots.hanabot.conventions.convention import ConventionDocument

basic = ConventionDocument(
    [
        Prompt(),
        SingleCardPlayClue(),
    ],
    [
        FiveSave(),
    ],
)
