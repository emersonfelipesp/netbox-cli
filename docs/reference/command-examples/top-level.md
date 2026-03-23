# Top-level

### `nbx --help`

=== ":material-console: Command"

    ```bash
    nbx --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root [OPTIONS] COMMAND [ARGS]...                                        
                                                                                    
     NetBox API-first CLI/TUI. Dynamic command form: nbx <group> <resource>         
     <action>                                                                       
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────╮
    │ init            Create or update the default NetBox CLI profile.             │
    │ config          Show the current default profile configuration.              │
    │ groups          List all available OpenAPI app groups.                       │
    │ resources       List resources available within a group.                     │
    │ ops             Show available HTTP operations for a resource.               │
    │ call            Call an arbitrary NetBox API path.                           │
    │ tui             Launch the interactive NetBox terminal UI.                   │
    │ logs            Show recent application logs from the shared on-disk log     │
    │                 file.                                                        │
    │ cli             CLI utilities: interactive command builder and helpers.      │
    │ docs            Generate reference documentation (captured CLI               │
    │                 input/output).                                               │
    │ demo            NetBox demo.netbox.dev profile and command tree.             │
    │ dev             Developer-focused tools and experimental interfaces.         │
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

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">2.119s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx init --help`

=== ":material-console: Command"

    ```bash
    nbx init --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root init [OPTIONS]                                                     
                                                                                    
     Create or update the default NetBox CLI profile.                               
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ *  --base-url            TEXT   NetBox base URL, e.g.                        │
    │                                 https://netbox.example.com                   │
    │                                 [required]                                   │
    │ *  --token-key           TEXT   NetBox API token key [required]              │
    │ *  --token-secret        TEXT   NetBox API token secret [required]           │
    │    --timeout             FLOAT  HTTP timeout in seconds [default: 30.0]      │
    │    --help                       Show this message and exit.                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.850s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx config --help`

=== ":material-console: Command"

    ```bash
    nbx config --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root config [OPTIONS]                                                   
                                                                                    
     Show the current default profile configuration.                                
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --show-token          Include API token in output                            │
    │ --help                Show this message and exit.                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.744s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx groups --help`

=== ":material-console: Command"

    ```bash
    nbx groups --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root groups [OPTIONS]                                                   
                                                                                    
     List all available OpenAPI app groups.                                         
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">2.104s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx resources --help`

=== ":material-console: Command"

    ```bash
    nbx resources --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root resources [OPTIONS] GROUP                                          
                                                                                    
     List resources available within a group.                                       
                                                                                    
    ╭─ Arguments ──────────────────────────────────────────────────────────────────╮
    │ *    group      TEXT  OpenAPI app group, e.g. dcim [required]                │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.782s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx ops --help`

=== ":material-console: Command"

    ```bash
    nbx ops --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root ops [OPTIONS] GROUP RESOURCE                                       
                                                                                    
     Show available HTTP operations for a resource.                                 
                                                                                    
    ╭─ Arguments ──────────────────────────────────────────────────────────────────╮
    │ *    group         TEXT  [required]                                          │
    │ *    resource      TEXT  [required]                                          │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.840s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx call --help`

=== ":material-console: Command"

    ```bash
    nbx call --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root call [OPTIONS] METHOD PATH                                         
                                                                                    
     Call an arbitrary NetBox API path.                                             
                                                                                    
    ╭─ Arguments ──────────────────────────────────────────────────────────────────╮
    │ *    method      TEXT  [required]                                            │
    │ *    path        TEXT  [required]                                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --query      -q      TEXT  Query parameter key=value                         │
    │ --body-json          TEXT  Inline JSON request body                          │
    │ --body-file          TEXT  Path to JSON request body file                    │
    │ --json                     Output raw JSON                                   │
    │ --yaml                     Output YAML                                       │
    │ --markdown                 Output Markdown (mutually exclusive with          │
    │                            --json/--yaml)                                    │
    │ --help                     Show this message and exit.                       │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.865s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx tui --help`

=== ":material-console: Command"

    ```bash
    nbx tui --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root tui [OPTIONS]                                                      
                                                                                    
     Launch the interactive NetBox terminal UI.                                     
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --theme          Theme selector. Use '--theme' to list available themes or   │
    │                  '--theme <name>' to launch with one.                        │
    │ --help           Show this message and exit.                                 │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.898s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx tui --theme`

=== ":material-console: Command"

    ```bash
    nbx tui --theme
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

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.782s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx docs --help`

=== ":material-console: Command"

    ```bash
    nbx docs --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root docs [OPTIONS] COMMAND [ARGS]...                                   
                                                                                    
     Generate reference documentation (captured CLI input/output).                  
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────╮
    │ generate-capture  Capture every nbx command (input + output) and write       │
    │                   docs/generated/nbx-command-capture.md.                     │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.882s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---

### `nbx docs generate-capture --help`

=== ":material-console: Command"

    ```bash
    nbx docs generate-capture --help
    ```

=== ":material-text-box-outline: Output"

    ```text
                                                                                    
     Usage: root docs generate-capture [OPTIONS]                                    
                                                                                    
     Capture every nbx command (input + output) and write                           
     docs/generated/nbx-command-capture.md.                                         
                                                                                    
     By default live-API specs run through ``nbx demo …`` (demo.netbox.dev).        
     Pass ``--live`` to run them against your configured default profile instead.   
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --output     -o                   PATH     Markdown destination. Default:    │
    │                                            <repo>/docs/generated/nbx-comman… │
    │ --raw-dir                         PATH     Raw JSON artifacts directory.     │
    │                                            Default:                          │
    │                                            <repo>/docs/generated/raw/        │
    │ --max-lines                       INTEGER  Max lines per command output in   │
    │                                            the Markdown.                     │
    │                                            [default: 200]                    │
    │ --max-chars                       INTEGER  Max chars per command output in   │
    │                                            the Markdown.                     │
    │                                            [default: 120000]                 │
    │ --live                                     Use the default profile (your     │
    │                                            real NetBox) instead of the demo  │
    │                                            profile. By default the generator │
    │                                            captures live-API specs against   │
    │                                            demo.netbox.dev.                  │
    │ --markdown       --no-markdown             Append --markdown to dynamic      │
    │                                            list/get/… and ``nbx call``       │
    │                                            captures so tables are plain      │
    │                                            Markdown (not Rich). Default: on. │
    │                                            [default: markdown]               │
    │ --help                                     Show this message and exit.       │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

<span class="nbx-badge nbx-badge--ok">exit&nbsp;0</span> <span class="nbx-badge nbx-badge--neutral">1.695s</span>

!!! warning "Truncated"
    Output was truncated. Full text is in `docs/generated/raw/`.

---
