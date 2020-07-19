# Google Drive Report Archiving API.
integration with GDrive that allows file reports from different business units to be archived and organized properly, through a simple REST API.

Uses Django, Flask and the GDrive API.

How to use:
The initial archive folder structure should be:
ArchiveBaseFolder
├── BusinessUnit1
| └── BusinessUnit1Label.noborrar
├── BusinessUnit2
| └── BusinessUnitLabel.noborrar

and so on. From then, this integration will handle archiving it in different folders according to date.

The following calls are available:

- /api/archive/addfile/<client_label>/<file_name> (POST)
The body should contain the BASE64 form of the file to archive, <client_label> is the business unit LABEL, the name of the .noborrar file. <file_name> should contain the filename including the file extension.

/api/archive/updateclients (POST)
This call force-checks for new business units, this is not necessary except for troubleshooting. Normally, trying to add a file to a currently non-cached business unit folder will trigger this automatically.


