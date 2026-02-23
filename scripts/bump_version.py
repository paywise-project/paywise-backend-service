#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
import json
from pathlib import Path
from typing import Optional


def load_dotenv(env_path: Path) -> dict:
    """Minimal .env loader — no external dependency required."""
    env_vars = {}
    if not env_path.exists():
        return env_vars
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            # Strip optional surrounding quotes
            value = value.strip().strip('"').strip("'")
            env_vars[key] = value
    return env_vars


class TelegramNotifier:
    API_URL = "https://telapi.fazelidev.ir/send"

    def __init__(self, token: Optional[str], chat_id: Optional[str], topic_id: Optional[str]) -> None:
        self.token = token
        self.chat_id = int(chat_id) if chat_id else None
        self.topic_id = int(topic_id) if topic_id else None

    def is_configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def send(self, message: str) -> None:
        if not self.is_configured():
            print("⚠️  Telegram not configured (missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID). Skipping notification.")
            return

        payload: dict = {
            "token": self.token,
            "message": message,
            "chat_id": self.chat_id,
        }
        if self.topic_id is not None:
            payload["topic_id"] = self.topic_id

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.API_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"📨 Telegram notification sent (HTTP {resp.status})")
        except urllib.error.HTTPError as e:
            print(f"⚠️  Telegram notification failed: HTTP {e.code} — {e.reason}")
        except urllib.error.URLError as e:
            print(f"⚠️  Telegram notification failed: {e.reason}")
        except Exception as e:
            print(f"⚠️  Telegram notification failed: {e}")


def build_telegram_message(
    app_name: Optional[str],
    deployer: Optional[str],
    new_version: str,
    user_message: Optional[str],
) -> str:
    lines = []

    # Header
    if app_name:
        lines.append(f"🚀 *{app_name}* — new version deployed!")
    else:
        lines.append("🚀 New version just deployed!")

    lines.append("")

    # Who deployed
    deployer_str = deployer or "unknown"
    lines.append(f"👤 *Deployed by:* {deployer_str}")

    # Version
    lines.append(f"🏷️  *Version:* `{new_version}`")

    # Optional message
    if user_message:
        lines.append(f"📝 *Message:* {user_message}")

    return "\n".join(lines)


def get_git_user_name() -> Optional[str]:
    """Try to read user.name from git config."""
    try:
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            check=True,
        )
        name = result.stdout.strip()
        return name if name else None
    except subprocess.CalledProcessError:
        return None


def get_project_name() -> Optional[str]:
    """Return the current working directory's name as the project/app name."""
    try:
        # Prefer the git repo root's folder name
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        repo_root = result.stdout.strip()
        if repo_root:
            return Path(repo_root).name
    except subprocess.CalledProcessError:
        pass
    # Fallback to cwd name
    return Path.cwd().name or None


