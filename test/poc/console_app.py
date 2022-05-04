from console import fg, fx, defx
from console.constants import ESC
from console.screen import Screen
from console.utils import wait_key, set_title

exit_keys = (ESC, "q", "Q")

with Screen() as screen:  # or screen.fullscreen():

    set_title(" 🤓 Hi, from console!")
    with screen.location(5, 4):
        print(
            fg.lightgreen("** Hi from a " f"{fx.i}fullscreen{defx.i} app! **"),
            screen.move_x(5),  # back up, then down
            screen.move_down(5),
            fg.yellow(f'(Hit the {fx.reverse("ESC")} key to exit): '),
            end="",
            flush=True,  # optional
        )

    with screen.hidden_cursor():
        wait_key(exit_keys)
