import ctypes
import time
import platform
import os
import numpy as np
import collections
import threading
import logging
import contextlib
import atexit
from enum import Enum

from ctypes import c_int32, c_uint32, c_short, c_double, c_void_p, c_char, POINTER, byref
from ctypes.wintypes import HANDLE

from .error_codes import ERROR_CODES
from .property_codes import PROPERTY_CODES

logger = logging.getLogger(__name__)

# TODO: add DCAM_GUID structure


#TODO: add optional arguments
class DCAMAPI_INIT(ctypes.Structure):
    _fields_ = [("size", c_int32), ("iDeviceCount", c_int32),
                ("reserved", c_int32)]


class DCAMDEV_OPEN(ctypes.Structure):
    _fields_ = [("size", c_int32), ("index", c_int32), ("hdcam", HANDLE)]


class DCAMDEV_CAPABILITY(ctypes.Structure):
    _fields_ = [("size", c_int32), ("domain", c_int32), ("capflag", c_int32),
                ("kind", c_int32)]


class DCAMDEV_CAPABILITY_LUT(ctypes.Structure):
    _fields_ = [("hdr", DCAMDEV_CAPABILITY), ("linearpointmax", c_int32)]


class DCAMDEV_CAPABILITY_REGION(ctypes.Structure):
    _fields_ = [("hdr", DCAMDEV_CAPABILITY), ("horzunit", c_int32),
                ("vertunit", c_int32)]


class DCAMDEV_CAPABILITY_FRAMEOPTION(ctypes.Structure):
    _fields_ = [("hdr", DCAMDEV_CAPABILITY), ("supportproc", c_int32)]


class DCAMDEV_STRING(ctypes.Structure):
    _fields_ = [("size", c_int32), ("iString", c_int32), ("text", c_char),
                ("textbytes", c_int32)]


class DCAMDEV_STRING(ctypes.Structure):
    _fields_ = [("size", c_int32), ("iString", c_int32), ("text", c_char),
                ("textbytes", c_int32)]


class DCAMDATA_HDR(ctypes.Structure):
    _fields_ = [("size", c_int32), ("iKind", c_int32), ("option", c_int32),
                ("reserved2", c_int32)]


class DCAMDATA_REGION(ctypes.Structure):
    _fields_ = [("hdr", DCAMDATA_HDR), ("option", c_int32), ("type", c_int32),
                ("data", c_void_p), ("datasize", c_int32),
                ("reserved", c_int32)]


class DCAMDATA_REGIONRECT(ctypes.Structure):
    _fields_ = [("left", c_short), ("top", c_short), ("right", c_short),
                ("bottom", c_short)]


class DCAMDATA_LUT(ctypes.Structure):
    _fields_ = [("hdr", DCAMDATA_HDR), ("type", c_int32), ("page", c_int32),
                ("data", c_void_p), ("datasize", c_int32),
                ("reserved", c_int32)]


class DCAMDATA_LINEARLUT(ctypes.Structure):
    _fields_ = [("lutin", c_int32), ("lutout", c_int32)]


class DCAMPROP_ATTR(ctypes.Structure):
    _fields_ = [("cbSize", c_int32), ("iProp", c_int32), ("option", c_int32),
                ("iReserved1", c_int32), ("attribute", c_int32),
                ("iGroup", c_int32),
                ("iUnit", c_int32), ("attribute2", c_int32),
                ("valuemin", c_double), ("valuemax", c_double),
                ("valuestep", c_double), ("valuedefault", c_double),
                ("nMaxChannel", c_int32), ("iReserved3", c_int32),
                ("nMaxView", c_int32), ("iProp_NumberOfElement", c_int32),
                ("iProp_ArrayBase", c_int32), ("iPropStep_Element", c_int32)]


class DCAMPROP_VALUETEXT(ctypes.Structure):
    _fields_ = [("cbSize", c_int32), ("iProp", c_int32), ("value", c_double),
                ("text", c_char), ("textbytes", c_int32)]


class DCAMBUF_ATTACH(ctypes.Structure):
    _fields_ = [("size", c_int32), ("iKind", c_int32),
                ("buffer", POINTER(c_void_p)), ("buffercount", c_int32)]


class DCAM_TIMESTAMP(ctypes.Structure):
    _fields_ = [("sec", c_int32), ("microsec", c_int32)]


class DCAMBUF_FRAME(ctypes.Structure):
    _fields_ = [("size", c_int32), ("iKind", c_int32), ("option", c_int32),
                ("iFrame", c_int32), ("buf", POINTER(c_void_p)),
                ("rowbytes", c_int32), ("type", c_int32), ("width", c_int32),
                ("height", c_int32), ("left", c_int32), ("top", c_int32),
                ("timestamp", DCAM_TIMESTAMP), ("framestamp", c_int32),
                ("camerastamp", c_int32)]


