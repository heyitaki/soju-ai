from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, cast

from src.constants import BOARD_HEIGHT, BOARD_WIDTH
from src.models.boards.champ_board import ChampBoard

if TYPE_CHECKING:
    from src.models.champion import Champion
    from src.models.player import Player
    from src.models.points.offset_point import OffsetPoint


class PlayerBoard(ChampBoard):
    """
    Hexagonal grid (offset evenr) representing a player's half of the full field.
    """

    player: Player

    def __init__(self, player: Player):
        super().__init__(BOARD_WIDTH, BOARD_HEIGHT)
        self.player = player

    def add_champ(self, champ: Champion, pos: OffsetPoint) -> Union[bool, Champion]:
        if not self.is_position_valid(pos):
            # Make sure given position is valid
            return False
        elif self.is_hex_empty(pos):
            # Place champ on board
            if len(self.champs) < self.player.max_champs:
                self.set(pos, champ)
                return True
            return False
        else:
            # Swap champs and return swapped champ
            champ_to_bench = cast(Champion, self.get(pos))

            self.set(pos, champ)
            return champ_to_bench

    def add_champ_from_carousel(self, champ: Champion) -> bool:
        """
        Add a champ to the board without a specified position. This happens when player picks
        champ from carousel with a full bench.
        """
        new_pos: Optional[OffsetPoint] = None
        for y in reversed(range(BOARD_HEIGHT)):
            for x in range(BOARD_WIDTH):
                pos = OffsetPoint(x, y)
                if self.is_hex_empty(pos):
                    new_pos = pos

        if new_pos:
            self.num_champs += 1
            self.set(new_pos, champ)
            return True
        return False

    def is_full(self) -> bool:
        return self.num_champs >= self.player.max_champs

    def move_champ(self, start_pos: OffsetPoint, end_pos: OffsetPoint) -> bool:
        """
        Move a champ on this board to a different position. Returns whether or not move was valid.
        """
        if (
            not self.is_position_valid(start_pos)
            or not self.is_position_valid(end_pos)
            or start_pos == end_pos
        ):
            return False

        champ1 = self.get(start_pos)
        champ2 = self.get(end_pos)
        if not champ1:
            return False
        elif champ2:
            # Swap champs
            self.set(start_pos, champ2)
            self.set(end_pos, champ1)
        else:
            # Place champ
            self.set(start_pos, None)
            self.set(end_pos, champ1)
        return True

    def remove_champ(self, pos: OffsetPoint) -> Union[Champion, None]:
        if not self.is_position_valid(pos):
            return None

        champ = self.get(pos)
        if champ:
            self.set(pos, None)
            self.num_champs -= 1
            return champ
        return None
