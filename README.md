# Confar

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/sanjairocky/Confar/pages%2Fpages-build-deployment)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

"Configuration Aggregator and Runner" is an application that consolidates configuration data and executes tasks or processes based on that configuration.

Confar is a Python CLI and library for configuration management, designed to aggregate and manage configuration data and execute tasks based on that configuration.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install `confar` easily using the provided installation script by running it with the `sh` command.

**Note**: Make sure you have a working internet connection before proceeding.

### Installation Steps

1. Open your terminal.

2. Download and run the installation script using `sh`:

   ```bash
   sh -c "$(curl -fsSL https://sanjairocky.github.io/confar/install.sh)"
   ```

   or

   Alternatively, you can use wget to download and execute the script:

   ```bash
   sh -c "$(wget https://sanjairocky.github.io/confar/install.sh -O -)"
   ```

   or

   Alternatively, you can use pip to install:

   ```bash
   pip install confar
   ```

3. To verify that confar is installed successfully, you can run the following command:

   ```bash
   confar --version
   ```

## Usage

### CLI

```bash
confar <command> [options]
```

For detailed CLI documentation and examples, refer to the CLI documentation.

### Library

```python
import confar

# library usage
```

For detailed library documentation and examples, refer to the [Library documentation](https://sanjairocky.github.io/docs/confar).

## Contributing

We welcome contributions from the community. If you'd like to contribute to Confar, please read our Contributing Guidelines and Code of Conduct.

## License

Confar is licensed under the MIT License - see the LICENSE file for details.
