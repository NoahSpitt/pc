import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pc_sim import VirtualPC
from builder import PCConfig, CPU, RAM, GPU, Storage, Network

def make_config():
    return PCConfig(
        name="pc",
        cpu=CPU("B","M",2,4,2.0,3.0,128,256,4.0,45),
        ram=RAM(4,"DDR4",2400,1),
        gpu=GPU("B","M",2,800,900),
        storage=Storage("SSD",128,500,400),
        network=Network("Wi-Fi 6","5.0",1.0,50,100)
    )

def test_run_program_ram_fail(monkeypatch):
    pc = VirtualPC(make_config())
    assert not pc.run_program(8, 100)

def test_download_no_network(monkeypatch):
    cfg = make_config()
    cfg.network.bandwidth_mbps = 0
    pc = VirtualPC(cfg)
    assert not pc.download(10)
