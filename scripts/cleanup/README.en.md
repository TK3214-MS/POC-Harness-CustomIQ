# scripts/cleanup/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Scripts for resetting and cleaning up the demo environment (`reset` / `cleanup` commands, instruction §28).

**Status: Implemented.** [cleanup-azure.sh](cleanup-azure.sh) is a destructive script that deletes actually deployed Azure resources by running `azd down --purge --force`. It requires manual confirmation by entering the environment name and is not invoked through automation or tests.
