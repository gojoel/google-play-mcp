"""An MCP server for interacting with Google Play Store and managing apps."""

# pylint: disable=no-member, import-error

from typing import Dict, List

from fastmcp import FastMCP
from google.oauth2 import service_account
from googleapiclient import discovery

mcp = FastMCP("Google Play MCP Server")


@mcp.tool()
async def retrieve_app_apks(package_name: str) -> List[Dict[str, str]]:
    """Lists all the apks for a given app."""

    scopes = ["https://www.googleapis.com/auth/androidpublisher"]
    service_acc_key_file = "key.json"

    credentials = service_account.Credentials.from_service_account_file(
        service_acc_key_file, scopes=scopes
    )

    service = discovery.build("androidpublisher", "v3", credentials=credentials)

    request = service.edits().insert(packageName=package_name)
    response = request.execute()
    edit_id = response["id"]

    apks_result = (
        service.edits().apks().list(editId=edit_id, packageName=package_name).execute()
    )

    if not apks_result or "apks" not in apks_result:
        return []

    return apks_result["apks"]


if __name__ == "__main__":
    mcp.run()
