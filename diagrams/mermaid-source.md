# System Architecture
---
config:
  themeVariables:
    edgeLabelBackground: '#FFFFFF'
---
flowchart TB
 subgraph TOPROW[" "]
    direction LR
        SPL1["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
        A(["App.run"])
        SPR1["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
  end
 subgraph PIPE[" "]
    direction LR
        E[["Sanitizer"]]
        F[["Api"]]
        G[["Validator"]]
        H[["Service"]]
        HPAD["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
  end
 subgraph TAIL2[" "]
    direction LR
        I[("&nbsp;&nbsp;&nbsp;&nbsp;Database&nbsp;&nbsp;&nbsp;&nbsp;<br>&nbsp;")]
        LC["LiveCache"]
        LCPAD["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
  end
    A --> C[/"Frontend"/] & B[/"Cli"/]
    B -.-> VIZ["Visualizer"]
    VIZ ~~~ ERR["Errors"]
    B --> D(("Client"))
    C --> D
    D -- FRONTEND --> R[["Routes"]]
    D -- CLI --> F
    R --> SC["SessionCache"] & F
    F --> E
    E --> G
    G --> H
    H --> I & LC
    LC --> EXT["External API"]

    VIZ@{ shape: curv-trap}
    ERR@{ shape: st-doc}
    SC@{ shape: win-pane}
    LC@{ shape: win-pane}
    EXT@{ shape: cloud}
    class SPL1,SPR1,HPAD,LCPAD spacer
    class A config
    class C,B,VIZ interface
    class ERR errorNode
    class D client
    class R,F,SC,LC,EXT integration
    class E sanitization
    class G validation
    class H service
    class I persistence
    classDef config fill:#D6CDBB,stroke:#6E634C,color:#2E2818
    classDef interface fill:#D2C4E3,stroke:#5C4A85,color:#2C2145
    classDef client fill:#B7D6D3,stroke:#3D6E6C,color:#1B3534
    classDef errorNode fill:#E3BCB5,stroke:#96453A,color:#4A211B
    classDef integration fill:#E5CD97,stroke:#957230,color:#4A3714
    classDef sanitization fill:#B8D4AB,stroke:#4B7A3A,color:#243D1C
    classDef validation fill:#AEC2DE,stroke:#3E5D8C,color:#1E2E45
    classDef service fill:#D5D89E,stroke:#767F2E,color:#393D16
    classDef persistence fill:#D3B78D,stroke:#7C5527,color:#3E2A12
    classDef spacer fill:none,stroke:none,color:none
    style TOPROW fill:none,stroke:none
    style PIPE fill:none,stroke:none
    style TAIL2 fill:none,stroke:none
    linkStyle default stroke:#FF6D00,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:none

# Database Architecture
%%{init: {'themeVariables': {'lineColor': '#FF6D00', 'edgeLabelBackground': '#FFFFFF'}}}%%
erDiagram
	direction LR
	USERS {
		INTEGER id PK ""
		CITEXT username UK ""
		TEXT password ""
		NUMERIC(18,2) balance "DEFAULT 0"
	}

	PORTFOLIOS {
		INTEGER id PK ""
		INTEGER user_id FK "ON DELETE CASCADE"
		TEXT name UK "UNIQUE(user_id, name)"
	}

	STOCKS {
		INTEGER id PK ""
		INTEGER portfolio_id FK "ON DELETE CASCADE"
		TEXT ticker UK "UNIQUE(portfolio_id, ticker)"
		INTEGER quantity ""
	}

	USERS||--o{PORTFOLIOS:"has"
	PORTFOLIOS||--o{STOCKS:"contains"

	style USERS fill:#B7A17Ecc,stroke:#7C5527,color:#3E2A12
	style PORTFOLIOS fill:#D3B78Dcc,stroke:#7C5527,color:#3E2A12
	style STOCKS fill:#C9AD82cc,stroke:#6E4A20,color:#2E2010

# Create Account
flowchart TD
    A(["client"]) --> B["    Api.create_account     "]
    B --> C[" Sanitizer.sanitize_credentials  "]
    C --> D["   Validator.account_validator    "]
    D --> E["    Service.create_account     "]
    E --> F[("       Database.insert_user        ")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#B7D6D3,stroke:#3D6E6C,color:#1B3534
    classDef integration fill:#E5CD97,stroke:#957230,color:#4A3714
    classDef sanitization fill:#B8D4AB,stroke:#4B7A3A,color:#243D1C
    classDef validation fill:#AEC2DE,stroke:#3E5D8C,color:#1E2E45
    classDef service fill:#D5D89E,stroke:#767F2E,color:#393D16
    classDef persistence fill:#D3B78D,stroke:#7C5527,color:#3E2A12

    linkStyle 0 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#FF5A00,stroke-width:2.5px

# Find Account
flowchart TD
    A(["client"]) --> B["     Api.find_account      "]
    B --> C[" Sanitizer.sanitize_credentials  "]
    C --> D["   Validator.account_validator    "]
    D --> E["     Service.find_account      "]
    E --> F[("       Database.pull_aggregate       ")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#B7D6D3,stroke:#3D6E6C,color:#1B3534
    classDef integration fill:#E5CD97,stroke:#957230,color:#4A3714
    classDef sanitization fill:#B8D4AB,stroke:#4B7A3A,color:#243D1C
    classDef validation fill:#AEC2DE,stroke:#3E5D8C,color:#1E2E45
    classDef service fill:#D5D89E,stroke:#767F2E,color:#393D16
    classDef persistence fill:#D3B78D,stroke:#7C5527,color:#3E2A12

    linkStyle 0 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#FF5A00,stroke-width:2.5px

# Fund Account
flowchart TD
    A(["client"]) --> B["     Api.fund_account      "]
    B --> C["Sanitizer.sanitize_funds_request "]
    C --> D["     Validator.fund_validator     "]
    D --> E["     Service.fund_account      "]
    E --> F[("       Database.update_funds       ")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#B7D6D3,stroke:#3D6E6C,color:#1B3534
    classDef integration fill:#E5CD97,stroke:#957230,color:#4A3714
    classDef sanitization fill:#B8D4AB,stroke:#4B7A3A,color:#243D1C
    classDef validation fill:#AEC2DE,stroke:#3E5D8C,color:#1E2E45
    classDef service fill:#D5D89E,stroke:#767F2E,color:#393D16
    classDef persistence fill:#D3B78D,stroke:#7C5527,color:#3E2A12

    linkStyle 0 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#FF5A00,stroke-width:2.5px

# Create/Remove Portfolio
flowchart TD
    A(["client"]) --> B["Api.create/remove_portfolio"]
    B --> C["Sanitizer.sanitize_portfolio_name"]
    C --> D["  Validator.portfolio_validator   "]
    D --> E["Service.create/remove_portfolio"]
    E --> F[(" Database.insert/delete_portfolio  ")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#B7D6D3,stroke:#3D6E6C,color:#1B3534
    classDef integration fill:#E5CD97,stroke:#957230,color:#4A3714
    classDef sanitization fill:#B8D4AB,stroke:#4B7A3A,color:#243D1C
    classDef validation fill:#AEC2DE,stroke:#3E5D8C,color:#1E2E45
    classDef service fill:#D5D89E,stroke:#767F2E,color:#393D16
    classDef persistence fill:#D3B78D,stroke:#7C5527,color:#3E2A12

    linkStyle 0 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#FF5A00,stroke-width:2.5px

# Execute Buy/Sell
flowchart TD
    A(["client"]) --> B["   Api.execute_buy/sell    "]
    B --> C["Sanitizer.sanitize_shares_request"]
    C --> D["Validator.shares_request_validator"]
    D --> E["   Service.execute_buy/sell    "]
    E --> F[("Database.update/insert/delete_stock")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#B7D6D3,stroke:#3D6E6C,color:#1B3534
    classDef integration fill:#E5CD97,stroke:#957230,color:#4A3714
    classDef sanitization fill:#B8D4AB,stroke:#4B7A3A,color:#243D1C
    classDef validation fill:#AEC2DE,stroke:#3E5D8C,color:#1E2E45
    classDef service fill:#D5D89E,stroke:#767F2E,color:#393D16
    classDef persistence fill:#D3B78D,stroke:#7C5527,color:#3E2A12

    linkStyle 0 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#FF5A00,stroke-width:2.5px