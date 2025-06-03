import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from builder import PCBuilder, PCConfig, CPU, RAM, GPU, Storage, Network


def test_save_and_load(tmp_path):
    builder = PCBuilder()
    builder.CONFIG_DIR = tmp_path.as_posix()
    cfg = PCConfig(
        name="testpc",
        cpu=CPU("Brand","Model",4,8,3.0,4.0,256,512,8.0,65),
        ram=RAM(8,"DDR4",3200,2),
        gpu=GPU("Brand","Model",4,1000,1500),
        storage=Storage("SSD",256,500,400),
        network=Network("Wi-Fi 6","5.0",1.0,50,100),
    )
    builder.save_config(cfg)
    loaded = builder.load_config("testpc")
    assert loaded == cfg
