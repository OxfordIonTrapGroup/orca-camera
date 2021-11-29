from orca_camera.driver import OrcaFusion
from matplotlib import pyplot as plt
import numpy as np

if __name__ == "__main__":
    dev = OrcaFusion()
    dev.open(camera_index=0)
    dev.set_subarray(848, 288, 904, 288)
    print(f"Exposure time set to {dev.set_exposure_time(0.3)} s.")
    print(f"Trigger source set to {dev.set_trigger_source(1)}.")
    img = np.array(dev.get_image())
    dev.close()
    plt.imshow(img)
    plt.show()
