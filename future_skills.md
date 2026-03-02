
### Initial data pattern

Apps expose initial data via `AppConfig.ready()` → management commands. See `example/apps.py` for the pattern. The files are in `<app>/initial_data.py`.


### Status workflow

`StatusControl` (primary key = string slug, e.g. `pre_start`, `draft`) drives state machines for survey registration, sending, and validation workflows. Status slugs are referenced directly as IDs throughout the codebase (e.g. `status_register_id = 'pre_start'`).



### Institution.save() side effects

`Institution.save()` automatically creates `Survey`, `AxisValue`, and `GoodPracticePackage` records for all existing periods filtered by `year_start`/`year_end`. Be aware of this cascade when creating or modifying Institution records in tests or migrations.