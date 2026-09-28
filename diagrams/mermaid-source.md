# System Architecture
---
config:
  themeVariables:
    edgeLabelBackground: '#FFFFFF'
---
flowchart TB
 subgraph APPCLIENT[" "]
    direction TB
        A(["App.run"])
        D(("Client"))
  end
 subgraph PIPE[" "]
    direction LR
        E[["Sanitizer"]]
        F[["Api"]]
        G[["Validator"]]
        H[["Service"]]
  end
 subgraph TAIL2[" "]
    direction LR
        I[("&nbsp;&nbsp;&nbsp;&nbsp;Database&nbsp;&nbsp;&nbsp;&nbsp;<br>&nbsp;")]
        LCPAD["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
        LC["LiveCache"]
  end
    A --> C[/"Frontend"/]
    A --> B[/"Cli"/]
    A ~~~ D
    D --> C
    D --> B
    B -.-> VIZ["Visualizer"]
    VIZ ~~~ ERR["Errors"]
    C --> R[["Routes"]]
    B --> F
    R --> SC["SessionCache"]
    R --> F
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
    class A appRunLayer
    class D clientLayer
    class C,B,VIZ presentationLayer
    class ERR errorNode
    class F interfaceLayer
    class E sanitizerLayer
    class G validatorLayer
    class H orchestrationLayer
    class I persistenceLayer
    class LC,EXT procurementLayer
    class R,SC IntegrationLayer
    class LCPAD spacer
    classDef appRunLayer fill:#C9CACC,stroke:#6B6E72,color:#2A2C2E
    classDef clientLayer fill:#5C8AD6,stroke:#2A4C8C,color:#F5F8FC
    classDef presentationLayer fill:#B08FCC,stroke:#4A3670,color:#F5F2FA
    classDef errorNode fill:#D9564A,stroke:#8C2A21,color:#FCF0EF
    classDef interfaceLayer fill:#E38A2E,stroke:#8C4E14,color:#FCF3E8
    classDef sanitizerLayer fill:#5FA854,stroke:#2E5C28,color:#F0F8EE
    classDef validatorLayer fill:#D9C22E,stroke:#8C7A14,color:#3A3308
    classDef orchestrationLayer fill:#2A4C8C,stroke:#152645,color:#EEF2FA
    classDef persistenceLayer fill:#A0603C,stroke:#5C3620,color:#FBF0E9
    classDef procurementLayer fill:#D9247A,stroke:#8C1450,color:#FCE9F3
    classDef IntegrationLayer fill:#5C6E7A,stroke:#2E3944,color:#F0F3F5
    classDef spacer fill:none,stroke:none,color:none
    style APPCLIENT fill:none,stroke:none
    style PIPE fill:none,stroke:none
    style TAIL2 fill:none,stroke:none
    linkStyle default stroke:#00C2A8,stroke-width:2.5px,fill:none
    linkStyle 2 stroke:none
    linkStyle 6 stroke:none

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