from bots.hanabot.conventions.basic.five_save import FiveSave
from bots.hanabot.conventions.basic.play_clue import PlayClue
from bots.hanabot.conventions.basic.prompt import Prompt
from bots.hanabot.conventions.convention import ConventionDocument

level_one = ConventionDocument(
    [
        Prompt(),
        PlayClue(),
    ],
    [
        FiveSave(),
    ],
)
