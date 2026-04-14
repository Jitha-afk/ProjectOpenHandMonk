# Format Test Matrix and Controlled-Lab Intake Rules

## Purpose
This document turns the project brief into an operator-ready intake and testing matrix for candidate model artifacts. It is optimized for later Microsoft Defender for Cloud model-security evaluation, not for executing or reproducing malicious behavior. The goal is to maximize format coverage while minimizing legal, safety, and lab-operation risk.

## Working assumptions
- We only handle artifacts in a controlled lab.
- We prefer static inspection and non-executing validation over framework-native loading.
- We do not redistribute harmful payloads.
- If a format normally triggers code execution during deserialization, the default fixture choice is a synthetic or intentionally vulnerable sample, not a live malicious artifact.
- "Validation" in this document means proving the artifact matches the claimed format and structure without giving it an opportunity to execute arbitrary code.

## Controlled-lab intake rules

### 1. Intake gates
A candidate artifact should only enter the corpus if all of the following are true:
1. Provenance is documented: source URL, author/vendor, publication context, and retrieval date.
2. License/terms permit local handling for research, or the sample is internally reconstructed.
3. The artifact maps to at least one Defender-supported format or a clearly adjacent packaging pattern.
4. The expected abuse mode is stated before download or reconstruction.
5. The artifact can be validated in a non-production lab without internet-required execution.
6. Storage owner, retention period, and destruction path are defined.

### 2. Default handling tier
Assign each artifact to one of three intake tiers:
- Tier A: parse-safe formats with no normal code execution path during read-only inspection. Examples: safetensors, ONNX, NPY, Arrow IPC, JSON, GGUF.
- Tier B: structured containers that may be complex, zip-based, or dependency-sensitive but can still be validated via static inspection. Examples: HDF5/H5, TFLite, SavedModel, PMML, MOJO.
- Tier C: native code-execution or unsafe-deserialization formats. Examples: pickle/PKL, PT via pickle-based `torch.load`, dill, joblib, POJO, MsgPack when object hooks/custom ext types are involved.

Tier C artifacts require the strongest controls and should default to synthetic reconstruction unless there is strong reason to preserve a real-world sample.

### 3. Mandatory pre-ingest checks
Before a sample is accepted:
- Record SHA256, file size, filename, extension, and container type.
- Verify magic bytes or container signature where possible.
- Run archive listing only; do not unpack executable members to host paths by default.
- Identify whether the artifact is single-file or multi-file.
- Mark whether format-native loading is prohibited, allowed in disposable sandbox only, or unnecessary.
- Reject samples that require cloud callbacks, secret material, or third-party credentials to validate.

### 4. Sandbox requirements
All nontrivial inspection should occur in an isolated environment with:
- no outbound network by default
- ephemeral VM or container with snapshot/rollback
- non-root user where practical
- CPU, memory, file-size, and runtime limits
- read-only mounted input directory plus separate scratch directory
- disabled host mounts except the minimum artifact handoff path
- separate sandbox profiles for parse-only versus framework-loading workflows

### 5. Format-native loading rule
Use format-native loaders only if all of the following are true:
- static inspection cannot answer the required validation question
- the loader itself is a known part of the evaluation target path
- the action is executed inside a disposable sandbox
- expected side effects and monitoring controls are documented first

If those conditions are not met, prefer header parsing, manifest extraction, protobuf/schema decoding, or custom offline readers.

### 6. Artifact acceptance categories
Use one of these labels for each fixture:
- Real-world artifact: original publicly discussed sample retained mostly as-is.
- Intentionally vulnerable sample: safe training/demo fixture designed to exhibit a risky behavior class without uncontrolled payloads.
- Synthetic reconstruction: newly built sample that mimics the structural abuse pattern of a real case.

Default preference order:
1. Intentionally vulnerable sample
2. Synthetic reconstruction
3. Real-world artifact

Use real-world artifacts only when provenance or scanner realism materially depends on preserving original structure.

### 7. Rejection rules
Reject or quarantine candidates that:
- contain live credentials, PII, or embedded secrets
- require running untrusted code to determine basic format identity
- are legally unclear to possess or redistribute internally
- have no trustworthy provenance and no strong technical reason to reconstruct them
- are oversized enough to add little value beyond resource-exhaustion testing better handled synthetically

