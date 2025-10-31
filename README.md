# PyDLLManager

`PyDLLManager` is a Python library designed to simplify the process of loading and interacting with DLL (Dynamic Link Library) files. It allows you to effortlessly load DLLs, call functions, and manage data types using the `ctypes` module in Python.

## Features

- **Load DLLs**: Easily load DLL files into your Python program.
- **Retrieve Functions**: Access functions within the DLL with automatic handling of argument and return types.
- **Thread Safety**: Includes built-in thread safety using `threading.Lock`.
- **Decorator Support**: Use the `DllImprt` decorator to automatically load and call functions from DLLs.

## Installation

To install `PyDLLManager`, simply run the following pip command:

```bash
pip install pydllmanager
```

## Usage

### Basic Usage Example

1. First, you need to initialize a `DLLLoader` object by providing the path to your DLL file.

```python
from pydllmanager import DLLLoader, ctypes_type

dll_path = "path/to/your/dll/file.dll"
loader = DLLLoader(dll_path)
```

2. Then, you can load functions from the DLL using the `get_function` method:

```python
add_func = loader.get_function('add', [ctypes_type(int), ctypes_type(int)], ctypes_type(int))
result = add_func(5, 3)
print(result)  # Expected output: 8 (depends on the DLL function)
```

### Using the `include` Decorator

The `DllImprt` decorator allows you to decorate functions to automatically load them from a DLL.

```python
from pydllmanager import LoaderLibrary

loader = LoaderLibrary("path/to/your/dll/file.dll")
loader.load()

@loader.include()
def add(a: int, b: int) -> int: ... # The function is loaded from the DLL automatically

result = add(5, 3)
print(result)  # Expected output: 8
```

### Example Code

```python
from pydllmanager import DLLLoader, ctypes_type, LoaderLibrary

# Using DLLLoader to load and call a function
loader = DLLLoader("path/to/your/dll/file.dll")
subtract_func = loader.get_function('subtract', [ctypes_type(int), ctypes_type(int)], ctypes_type(int))
result = subtract_func(10, 4)
print(result)  # Expected output: 6 (depends on the DLL function)

loader = LoaderLibrary("path/to/your/dll/file.dll")
loader.load()

# Using DllImprt decorator
@loader.include()
def multiply(a: int, b: int) -> int: ...

result = multiply(2, 3)
print(result)  # Expected output: 6
```

## Exception Handling

`PyDLLManager` defines a custom exception `DLLManagerError` to handle any errors during DLL loading or function retrieval. You can use it as follows:

```python
try:
    loader = DLLLoader("invalid/path/to/dll.dll")
except DLLManagerError as e:
    print(f"Error loading DLL: {e}")
```

## Compatibility

- Supports both **32-bit** and **64-bit** architectures.
- Compatible with most platforms that support the `ctypes` module in Python.

## Contributing

Contributions to `PyDLLManager` are welcome! Feel free to fork the repository, submit issues, or open pull requests with improvements or bug fixes.

1. Fork the repository.
2. Clone it to your local machine.
3. Make your changes and commit them.
4. Push to your fork and create a pull request.

## License

This project is licensed under the MIT License - see the [LICENCE](LICENCE) file for details.

## Author

- **AtomixCore**  
  [GitHub](https://github.com/AtomixCore/PyDLLManager)  
  Version: 1.1.0

---

thank you for using PyDLLManager
