"""Service account credentials."""

import os

from google.auth.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import Resource, build


def get_credentials() -> Credentials:
    """Retrieve service account credentials from JSON key file."""

    service_acc_key_file = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
    if not service_acc_key_file:
        raise ValueError("GCP_SERVICE_ACCOUNT_KEY not defined")

    scopes = ["https://www.googleapis.com/auth/androidpublisher"]

    return service_account.Credentials.from_service_account_file(
        service_acc_key_file, scopes=scopes
    )


def get_publisher_service() -> Resource:
    """Creates a Resource for interacting with the publishing API."""
    credentials = get_credentials()
    return build("androidpublisher", "v3", credentials=credentials)
