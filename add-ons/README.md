# Sage Dashboard Add Ons

Due to the limitation of plugins and permissions and such, some items do need to be ran from a macro to get around this. These add-ons enable additional information.

## Plugin - Sage Dashboard

1. Macro OS/VM Disk Space: Gathers the "data_dir" disk space usage.
    1. V.2025.06.25.1
    1. Install plugin, add macro to data gather scenario as a 'second' step


[os-vm-filesystem]
category = "disk_space"
id = "pyrunnable_sage-dashboard_os-vm-filesystem"
[os-vm-filesystem.params]

[os-vm-diskspace]
category = "disk_space"
id = "pyrunnable_sage-dashboard_os-vm-diskspace"
[os-vm-diskspace.params]
"min_disk_space" = 1