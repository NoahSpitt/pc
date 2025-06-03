"""PC configuration builder.
"""

from dataclasses import dataclass, asdict
from typing import List
import json
import os


@dataclass
class CPU:
    brand: str
    model: str
    cores: int
    threads: int
    base_clock_ghz: float
    boost_clock_ghz: float
    l1_cache_kb: int
    l2_cache_kb: int
    l3_cache_mb: float
    tdp_w: int


@dataclass
class RAM:
    size_gb: int
    type: str
    speed_mhz: int
    sticks: int


@dataclass
class GPU:
    brand: str
    model: str
    vram_gb: int
    core_clock_mhz: int
    memory_clock_mhz: int


@dataclass
class Storage:
    type: str
    capacity_gb: int
    read_mb_s: int
    write_mb_s: int


@dataclass
class Network:
    wifi: str
    bluetooth: str
    ethernet_gb: float
    latency_ms: int
    bandwidth_mbps: int


@dataclass
class PCConfig:
    name: str
    cpu: CPU
    ram: RAM
    gpu: GPU
    storage: Storage
    network: Network


class PCBuilder:
    CONFIG_DIR = "configs"

    def __init__(self):
        os.makedirs(self.CONFIG_DIR, exist_ok=True)

    def _validate_name(self, name: str) -> bool:
        return not (os.path.sep in name or os.path.altsep and os.path.altsep in name or '..' in name)

    def list_configs(self) -> List[str]:
        return [f[:-5] for f in os.listdir(self.CONFIG_DIR) if f.endswith('.json')]

    def save_config(self, config: PCConfig):
        if not self._validate_name(config.name):
            raise ValueError('Invalid configuration name')
        path = os.path.join(self.CONFIG_DIR, config.name + '.json')
        with open(path, 'w') as f:
            json.dump(asdict(config), f, indent=2)

    def load_config(self, name: str) -> PCConfig:
        if not self._validate_name(name):
            raise ValueError('Invalid configuration name')
        path = os.path.join(self.CONFIG_DIR, name + '.json')
        with open(path) as f:
            data = json.load(f)
        return PCConfig(
            name=data['name'],
            cpu=CPU(**data['cpu']),
            ram=RAM(**data['ram']),
            gpu=GPU(**data['gpu']),
            storage=Storage(**data['storage']),
            network=Network(**data['network']),
        )

    def prompt_cpu(self) -> CPU:
        print("=== CPU ===")
        brand = input("Brand: ")
        model = input("Model: ")
        cores = int(input("Cores: "))
        threads = int(input("Threads: "))
        base_clock = float(input("Base clock (GHz): "))
        boost_clock = float(input("Boost clock (GHz): "))
        l1 = int(input("L1 cache (KB): "))
        l2 = int(input("L2 cache (KB): "))
        l3 = float(input("L3 cache (MB): "))
        tdp = int(input("TDP (W): "))
        return CPU(brand, model, cores, threads, base_clock, boost_clock, l1, l2, l3, tdp)

    def prompt_ram(self) -> RAM:
        print("=== RAM ===")
        size_gb = int(input("Size (GB): "))
        type_ = input("Type (DDR4/DDR5): ")
        speed_mhz = int(input("Speed (MHz): "))
        sticks = int(input("Number of sticks: "))
        return RAM(size_gb, type_, speed_mhz, sticks)

    def prompt_gpu(self) -> GPU:
        print("=== GPU ===")
        brand = input("Brand: ")
        model = input("Model: ")
        vram_gb = int(input("VRAM (GB): "))
        core_clock = int(input("Core clock (MHz): "))
        mem_clock = int(input("Memory clock (MHz): "))
        return GPU(brand, model, vram_gb, core_clock, mem_clock)

    def prompt_storage(self) -> Storage:
        print("=== Storage ===")
        type_ = input("Type (HDD/SSD/NVMe): ")
        capacity_gb = int(input("Capacity (GB): "))
        read_mb_s = int(input("Read speed (MB/s): "))
        write_mb_s = int(input("Write speed (MB/s): "))
        return Storage(type_, capacity_gb, read_mb_s, write_mb_s)

    def prompt_network(self) -> Network:
        print("=== Network ===")
        wifi = input("WiFi standard (e.g. Wi-Fi 6): ")
        bluetooth = input("Bluetooth version: ")
        ethernet_gb = float(input("Ethernet speed (Gbps, 0 if none): "))
        latency_ms = int(input("Latency (ms): "))
        bandwidth_mbps = int(input("Bandwidth (Mbps): "))
        return Network(wifi, bluetooth, ethernet_gb, latency_ms, bandwidth_mbps)

    def create_config(self) -> PCConfig:
        name = input("Configuration name: ")
        cpu = self.prompt_cpu()
        ram = self.prompt_ram()
        gpu = self.prompt_gpu()
        storage = self.prompt_storage()
        network = self.prompt_network()
        config = PCConfig(name, cpu, ram, gpu, storage, network)
        self.save_config(config)
        print(f"Configuration '{name}' saved.")
        return config

