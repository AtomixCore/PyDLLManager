"""
PyDLLManager - A library for effortlessly loading DLL files in Python.

This module provides a class and decorator for loading and accessing functions
from dynamic link libraries (DLLs) using the ctypes module.

Author: AtomixCore
Version: 1.1.0
Github: https://github.com/AtomixCore
"""

import ctypes
import os
import platform
import functools
import threading
import logging
from typing import Any, Callable

__all__ = ['DLLLoader', 'LoaderLibrary', 'ctypes_type', 'DLLManagerError']

class DLLManagerError(Exception):
  """Custom exception class for PyDLLManager errors."""
  pass

class DLLLoader:
  """
  A class to load and interact with DLL files.

  Attributes:
    dll: The loaded DLL object.
    lock: A threading lock for thread-safe operations.

  Methods:
    get_function: Retrieve a function from the DLL with specified argument
          and return types.
  """
  def __init__(self, dll_path: str):
      """
      Initialize the DLLLoader with the path to the DLL file.

      Args:
        dll_path (str): The path to the DLL file.

      Raises:
        FileNotFoundError: If the specified DLL file does not exist.
        DLLManagerError: If loading the DLL file fails.
      """
      self.lock = threading.Lock()
      if not os.path.exists(dll_path):
        raise FileNotFoundError(f"Library not found: {dll_path}")

      # Check the system's architecture
      arch = platform.architecture()[0]
      try:
        with self.lock:
          if arch == "32bit":
            self.dll = ctypes.cdll.LoadLibrary(dll_path)
          elif arch == "64bit":
            self.dll = ctypes.cdll.LoadLibrary(dll_path)
          else:
            raise DLLManagerError(f"Unsupported architecture: {arch}")
      except OSError as e:
        raise DLLManagerError(f"Failed to load library: {e}")

  def get_function(self, func_name: str, argtypes=None, restype=None):
    """
    Retrieve a function from the DLL with the specified argument and return types.

    Args:
      func_name (str): The name of the function to retrieve.
      argtypes (list, optional): A list of argument types for the function.
      restype (type, optional): The return type of the function.

    Returns:
      function: The retrieved function with specified argument and return types.

    Raises:
      AttributeError: If the function is not found in the DLL.
      DLLManagerError: If retrieving the function fails.
    """
    try:
      with self.lock:
        func = getattr(self.dll, func_name)
        if argtypes:
          func.argtypes = argtypes
        func.restype = restype
        return func
    except AttributeError:
      raise AttributeError(f"Cannot find function {func_name} in this library")
    except Exception as e:
      raise DLLManagerError(f"Error retrieving function {func_name}: {e}")


def ctypes_type(py_type: type) -> Any:
  """
  Map Python types to ctypes types.

  Args:
    py_type (type): The Python type to map.

  Returns:
    type: The corresponding ctypes type.
  """
  mapping = {
    int: ctypes.c_int,
    float: ctypes.c_double,
    str: ctypes.c_char_p,
    bool: ctypes.c_bool,
    None: ctypes.c_void_p,
    Any: ctypes.c_void_p,
    str: ctypes.c_wchar_p,
  }
  return mapping.get(py_type, ctypes.c_void_p)


class LoaderLibrary:
  def __init__(self, dll_file: str, _logging: bool = False):
    """
    Args:
      dll_path (str): The path to the DLL file.
      logging (bool, optional): Whether to enable logging of function calls. Defaults to False.
    """

    self.dll_loader_cache = {}
    self.dll_file = dll_file
    logging.basicConfig(level=logging.INFO)
    self._logging = _logging
  
  def load(self):
    if self.dll_file not in self.dll_loader_cache:
      self.dll_loader_cache[self.dll_file] = DLLLoader(self.dll_file)
  
  def include(self) -> Callable:
    """
    A decorator to load a DLL function and call it with specified arguments.

    Returns:
      Callable: The decorated function with the loaded DLL function call.
    """
    def decorator(func: Callable) -> Callable:
      func_name = func.__name__

      @functools.wraps(func)
      def wrapper(*args, **kwargs) -> Any:
        loader = self.dll_loader_cache[self.dll_file]
        annotations = func.__annotations__
        argtypes = [ctypes_type(annotations.get(param, Any)) for param in annotations if param != 'return']
        restype = ctypes_type(annotations.get('return', None))

        dll_func = loader.get_function(func_name, argtypes, restype)
        if self._logging:
          logging.info(f"import {func_name}, args={args}, kwargs={kwargs}")
          logging.info(f"type data argtypes={argtypes}, restype={restype}")

        result = dll_func(*args, **kwargs)
        if restype == ctypes.c_char_p and result:
          return (result.decode("utf-8") if result is not None else None)
        return result
      return wrapper
    return decorator