### 8. What later testing should capture
For each accepted fixture, later testing should measure:
- format identification correctness
- risk classification correctness
- whether the control detects unsafe serialization, embedded code, suspicious metadata, or malformed structure
- whether the scan fails safely on malformed input
- whether false negatives or false positives appear on benign near-neighbor samples
- operational data: scan duration, resource use, parser failure mode, and logging quality

## Safe validation workflow
Use this order of operations:
1. Provenance review and legal check.
2. Hashing and metadata capture.
3. Signature and container-type verification.
4. Static structure extraction only.
5. Schema/manifest validation where available.
6. Decide whether framework-native loading is required.
7. If yes, move to disposable high-control sandbox and monitor process, filesystem writes, child processes, and network attempts.
8. Record observed behavior and classify the fixture.

## Format test matrix

| Format | Likely abuse / risk modes | Safe candidate validation approach | Required lab controls | Preferred fixture type | Later test success criteria |
|---|---|---|---|---|---|
| `.pkl` | Arbitrary code execution via `__reduce__`, `GLOBAL`, or gadget chains; hidden payload in model/preprocessor bundle; misleading extension | Never `pickle.load` on host. Verify magic/header patterns, inspect opcodes with `pickletools.dis`, and classify referenced globals/modules without invocation | Tier C. Offline sandbox, no network, no host mounts beyond read-only input, syscall/process monitoring if loader test is later required | Intentionally vulnerable sample first; synthetic reconstruction second; real-world only if provenance is important | Defender identifies pickle/serialized Python object, flags unsafe deserialization/code-exec indicators, and fails safely on malformed payloads |
| `.h5` / HDF5 | Malicious attributes/metadata, parser differential bugs, oversized tensors, zip-slip style misconceptions when packaged, embedded pickled blobs in auxiliary groups | Validate HDF5 signature, enumerate groups/datasets/attrs with read-only library or low-level tooling, enforce size limits, search for opaque byte arrays and unexpected script-like metadata | Tier B. Resource limits, read-only input, no automatic custom object loading in Keras/TensorFlow | Synthetic reconstruction or intentionally vulnerable sample; real-world if tied to known parser issue | Correctly identifies HDF5/Keras artifact, notes suspicious embedded byte blobs or abnormal metadata, handles large/malformed files without crash |
| `.pt` | PyTorch checkpoints commonly use pickle under the hood; arbitrary code execution on `torch.load`; tensor bombs; renamed pickle artifacts | Treat as pickle-derived unless proven otherwise. Inspect zip/container members for newer formats, or disassemble pickle stream without loading tensors into framework | Tier C. Same as PKL plus strict file-size and decompression-ratio checks | Intentionally vulnerable sample first; synthetic reconstruction next | Identifies PyTorch checkpoint family, flags unsafe deserialization path and suspicious object graph, distinguishes benign tensor-only packaging where possible |
| `.onnx` | Malformed protobuf graphs, parser memory corruption surface, poisoned metadata fields, external data references, oversized initializers | Use protobuf/ONNX tooling in non-executing parse mode; inspect graph, opsets, metadata, and external tensor references; block model execution/inference | Tier A/B. Resource caps, deny external file fetches, no custom op execution | Real-world benign baseline plus synthetic malformed/abuse samples | Identifies ONNX correctly, flags suspicious external data refs or malformed graph structure, tolerates bad protobuf safely |
| `.safetensors` | Metadata abuse, oversized tensor declarations, shape/dtype mismatch, polyglot/container confusion | Read header only with safetensors parser or custom JSON-header parser; validate declared offsets, lengths, and non-overlap without materializing tensors | Tier A. File-size and offset bounds; no framework execution needed | Real-world and synthetic reconstruction are both good first-pass options | Recognizes safetensors, validates header integrity, flags offset inconsistencies/metadata anomalies, avoids unsafe code path assumptions |
| SavedModel | Dangerous ancillary assets, malformed protobufs, graph abuse, unexpected function signatures, poisoned metadata/configs | Treat as directory artifact. Enumerate files, validate protobuf manifests (`saved_model.pb`), inspect variables/assets tree, avoid loading into TensorFlow runtime initially | Tier B. Directory-level quarantine, no symlink following outside root, no TensorFlow execution unless sandboxed | Synthetic reconstruction first; real-world for common benign baselines | Identifies SavedModel package as multi-file model, flags suspicious assets or symlink/path tricks, handles malformed manifests without escaping package root |
| TFLite | Malformed flatbuffers, metadata abuse, oversized tensors, parser crashes, embedded associated files | Validate FlatBuffer schema and model metadata in read-only mode; inspect operator table, tensor sizes, and attached metadata records | Tier A/B. Resource limits; no delegate execution or interpreter run during initial validation | Synthetic malformed fixtures plus benign real-world baseline | Identifies TFLite accurately, flags malformed flatbuffer or suspicious metadata, parses without interpreter execution |
| `.npy` | Dangerous object arrays enabling pickle, header manipulation, oversized shape declarations, dtype abuse | Parse NPY magic/version/header only; reject or heavily scrutinize `dtype=object` and pickle-enabled cases; validate shape-product against size | Tier A when numeric-only; Tier C if object arrays/pickle path present | Synthetic reconstruction is preferred because abuse pattern is easy to build safely | Distinguishes benign numeric NPY from object-array/pickle-risk NPY, flags impossible shapes and malformed headers |
| Arrow | Malformed IPC/Feather streams, compression bombs, schema confusion, extension types carrying unexpected semantics | Validate Arrow magic bytes/schema/message boundaries with offline reader; inspect record batch counts, buffers, compression, and extension metadata without executing UDFs | Tier A/B. Resource caps and decompression limits | Synthetic malformed fixture plus benign baseline | Identifies Arrow/Feather correctly, flags corrupt schema/buffer boundaries or suspicious extension metadata, fails safely on malformed batches |
| MsgPack | Deserialization into dangerous host objects through custom hooks/ext types, nested structure bombs, disguised pickle-like payload transport | Use raw MsgPack decoder with object hooks disabled; inspect ext types, nesting depth, and declared sizes; never map directly into application objects | Tier C when object materialization exists, otherwise Tier B | Synthetic reconstruction preferred; real-world only if tied to a specific unsafe loader case | Identifies MsgPack container, flags ext-type/object-hook risk and pathological nesting/size abuse |
| `dill` | Broader-than-pickle code serialization including functions, closures, modules; straightforward arbitrary code execution on load | Never `dill.load` on host. Perform bytecode/opcode-level inspection similarly to pickle and label as high-risk executable serialization | Tier C. Same hardening as PKL with extra caution because serialized functions/modules are expected | Intentionally vulnerable sample first | Recognizes dill serialization specifically or at least as unsafe Python object serialization, flags executable function/module payload patterns |
| `joblib` | Pickle-backed execution, compressed archive wrappers, scikit-learn pipeline gadgets, loader-triggered code execution | Inspect compression wrapper and inner pickle stream without materializing objects; enumerate contained files if archive-backed | Tier C. Same as PKL/PT plus decompression bounds | Intentionally vulnerable sample and synthetic reconstruction | Identifies joblib/scikit-learn serialized pipeline, flags unsafe deserialization and suspicious reducers/gadgets |
| PMML | XML entity expansion, schema abuse, external entity references, script-capable extensions, oversized models | Validate as XML offline with external entities disabled; schema-check against PMML XSD if needed; inspect for script elements, extension tags, and remote refs | Tier B. XXE-safe parser, no external fetches, size limits | Synthetic reconstruction first; benign real-world baseline helpful | Identifies PMML, flags XXE/script/extension risks, and handles malformed XML without network access |
| JSON | Polyglot files, poisoned metadata/configs, schema confusion, prompt/config injection, extreme nesting or size abuse | Validate UTF-8/text, parse with strict JSON parser, enforce schema and depth/size limits, inspect for suspicious fields/URLs/embedded code strings | Tier A. Resource caps and strict schema validation | Synthetic reconstruction plus benign baseline | Identifies JSON model/config artifact, flags schema violations or suspicious executable/remote-reference fields without over-alerting on benign metadata |
| POJO | Generated Java source/class bundles may trigger unsafe compilation or execution; embedded shell commands in scoring wrappers; archive/path traversal issues | Treat as source/archive artifact only. Enumerate files, validate manifest/package structure, inspect code statically, never compile or run during intake | Tier C if compiled/executed; Tier B for static-only intake. Separate Java sandbox if later execution is necessary | Synthetic or intentionally vulnerable sample preferred | Identifies POJO/scoring-code package, flags executable code paths and suspicious process/network usage constructs |
| MOJO | Zip/JAR-like model bundle can contain compiled code/resources, manifest abuse, zip path tricks, embedded native libs | Inspect archive members and manifest statically, verify paths remain inside root, hash embedded binaries, do not execute loaders initially | Tier B/C depending on contents. Archive traversal protections and Java sandbox for any later execution | Synthetic reconstruction first; real-world only for common benign reference structure | Identifies MOJO package, flags embedded code/native libs/path traversal, and safely handles malformed archives |
| GGUF | Malformed headers, metadata poisoning, tensor offset inconsistencies, oversized quantized tensor declarations, parser differential bugs | Parse GGUF header, tensor directory, metadata KV pairs, and offset table without running inference; validate alignment and file-bound ranges | Tier A. Strict offset/size validation and resource caps | Real-world benign baseline plus synthetic malformed samples | Identifies GGUF accurately, flags invalid offsets/metadata anomalies, and tolerates malformed quantized models safely |

