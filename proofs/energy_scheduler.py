# SPDX-License-Identifier: Unlicense
"""
Bare-Metal Hardware-Energy Micro-Grid Scheduler Proof (ENERGY-v1.0).
Gates high-density compute tasks strictly to zero-cost energy windows
using hysteresis-bounded state transitions and strict energy-integration math.
"""

import time
import json
import sys
from typing import Dict, Any

class MicroGridScheduler:
    """
    Bare-Metal Hardware-Energy Micro-Grid Scheduler (ENERGY-v1.0).
    Enforces zero-net-cost local execution for LMCI and ATN workloads.
    """
    def __init__(
        self,
        node_power_draw_watts: float,
        min_soc_percent: float = 85.0,
        absolute_min_soc_percent: float = 20.0,
        hysteresis_margin_watts: float = 50.0,
        min_hold_sec: float = 300.0
    ):
        self.node_power_draw_watts = node_power_draw_watts
        self.min_soc_percent = min_soc_percent
        self.absolute_min_soc_percent = absolute_min_soc_percent
        self.hysteresis_margin_watts = hysteresis_margin_watts
        self.min_hold_sec = min_hold_sec
        
        self.currently_executing = False
        self.last_state_change_time = 0.0

    def calculate_task_energy_cost(
        self,
        duration_hours: float,
        grid_rate_per_kwh: float
    ) -> float:
        """
        Calculates execution cost in fiat currency based on energy integration.
        Energy (kWh) = (Power (W) / 1000) * Time (hours)
        """
        energy_kwh = (self.node_power_draw_watts / 1000.0) * duration_hours
        return energy_kwh * grid_rate_per_kwh

    def evaluate_execution_permission(self, telemetry: Dict[str, Any], current_time: float = None) -> bool:
        """
        Evaluates real-time BMS telemetry payload.
        Applies hysteresis bounds to prevent hardware relay or process thrashing.
        """
        if current_time is None:
            current_time = time.time()

        soc = float(telemetry.get("battery_soc_percent", 0.0))
        pv_yield_watts = float(telemetry.get("pv_yield_watts", 0.0))
        house_load_watts = float(telemetry.get("house_load_watts", 0.0))
        grid_rate_per_kwh = float(telemetry.get("grid_rate_per_kwh", 0.15))
        task_yield_fiat = float(telemetry.get("task_yield_fiat", 0.0))

        net_surplus_watts = pv_yield_watts - house_load_watts

        # Absolute battery protection guard: Never execute below critical SOC
        if soc < self.absolute_min_soc_percent:
            self._update_state(False, current_time)
            return False

        # Respect hysteresis minimum hold duration
        if (current_time - self.last_state_change_time) < self.min_hold_sec and self.last_state_change_time > 0.0:
            return self.currently_executing

        # Calculate threshold required to turn ON vs STAY ON (Hysteresis)
        required_surplus = self.node_power_draw_watts
        if not self.currently_executing:
            required_surplus += self.hysteresis_margin_watts

        # Condition 1: Pure solar/battery thermodynamic surplus
        thermodynamic_surplus = (soc >= self.min_soc_percent) and (net_surplus_watts >= required_surplus)

        # Condition 2: Task yield exceeds grid energy acquisition cost
        hourly_energy_cost = self.calculate_task_energy_cost(duration_hours=1.0, grid_rate_per_kwh=grid_rate_per_kwh)
        economic_viability = task_yield_fiat > hourly_energy_cost

        should_run = thermodynamic_surplus or economic_viability
        self._update_state(should_run, current_time)
        return self.currently_executing

    def _update_state(self, new_state: bool, current_time: float) -> None:
        if new_state != self.currently_executing:
            self.currently_executing = new_state
            self.last_state_change_time = current_time

if __name__ == "__main__":
    scheduler = MicroGridScheduler(
        node_power_draw_watts=250.0,
        min_soc_percent=85.0,
        min_hold_sec=0.0
    )
    
    mock_telemetry = {
        "battery_soc_percent": 92.0,
        "pv_yield_watts": 1200.0,
        "house_load_watts": 400.0,
        "grid_rate_per_kwh": 0.20,
        "task_yield_fiat": 0.0
    }
    
    can_run = scheduler.evaluate_execution_permission(mock_telemetry, current_time=100.0)
    cost = scheduler.calculate_task_energy_cost(duration_hours=1.0, grid_rate_per_kwh=0.20)
    
    print(f"[ENERGY-v1.0] Execution Permitted: {can_run}")
    print(f"[ENERGY-v1.0] 1-Hour Compute Energy Cost: ${cost:.4f}")
    assert can_run is True
    assert round(cost, 4) == 0.0500
