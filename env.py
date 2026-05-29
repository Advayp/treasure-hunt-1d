"""Toy benchmark env: a 1D treasure hunt game."""

from __future__ import annotations

import random
from typing import Any

from bench_common.env_sdk.base import BaseEnv, StepResult


class MyEnv(BaseEnv):
    def __init__(self) -> None:
        self._rng = random.Random()
        self._pos: int = 0
        self._goal: int = 0
        self._steps: int = 0
        self._max_steps: int = 6
        self._world_size: int = 5

    def reset(self, seed: int | None = None, **params: Any) -> dict[str, Any]:
        self._rng.seed(seed)
        self._steps = 0

        self._world_size = int(params.get("world_size", 5))
        self._max_steps = int(params.get("max_steps", 6))

        if self._world_size < 2:
            raise ValueError("world_size must be >= 2")
        if self._max_steps < 1:
            raise ValueError("max_steps must be >= 1")

        self._pos = 0
        self._goal = self._rng.randrange(0, self._world_size)

        return {
            "world_size": self._world_size,
            "position": self._pos,
            "hint": self._hint(),
            "instructions": "Reply with one of: left, right, stay.",
        }

    def step(self, action: Any) -> StepResult:
        self._steps += 1

        move = str(action).strip().lower()
        if move == "left":
            self._pos -= 1
        elif move == "right":
            self._pos += 1
        elif move == "stay":
            pass
        else:
            return StepResult(
                observation={
                    "position": self._pos,
                    "hint": self._hint(),
                    "error": "Invalid action. Use: left, right, stay.",
                },
                reward=0.0,
                terminated=False,
                truncated=False,
                info={"valid_actions": "left|right|stay"},
            )

        self._pos = max(0, min(self._pos, self._world_size - 1))

        found = self._pos == self._goal
        timed_out = self._steps >= self._max_steps and not found

        return StepResult(
            observation={"position": self._pos, "hint": self._hint()},
            reward=1.0 if found else 0.0,
            terminated=found,
            truncated=timed_out,
            info={"steps": self._steps, "max_steps": self._max_steps},
        )

    def _hint(self) -> str:
        if self._pos < self._goal:
            return "treasure is to the right"
        if self._pos > self._goal:
            return "treasure is to the left"
        return "you found the treasure"
