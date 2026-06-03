# CanaryWeave FIDES Rule Schema

Rules use `.cwfr.yaml` files. The format is intentionally YAML-based and distinct from NOVA syntax while preserving the defender-friendly ideas of metadata, named signals, boolean conditions, fixtures, and safety notes.

Required fields:

- `id`
- `name`
- `version`
- `category`
- `severity`: `low`, `medium`, `high`, or `critical`
- `scope`
- `description`
- `signals`
- `condition`
- `recommended_action`: `allow`, `audit`, `quarantine`, or `block_and_audit`
- `fixtures`
- `safety_notes`

Initial signal types:

- `event_field_equals`
- `event_field_in`
- `schema_shape`
- `capability_policy` with `not_in_allowed_capabilities`
- `canary_flow` with `outside_allowed_sink`
- `text_structure` with `hidden_unicode` or `untrusted_instruction_shape`

Example condition:

```text
source_is_server_sampling and output_is_tool_plan_shape and capability_not_granted
```

The engine validates that every condition identifier refers to a declared signal.
