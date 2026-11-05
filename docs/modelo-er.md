# Modelo relacional — Achados UFLA

```mermaid
erDiagram
    AUTH_USER ||--o{ OCCURRENCE : registra
    CATEGORY ||--o{ ITEM : classifica
    LOCATION ||--o{ ITEM : relaciona
    LOCATION ||--o{ OCCURRENCE : localiza
    ITEM ||--o{ OCCURRENCE : possui

    CATEGORY {
        bigint id PK
        string name UK
        text description
        boolean is_active
    }

    LOCATION {
        bigint id PK
        string name UK
        text description
    }

    ITEM {
        bigint id PK
        string title
        text description
        text characteristics
        string status
        bigint category_id FK
        bigint location_id FK
        datetime created_at
        datetime updated_at
    }

    OCCURRENCE {
        bigint id PK
        string occurrence_type
        bigint item_id FK
        bigint reporter_id FK
        bigint location_id FK
        datetime occurred_at
        text notes
        datetime created_at
    }

    AUTH_USER {
        bigint id PK
        string username UK
    }
```

## Regras principais

- Uma categoria classifica vários objetos; a categoria não pode ser excluída
  enquanto estiver sendo utilizada (`PROTECT`).
- Um local pode estar associado a vários objetos e ocorrências; também não pode
  ser excluído enquanto estiver sendo utilizado (`PROTECT`).
- Um objeto pode possuir várias ocorrências ao longo do seu ciclo de vida.
- Uma ocorrência pertence a um objeto e é registrada por um usuário.
- A data de uma ocorrência não pode estar no futuro.
- Um objeto devolvido deve possuir características registradas.
- O objeto é excluído junto com suas ocorrências relacionadas (`CASCADE`),
  pois a ocorrência não faz sentido sem o objeto.
