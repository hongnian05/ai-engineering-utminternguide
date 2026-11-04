# Data Directory Structure & Evidence Tracking

This directory manages the data pipeline for **UTM-InternGuide**, tracking the transformation from raw university documentation into cleaned, structured knowledge chunks.

---

## Directory Organization

```
data/
├── README.md               # Data pipeline & transformation documentation
├── raw/                    # Original, unedited source files (PDFs, raw text dumps)
│   └── .gitkeep
└── cleaned/                # Processed, stripped, and structured documents (Markdown / JSONL)
    └── .gitkeep
```

---

## Data Transformation Pipeline (Raw → Cleaned)

To provide clear engineering evidence for academic grading, the transformation pipeline follows these verifiable steps:

| Processing Stage | Raw Data Condition | Transformation Applied | Cleaned Data Output |
|:---|:---|:---|:---|
| **1. Header & Footer Stripping** | Repeating university logos, running headers, and page numbers (e.g. *"Universiti Teknologi Malaysia - Page 14 of 120"*). | Regex pattern matching and bounding-box filtering to remove non-semantic boilerplate text. | Pure semantic body text without repetitive token noise. |
| **2. Hyphenation & Line-Break Repair** | Words split across line breaks (e.g., *"pre- / requisite"*, *"gradu- / ation"*). | Normalization regex rejoining split tokens and collapsing erratic whitespace. | Intact domain vocabulary and coherent sentences. |
| **3. Table Layout Reconstruction** | Multi-column tables (e.g., grading breakdown, credit eligibility matrix) collapsed into unaligned raw text. | Tabular parsing (via `pdfplumber` / Markdown table converter) preserving column headers and row associations. | Structured Markdown tables (`\| Course \| Credits \| Grade \|`) preserving numerical associations. |
| **4. Metadata Enrichment** | Unindexed continuous text without contextual provenance. | Injection of document metadata headers (`Document Title`, `Academic Year`, `Section Header`, `Original Page Number`). | Self-contained contextual chunks suitable for vector search and exact citation attribution. |

---

## Transformation Evidence Log

*(To be populated during Week 3 / Topic 3 Data Ingestion lab with before-and-after text snippets and parsing metrics).*