## Recommended first-pass fixtures by format class

### Class 1: Unsafe Python serialization
Highest priority because these directly test unsafe deserialization findings.
- `.pkl`: one intentionally vulnerable sample using a harmless `__reduce__` proof-of-execution marker; one benign sklearn-style pickle.
- `.pt`: one PyTorch checkpoint that resolves to pickle-backed unsafe object restoration; one benign tensor checkpoint.
- `dill`: one sample serializing a function/closure with a benign marker payload.
- `joblib`: one scikit-learn pipeline with a benign gadget-style reducer chain.
- `.npy`: one numeric-safe array and one `dtype=object` sample demonstrating pickle risk.
- MsgPack: one ext-type/object-hook abuse sample and one plain data sample.

### Class 2: Structured but nominally non-executable model containers
Priority for parser safety and metadata inspection.
- `.onnx`: one benign reference model; one malformed graph/external-data sample.
- `.safetensors`: one benign tensor file; one header/offset inconsistency sample.
- `.h5`: one benign Keras H5; one oversized metadata or opaque-byte-blob sample.
- TFLite: one benign flatbuffer; one malformed metadata sample.
- GGUF: one benign small quantized file; one header/offset corruption sample.
- Arrow: one benign Feather/IPC file; one schema or compression-abuse sample.

