import ctypes
import ctypes.util

ASS_FUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_void_p)

class PySequenceMethods(ctypes.Structure):
    _fields_ = [
        ("sq_length", ctypes.c_void_p),
        ("sq_concat", ctypes.c_void_p),
        ("sq_repeat", ctypes.c_void_p),
        ("sq_item", ctypes.c_void_p),
        ("sq_slice", ctypes.c_void_p),
        ("sq_ass_item", ASS_FUNC),
        ("sq_ass_slice", ctypes.c_void_p),
        ("sq_contains", ctypes.c_void_p),
        ("sq_inplace_concat", ctypes.c_void_p),
        ("sq_inplace_repeat", ctypes.c_void_p),
    ]

class PyTypeObject(ctypes.Structure):
    pass

PyTypeObject._fields_ = (
        ("ob_refcnt", ctypes.c_int),
        ("ob_type", ctypes.c_void_p),
        ("ob_size", ctypes.c_int),
        ("tp_name", ctypes.c_char_p),
        ("tp_basicsize", ctypes.c_ssize_t),
        ("tp_itemsize", ctypes.c_ssize_t),
        ("tp_dealloc", ctypes.c_void_p),
        ("tp_print", ctypes.c_void_p),
        ("tp_getattr", ctypes.c_void_p),
        ("tp_setattr", ctypes.c_void_p),
        ("tp_reserved", ctypes.c_void_p),
        ("tp_repr", ctypes.c_void_p),
        ("tp_as_number", ctypes.c_void_p),
        ("tp_as_sequence", ctypes.POINTER(PySequenceMethods)),
        ("tp_as_wrapping", ctypes.c_void_p),
        ("tp_hash", ctypes.c_void_p),
        ("tp_call", ctypes.c_void_p),
    )

class PyObject(ctypes.Structure):
    _fields_ = [
        ('ob_refcnt', ctypes.c_ssize_t),
        ('ob_type', ctypes.POINTER(PyTypeObject)),
    ]

libpython = ctypes.PyDLL(ctypes.util.find_library("python"))

@ASS_FUNC
def sq_ass_item(obj, size, item):
    pyobj = PyObject.from_address(obj)
    old_refcnt = pyobj.ob_refcnt
    pyobj.ob_refcnt = 1
    ret =  libpython.PyTuple_SetItem(ctypes.c_void_p(obj), ctypes.c_ssize_t(size), ctypes.c_void_p(item))
    pyobj.ob_refcnt = old_refcnt
    return ret

tup = (1, 2, 3)
ptr = PyObject.from_address(id(tup))
ptr.ob_type.contents.tp_as_sequence.contents.sq_ass_item = sq_ass_item
