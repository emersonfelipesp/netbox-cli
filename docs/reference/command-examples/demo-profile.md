# Demo profile

### `nbx demo --help`

=== ":material-console: Command"

    ```bash
    nbx demo --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root demo [OPTIONS] COMMAND [ARGS]...                                   
                                                                                    
     NetBox demo.netbox.dev profile and command tree.                               
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --token-key           TEXT  Set the demo profile directly without            │
    │                             Playwright.                                      │
    │ --token-secret        TEXT  Set the demo profile directly without            │
    │                             Playwright.                                      │
    │ --help                      Show this message and exit.                      │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────╮
    │ init            Authenticate with demo.netbox.dev via Playwright and save    │
    │                 the demo profile.                                            │
    │ config          Show the configured demo profile settings.                   │
    │ test            Test connectivity to demo.netbox.dev using the configured    │
    │                 demo profile.                                                │
    │ reset           Remove the saved demo profile configuration.                 │
    │ tui             Launch the TUI against the demo profile.                     │
    │ cli             CLI builder tools against the demo.netbox.dev profile.       │
    │ dev             Developer-focused tools against the demo.netbox.dev profile. │
    │ circuits        OpenAPI app group: circuits                                  │
    │ core            OpenAPI app group: core                                      │
    │ dcim            OpenAPI app group: dcim                                      │
    │ extras          OpenAPI app group: extras                                    │
    │ ipam            OpenAPI app group: ipam                                      │
    │ plugins         OpenAPI app group: plugins                                   │
    │ tenancy         OpenAPI app group: tenancy                                   │
    │ users           OpenAPI app group: users                                     │
    │ virtualization  OpenAPI app group: virtualization                            │
    │ vpn             OpenAPI app group: vpn                                       │
    │ wireless        OpenAPI app group: wireless                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">2.030s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx demo init --help`

=== ":material-console: Command"

    ```bash
    nbx demo init --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root demo init [OPTIONS]                                                
                                                                                    
     Authenticate with demo.netbox.dev via Playwright and save the demo profile.    
                                                                                    
     Pass ``--username`` and ``--password`` for non-interactive / CI use.           
     Alternatively, supply an existing token directly with ``--token-key`` and      
     ``--token-secret`` to skip Playwright entirely.                                
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --headless          --headed          Run Playwright headless (default). Use │
    │                                       --headed only when a desktop/X server  │
    │                                       is available.                          │
    │                                       [default: headless]                    │
    │ --username      -u              TEXT  demo.netbox.dev username. Prompted     │
    │                                       interactively when omitted.            │
    │ --password      -p              TEXT  demo.netbox.dev password. Prompted     │
    │                                       interactively when omitted.            │
    │ --token-key                     TEXT  Set the demo profile directly without  │
    │                                       Playwright (requires --token-secret).  │
    │ --token-secret                  TEXT  Set the demo profile directly without  │
    │                                       Playwright (requires --token-key).     │
    │ --help                                Show this message and exit.            │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.911s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx demo config --help`

=== ":material-console: Command"

    ```bash
    nbx demo config --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root demo config [OPTIONS]                                              
                                                                                    
     Show the configured demo profile settings.                                     
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --show-token          Include API token in output                            │
    │ --help                Show this message and exit.                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.954s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx demo test --help`

=== ":material-console: Command"

    ```bash
    nbx demo test --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root demo test [OPTIONS]                                                
                                                                                    
     Test connectivity to demo.netbox.dev using the configured demo profile.        
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">2.008s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx demo reset --help`

=== ":material-console: Command"

    ```bash
    nbx demo reset --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root demo reset [OPTIONS]                                               
                                                                                    
     Remove the saved demo profile configuration.                                   
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">2.037s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx demo tui --help`

=== ":material-console: Command"

    ```bash
    nbx demo tui --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root demo tui [OPTIONS]                                                 
                                                                                    
     Launch the TUI against the demo profile.                                       
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --theme          Theme selector. Use '--theme' to list available themes or   │
    │                  '--theme <name>' to launch with one.                        │
    │ --help           Show this message and exit.                                 │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.841s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx demo tui --theme`

=== ":material-console: Command"

    ```bash
    nbx demo tui --theme
    ```

=== ":material-text-box-outline: Output"

    ```text
    Available themes:
    - dracula
    - netbox-dark
    - netbox-light
    - onedark-pro
    - tokyo-night
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.860s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx demo dev --help`

=== ":material-console: Command"

    ```bash
    nbx demo dev --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root demo dev [OPTIONS] COMMAND [ARGS]...                               
                                                                                    
     Developer-focused tools against the demo.netbox.dev profile.                   
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────╮
    │ tui   Launch the developer request workbench TUI against the demo profile.   │
    │ http  Direct HTTP operations mapped from OpenAPI paths (nbx dev http         │
    │       <method> --path ...).                                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.904s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx demo dev tui --help`

=== ":material-console: Command"

    ```bash
    nbx demo dev tui --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root demo dev tui [OPTIONS]                                             
                                                                                    
     Launch the developer request workbench TUI against the demo profile.           
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --theme          Theme selector. Use '--theme' to list available themes or   │
    │                  '--theme <name>' to launch with one.                        │
    │ --help           Show this message and exit.                                 │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.852s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx demo dev tui --theme`

=== ":material-console: Command"

    ```bash
    nbx demo dev tui --theme
    ```

=== ":material-text-box-outline: Output"

    ```text
    Available themes:
    - dracula
    - netbox-dark
    - netbox-light
    - onedark-pro
    - tokyo-night
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.729s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---
