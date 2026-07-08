#!/usr/bin/env python3
import numpy as np

from openpilot.common.pid import PIDController


class FanController:
  def __init__(self, rate: int) -> None:
    self.last_ignition = False
    self.controller = PIDController(k_p=0, k_i=4e-3, rate=rate)

  def update(self, cur_temp: float, ignition: bool) -> int:
    # 统一行车和熄火状态的风扇控制逻辑
    self.controller.pos_limit = 100
    self.controller.neg_limit = 0

    if ignition != self.last_ignition:
      self.controller.reset()
    self.last_ignition = ignition

    return int(self.controller.update(
                 error=(cur_temp - 75.0),  # 目标温度 75°C
                 feedforward=np.interp(cur_temp, [60.0, 75.0], [70, 100])
              ))