# TODO: add DCAMREC_FRAME structure


class DCAMWAIT_OPEN(ctypes.Structure):
    _fields_ = [("size", c_int32), ("supportevent", c_int32),
                ("hwait", HANDLE), ("hdcam", HANDLE)]


class DCAMWAIT_START(ctypes.Structure):
    _fields_ = [("size", c_int32), ("eventhappened", c_int32),
                ("eventmask", c_int32), ("timeout", c_int32)]


class DCAMCAP_TRANSFERINFO(ctypes.Structure):
    _fields_ = [("size", c_int32), ("iKind", c_int32),
                ("nNewestFrameIndex", c_int32), ("nFrameCount", c_int32)]


# TODO: add DCAMREC_OPEN structure


class DCAM_METADATAHDR(ctypes.Structure):
    _fields_ = [("size", c_int32), ("iKind", c_int32), ("option", c_int32),
                ("iFrame", c_int32)]


class DCAM_METADATABLOCKHDR(ctypes.Structure):
    _fields_ = [("size", c_int32), ("iKind", c_int32), ("option", c_int32),
                ("iFrame", c_int32), ("in_count", c_int32),
                ("outcount", c_int32)]


class DCAM_USERDATATEXT(ctypes.Structure):
    _fields_ = [("hdr", DCAM_METADATAHDR), ("text", c_char),
                ("text_len", c_int32), ("codepage", c_int32)]


class DCAM_USERDATABIN(ctypes.Structure):
    _fields_ = [("hdr", DCAM_METADATAHDR), ("bin", c_void_p),
                ("bin_len", c_int32), ("reserved", c_int32)]


class DCAM_TIMESTAMPBLOCK(ctypes.Structure):
    _fields_ = [("hdr", DCAM_METADATABLOCKHDR), ("timestamps", DCAM_TIMESTAMP),
                ("timestampsize", c_int32), ("timestampvalidsize", c_int32),
                ("timestampkind", c_int32), ("reserved", c_int32)]


class DCAM_FRAMESTAMPBLOCK(ctypes.Structure):
    _fields_ = [("hdr", DCAM_METADATABLOCKHDR), ("framestamps", c_int32),
                ("reserved", c_int32)]


class DCAM_METADATATEXTBLOCK(ctypes.Structure):
    _fields_ = [("hdr", DCAM_METADATABLOCKHDR), ("text", c_void_p),
                ("textsizes", c_int32), ("bytesperunit", c_int32),
                ("reserved", c_int32), ("textcodepage", c_int32)]


class DCAM_METADATABINBLOCK(ctypes.Structure):
    _fields_ = [("hdr", DCAM_METADATABLOCKHDR), ("bin", c_void_p),
                ("binsizes", c_int32), ("bytesperunit", c_int32),
                ("reserved", c_int32)]


class DCAMREC_STATUS(ctypes.Structure):
    _fields_ = [("size", c_int32), ("currentsession_index", c_int32),
                ("maxframecount_per_session", c_int32),
                ("countframe_index", c_int32), ("missingframe_count", c_int32),
                ("flags", c_int32), ("totalframecount", c_int32),
                ("reserved", c_int32)]


