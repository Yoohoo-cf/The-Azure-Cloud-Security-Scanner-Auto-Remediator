import os
import sys
from azure.identity import DefaultAzureCredentials
from azure.mgmt.storage import StorageManagementClient

RESOURCE_GROUP='rg-security-automation-lab'

def run_security_audit():
    # Authentication using Azure CLI credentials
    credential=DefaultAzureCredentials()

    # Retrieve Azure Subscription ID from environment or Azure CLI context
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        print("[!] Error: AZURE_SUBSCRIPTION_ID environment variable not set.")
        sys.exit(1)


    storage_client = StorageManagementClient(credential, subscription_id)
    print(f"[*] Auditing Storage Accounts in Resource Group: '{RESOURCE_GROUP}'...\n")

    accounts = storage_client.storage_accounts.list_by_resource_group(RESOURCE_GROUP)

    for sa in accounts:
        print(f"-> Inspecting: {sa.name}")

        # Check public nested items rule
        if sa.allow_nested_items_to_be_public:
            print(f" [!] VULNERBILITY DETECTED: Public access allowed on {sa.name}")
            print(f" [*] Executing Auto-Remediation...")

            # Apply fix: Disable public access
            storage_client.storage_accounts.update(
                RESOURCE_GROUP,
                sa.name,
                {"allow_nested_items_to_be_public": False}
            )
            print(" [√] REMEDIATED: Public nested access successfully disabled.\n")
        else:
            print(" [√] COMPLIANT: Public access disabled.\n")

if __name__ == "__main__":
    run_security_audit()