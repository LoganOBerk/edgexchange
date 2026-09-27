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
%%{init: {'themeVariables': {'lineColor': '#00C2A8', 'edgeLabelBackground': '#FFFFFF'}}}%%
erDiagram
	direction LR
	USERS {
		INTEGER id PK
		CITEXT username UK
		TEXT password
		NUMERIC(18,2) balance
	}

	PORTFOLIOS {
		INTEGER id PK
		INTEGER user_id FK
		TEXT name UK
	}

	STOCKS {
		INTEGER id PK
		INTEGER portfolio_id FK
		TEXT ticker UK
		INTEGER quantity
	}

	USERS||--o{PORTFOLIOS:"has"
	PORTFOLIOS||--o{STOCKS:"contains"

	style USERS fill:#A0603Ccc,stroke:#5C3620,color:#FBF0E9
	style PORTFOLIOS fill:#B8734Bcc,stroke:#5C3620,color:#FBF0E9
	style STOCKS fill:#8C4E30cc,stroke:#5C3620,color:#FBF0E9

# Create Account
flowchart TD
    A(["client"]) --> B["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Api.create_account&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    B --> C["&nbsp;&nbsp;&nbsp;Sanitizer.sanitize_credentials&nbsp;&nbsp;&nbsp;&nbsp;"]
    C --> D["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Validator.account_validator&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    D --> E["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Service.create_account&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    E --> F[("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Database.insert_user&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#5C8AD6,stroke:#2A4C8C,color:#F5F8FC
    classDef integration fill:#E38A2E,stroke:#8C4E14,color:#FCF3E8
    classDef sanitization fill:#5FA854,stroke:#2E5C28,color:#F0F8EE
    classDef validation fill:#D9C22E,stroke:#8C7A14,color:#3A3308
    classDef service fill:#2A4C8C,stroke:#152645,color:#EEF2FA
    classDef persistence fill:#A0603C,stroke:#5C3620,color:#FBF0E9

    linkStyle 0 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#00C2A8,stroke-width:2.5px

# Find Account
flowchart TD
    A(["client"]) --> B["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Api.find_account&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    B --> C["&nbsp;&nbsp;&nbsp;Sanitizer.sanitize_credentials&nbsp;&nbsp;&nbsp;&nbsp;"]
    C --> D["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Validator.account_validator&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    D --> E["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Service.find_account&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    E --> F[("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Database.pull_aggregate&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#5C8AD6,stroke:#2A4C8C,color:#F5F8FC
    classDef integration fill:#E38A2E,stroke:#8C4E14,color:#FCF3E8
    classDef sanitization fill:#5FA854,stroke:#2E5C28,color:#F0F8EE
    classDef validation fill:#D9C22E,stroke:#8C7A14,color:#3A3308
    classDef service fill:#2A4C8C,stroke:#152645,color:#EEF2FA
    classDef persistence fill:#A0603C,stroke:#5C3620,color:#FBF0E9

    linkStyle 0 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#00C2A8,stroke-width:2.5px

# Fund Account
flowchart TD
    A(["client"]) --> B["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Api.fund_account&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    B --> C["&nbsp;&nbsp;Sanitizer.sanitize_funds_request&nbsp;&nbsp;&nbsp;"]
    C --> D["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Validator.fund_validator&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    D --> E["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Service.fund_account&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    E --> F[("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Database.update_funds&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#5C8AD6,stroke:#2A4C8C,color:#F5F8FC
    classDef integration fill:#E38A2E,stroke:#8C4E14,color:#FCF3E8
    classDef sanitization fill:#5FA854,stroke:#2E5C28,color:#F0F8EE
    classDef validation fill:#D9C22E,stroke:#8C7A14,color:#3A3308
    classDef service fill:#2A4C8C,stroke:#152645,color:#EEF2FA
    classDef persistence fill:#A0603C,stroke:#5C3620,color:#FBF0E9

    linkStyle 0 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#00C2A8,stroke-width:2.5px

# Create/Remove Portfolio
flowchart TD
    A(["client"]) --> B["&nbsp;&nbsp;Api.create/remove_portfolio&nbsp;&nbsp;"]
    B --> C["&nbsp;&nbsp;Sanitizer.sanitize_portfolio_name&nbsp;&nbsp;"]
    C --> D["&nbsp;&nbsp;&nbsp;&nbsp;Validator.portfolio_validator&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    D --> E["&nbsp;&nbsp;Service.create/remove_portfolio&nbsp;&nbsp;"]
    E --> F[("&nbsp;&nbsp;&nbsp;Database.insert/delete_portfolio&nbsp;&nbsp;&nbsp;&nbsp;")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#5C8AD6,stroke:#2A4C8C,color:#F5F8FC
    classDef integration fill:#E38A2E,stroke:#8C4E14,color:#FCF3E8
    classDef sanitization fill:#5FA854,stroke:#2E5C28,color:#F0F8EE
    classDef validation fill:#D9C22E,stroke:#8C7A14,color:#3A3308
    classDef service fill:#2A4C8C,stroke:#152645,color:#EEF2FA
    classDef persistence fill:#A0603C,stroke:#5C3620,color:#FBF0E9

    linkStyle 0 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#00C2A8,stroke-width:2.5px

# Execute Buy/Sell
flowchart TD
    A(["client"]) --> B["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Api.execute_buy/sell&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    B --> C["&nbsp;&nbsp;Sanitizer.sanitize_shares_request&nbsp;&nbsp;"]
    C --> D["&nbsp;&nbsp;Validator.shares_request_validator&nbsp;&nbsp;"]
    D --> E["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Service.execute_buy/sell&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
    E --> F[("&nbsp;&nbsp;Database.update/insert/delete_stock&nbsp;&nbsp;")]

    A:::client
    B:::integration
    C:::sanitization
    D:::validation
    E:::service
    F:::persistence

    classDef client fill:#5C8AD6,stroke:#2A4C8C,color:#F5F8FC
    classDef integration fill:#E38A2E,stroke:#8C4E14,color:#FCF3E8
    classDef sanitization fill:#5FA854,stroke:#2E5C28,color:#F0F8EE
    classDef validation fill:#D9C22E,stroke:#8C7A14,color:#3A3308
    classDef service fill:#2A4C8C,stroke:#152645,color:#EEF2FA
    classDef persistence fill:#A0603C,stroke:#5C3620,color:#FBF0E9

    linkStyle 0 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 4 stroke:#00C2A8,stroke-width:2.5px