class LibInstance:
    #DCAM API return codes
    return_codes = {}

    def __init__(self):
        def wrapper(f, argtypes=None):
            if argtypes is not None:
                f.argtypes = argtypes
            f.restype = c_uint32
            return f

        self.hdcam = ctypes.windll.dcamapi

        # Initialize, uninitialize and misc.
        self.dcamapi_init = wrapper(self.hdcam.dcamapi_init,
                                    [POINTER(DCAMAPI_INIT)])
        self.dcamapi_uninit = wrapper(self.hdcam.dcamapi_uninit)
        self.dcamdev_open = wrapper(self.hdcam.dcamdev_open,
                                    [POINTER(DCAMDEV_OPEN)])
        self.dcamdev_close = wrapper(self.hdcam.dcamdev_close, [HANDLE])

        # Property control
        self.dcamprop_getattr = wrapper(
            self.hdcam.dcamprop_getattr,
            [HANDLE, POINTER(DCAMPROP_ATTR)])
        self.dcamprop_getvalue = wrapper(
            self.hdcam.dcamprop_getvalue,
            [HANDLE, c_int32, POINTER(c_double)])
        self.dcamprop_setvalue = wrapper(self.hdcam.dcamprop_setvalue,
                                         [HANDLE, c_int32, c_double])
        self.dcamprop_setgetvalue = wrapper(
            self.hdcam.dcamprop_setgetvalue,
            [HANDLE, c_int32, POINTER(c_double), c_int32])
        self.dcamprop_queryvalue = wrapper(
            self.hdcam.dcamprop_queryvalue,
            [HANDLE, c_int32, POINTER(c_double), c_int32])
        self.dcamprop_getnextid = wrapper(
            self.hdcam.dcamprop_getnextid,
            [HANDLE, POINTER(c_int32), c_int32])
        self.dcamprop_getname = wrapper(
            self.hdcam.dcamprop_getname,
            [HANDLE, c_int32, POINTER(c_char), c_int32])
        self.dcamprop_getvaluetext = wrapper(
            self.hdcam.dcamprop_getvaluetext,
            [HANDLE, POINTER(DCAMPROP_VALUETEXT)])

        # Buffer control
        self.dcambuf_alloc = wrapper(self.hdcam.dcambuf_alloc,
                                     [HANDLE, c_int32])
        self.dcambuf_attach = wrapper(self.hdcam.dcambuf_attach,
                                      [HANDLE, POINTER(DCAMBUF_ATTACH)])
        self.dcambuf_release = wrapper(self.hdcam.dcambuf_release,
                                       [HANDLE, c_int32])
        self.dcambuf_lockframe = wrapper(
            self.hdcam.dcambuf_lockframe,
            [HANDLE, POINTER(DCAMBUF_FRAME)])
        self.dcambuf_copyframe = wrapper(
            self.hdcam.dcambuf_copyframe,
            [HANDLE, POINTER(DCAMBUF_FRAME)])
        self.dcambuf_copymetadata = wrapper(
            self.hdcam.dcambuf_copymetadata,
            [HANDLE, POINTER(DCAM_METADATAHDR)])

        # Capturing control
        self.dcamcap_start = wrapper(self.hdcam.dcamcap_start,
                                     [HANDLE, c_int32])
        self.dcamcap_stop = wrapper(self.hdcam.dcamcap_stop, [HANDLE])
        self.dcamcap_status = wrapper(self.hdcam.dcamcap_status,
                                      [HANDLE, POINTER(c_int32)])
        self.dcamcap_transferinfo = wrapper(
            self.hdcam.dcamcap_transferinfo,
            [HANDLE, POINTER(DCAMCAP_TRANSFERINFO)])
        self.dcamcap_firetrigger = wrapper(self.hdcam.dcamcap_firetrigger,
                                           [HANDLE, c_int32])
        self.dcamcap_record = wrapper(self.hdcam.dcamcap_record,
                                      [HANDLE, HANDLE])

        # Waiting event control
        self.dcamwait_open = wrapper(self.hdcam.dcamwait_open,
                                     [POINTER(DCAMWAIT_OPEN)])
        self.dcamwait_close = wrapper(self.hdcam.dcamwait_close, [HANDLE])
        self.dcamwait_start = wrapper(self.hdcam.dcamwait_start,
                                      [HANDLE, POINTER(DCAMWAIT_START)])
        self.dcamwait_abort = wrapper(self.hdcam.dcamwait_abort, [HANDLE])

        # TODO: add recording control


class Trigger(Enum):
    INTERNAL = 1
    EXTERNAL = 2


class Speed(Enum):
    QUIET = 1
    STANDARD = 2
    FAST = 3


