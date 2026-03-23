# Dynamic Commands

### `nbx dcim --help`

=== ":material-console: Command"

    ```bash
    nbx dcim --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root dcim [OPTIONS] COMMAND [ARGS]...                                   
                                                                                    
     OpenAPI app group: dcim                                                        
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────╮
    │ cable-terminations             Resource: dcim/cable-terminations             │
    │ cables                         Resource: dcim/cables                         │
    │ connected-device               Resource: dcim/connected-device               │
    │ console-port-templates         Resource: dcim/console-port-templates         │
    │ console-ports                  Resource: dcim/console-ports                  │
    │ console-server-port-templates  Resource: dcim/console-server-port-templates  │
    │ console-server-ports           Resource: dcim/console-server-ports           │
    │ device-bay-templates           Resource: dcim/device-bay-templates           │
    │ device-bays                    Resource: dcim/device-bays                    │
    │ device-roles                   Resource: dcim/device-roles                   │
    │ device-types                   Resource: dcim/device-types                   │
    │ devices                        Resource: dcim/devices                        │
    │ front-port-templates           Resource: dcim/front-port-templates           │
    │ front-ports                    Resource: dcim/front-ports                    │
    │ interface-templates            Resource: dcim/interface-templates            │
    │ interfaces                     Resource: dcim/interfaces                     │
    │ inventory-item-roles           Resource: dcim/inventory-item-roles           │
    │ inventory-item-templates       Resource: dcim/inventory-item-templates       │
    │ inventory-items                Resource: dcim/inventory-items                │
    │ locations                      Resource: dcim/locations                      │
    │ mac-addresses                  Resource: dcim/mac-addresses                  │
    │ manufacturers                  Resource: dcim/manufacturers                  │
    │ module-bay-templates           Resource: dcim/module-bay-templates           │
    │ module-bays                    Resource: dcim/module-bays                    │
    │ module-type-profiles           Resource: dcim/module-type-profiles           │
    │ module-types                   Resource: dcim/module-types                   │
    │ modules                        Resource: dcim/modules                        │
    │ platforms                      Resource: dcim/platforms                      │
    │ power-feeds                    Resource: dcim/power-feeds                    │
    │ power-outlet-templates         Resource: dcim/power-outlet-templates         │
    │ power-outlets                  Resource: dcim/power-outlets                  │
    │ power-panels                   Resource: dcim/power-panels                   │
    │ power-port-templates           Resource: dcim/power-port-templates           │
    │ power-ports                    Resource: dcim/power-ports                    │
    │ rack-reservations              Resource: dcim/rack-reservations              │
    │ rack-roles                     Resource: dcim/rack-roles                     │
    │ rack-types                     Resource: dcim/rack-types                     │
    │ racks                          Resource: dcim/racks                          │
    │ rear-port-templates            Resource: dcim/rear-port-templates            │
    │ rear-ports                     Resource: dcim/rear-ports                     │
    │ regions                        Resource: dcim/regions                        │
    │ site-groups                    Resource: dcim/site-groups                    │
    │ sites                          Resource: dcim/sites                          │
    │ virtual-chassis                Resource: dcim/virtual-chassis                │
    │ virtual-device-contexts        Resource: dcim/virtual-device-contexts        │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.924s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx dcim devices --help`

=== ":material-console: Command"

    ```bash
    nbx dcim devices --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root dcim devices [OPTIONS] COMMAND [ARGS]...                           
                                                                                    
     Resource: dcim/devices                                                         
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────╮
    │ list    list dcim/devices                                                    │
    │ get     get dcim/devices                                                     │
    │ create  create dcim/devices                                                  │
    │ update  update dcim/devices                                                  │
    │ patch   patch dcim/devices                                                   │
    │ delete  delete dcim/devices                                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">2.061s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx dcim devices list --help`

=== ":material-console: Command"

    ```bash
    nbx dcim devices list --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root dcim devices list [OPTIONS]                                        
                                                                                    
     list dcim/devices                                                              
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --id                  INTEGER  Object ID for detail operations               │
    │ --query       -q      TEXT     Query parameter key=value                     │
    │ --body-json           TEXT     Inline JSON request body                      │
    │ --body-file           TEXT     Path to JSON request body file                │
    │ --json                         Output raw JSON                               │
    │ --yaml                         Output YAML                                   │
    │ --markdown                     Output Markdown (mutually exclusive with      │
    │                                --json/--yaml)                                │
    │ --trace                        Fetch and render the cable trace as ASCII     │
    │                                when supported.                               │
    │ --trace-only                   Render only the cable trace ASCII output when │
    │                                supported.                                    │
    │ --help                         Show this message and exit.                   │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.997s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx ipam prefixes --help`

=== ":material-console: Command"

    ```bash
    nbx ipam prefixes --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root ipam prefixes [OPTIONS] COMMAND [ARGS]...                          
                                                                                    
     Resource: ipam/prefixes                                                        
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────╮
    │ list    list ipam/prefixes                                                   │
    │ get     get ipam/prefixes                                                    │
    │ create  create ipam/prefixes                                                 │
    │ update  update ipam/prefixes                                                 │
    │ patch   patch ipam/prefixes                                                  │
    │ delete  delete ipam/prefixes                                                 │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.914s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx dcim interfaces get --help`

=== ":material-console: Command"

    ```bash
    nbx dcim interfaces get --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root dcim interfaces get [OPTIONS]                                      
                                                                                    
     get dcim/interfaces                                                            
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --id                  INTEGER  Object ID for detail operations               │
    │ --query       -q      TEXT     Query parameter key=value                     │
    │ --body-json           TEXT     Inline JSON request body                      │
    │ --body-file           TEXT     Path to JSON request body file                │
    │ --json                         Output raw JSON                               │
    │ --yaml                         Output YAML                                   │
    │ --markdown                     Output Markdown (mutually exclusive with      │
    │                                --json/--yaml)                                │
    │ --trace                        Fetch and render the cable trace as ASCII     │
    │                                when supported.                               │
    │ --trace-only                   Render only the cable trace ASCII output when │
    │                                supported.                                    │
    │ --help                         Show this message and exit.                   │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.837s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx circuits circuit-terminations get --help`

=== ":material-console: Command"

    ```bash
    nbx circuits circuit-terminations get --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root circuits circuit-terminations get [OPTIONS]                        
                                                                                    
     get circuits/circuit-terminations                                              
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --id                  INTEGER  Object ID for detail operations               │
    │ --query       -q      TEXT     Query parameter key=value                     │
    │ --body-json           TEXT     Inline JSON request body                      │
    │ --body-file           TEXT     Path to JSON request body file                │
    │ --json                         Output raw JSON                               │
    │ --yaml                         Output YAML                                   │
    │ --markdown                     Output Markdown (mutually exclusive with      │
    │                                --json/--yaml)                                │
    │ --trace                        Fetch and render the cable trace as ASCII     │
    │                                when supported.                               │
    │ --trace-only                   Render only the cable trace ASCII output when │
    │                                supported.                                    │
    │ --help                         Show this message and exit.                   │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.803s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---
