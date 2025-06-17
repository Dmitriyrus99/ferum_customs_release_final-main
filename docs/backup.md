# Backup and Restore

This guide describes how to create backups of the Ferum Customs site and restore them if needed.

## Manual backup

Use `scripts/backup.sh` to create a backup with database and files. By default the script uses the site name stored in `SITE` environment variable.

```bash
./scripts/backup.sh
```

Backups are placed under `sites/{site}/private/backups`.

## Manual restore

Provide the path to a previously created archive:

```bash
./scripts/restore.sh /path/to/backup.sql.gz
```

The script will drop the existing database and restore data from the archive.

## Automation via systemd

Timer and service unit files are located in `scripts/systemd`. Install them to `/etc/systemd/system` and enable the timer:

```bash
sudo cp scripts/systemd/ferum_backup.* /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ferum_backup.timer
```

The timer runs `ferum_backup.service` daily and keeps archives for seven days.
