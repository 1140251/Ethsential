# EthSential (Visual Studio Code Extension)

Visual Studio Code integration for EthSential.

EthSential is a security analysis framework for Ethereum smart contracts. It bundles security analysis tools to find vulnerabilities in smart contracts code.

## Features

- Visual Studio Code integration of security analysis tools for Solidity smart contracts.
- Analyze current active Solidity file.
- Present code diagnostic resulst in source code as native Visual Studio Code information/warnings/errors.
- Handle installation of security analysis tools using Docker API.

## Supported Tools

- [Mythril](https://github.com/ConsenSys/mythril)
- [Securify](https://github.com/eth-sri/securify2)
- [Slither](https://github.com/crytic/slither)

## Prerequisites

The Visual Studio Code integration requires [Docker](https://docs.docker.com/install), [Python3](https://www.python.org) and [EthSential](https://pypi.python.org/pypi/ethsential) to be installed in the system.

## Usage

Run the extension from the command palette by pressing (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac)
and typing `EthSential`. Two commands should appear in the command palette.

<img src="https://raw.githubusercontent.com/1140251/Ethsential/master/vscode-client/resources/vscode-analysis-execution-select.PNG" alt="select-command" width="900"/>

When the analysis is completed the diagonistics should be present in the source code and Problems tab.

<img src="https://raw.githubusercontent.com/1140251/Ethsential/master/vscode-client/resources/vscode-analysis-execution-complete.PNG" alt="complete-command" width="900"/>

## How to contribute

Please read [CONTRIBUTING.md](https://github.com/1140251/Ethsential/blob/master/CONTRIBUTING.md) for details about how to proceed.

Everyone interacting in Ethsential and its sub-projects' codebases and issue trackers, is expected to follow the Contributor Covenant [code of conduct](https://github.com/1140251/Ethsential/blob/master/CODE_OF_CONDUCT.md).

## License

This project is licensed under the Apache-2.0 license - see the [LICENSE.md](https://github.com/1140251/Ethsential/blob/master/LICENSE.md) file for details.
