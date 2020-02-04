from __future__ import annotations
from typing import List
import enum


class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def opposite(self) -> Player:
        return Player.black if self == Player.white else Player.white


class GameState:
    def __init__(self, board: List[List[int]], next_player: Player, prev_state: GameState = None):
        self.board = board
        self.prev_state = prev_state
        self.next_player = next_player

    def __eq__(self, other) -> bool:
        if not isinstance(GameState, other):
            return False
        for i in range(len(self.board)):
            if self.board[i] != other.board[i]:
                return False
        if self.next_player != other.next_player:
            return False
        if self.prev_state != other.prev_state:
            return False
        return True

    def __str__(self) -> str:
        dim = len(self.board)
        signature = sum([sum(l) for l in self.board])
        depth = 1
        _gs = self.prev_state
        while _gs is not None:
            depth += 1
            _gs = _gs.prev_state
        return "{}x{} -> {}, {}, depth={}".format(dim, dim, signature, self.next_player, depth)


def create_dummy_game_state() -> GameState:
    import random
    list_template = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    board: List[List[int]] = []
    for i in range(len(list_template)):
        l1 = list_template.copy()
        random.shuffle(l1)
        board.append(l1)
    return GameState(board, Player.black, None)


def create_dummy_linked_game_states(n: int) -> GameState:
    root: GameState = create_dummy_game_state()
    for i in range(n - 1):
        _gs: GameState = create_dummy_game_state()
        _gs.next_player = _gs.next_player.opposite
        _gs.prev_state = root
        root = _gs
    return root
