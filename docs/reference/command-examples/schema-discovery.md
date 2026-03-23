# Schema Discovery

### `nbx groups`

=== ":material-console: Command"

    ```bash
    nbx groups
    ```

=== ":material-text-box-outline: Output"

    ```text
    circuits
    core
    dcim
    extras
    ipam
    plugins
    tenancy
    users
    virtualization
    vpn
    wireless
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">2.299s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx resources dcim`

=== ":material-console: Command"

    ```bash
    nbx resources dcim
    ```

=== ":material-text-box-outline: Output"

    ```text
    cable-terminations
    cables
    connected-device
    console-port-templates
    console-ports
    console-server-port-templates
    console-server-ports
    device-bay-templates
    device-bays
    device-roles
    device-types
    devices
    front-port-templates
    front-ports
    interface-templates
    interfaces
    inventory-item-roles
    inventory-item-templates
    inventory-items
    locations
    mac-addresses
    manufacturers
    module-bay-templates
    module-bays
    module-type-profiles
    module-types
    modules
    platforms
    power-feeds
    power-outlet-templates
    power-outlets
    power-panels
    power-port-templates
    power-ports
    rack-reservations
    rack-roles
    rack-types
    racks
    rear-port-templates
    rear-ports
    regions
    site-groups
    sites
    virtual-chassis
    virtual-device-contexts
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.874s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx ops dcim devices`

=== ":material-console: Command"

    ```bash
    nbx ops dcim devices
    ```

=== ":material-text-box-outline: Output"

    ```text
                                      dcim/devices                                  
    ┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Method ┃ Path                             ┃ Operation ID                     ┃
    ┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ DELETE │ /api/dcim/devices/               │ dcim_devices_bulk_destroy        │
    │ GET    │ /api/dcim/devices/               │ dcim_devices_list                │
    │ PATCH  │ /api/dcim/devices/               │ dcim_devices_bulk_partial_update │
    │ POST   │ /api/dcim/devices/               │ dcim_devices_create              │
    │ PUT    │ /api/dcim/devices/               │ dcim_devices_bulk_update         │
    │ DELETE │ /api/dcim/devices/{id}/          │ dcim_devices_destroy             │
    │ GET    │ /api/dcim/devices/{id}/          │ dcim_devices_retrieve            │
    │ PATCH  │ /api/dcim/devices/{id}/          │ dcim_devices_partial_update      │
    │ PUT    │ /api/dcim/devices/{id}/          │ dcim_devices_update              │
    │ POST   │ /api/dcim/devices/{id}/render-c… │ dcim_devices_render_config_crea… │
    └────────┴──────────────────────────────────┴──────────────────────────────────┘
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">2.536s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx resources ipam`

=== ":material-console: Command"

    ```bash
    nbx resources ipam
    ```

=== ":material-text-box-outline: Output"

    ```text
    aggregates
    asn-ranges
    asns
    fhrp-group-assignments
    fhrp-groups
    ip-addresses
    ip-ranges
    prefixes
    rirs
    roles
    route-targets
    service-templates
    services
    vlan-groups
    vlan-translation-policies
    vlan-translation-rules
    vlans
    vrfs
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">2.168s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---
