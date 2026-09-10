#!/usr/bin/env bash
# Cleanup script for a real Azure deployment created via `azd up` (deployment/azd).
# NOT executed automatically by any test or CI job - this deletes real Azure
# resources and must be run deliberately by a human.
#
# Usage: ./scripts/cleanup/cleanup-azure.sh
set -euo pipefail

echo "This will run 'azd down --purge --force' for the current azd environment."
echo "That PERMANENTLY deletes the resource group and all resources created by 'azd up'."
read -r -p "Type the azd environment name to confirm deletion: " confirm_env

current_env="$(azd env get-values 2>/dev/null | grep '^AZURE_ENV_NAME=' | cut -d'=' -f2- | tr -d '"' || true)"

if [ -z "$current_env" ]; then
  echo "Could not determine the current azd environment (is one selected? 'azd env list'). Aborting."
  exit 1
fi

if [ "$confirm_env" != "$current_env" ]; then
  echo "Confirmation did not match current environment '$current_env'. Aborting."
  exit 1
fi

azd down --purge --force
