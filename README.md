# odoo_communication_progress_02

Odoo communication progress

### odoo search

```markdown
        A, B
        &, A, B     AND
        |, A, B     OR
        |, &, A, B, C     A AND B OR C
        &, A, |, B, C           A AND (B OR C)
        &, &, &, |, A, B, C, D, |, E, F     A OR (B AND C AND D) AND (E OR F)
```