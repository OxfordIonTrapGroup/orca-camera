ERROR_CODES = {
    # status error
    0x80000101: "API cannot process in busy state.",
    0x80000103: "API requires ready state",
    0x80000104: "API requires stable or unstable state.",
    0x80000105: "API does not support in unstable state.",
    0x80000107: "API requires busy state.",
    0x80000110: "some resource is exclusive and already used",
    0x80000302: "something happens near cooler",
    0x80000303:
    "no trigger when necessary. Some camera supports this error.",
    0x80000304: "camera warns its temperature",
    0x80000305:
    "input too frequent trigger. Some camera supports this error.",

    # wait error
    0x80000102: "abort process",
    0x80000106: "timeout",
    0x80000301: "frame data is lost",
    0x80000f06: "frame is lost but reason is low lever driver's bug",
    0x80000321: "hpk format data is invalid data",

    # initialization error
    0x80000201: "not enough resource except memory",
    0x80000203: "not enough memory",
    0x80000204: "no sub module",
    0x80000205: "no driver",
    0x80000206: "no camera",
    0x80000207: "no grabber",
    0x80000208: "no combination on registry",
    0x80001001: "ECATED",
    0x80000211: "dcam_init() found invalid module",
    0x80000212: "invalid serial port",
    0x81001001: "the bus or driver are not available",
    0x82001001: " camera report error during opening",
    0x80001002: "need to update frame grabber firmware to use the camera",

    # calling error
    0x80000806: "invalid camera",
    0x80000807: "invalid camera handle",
    0x80000808: "invalid parameter",
    0x80000821: "invalid property value",
    0x80000822: "value is out of range",
    0x80000823: "the property is not writable",
    0x80000824: "the property is not readable",
    0x80000825: "the property id is invalid",
    0x80000826: "old API cannot present the value because only new API need to be used",
    0x80000827: "this error happens DCAM get error code from camera unexpectedly",
    0x80000828: "there is no altenative or influence id, or no more property id",
    0x80000829: "the property id specifies channel but channel is invalid",
    0x8000082a: "the property id specifies channel but channel is invalid",
    0x8000082b: "the combination of subarray values are invalid..",
    0x8000082c: "the property cannot access during this DCAM STATUS",
    0x8000082d: "the property does not have value text",
    0x8000082e: "at least one property value is wrong",
    0x80000830: "the paired camera does not have same parameter",
    0x80000832: "framebundle mode should be OFF under current property settings",
    0x80000833: "the frame index is invalid",
    0x80000834: "the session index is invalid",
    0x80000838: "not take the dark and shading correction data yet.",
    0x80000839: "each channel has own property value so can't return overall property value.",
    0x8000083a: "each view has own property value so can't return overall property value.",
    0x8000083b: "the frame count is larger than device momory size on using device memory.",
    0x8000083c: "the capture mode is sequence on using device memory.",
    0x8000083f: "the sysmem memory size is too small. PC doesn't have enough memory or is limited memory by 32bit OS.",
    0x80000f03: "camera does not support the function or property with current settings",

    # camera or bus trouble */
    0x83001002: "failed to read data from camera",
    0x83001003: "failed to write data to the camera",
    0x83001004: "conflict the com port name user set",
    0x83001005: "Optics part is unplugged so please check it.",
    0x83001006: "fail calibration",
    0x83001011: "mismatch between camera output(connection) and frame grabber specs",

    # /* '0x84000100' - '0x840001FF', DCAMERR_INVALIDMEMBER_x */
    0x84000103: "3th member variable is invalid value",
    0x84000105: "5th member variable is invalid value",
    0x84000107: "7th member variable is invalid value",
    0x84000108: "7th member variable is invalid value",
    0x84000109: "9th member variable is invalid value",
    0x84001001: "DCAMREC failed to open the file",
    0x84001002: "DCAMREC is invalid handle",
    0x84001003: "DCAMREC failed to write the data",
    0x84001004: "DCAMREC failed to read the data",
    0x84001005: "DCAMREC is recording data now",
    0x84001006: "DCAMREC writes full frame of the session",
    0x84001007: "DCAMREC handle is already occupied by other HDCAM",
    0x84001008: "DCAMREC is set the large value to user data size",
    0x84002001: "DCAMWAIT is invalid handle",
    0x84002002: "DCAM Module Version is older than the version that the camera requests",
    0x84002003: "Camera returns the error on setting parameter to limit version",
    0x84002004: "Camera is running as a factory mode",
    0x84003001: "sigunature of image header is unknown or corrupted",
    0x84003002: "version of image header is newer than version that used DCAM supports",
    0x84003003: "image header stands error status",
    0x84004004: "image header value is strange",
    0x84004005: "image content is corrupted",

    # calling error for DCAM-API 2.1.3
    0x80000801: "unknown message id",
    0x80000802: "unknown string id",
    0x80000803: "unkown parameter id",
    0x80000804: "unknown bitmap bits type",
    0x80000805: "unknown frame data type",

    # internal error
    0: "no error, nothing to have done",
    0x80000f00: "installation progress",
    0x80000f01: "internal error",
    0x80000f04: "calling after process terminated",
    # '0x80000f05': "",
    0x80000f07: "HDCAM lost connection to camera",
    0x80000f02: "not yet implementation",
    0x80000f09:
    "the frame waiting re-load from hardware buffer with SNAPSHOT of DEVICEBUFFER MODE",
    0xa4010003: "DCAMAPI_INIT::initoptionbytes is invalid",
    0xa4010004: "DCAMAPI_INIT::initoption is invalid",
    # DCAMERR_INITOPTION_COLLISION_BASE='0xa401C000',
    # DCAMERR_INITOPTION_COLLISION_MAX= '0xa401FFFF',

    # /* Between DCAMERR_INITOPTION_COLLISION_BASE and DCAMERR_INITOPTION_COLLISION_MAX
    # means there is collision with initoption in DCAMAPI_INIT. */
    # /* The value "(error code) - DCAMERR_INITOPTION_COLLISION_BASE" indicates
    # the index which second INITOPTION group happens. */
    0xE0100110: "the trigger mode is internal or syncreadout on using device memory.",

    # success
    1: "no error, general success code, app should check the value is positive"
}
