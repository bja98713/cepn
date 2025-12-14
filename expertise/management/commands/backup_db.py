from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Backup the SQLite database and keep the last three daily snapshots."

    def handle(self, *args, **options):
        database_name = settings.DATABASES.get("default", {}).get("NAME")
        if not database_name:
            self.stderr.write(self.style.ERROR("No default database path found in settings."))
            return

        db_path = Path(database_name)
        if not db_path.exists():
            self.stderr.write(self.style.ERROR(f"Database file not found: {db_path}"))
            return

        backups_root = Path(settings.BASE_DIR) / "backups"
        backups_root.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{db_path.stem}_{timestamp}{db_path.suffix}"
        backup_path = backups_root / backup_name

        shutil.copy2(db_path, backup_path)
        self.stdout.write(self.style.SUCCESS(f"Backup created: {backup_path}"))

        pattern = f"{db_path.stem}_*{db_path.suffix}"
        existing_backups = sorted(
            backups_root.glob(pattern),
            key=lambda item: item.stat().st_mtime,
            reverse=True,
        )

        for outdated in existing_backups[3:]:
            try:
                outdated.unlink()
                self.stdout.write(f"Removed old backup: {outdated}")
            except OSError as exc:
                self.stderr.write(self.style.WARNING(f"Unable to delete {outdated}: {exc}"))
