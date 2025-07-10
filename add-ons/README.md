# Sage Dashboard Add Ons

Due to the limitation of plugins and permissions and such, some items do need to be ran from a macro to get around this. These add-ons enable additional information.

## Plugin - Sage Dashboard :: V.2025.07.X

1. Macro OS/VM Disk Space: Gathers the "data_dir" disk space usage.
    1. Sage will connect to a project and call the macro and will stash the results itself
    1. Gathers OS usage 3 layers deep on the data_dir directory
1. Macro OS/VM Filesystem: Basically a `du`
    1. Sage will connect to a project and call the macro and will stash the results itself
    1. Gathers filesystem usage
1. Add the following code to the project library section under
    1. `lib/python/sage_custom/macro_configs.toml`

    ```toml
    [os-vm-filesystem]
    category = "disk_space"
    id = "pyrunnable_sage-dashboard_os-vm-filesystem"
    [os-vm-filesystem.params]

    [os-vm-diskspace]
    category = "disk_space"
    id = "pyrunnable_sage-dashboard_os-vm-diskspace"
    [os-vm-diskspace.params]
    "min_disk_space" = 1
    ```
