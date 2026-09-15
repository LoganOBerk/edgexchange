# System Architecture
flowchart TB
    A(["App.run"]) --> B["Cli"] & C["Frontend"]
    B -.-> VIZ(["Visualizer"])
    VIZ ~~~ ERR[/"Errors"/]
    B --> D(["Client"])
    C --> D
    D --> F["Api"]
    F --> E["Sanitizer"]
    E --> G["Validator"]
    G --> H["Service"]
    H --> DOM["Domain Models"] & I[("Database")] & LC["LiveCache"]
    LC --> EXT["External API"]

     A:::config
     B:::interface
     C:::interface
     VIZ:::interface
     ERR:::errorNode
     D:::client
     F:::integration
     E:::sanitization
     G:::validation
     H:::service
     DOM:::domain
     I:::persistence
     LC:::integration
     EXT:::integration
    classDef config fill:#D6CDBB,stroke:#6E634C,color:#2E2818
    classDef interface fill:#D2C4E3,stroke:#5C4A85,color:#2C2145
    classDef client fill:#B7D6D3,stroke:#3D6E6C,color:#1B3534
    classDef errorNode fill:#E3BCB5,stroke:#96453A,color:#4A211B
    classDef integration fill:#E5CD97,stroke:#957230,color:#4A3714
    classDef sanitization fill:#B8D4AB,stroke:#4B7A3A,color:#243D1C
    classDef validation fill:#AEC2DE,stroke:#3E5D8C,color:#1E2E45
    classDef service fill:#D5D89E,stroke:#767F2E,color:#393D16
    classDef persistence fill:#D3B78D,stroke:#7C5527,color:#3E2A12
    classDef domain fill:#D9A9C5,stroke:#84315E,color:#421830
    linkStyle 0 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 1 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 3 stroke:none
    linkStyle 4 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 5 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 6 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 7 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 8 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 9 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 10 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 11 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 12 stroke:#FF5A00,stroke-width:2.5px,fill:none
    linkStyle 13 stroke:#FF5A00,stroke-width:2.5px

# Database Architecture
erDiagram
	direction LR
	USERS {
		INTEGER id PK ""  
		TEXT username UK ""  
		TEXT password  ""  
		REAL balance  ""  
	}

	PORTFOLIOS {
		INTEGER id PK ""  
		INTEGER user_id FK ""  
		TEXT name  ""  
	}

	STOCKS {
		INTEGER id PK ""  
		INTEGER portfolio_id FK ""  
		TEXT ticker  ""  
		INTEGER quantity  ""  
	}

	USERS||--o{PORTFOLIOS:"has"
	PORTFOLIOS||--o{STOCKS:"contains"

	style USERS fill:#8C2F12,stroke:#5A1D0B,color:#FFFFFF
	style PORTFOLIOS fill:#D94A24,stroke:#8C2F12,color:#FFFFFF
	style STOCKS fill:#FF3B1F,stroke:#B33A15,color:#FFFFFF

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
    E --> F[("       Database.pull_account       ")]

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