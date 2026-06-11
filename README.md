A production-grade ELT data pipeline orchestrating **dbt** transformations within **Snowflake**, fully automated and scheduled using **Dagster Cloud**. This architecture processes enterprise e-commerce data under a strictly isolated role-based security framework.

```
                    [ Dagster Cloud ]
                    (Orchestration)
                           │
        ┌──────────────────┴──────────────────┐
        ▼                                     ▼
 [ dbt Core ]                          [ Environment ]

```

(Transformations)                    (Variables Validation)
│                                     │
└──────────────────┬──────────────────┘
▼
[ Snowflake DW ]
┌──────────────────┐
│ engineering_role │ (Strict Isolation)
└─────────┬────────┘
▼
[ olist_project ]
(Analytics DB)

```

The pipeline enforces a modern data stack pattern:
* **Orchestration Engine:** Dagster Cloud handles deployment, lineage tracking, variable execution contexts, and time-based automation.
* **Transformation Layer:** dbt Core modularizes SQL queries into version-controlled staging and analytics models.
* **Data Warehouse:** Snowflake stores database layers, executing queries using specific compute configurations (`ENGINEERING_WH`).

---

## 🔐 Security & Access Control Model

To adhere to data governance best practices, this project implements a strict separation of **Authentication** (Identity) and **Authorization** (Privileges).

* **Identity (User):** `PEGI` acts as the account authentication identity.
* **Privileges (Role):** `engineering_role` holds exclusive rights to write and modify the analytics database.

While the user profile can default to `ACCOUNTADMIN` for global configurations, the automated pipeline strictly explicitly assumes `engineering_role` during the session handshake to prevent permission bleeding.

```sql
-- Role Isolation setup executed in Snowflake
CREATE ROLE engineering_role;
GRANT ALL PRIVILEGES ON DATABASE olist_project TO ROLE engineering_role;
GRANT USAGE ON WAREHOUSE ENGINEERING_WH TO ROLE engineering_role;

```

---

## 📁 Repository Structure

The code is consolidated inside a unified root layout for continuous deployment:

```
├── .github/workflows/     # CI/CD deployment configurations
├── models/                # dbt staging and core analytics SQL models
│   ├── staging/           # Raw view casting and initial typing
│   └── marts/             # Business intelligence tables
├── target/                # Compiled dbt assets
│   └── manifest.json      # Pipeline state graph read by Dagster
├── definitions.py         # Dagster definitions, asset tracking, and schedules
├── dbt_project.yml        # dbt project scoping configuration
├── profiles.yml           # Database connection mapping environment
└── README.md              # Project documentation

```

---

## 🛠 Project Configurations

### 1. dbt Profile Config (`profiles.yml`)

Located at the root directory to map incoming environment fields safely:

```yaml
olist_transform:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE') }}"
      warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE') }}"
      database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
      schema: "{{ env_var('SNOWFLAKE_SCHEMA') }}"

```

### 2. Dagster Orchestration (`definitions.py`)

Declares data lineage assets, registers execution jobs, and bounds production runtime schedules:

```python
import os
from dagster import Definitions, ScheduleDefinition, DefineAssetJob
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path

# Track root directory context
dbt_project_dir = Path(__file__).parent.absolute()

@dbt_assets(manifest=dbt_project_dir / "target/manifest.json")
def olist_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

# Register pipeline targets
olist_dbt_job = DefineAssetJob(name="olist_dbt_job", selection="*")

# Production automation profile (Every day at midnight)
olist_dbt_schedule = ScheduleDefinition(
    job=olist_dbt_job,
    cron_schedule="0 0 * * *", 
)

# Bundle context mappings
defs = Definitions(
    assets=[olist_dbt_assets],
    schedules=[olist_dbt_schedule],
    jobs=[olist_dbt_job],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    },
)

```

---

## 🚀 Deployment & Automation Workflow

### Environment Variables

The following keys are mapped cleanly inside the **Dagster Cloud UI** under `Deployment` -> `Environment Variables`:

* `SNOWFLAKE_ACCOUNT`: `DCWKBGQ-QH90954`
* `SNOWFLAKE_USER`: `PEGI`
* `SNOWFLAKE_PASSWORD`: `ytdEMbAL8iuCvzw`
* `SNOWFLAKE_ROLE`: `engineering_role`
* `SNOWFLAKE_WAREHOUSE`: `ENGINEERING_WH`
* `SNOWFLAKE_DATABASE`: `olist_project`
* `SNOWFLAKE_SCHEMA`: `PUBLIC`

### Triggering Operations

1. **Code Changes:** When any update is pushed to GitHub `main` branch, Dagster Cloud parses `definitions.py`.
2. **Activation:** The schedule can be activated by toggling it under the **Automation** panel inside Dagster Cloud.
3. **Manual Materialization:** Full pipelines can be force-triggered anytime directly via the **Asset Graph** screen by hitting `Materialize All`.
"""