class LibVersionBumper:
    def __init__(self) -> None:
        self.valid_bump_types = ["major", "minor", "patch"]
        self._sync_with_remote()

        # Load .env from repo root (or cwd)
        env_path = self._find_env_file()
        env_vars = load_dotenv(env_path)

        # Merge into os.environ so callers can also override via real env vars
        for k, v in env_vars.items():
            os.environ.setdefault(k, v)

        # Build notifier — all values fall back to None if missing
        self.notifier = TelegramNotifier(
            token=os.environ.get("TELEGRAM_BOT_TOKEN") or None,
            chat_id=os.environ.get("TELEGRAM_CHAT_ID") or None,
            topic_id=os.environ.get("TELEGRAM_TOPIC_ID") or None,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_env_file(self) -> Path:
        """Return the .env path at the git repo root, falling back to cwd."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
            )
            repo_root = Path(result.stdout.strip())
        except subprocess.CalledProcessError:
            repo_root = Path.cwd()
        return repo_root / ".env"

    def _parse_version(self, version_str: str) -> tuple[tuple[int, int, int], Optional[str]]:
        """Parse version string into components and optional suffix."""
        match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9]+))?$", version_str)
        if not match:
            raise ValueError(f"Invalid version format: {version_str}")

        major, minor, patch = map(int, match.groups()[:3])
        suffix = match.group(4) if match.group(4) else None
        return (major, minor, patch), suffix

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_current_version(self) -> tuple[str, tuple[int, int, int], Optional[str]]:
        """Get the current version from git tags."""
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                check=True,
            )
            current_version = result.stdout.strip().lstrip("v")
            version_tuple, suffix = self._parse_version(current_version)
            return current_version, version_tuple, suffix

        except subprocess.CalledProcessError:
            print("No existing tags found. Starting from v0.0.0")
            return "0.0.0", (0, 0, 0), None
        except ValueError as e:
            print(f"Error parsing version: {e}")
            sys.exit(1)

    def calculate_new_version(
        self,
        current_version: tuple[int, int, int],
        current_suffix: Optional[str],
        bump_type: str,
        new_suffix: Optional[str],
    ) -> str:
        """Calculate the new version based on bump type and suffix."""
        major, minor, patch = current_version

        if current_suffix is not None and new_suffix is None:
            # Just strip the suffix, don't bump
            version_str = f"{'.'.join(map(str, current_version))}"
        else:
            if bump_type == "major":
                new_version = (major + 1, 0, 0)
            elif bump_type == "minor":
                new_version = (major, minor + 1, 0)
            elif bump_type == "patch":
                new_version = (major, minor, patch + 1)
            else:
                raise ValueError(f"Invalid bump type: {bump_type}")

            version_str = f"{'.'.join(map(str, new_version))}"

        if new_suffix:
            version_str += f"-{new_suffix}"

        return version_str

    def create_and_push_tag(self, new_version: str, message: Optional[str] = None) -> None:
        """Create and push a new git tag."""
        try:
            self._sync_with_remote(tags_only=True)

            tag_version = f"{new_version}"
            result = subprocess.run(["git", "tag", "-l", tag_version], capture_output=True, text=True, check=True)
            if tag_version in result.stdout:
                print(f"Tag {tag_version} already exists!")
                sys.exit(1)

            tag_message = message or f"Release {tag_version}"
            subprocess.run(["git", "tag", "-a", tag_version, "-m", tag_message], check=True)
            subprocess.run(["git", "push", "origin", tag_version], check=True)

            print(f"✅ Successfully created and pushed tag: {tag_version}")
            print(f"   Tag message: {tag_message}")

        except subprocess.CalledProcessError as e:
            print(f"Error in git operations: {e}")
            sys.exit(1)

    def bump_version(
        self,
        bump_type: str,
        message: Optional[str] = None,
        suffix: Optional[str] = None,
        dry_run: bool = False,
    ) -> None:
        """Main function to bump version."""
        if bump_type not in self.valid_bump_types:
            print(f"Invalid bump type. Must be one of: {self.valid_bump_types}")
            sys.exit(1)

        current_version_str, current_version_tuple, current_suffix = self.get_current_version()
        print(f"Current version: {current_version_str}{f'-{current_suffix}' if current_suffix else ''}")

        new_version = self.calculate_new_version(current_version_tuple, current_suffix, bump_type, suffix)
        print(f"New version will be: {new_version}")
        if message:
            print(f"Tag message will be: {message}")

        if dry_run:
            print("Dry run — would create tag:", new_version)
            # Still show the Telegram message preview
            tg_msg = build_telegram_message(
                app_name=get_project_name(),
                deployer=get_git_user_name(),
                new_version=new_version,
                user_message=message,
            )
            print("\n--- Telegram message preview ---")
            print(tg_msg)
            print("--------------------------------")
            return

        if input("Proceed with version bump? [y/N]: ").lower() != "y":
            print("Version bump cancelled.")
            sys.exit(0)

        self.create_and_push_tag(new_version, message)

        # Send Telegram notification
        tg_msg = build_telegram_message(
            app_name=get_project_name(),
            deployer=get_git_user_name(),
            new_version=new_version,
            user_message=message,
        )
        self.notifier.send(tg_msg)

    def _sync_with_remote(self, tags_only: bool = False) -> None:
        if tags_only:
            subprocess.run(["git", "fetch", "--tags"], capture_output=True, text=True, check=True)
        else:
            subprocess.run(["git", "fetch", "--all"], capture_output=True, text=True, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump version using git tags")
    parser.add_argument("bump_type", choices=["major", "minor", "patch"], help="Type of version bump")
    parser.add_argument("-m", "--message", help="Custom tag message (optional)")
    parser.add_argument("--suffix", help="Add a version suffix (e.g., 'dev', 'test')")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without making changes")

    args = parser.parse_args()

    try:
        bumper = LibVersionBumper()
        bumper.bump_version(args.bump_type, args.message, args.suffix, args.dry_run)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
