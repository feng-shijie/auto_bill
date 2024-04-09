#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ctypes
import inspect
import threading

mutex = threading.Lock()

class Tools_Log:
    #私有成员
    __m_only = None
    __b_only = False
    __m_path = '../log_info'

    def __init__(self):  pass
    def __del__( self):  self.__lib.close()

    #单例
    def __new__(cls, *args, **kwargs):
        if cls.__b_only is False:       raise Exception("This class cannot be instantiated more than once.")
        if cls.__m_only is None:
            cls.__m_only = super().__new__(cls)
            cls.__lib = ctypes.cdll.LoadLibrary('lib/tools_log.so')

            cls.__lib.set_dir_path.restype   = ctypes.c_void_p
            cls.__lib.set_dir_path.argtypes  = [ctypes.c_char_p]
            cls.__lib.set_dir_path(ctypes.c_char_p(cls.__m_path.encode('utf-8')))

            cls.__lib.init.restype  = ctypes.c_void_p
            cls.__lib.init.argtypes = [ctypes.c_bool, ctypes.c_bool]
            cls.__lib.init(True, False)
        return cls.__m_only

    def g():
        mutex.acquire()
        if Tools_Log.__m_only is None:
            Tools_Log.__b_only = True
            Tools_Log.__m_only = Tools_Log()
        mutex.release()
        return Tools_Log.__m_only

    def __get_log_head_info(self, _log):
        stack = inspect.stack()
        if len(stack) > 1:
            caller_frame = stack[len(stack) - 1]
            self.__line      = caller_frame.lineno
            self.__log       = ctypes.c_char_p(_log.encode('utf-8'))
            self.__file_name = ctypes.c_char_p(caller_frame.filename.encode('utf-8'))
            self.__fun_name  = ctypes.c_char_p(caller_frame.function.encode('utf-8'))
            self.__lib.write_log.restype  = ctypes.c_void_p
            self.__lib.write_log.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
            return True
        print("__get_log_head_info fail !!!")
        return False
    
    def log_info( self, _log_str: str):
        if(self.__get_log_head_info(_log_str)):
            self.__lib.write_log(self.__file_name, self.__fun_name, self.__line, 0, self.__log)

    def log_warning(self, _log_str: str):
        if(self.__get_log_head_info(_log_str)):
            self.__lib.write_log(self.__file_name, self.__fun_name, self.__line, 1, self.__log)

    def log_error(self, _log_str: str):
        if(self.__get_log_head_info(_log_str)):
            self.__lib.write_log(self.__file_name, self.__fun_name, self.__line, 2, self.__log)