# Issue #3 Project Brief — Vulnerable AI Model Corpus

Related issue: https://github.com/Jitha-afk/ProjectOpenHandMonk/issues/3

## Goal
Produce a reusable corpus and decision framework for selecting vulnerable or intentionally unsafe AI model artifacts for later product testing against Microsoft Defender for Cloud model security features.

## Scope
This project is research-first. The initial deliverable is not a downloader or scanner. It is:
1. a candidate inventory,
2. a format coverage matrix,
3. a lab-safety / legality assessment,
4. recommendations for which artifacts or reconstructed fixtures should be used later.

## Required deliverables
- research/candidate-inventory.md
- design/format-test-matrix.md
- docs/testing-playbook.md
- docs/executive-summary.md

## Decision rules
A candidate is strong if it has most of the following:
- credible provenance (vendor advisory, academic paper, incident write-up, or known security-research repo)
- a concrete artifact or reproducible package reference
- clear indication of unsafe deserialization, embedded executable behavior, poisoned metadata, or similar model-supply-chain risk
- direct or indirect fit to one of the Defender-supported artifact formats
- practical lab handling path without violating terms, law, or platform rules

## Candidate classes
- intentionally vulnerable demonstration models or model packages
- malicious pickle/joblib/dill/torch artifacts used in security demonstrations
- unsafe checkpoint/config packaging patterns discussed by researchers
- model-adjacent artifacts that Defender should inspect (weights, configs, serialized preprocessing pipelines, tokenizers, metadata bundles)
- reconstructed/synthetic fixtures when real-world samples cannot be safely handled

## Out of scope for initial pass
- mass downloading random internet artifacts
- redistributing harmful payloads
- executing untrusted artifacts outside isolated analysis workflow
- claiming a candidate is confirmed malicious without source support

## Handoff plan
1. Alan: research inventory with source-backed evidence and confidence ratings.
2. Turing: convert inventory into a testable lab matrix and identify gaps by file format.
3. Mira: package the findings into reusable operator-facing docs.
4. Hermes: review, dedupe, and decide next implementation/testing steps.
