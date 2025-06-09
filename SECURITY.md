# 😌  SECURITY.md

## Security Overview

### Structural Security

- Authentication: based on Frappe/ERPNex roles and permissions
- Roles used from fixtures: custom_docperm, custom_fields, roles, workflows
- Filters implemented in hooks.py with permission_query_conditions to limit visibility

### Data Protection
- DocTypes configured with role/field/action permissions
- Public access controlled via custom API and overrides
- Attachment security via CustomAttachment

### Audit Trails
- Server-side auditing based on **audit.py**
- Includes timestamped creation/editing info

### Restrictions
- No secret config in repos
- Recommend to add .env to .gitignore
- Enable SMTPS/SSL when deploying

