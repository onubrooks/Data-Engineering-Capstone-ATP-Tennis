# Data Modelling with Data Build Tool(DBT)

Two important handy commands DBT provides are:
To generate base model SQL:

```sh
dbt run-operation generate_base_model --args '{"source_name": "atp_tennis_data", "table_name": "atp_players"}'
```

To generate base model YAML files:

```sh
dbt run-operation generate_model_yaml --args '{"model_names": ["atp_players", "atp_rankings", "atp_matches"]}'
```
