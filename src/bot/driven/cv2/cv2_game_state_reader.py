import logging
from dataclasses import dataclass
from typing import List, Set, FrozenSet, Tuple

import cv2
import numpy as np

from bot.domain.card import Card, Suit, Rank
from bot.domain.game import GameStateReader, GameState
from bot.domain.player import Player, generate_unknown_hand

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _ColorBoundary:
    suit: Suit
    lower_bound: np.array
    upper_bound: np.array


_card_detection_color_boundaries = [
    _ColorBoundary(Suit.RED, np.array([0, 20, 100]), np.array([20, 255, 255])),
    _ColorBoundary(Suit.BLUE, np.array([105, 20, 100]), np.array([110, 255, 255])),
    _ColorBoundary(Suit.PURPLE, np.array([120, 40, 100]), np.array([140, 255, 255])),
    _ColorBoundary(Suit.YELLOW, np.array([30, 120, 100]), np.array([50, 200, 200])),
    _ColorBoundary(Suit.GREEN, np.array([50, 0, 0]), np.array([60, 255, 220])),
]

_card_ranking_color_boundaries = [
    _ColorBoundary(Suit.RED, np.array([0, 200, 100]), np.array([20, 255, 255])),
    _ColorBoundary(Suit.BLUE, np.array([20, 200, 0]), np.array([200, 255, 255])),
    _ColorBoundary(Suit.PURPLE, np.array([120, 200, 100]), np.array([140, 255, 255])),
    _ColorBoundary(Suit.YELLOW, np.array([0, 0, 0]), np.array([255, 150, 255])),
    _ColorBoundary(Suit.GREEN, np.array([50, 200, 0]), np.array([60, 255, 220])),
]


@dataclass(frozen=True)
class DetectedCard:
    card: Card
    rect: Tuple[int, int, int, int]


class LazyImage:
    def __init__(self, screenshot: np.ndarray):
        self._screenshot = screenshot
        self._hsv = None
        self._hsv_filtered = None

    def original(self) -> np.ndarray:
        return self._screenshot

    def hsv(self) -> np.ndarray:
        if self._hsv is not None:
            return self._hsv

        self._hsv = cv2.cvtColor(self._screenshot, cv2.COLOR_BGR2HSV)
        return self._hsv

    def hsv_filtered(self) -> np.ndarray:
        if self._hsv_filtered is not None:
            return self._hsv_filtered

        self._hsv_filtered = cv2.fastNlMeansDenoising(self.hsv(), h=10, templateWindowSize=7, searchWindowSize=21)
        return self._hsv_filtered

    def __getitem__(self, item) -> np.ndarray:
        return self._screenshot[item]


def __test_write(image: np.ndarray | LazyImage):
    if type(image) == LazyImage:
        image = image.original()
    return cv2.imwrite("../target/test.png", image)


class Screenshotter:
    def screenshot(self) -> LazyImage:
        raise NotImplementedError


class FromFileScreenshotter(Screenshotter):
    def __init__(self, filename: str):
        self._filename = filename

    def screenshot(self) -> LazyImage:
        return LazyImage(cv2.imread(self._filename))


class Cv2GameStateReader(GameStateReader):
    def __init__(self, screenshotter: Screenshotter):
        self.screenshotter = screenshotter
        self.first_turn = True

    def see_current_state(self) -> GameState | None:
        """
        algo:

        if previous state is None
          previous state = read state()
          return previous state

        if previous state is first turn:
          left arrow
          previous state = read state()
          if nothing changed
            return None

        right arrow
        previous state = read state()
        if nothing changed
          return None

        return previous state
        """

        screenshot = self.screenshotter.screenshot()

        players = _read_player_hands(screenshot)

        return None


width_card_crop_ratio = 1 / 13
height_card_crop_ratio = 1 / 6


def _read_card_rank(card: LazyImage, suit: Suit) -> Rank:
    boundary = next(boundary for boundary in _card_ranking_color_boundaries if boundary.suit == suit)

    height = len(card.original())
    width = len(card.original()[0])
    card = LazyImage(
        card.original()[
            int(height_card_crop_ratio * height) : -int(height_card_crop_ratio * height),
            int(width_card_crop_ratio * width) : -int(width_card_crop_ratio * width),
        ]
    )
    mask = cv2.inRange(card.hsv_filtered(), boundary.lower_bound, boundary.upper_bound)
    inv = cv2.bitwise_not(mask)

    contours = cv2.findContours(inv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    min_area = 100
    max_area = 1000

    rank = len([contour for contour in contours if min_area < cv2.contourArea(contour) < max_area])
    return Rank.from_char(rank)


def _read_all_cards_for_suit(screenshot: LazyImage, suit: Suit) -> Set[DetectedCard]:
    logger.debug(f"Finding card of the {suit} suit.")

    color_boundary = next(boundary for boundary in _card_detection_color_boundaries if boundary.suit == suit)

    mask = cv2.inRange(screenshot.hsv_filtered(), color_boundary.lower_bound, color_boundary.upper_bound)

    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = [contour for contour in contours if len(contour) >= 4]

    min_area = 10000
    cards = set()
    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            rect = cv2.boundingRect(contour)
            x, y, w, h = rect
            card_image = LazyImage(screenshot[y : y + h, x : x + w])
            __test_write(card_image.original())
            card = DetectedCard(Card(suit, _read_card_rank(card_image, suit)), rect)
            logger.debug(f"Found {suit} {card.card.rank} card in {rect}.")
            cards.add(card)

    logger.debug(f"Found {len(cards)} {suit} cards.")
    return cards


def _read_all_cards(screenshot: LazyImage) -> FrozenSet[DetectedCard]:
    return frozenset(card for suit in Suit for card in _read_all_cards_for_suit(screenshot, suit))


def _read_player_hands(screenshot: LazyImage) -> List[Player]:
    players = [Player(0, generate_unknown_hand())]

    cards = _read_all_cards(screenshot)

    return players
