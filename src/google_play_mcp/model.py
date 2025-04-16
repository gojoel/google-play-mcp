"""Google Play API models."""

# pylint: disable=invalid-name

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Status(str, Enum):
    """The status of a release."""

    statusUnspecified = "statusUnspecified"
    draft = "draft"
    inProgress = "inProgress"
    halted = "halted"
    completed = "completed"


class ApkBinary(BaseModel):
    """Represents the binary payload of an APK."""

    sha1: str = Field(
        description="A sha1 hash of the APK payload, encoded as a "
        "hex string and matching the output of the sha1sum command."
    )
    sha256: str = Field(
        description="A sha256 hash of the APK payload, "
        "encoded as a hex string and matching the output of the sha256sum command."
    )


class Apk(BaseModel):
    """Represents information about an APK."""

    versionCode: int = Field(
        description="The version code of the APK, as specified in the manifest file."
    )
    binary: ApkBinary = Field(
        description="Information about the binary payload of this APK."
    )


class LocalizedText(BaseModel):
    """Represents localized text in given language."""

    language: str = Field(
        description="Language localization code "
        "(a BCP-47 language tag; for example, 'de-AT' for Austrian German)."
    )
    text: str = Field(description="The text in the given language.")


class CountryTargeting(BaseModel):
    """Represents country targeting specification."""

    countries: List[str] = Field(
        description="Countries to target, specified as two letter CLDR codes."
    )
    includeRestOfWorld: bool = Field(
        description="Include 'rest of world' as well as explicitly targeted countries."
    )


class TrackReleaseInfo(BaseModel):
    """Represents desired changes for a track."""

    name: str = Field(
        description="The release name. Not required to be unique. "
        "If not set, the name is generated from the APK's versionName. "
        "If the release contains multiple APKs, the name is generated from the date."
    )
    versionCodes: List[str] = Field(
        description="Version codes of all APKs in the release. "
        "Must include version codes to retain from previous releases."
    )
    releaseNotes: List[LocalizedText] = Field(
        description="A description of what is new in this release."
    )
    status: Status = Field(description="The status of the release.")
    userFraction: float = Field(
        description="Fraction of users who are eligible for a staged release. "
        "0 < fraction < 1. Can only be set when status is 'inProgress' or 'halted'."
    )
    countryTargeting: CountryTargeting = Field(
        description="Restricts a release to a specific set of countries."
    )
    inAppUpdatePriority: int = Field(
        description="In-app update priority of the release. "
        "All newly added APKs in the release will be considered at this priority. "
        "Can take values in the range [0, 5], with 5 the highest priority. Defaults to 0. "
        "inAppUpdatePriority can not be updated once the release is rolled out"
    )


class Track(BaseModel):
    """Represents a track configuration."""

    track: str = Field(description="Identifier of the track.")
    releases: List[TrackReleaseInfo] = Field(
        description="In a read request, represents all active releases in the track. "
        "In an update request, represents desired changes."
    )


class AppEdit(BaseModel):
    """Represents an app edit."""

    id: str = Field(
        description="Identifier of the edit. Can be used in subsequent API calls."
    )
    expiryTimeSeconds: str = Field(
        description="The time (as seconds since Epoch) at which the edit will expire "
        "and will be no longer valid for use."
    )