class OrcaFusion:
    SUBARRAY_QUANTISATION = 4

    def __init__(self):
        self.lib = LibInstance()

        self.dcamapi_init_struct = DCAMAPI_INIT(size=32)
        self.lib.dcamapi_init(byref(self.dcamapi_init_struct))
        self.num_dev = self.dcamapi_init_struct.iDeviceCount
        logger.info(f"Found {self.num_dev} devices.")

        self._frame_call_list = []
        self.camera_handle = None
        atexit.register(self._cleanup)

    def _cleanup(self):
        if self.camera_handle is not None:
            self.close()

    def open(self, camera_index, framebuffer_len=100):
        """
        Open a connection to the camera.
        :param camera_index: index of the camera to connect to
        :param framebuffer_len: maximum number of stored frames before
        oldest are discarded
        """
        self.dcamdev_open_struct = DCAMDEV_OPEN(size=32, index=camera_index)
        open_code = self.lib.dcamdev_open(byref(self.dcamdev_open_struct))
        if open_code == 1:
            logger.info(
                f"Connected to camera with index {self.dcamdev_open_struct.index}."
            )
        else:
            raise Exception("Connection to camera unsuccessful.")

        self.camera_handle = self.dcamdev_open_struct.hdcam
        self.frame_buffer = collections.deque([], framebuffer_len)

        self._stopping = threading.Event()

        # Start image acquisition thread
        self._thread = threading.Thread(target=self._acquisition_thread, daemon=True)
        self._thread.start()

    def _err_code(self, err):
        if err == 1:
            return None
        return ERROR_CODES[err_code]

    def _check_err(self, err):
        err_code = self._err_code(err)
        if err_code:
            raise Exception(ERROR_CODES[err_code])

    def _get_property(self, code):
        result = c_double()
        err = self.lib.dcamprop_getvalue(self.camera_handle, c_int32(code),
                                         byref(result))
        self._check_err(err)

        return result.value

    def _set_property(self, code, val):
        result = c_double(val)
        err = self.lib.dcamprop_setgetvalue(self.camera_handle, c_int32(code),
                                            byref(result), c_int32(0))
        self._check_err(err)

        return result.value

    def get_status(self):
        """Reads the camera acquisition status"""
        status = c_int32(0)
        self.lib.dcamcap_status(self.camera_handle, byref(status))
        return status.value

    def get_exposure_time(self):
        """Reads the current value of the exposure time in seconds."""
        return self._get_property(PROPERTY_CODES["EXPOSURETIME"])

    def set_exposure_time(self, t):
        """
        Set the camera exposure time.
        :param time: New target value of the exposure time in seconds.
        :return: The new value of the exposure time in seconds.
        """
        return self._set_property(PROPERTY_CODES["EXPOSURETIME"], t)

    def set_readout_speed(self, speed=Speed.STANDARD):
        """
        Set the camera readout speed.
        """
        return self._set_property(PROPERTY_CODES["READOUTSPEED"], speed)

    def get_internal_frame_rate(self):
        """
        Get the frame rate of the camera when internally triggered.
        """
        return self._get_property(PROPERTY_CODES["INTERNALFRAMERATE"])

    def set_subarray(self, xmin, xsize, ymin, ysize):
        """
        Set the region of interest in pixels. Pixel indexing starts from
        0 with x=0 being the leftmost pixel, and y=0 being the top pixel.
        All the parameters must be divisible by 4
        :param xmin: leftmost pixel number
        :param xsize: horizontal extent of the region
        :param ymin: top pixel number
        :param ysize: vertical extent of the region
        """

        # Check parameters all are divisible by 4
        def check_quantisation(name, param):
            if param % self.SUBARRAY_QUANTISATION:
                raise ValueError(f"Subarray parameter '{name}' must be divisible by {self.SUBARRAY_QUANTISATION}")
        check_quantisation("xmin", xmin)
        check_quantisation("xsize", xsize)
        check_quantisation("ymin", ymin)
        check_quantisation("ysize", ysize)

        self._set_property(PROPERTY_CODES["SUBARRAYMODE"], 1)
        self._set_property(PROPERTY_CODES["SUBARRAYHPOS"], xmin)
        self._set_property(PROPERTY_CODES["SUBARRAYHSIZE"], xsize)
        self._set_property(PROPERTY_CODES["SUBARRAYVPOS"], ymin)
        self._set_property(PROPERTY_CODES["SUBARRAYVSIZE"], ysize)
        self._set_property(PROPERTY_CODES["SUBARRAYMODE"], 2)

    def get_subarray(self):
        xmin = self._get_property(PROPERTY_CODES["SUBARRAYHPOS"])
        xsize = self._get_property(PROPERTY_CODES["SUBARRAYHSIZE"])
        ymin = self._get_property(PROPERTY_CODES["SUBARRAYVPOS"])
        ysize = self._get_property(PROPERTY_CODES["SUBARRAYVSIZE"])

        return xmin, xsize, ymin, ysize

    def set_trigger_source(self, mode=Trigger.INTERNAL):
        """
        Set the camera trigger source.
        """
        return self._set_property(PROPERTY_CODES["TRIGGERSOURCE"], mode)

    def get_trigger_mode(self):
        return self._get_property(PROPERTY_CODES["TRIGGERSOURCE"])

    def _access_frame(self, frame_idx=-1):
        """
        Access data from a single frame.
        :param frame_idx: index of the frame; set to -1 to access the
        latest frame
        :return: the image corresponding to the specified frame index as
        a 2D numpy array
        """
        width = int(self._get_property(PROPERTY_CODES["IMAGE_WIDTH"]))
        height = int(self._get_property(PROPERTY_CODES["IMAGE_HEIGHT"]))
        rowbytes = int(self._get_property(PROPERTY_CODES["IMAGE_ROWBYTES"]))
        pixel_type = int(self._get_property(PROPERTY_CODES["IMAGE_PIXELTYPE"]))

        bsize = 2 * width * height
        buf = (bsize * c_int32)()
        img_raw = np.empty(bsize, dtype=np.uint16)

        # prepare frame param
        bufframe = DCAMBUF_FRAME()
        bufframe.size = ctypes.sizeof(bufframe)
        bufframe.iFrame = c_int32(frame_idx)
        bufframe.buf = ctypes.cast(byref(buf), POINTER(c_void_p))
        bufframe.rowbytes = c_int32(rowbytes)
        bufframe.left = c_int32(0)
        bufframe.top = c_int32(0)
        bufframe.type = c_int32(0)
        bufframe.width = c_int32(width)
        bufframe.height = c_int32(height)
        bufframe.type = c_int32(pixel_type)

        err = self.lib.dcambuf_lockframe(self.camera_handle, byref(bufframe))
        self._check_err(err)

        ctypes.memmove(img_raw.ctypes.data, bufframe.buf, img_raw.nbytes)

        img = np.zeros((height, width))

        for i in range(height):
            img[i] = img_raw[i * int(width):(i + 1) * int(width)]

        return np.array(img)

    def start_capture(self):
        """
        Start capture.
        """
        err = self.lib.dcambuf_alloc(self.camera_handle, c_int32(10))
        self._check_err(err)

        err = self.lib.dcamcap_start(self.camera_handle, -1)
        self._check_err(err)

    def stop_capture(self):
        """
        Stop capturing. This method will interrupt capturing in SNAP
        mode even if the required number of frames has not been
        reached.
        """
        self.lib.dcamcap_stop(self.camera_handle)

    def register_callback(self, f):
        """
        Register a function to be called from the acquisition thread for each
        new image
        """
        self._frame_call_list.append(f)

    def deregister_callback(self, f):
        """
        Deregister a function from the acquisition thread call list
        """
        if f in self._frame_call_list:
            self._frame_call_list.remove(f)

    def _acquisition_thread(self):
        # open wait handle
        waitopen = DCAMWAIT_OPEN()
        ctypes.memset(byref(waitopen), 0, ctypes.sizeof(waitopen))
        waitopen.size = ctypes.sizeof(waitopen)
        waitopen.hdcam = self.camera_handle

        err = self.lib.dcamwait_open(byref(waitopen))
        self._check_err(err)

        # wait start param
        waitstart = DCAMWAIT_START()
        ctypes.memset(byref(waitstart), 0, ctypes.sizeof(waitstart))
        waitstart.size = ctypes.sizeof(waitstart)
        waitstart.eventmask = c_int32(2)
        waitstart.timeout = c_int32(200)

        while True:
            if self._stopping.is_set():
                break

            err = self.lib.dcamwait_start(waitopen.hwait,
                                          ctypes.pointer(waitstart))

            if err == 0x80000106:
                # Wait timeout
                continue
            elif err == 0x80000102:
                # Abort
                break
            elif err != 1:
                self._check_err(err)

            im = self._access_frame()
            self.frame_buffer.append(im)
            for f in self._frame_call_list:
                f(im)

        self.lib.dcamwait_close(waitopen.hwait)

    def get_all_images(self):
        """
        Get all images stored in the frame buffer.
        """
        if len(self.frame_buffer):
            images= []
            while len(self.frame_buffer) > 0:
                images.append(self.frame_buffer.popleft())
        else:
            images = None

        return images

    def get_image(self):
        """Returns the oldest image in the buffer as a numpy array, or
        None if no new images."""
        if len(self.frame_buffer) == 0:
            return None

        return self.frame_buffer.popleft()

    def wait_for_image(self):
        """Returns the oldest image in the buffer as a numpy array,
        blocking until there is an image available."""
        while True:
            image = self.get_image()
            if image is not None:
                break
            time.sleep(10e-3)

        return image

    def flush_images(self):
        """Delete all images from the buffer"""
        while len(self.frame_buffer) > 0:
            self.frame_buffer.popleft()


    def close(self, uninit=True):

        logger.debug("Stopping acquisition thread")
        self._stopping.set()
        self.lib.dcamwait_abort(self.camera_handle)
        self._thread.join()
        logger.debug("Closing camera connection")
        self.lib.dcamdev_close(self.camera_handle)

        if uninit:
            self.lib.dcamapi_uninit()
            self.lib = None
        self.camera_handle = None