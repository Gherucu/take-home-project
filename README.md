
# Take-Home Project

## Description

This project is tailored for a DevOps job interview, focusing on demonstrating expertise in Docker container management and Python-based automation. It features a Python application that orchestrates Docker containers on a custom network, enabling simulated network interactions and testing. The setup leverages Makefile for task automation and Poetry for dependency management, ensuring a streamlined workflow from installation to execution.

## Features

- **Docker Container Orchestration**: Dynamically creates and manages Docker containers within a custom network environment.
- **Python Automation**: Utilizes Python scripts for network and container setup, including network communication tests.
- **Makefile Integration**: Simplifies command execution for setup, testing, and cleanup through Makefile tasks.
- **Poetry for Dependency Management**: Ensures project dependencies are consistently managed and installed.

## Prerequisites

Before getting started, ensure you have the following installed on your system:
- Docker: For containerization and network management.
- Python 3.11 or higher: Required for running the Python scripts.
- Poetry: Used for managing Python dependencies in an isolated environment.


## Installation

### Installing Make

Make is a build automation tool that automatically builds executable programs and libraries from source code. It reads a file named `Makefile` to figure out which source files need to be compiled and how to compile them.

-   **Linux:**

`sudo apt-get install make` 

-   **Mac:**

`brew install make` 

### Installing Poetry

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

```pip install poetry```


##
1. **Clone the Project**:
   ```bash
   git clone https://gitlab.com/alexgheara/take-home-project
   cd take-home-project
   ```

2. **Install Dependencies**:
   Use the Makefile command to install Python dependencies via Poetry:
   ```bash
   make install
   ```

## Usage

To run the application, use the following commands as per your requirements:

- **Running the Application**:
  ```bash
  make run n=<number-of-targets>
  ```
  Replace `<number-of-targets>` with the number of target Docker containers you wish to create and test against.

- **Running Tests**:
  Execute unit tests to ensure the application functions as expected:
  ```bash
  make test
  ```

- **Cleanup**:
  Remove all created Docker containers and networks to reset the environment:
  ```bash
  make clean
  ```

## Development

The project is structured as follows:
- `Makefile` contains tasks for running the application, installing dependencies, running tests, and cleaning up Docker artifacts.
- `main.py` is the main Python script that orchestrates Docker containers, setting up a network, creating containers, conducting ping tests, and cleaning up.
- `pyproject.toml` defines project metadata and dependencies managed by Poetry.
- `test_main_pytest.py` includes tests for the Python script, utilizing pytest and mocking Docker interactions for unit testing.

## Contributing

We welcome contributions! Please feel free to submit pull requests or open issues to discuss proposed changes or improvements.

## License

This project is currently not open for unauthorized use. For any use beyond viewing and reviewing the code for hiring purposes, please contact [alexandrugheara@yahoo.com](mailto:alexandrugheara@yahoo.com).

## Contact

For any questions or comments regarding this project, please reach out to [alexandrugheara@yahoo.com](mailto:alexandrugheara@yahoo.com).
