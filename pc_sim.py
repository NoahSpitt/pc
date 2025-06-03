"""Very lightweight PC simulation utilities."""

from time import sleep
from typing import Optional

from builder import PCConfig


class VirtualPC:
    """Simulate very basic resource usage based on a PC configuration."""

    def __init__(self, config: PCConfig):
        self.config = config
        self.used_ram_gb = 0
        self.clock_speed = self.config.cpu.base_clock_ghz * self.config.cpu.cores
        self.bandwidth_mbps = self.config.network.bandwidth_mbps
        self.latency_ms = self.config.network.latency_ms

    @property
    def total_ram_gb(self) -> int:
        return self.config.ram.size_gb

    def allocate_ram(self, amount_gb: int) -> bool:
        if self.used_ram_gb + amount_gb > self.total_ram_gb:
            return False
        self.used_ram_gb += amount_gb
        return True

    def free_ram(self, amount_gb: int):
        self.used_ram_gb = max(0, self.used_ram_gb - amount_gb)

    def cpu_delay(self, units: int):
        delay = units / self.clock_speed
        sleep(delay)

    def network_delay(self, size_mb: int):
        if self.bandwidth_mbps <= 0:
            print('No network connection')
            return False
        seconds = (size_mb * 8) / self.bandwidth_mbps
        seconds += self.latency_ms / 1000
        sleep(seconds)
        return True

    def run_program(self, ram_gb: int, cycles: int):
        if not self.allocate_ram(ram_gb):
            print('Not enough RAM')
            return False
        self.cpu_delay(cycles)
        self.free_ram(ram_gb)
        return True

    def download(self, size_mb: int):
        return self.network_delay(size_mb)

    def info(self) -> str:
        return (
            f"CPU: {self.config.cpu.brand} {self.config.cpu.model} "
            f"{self.config.cpu.cores}C/{self.config.cpu.threads}T\n"
            f"RAM: {self.total_ram_gb} GB\n"
            f"GPU: {self.config.gpu.brand} {self.config.gpu.model} "
            f"{self.config.gpu.vram_gb} GB VRAM\n"
            f"Network: {self.bandwidth_mbps} Mbps, {self.latency_ms} ms latency"
        )

