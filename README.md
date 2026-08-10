# ReqInsight

**ReqInsight: An Intelligent Software Requirements Quality Analyzer Using Natural Language Processing**

A lightweight Python/OOP research prototype for evaluating selected software-requirement quality characteristics based on ISO/IEC/IEEE 29148:2018.

## Current development stage

Step 1 — Project foundation and OOP domain models.

## Planned pipeline

SRS document
→ text extraction
→ requirement identification
→ NLP preprocessing
→ ISO-aligned rule analysis
→ duplicate/similarity analysis
→ quality scoring
→ detailed report

## Current scope

The prototype will focus on selected, text-assessable quality characteristics and language indicators rather than attempting full ISO compliance certification.

## Run

```bash
python main.py
```

## Test

```bash
python -m unittest discover -s tests -v
```
