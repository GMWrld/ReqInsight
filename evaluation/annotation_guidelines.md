# ReqInsight Quality Evaluation Annotation Guidelines

## 1. Purpose

This document defines the ground truth annotation rules used to evaluate
ReqInsight's requirement quality detection capabilities.

Each requirement is independently evaluated against four quality dimensions:

1. Modal Consistency
2. Vague Terminology
3. Measurability
4. Verifiability

For each dimension:

- 1 = quality issue is present
- 0 = quality issue is not present

The human annotation is treated as the ground truth.

---

## 2. Modal Consistency

### Definition

A modal consistency issue exists when the requirement's modal language creates
uncertainty about whether the stated behavior is mandatory.

### Issue = 1

Examples:

"The system should encrypt patient data."

"The application may allow users to export reports."

### Issue = 0

Examples:

"The system shall encrypt patient data."

"The system must lock an account after five failed attempts."

### Annotation rule

Do not classify a requirement as defective merely because it uses a word
such as "should". The question is whether the modal wording creates
uncertainty about the mandatory status of the requirement.

---

## 3. Vague Terminology

### Definition

A vague terminology issue exists when a requirement contains terminology
whose interpretation cannot be determined objectively from the requirement
or an explicitly defined criterion or standard.

### Issue = 1

Examples:

"The system shall provide a fast response."

"The interface shall be user-friendly."

"The system shall provide adequate security."

"The application shall display information clearly."

### Issue = 0

Examples:

"The system shall respond within 2 seconds."

"The system shall use TLS 1.3."

"The system shall maintain 99.9% uptime."

### Important rule

Recognized technical terminology must not automatically be classified as
vague.

Examples include:

- TLS 1.3
- AES-256
- HL7
- FHIR
- BCrypt
- Docker
- Kubernetes

A term is vague only when its meaning is insufficiently precise for objective
interpretation.

---

## 4. Measurability

### Definition

A measurability issue exists when a requirement lacks an objective criterion
that can be assessed using a quantity, threshold, limit, frequency, percentage,
time, capacity, or equivalent objectively assessable condition.

### Issue = 1

"The system shall provide good performance."

"The system shall support many users simultaneously."

"The interface shall be easy to use."

### Issue = 0

"The system shall support 10,000 concurrent users."

"The system shall respond within 2 seconds."

"The system shall maintain 99.9% uptime."

"The system shall perform backups every 24 hours."

### Important rule

A requirement does not need to contain a number to be objectively
assessable.

For example:

"The system shall use TLS 1.3."

can be objectively inspected or tested and therefore should not automatically
be considered defective merely because it contains no numeric threshold.

---

## 5. Verifiability

### Definition

A verifiability issue exists when it is not possible to objectively determine
whether the requirement has been satisfied through testing, inspection,
measurement, demonstration, or analysis.

### Issue = 1

"The system should be highly secure."

"The interface should be attractive."

"The application should handle transactions efficiently."

### Issue = 0

"The system shall encrypt data using AES-256."

"The system shall respond within 500ms."

"The system shall expose /health and /ready endpoints."

---

## 6. Overlap Between Dimensions

A requirement may contain multiple quality issues.

For example:

"The system should provide a fast and user-friendly interface."

may be annotated:

- Modal = 1
- Vague = 1
- Measurability = 1
- Verifiability = 1

Each dimension is evaluated independently.

---

## 7. Ground Truth Policy

Human annotations constitute the ground truth.

ReqInsight predictions must not be used to change the ground truth labels.

If ReqInsight disagrees with the human annotation, the disagreement is
recorded as a prediction error.

This enables calculation of:

- True Positive
- False Positive
- False Negative
- True Negative
- Precision
- Recall
- F1-score

---

## 8. Evaluation Principle

The evaluation measures how accurately ReqInsight identifies requirement
quality issues.

It does not measure whether the original SRS is universally "good" or
"bad".

The evaluation is performed independently for each quality dimension.