# Show Approvals

Display pending approvals from the approvals queue.

## Usage

Copy and follow these steps:

## Step 1: Read Approvals File

Read `.universal-mwp/queue/approvals.md`:

```markdown
# Approvals

Pending approvals for medium/high risk tasks.

## Pending Approvals

- [ ] P{0-3} {ID} | {description} | risk: {level}

## Approved

| ID | Description | Risk | Approved |
...

## Rejected

| ID | Description | Reason | Rejected |
...
```

## Step 2: Count Items

- **Pending**: N tasks
- **Approved**: M tasks
- **Rejected**: K tasks

## Step 3: Format Output

```
Approvals ({N} pending, {M} approved, {K} rejected)

## Pending

1. [P{0-3}] {ID} | {title} | risk: {medium|high}

## Approved

- {ID}: {title} ({date})

## Rejected

- {ID}: {title} - {reason}
```

## No Output Files Modified

This is a read-only operation.