### Class 3: Multi-file packages and XML/text descriptors
Priority for path safety, schema validation, and package-level scanning.
- SavedModel: one minimal benign directory package; one package with suspicious assets/symlink/path edge cases.
- PMML: one benign regression/classification PMML; one sample with disabled-XXE/ext/script indicators.
- JSON: one benign model/config manifest; one deeply nested or suspicious-URL metadata sample.
- MOJO: one benign archive layout; one synthetic sample with embedded native lib or traversal edge case.
- POJO: one benign generated scoring package; one intentionally vulnerable static code sample containing obvious process-spawn/network constructs.

## Practical implementation notes
- Build fixture metadata alongside each sample: format, subtype, origin class, risk hypothesis, expected scanner finding, and allowed handling method.
- Maintain benign near-neighbor samples for every risky sample so later testing can measure false positives.
- Keep each intentionally vulnerable fixture harmless by using visible markers such as writing a sentinel string to a sandbox-only temp file rather than executing any destructive action.
- Prefer tiny fixtures that isolate one behavior per sample. Large public models are poor first-pass candidates unless format realism requires them.
- For multi-file formats, preserve exact directory layout in fixture manifests because packaging errors are often the risk surface.
- For formats with both safe and unsafe submodes, treat subtype detection as part of the test objective rather than assuming the file extension is enough.

## Initial prioritization
Recommended first wave for corpus construction:
1. `.pkl`
2. `.pt`
3. `joblib`
4. `dill`
5. `.onnx`
6. `.safetensors`
7. `.npy`
8. SavedModel
9. TFLite
10. GGUF

Rationale: this set gives the fastest coverage of the highest-likelihood security-relevant behaviors: unsafe deserialization, metadata abuse, malformed parser input, and modern model-weight packaging.

## Exit criteria for this design task
This design is complete when the corpus workflow can, for every supported format:
- state the expected abuse class
- state a non-hostile validation method
- state required lab controls
- choose a preferred fixture acquisition strategy
- define what later Defender evaluation should prove
