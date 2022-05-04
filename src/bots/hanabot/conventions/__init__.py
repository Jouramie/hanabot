from bots.hanabot.conventions.basic.five_save import FiveSave
from bots.hanabot.conventions.basic.prompt import Prompt
from bots.hanabot.conventions.basic.single_card_play_clue import SingleCardPlayClueConvention
from bots.hanabot.conventions.convention import Conventions

basic = Conventions(
    [
        Prompt(),
        SingleCardPlayClueConvention(),
    ],
    [
        FiveSave(),
    ],
)
