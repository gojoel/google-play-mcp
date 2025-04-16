"""An MCP server for interacting with Google Play Store and managing apps."""

# pylint: disable=no-member, import-error

from typing import Any, List

from fastmcp import Context, FastMCP

from google_play_mcp.credentials import get_publisher_service
from google_play_mcp.model import Apk, AppEdit, Track, TrackReleaseInfo

mcp = FastMCP("Google Play MCP Server")


@mcp.tool()
async def upload_apk(
    package_name: str,
    apk_file: str,
    ctx: Context,
) -> Apk:
    """Uploads an APK and adds to the current edit."""

    service = get_publisher_service()
    edit_id = get_edit_id(service=service, package_name=package_name)

    response = (
        service.edits()
        .apks()
        .upload(editId=edit_id, packageName=package_name, media_body=apk_file)
        .execute()
    )

    await ctx.debug(response)

    return Apk.model_validate(response)


@mcp.tool()
async def update_track(
    package_name: str,
    track: str,
    release_info: TrackReleaseInfo,
    ctx: Context,
) -> Track:
    """Updates a track."""

    service = get_publisher_service()
    edit_id = get_edit_id(service=service, package_name=package_name)

    response = (
        service.edits()
        .tracks()
        .update(
            editId=edit_id,
            track=track,
            packageName=package_name,
            body={"releases": [dict(release_info)]},
        )
        .execute()
    )

    await ctx.debug(response)

    return Track.model_validate(response)


@mcp.tool()
async def commit(
    package_name: str,
    ctx: Context,
) -> AppEdit:
    """Commits an app edit."""

    service = get_publisher_service()
    edit_id = get_edit_id(service=service, package_name=package_name)

    response = (
        service.edits().commit(editId=edit_id, packageName=package_name).execute()
    )

    await ctx.debug(response)

    return AppEdit.model_validate(response)


@mcp.tool()
async def retrieve_apks(package_name: str) -> List[Apk]:
    """Lists all the apks for a given app."""

    service = get_publisher_service()
    edit_id = get_edit_id(service=service, package_name=package_name)

    response = (
        service.edits().apks().list(editId=edit_id, packageName=package_name).execute()
    )

    if not response or "apks" not in response:
        return []

    return [Apk.model_validate(apk) for apk in response["apks"]]


def get_edit_id(service: Any, package_name: str) -> str:
    """Retrieves the edit ID for a package."""

    request = service.edits().insert(packageName=package_name)
    response = request.execute()

    return response["id"]


def run_server():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    run_server()
