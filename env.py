"""Toy benchmark env: 1D treasure hunt with sparse observations."""

from __future__ import annotations

import random
import re
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

        self._world_size = int(params.get("world_size", 9))
        self._max_steps = int(params.get("max_steps", 5))

        if self._world_size < 2:
            raise ValueError("world_size must be >= 2")
        if self._max_steps < 1:
            raise ValueError("max_steps must be >= 1")

        self._pos = self._rng.randrange(0, self._world_size)
        self._goal = self._rng.randrange(0, self._world_size)
        if self._world_size > 1:
            while self._goal == self._pos:
                self._goal = self._rng.randrange(0, self._world_size)

        return {
            "world_size": self._world_size,
            "distance": abs(self._goal - self._pos),
            "distance_delta": 0,
            "steps_left": self._max_steps - self._steps,
            "instructions": "Reply with EXACTLY one token: left OR right OR stay. No punctuation, no extra text.",
        }

    def step(self, action: Any) -> StepResult:
        self._steps += 1

        prev_distance = abs(self._goal - self._pos)

        move = self._parse_action(action)
        if move == "left":
            self._pos -= 1
        elif move == "right":
            self._pos += 1
        elif move == "stay":
            pass
        else:
            return StepResult(
                observation={
                    "world_size": self._world_size,
                    "distance": prev_distance,
                    "distance_delta": None,
                    "steps_left": max(0, self._max_steps - self._steps),
                    "error": "Invalid action. Use: left, right, stay.",
                },
                reward=0.0,
                terminated=False,
                truncated=False,
                info={"valid_actions": "left|right|stay"},
            )

        self._pos = max(0, min(self._pos, self._world_size - 1))
        current_distance = abs(self._goal - self._pos)
        distance_delta = prev_distance - current_distance

        found = self._pos == self._goal
        timed_out = self._steps >= self._max_steps and not found

        return StepResult(
            observation={
                "world_size": self._world_size,
                "distance": current_distance,
                "distance_delta": distance_delta,
                "steps_left": max(0, self._max_steps - self._steps),
            },
            reward=1.0 if found else 0.0,
            terminated=found,
            truncated=timed_out,
            info={"steps": self._steps, "max_steps": self._max_steps},
        )

    @staticmethod
    def _parse_action(action: Any) -> str:
        text = str(action).strip().lower()
        matches = re.findall(r"\b(left|right|stay)\b", text)
        return matches[-1] if matches else text
