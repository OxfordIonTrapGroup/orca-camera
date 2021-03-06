"""Wait for a single image and show result."""
from orca_camera.driver import OrcaFusion
from matplotlib import pyplot as plt
import numpy as np

if __name__ == "__main__":
    dev = OrcaFusion()
    dev.open(camera_index=0)
    dev.set_subarray(848, 288, 904, 288)
    dev.set_exposure_time(0.3)
    dev.set_trigger_source(1)
    dev.start_capture()
    img = dev.wait_for_image()
    dev.close()
    plt.imshow(img)
    plt.show()
