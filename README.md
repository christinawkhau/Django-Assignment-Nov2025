
🧠 Django DB Tool
A command-line utility for orchestrating a full data pipeline—download, transform, import, and export—for Django applications. This tool simplifies running management commands and provides feedback on data volume processed at each stage.

📦 Features
Interactive selection of data type (UserProfiles, Products, Carts)

Sequential execution of Django management commands:

download_<app>

transform_<app>

import_<app>

export_<app>

Automatic reporting of record counts from JSON output files



