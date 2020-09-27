# EthSential - Security analysis for Ethereum smart contracts

[![Test](https://github.com/1140251/Ethsential/workflows/Test/badge.svg)](https://github.com/1140251/Ethsential/actions)
[![Release](https://github.com/1140251/Ethsential/workflows/Release/badge.svg)](https://github.com/1140251/Ethsential/actions)

 <!-- <a href="https://github.com/smartbugs/smartbugs/releases">
        <img alt="Smartbugs release" src="https://img.shields.io/github/release/smartbugs/smartbugs.svg"> -->

EthSential is a security analysis framework for Ethereum smart contracts. It bundles other tools to find vulnerabilities in smart contracts code.

## Features

- A system that uses analysis tools based on Docker images.
- Provides two types of interfaces for the command-line interface and language server protocol ([lsp](https://microsoft.github.io/language-server-protocol/)).
- Normalize the output of the tools in a single file or lsp response.

## Supported Tools

- [Mythril](https://github.com/ConsenSys/mythril)
- [Securify](https://github.com/eth-sri/securify2)
- [Slither](https://github.com/crytic/slither)

## Prerequisites

EthSential requires [Docker](https://docs.docker.com/install) and [Python3](https://www.python.org) to be installed in the system.

## Install

Install from Pypi:

```bash
$ pip install ethsential
```

## Usage

Run `ethsent` without arguments to get more information:

```text
Usage: solhint [actions] [options] <file>

Actions:

```

## IDE Integrations

- **[VS Code](https://marketplace.visualstudio.com/items?itemName=1140251.ethsential)**
