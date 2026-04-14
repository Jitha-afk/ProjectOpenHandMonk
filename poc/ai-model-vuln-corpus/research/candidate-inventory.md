# Candidate inventory: vulnerable / unsafe AI model artifacts

Date: 2026-04-14
Issue: #3
Scope: initial research inventory for controlled-lab testing candidates only. This document is evidence-first and intentionally skeptical. If a concrete sample was not directly located in this pass, it is labeled as reconstructed/synthetic or theoretical.

## Quick take

Strongest early candidates are not "mystery malware models" from the internet. They are classes with credible documentation, reproducible unsafe behavior, and clean lab reconstruction paths:

1. Fickling-generated malicious pickle/PyTorch files (.pkl, .pt/.pth) for deliberate unsafe-deserialization tests.
2. NumPy object-array .npy fixtures that require `allow_pickle=True` and can execute pickled payloads.
3. Keras models with `Lambda` / unsafe deserialization paths (.h5 and modern Keras format) for bytecode/custom-object loading tests.
4. ONNX files with malicious `external_data` references (.onnx) for traversal/path-handling tests.
5. TensorFlow Lite malformed FlatBuffer models (.tflite) for parser robustness / memory-safety testing.
6. GGUF malformed files (.gguf) for parser robustness in local model runtimes.
7. PyArrow IPC/Feather/Parquet files (Arrow family) where the deserializer itself had documented arbitrary-code-execution exposure.

## Source highlights used in this pass

- Hugging Face, "Pickle Scanning": warns that loading pickle files can enable dangerous arbitrary code execution, and recommends safer formats where possible. https://huggingface.co/docs/hub/security-pickle
- Rapid7, "From .pth to p0wned": reports malicious PyTorch `.pth` files uploaded to Hugging Face that executed system commands and downloaded RAT payloads. https://www.rapid7.com/blog/post/from-pth-to-p0wned-abuse-of-pickle-files-in-ai-model-supply-chains/
- Trail of Bits Fickling: explicitly supports detecting and creating malicious pickle / PyTorch files, including PyTorch polyglots. https://github.com/trailofbits/fickling
- PyTorch serialization notes: `torch.load(..., weights_only=False)` can result in arbitrary code execution; safer `weights_only=True` exists for trusted workflows. https://pytorch.org/docs/stable/notes/serialization.html
- scikit-learn model persistence: pickle/joblib/cloudpickle loading can execute arbitrary code. https://scikit-learn.org/stable/model_persistence.html
- joblib persistence docs: `joblib.load()` is based on pickle and arbitrary Python code can execute when loading. https://joblib.readthedocs.io/en/latest/persistence.html
- dill docs: dill extends Python pickle and can serialize broad interpreter state. https://dill.readthedocs.io/en/latest/
- NumPy docs and CVE-2019-6446: loading pickled object arrays from `.npy` can execute arbitrary code. https://numpy.org/doc/stable/reference/generated/numpy.load.html and https://nvd.nist.gov/vuln/detail/CVE-2019-6446
- Keras Lambda docs: Lambda layers are saved by serializing Python bytecode and are "potentially unsafe." https://keras.io/api/layers/core_layers/lambda/
- TensorFlow / Keras load docs: `safe_mode=False` can trigger arbitrary code execution during deserialization. https://www.tensorflow.org/api_docs/python/tf/keras/models/load_model
- TensorFlow security policy: untrusted models/graphs are equivalent to running untrusted code. https://github.com/tensorflow/tensorflow/security/policy
- ONNX CVEs for `external_data` traversal: https://nvd.nist.gov/vuln/detail/CVE-2022-25882 and https://nvd.nist.gov/vuln/detail/CVE-2024-27318
- ONNX external data mechanism docs: https://onnx.ai/onnx/repo-docs/ExternalData.html
- PyArrow CVE-2023-47248: untrusted Arrow IPC / Feather / Parquet deserialization could allow arbitrary code execution. https://nvd.nist.gov/vuln/detail/CVE-2023-47248
- MessagePack Python API: explicitly advises setting bounds when unpacking untrusted data. https://msgpack-python.readthedocs.io/en/latest/api.html
- safetensors README: positions safetensors as a safer weights format that should not run arbitrary code when randomly downloaded. https://github.com/huggingface/safetensors
- Hugging Face Transformers docs: `trust_remote_code=True` can execute malicious custom model code. https://huggingface.co/docs/transformers/v4.39.2/custom_models
- llama.cpp / GGUF security guidance and GGUF parser CVEs: https://github.com/ggml-org/llama.cpp/security and https://nvd.nist.gov/vuln/detail/CVE-2024-21802
- H2O model export docs for POJO/MOJO packaging: https://docs.h2o.ai/h2o/latest-stable/h2o-docs/save-and-load-model.html
- PMML general structure spec: https://dmg.org/pmml/v4-4-1/GeneralStructure.html

## Inventory

| Candidate / class | Format(s) covered | Source / provenance URL(s) | Risk type | Classification | Lab suitability | Confidence |
|---|---|---|---|---|---|---|
| Rapid7-documented malicious PyTorch checkpoints hosted on Hugging Face | `.pth`, `.pt`, pickle-backed PyTorch weights | Rapid7 report: https://www.rapid7.com/blog/post/from-pth-to-p0wned-abuse-of-pickle-files-in-ai-model-supply-chains/ ; HF pickle security note: https://huggingface.co/docs/hub/security-pickle | Arbitrary code execution on deserialization; embedded system-command execution; downloader/RAT staging | Intentionally malicious in the wild, but specific samples/URLs were not directly recovered in this pass | Medium. High value if original artifacts/hashes can be recovered; otherwise better treated as a provenance anchor for reconstructed fixtures | High for the class; Medium for recoverable sample availability |
| Fickling-generated malicious pickle demo files | `.pkl`, `.pickle` | Fickling repo: https://github.com/trailofbits/fickling ; HF pickle note includes Fickling example: https://huggingface.co/docs/hub/security-pickle | Deliberate pickle code injection / unsafe deserialization | Intentionally vulnerable demonstration | High. Easy to reconstruct under lab control; good first fixture family | High |
| Fickling-generated PyTorch polyglot / weaponized checkpoint demos | `.pt`, `.pth` | Fickling repo (PyTorch polyglots support): https://github.com/trailofbits/fickling ; PyTorch serialization warning: https://pytorch.org/docs/stable/notes/serialization.html | Pickle-based code execution inside model checkpoint loading | Intentionally vulnerable demonstration / reconstructed | High. Directly aligned to model-loading threat path | High |
| Generic pickle-backed Python model artifacts | `.pkl`, `.pickle` | scikit-learn model persistence: https://scikit-learn.org/stable/model_persistence.html ; HF pickle note: https://huggingface.co/docs/hub/security-pickle | Arbitrary code execution during load | Incidentally unsafe by design, unless deliberately weaponized | High. Straightforward to reconstruct for many frameworks and serializers | High |
| joblib model bundles | `.joblib` | joblib persistence warning: https://joblib.readthedocs.io/en/latest/persistence.html ; scikit-learn persistence: https://scikit-learn.org/stable/model_persistence.html | Arbitrary Python code execution on load because joblib uses the pickle model | Incidentally unsafe; easy to weaponize synthetically | High. Very practical for controlled fixture generation | High |
| dill-serialized model/session artifacts | `.dill` | dill docs: https://dill.readthedocs.io/en/latest/ | Broad Python object / interpreter-state deserialization, inheriting pickle-like execution risk | Incidentally unsafe; best treated as synthetic/reconstructed | High. Useful because dill can serialize more than standard pickle | Medium-High |
| NumPy object-array fixtures requiring pickled load path | `.npy`, `.npz` | NumPy load docs: https://numpy.org/doc/stable/reference/generated/numpy.load.html ; NumPy save docs: https://numpy.org/doc/stable/reference/generated/numpy.save.html ; CVE-2019-6446: https://nvd.nist.gov/vuln/detail/CVE-2019-6446 | Arbitrary code execution when object arrays are loaded with pickling enabled | Incidentally unsafe / reconstructed | High. Very easy to synthesize and valuable because `.npy` is on many ML paths | High |
| Keras model with Lambda bytecode or unsafe custom-object path | `.h5`, `.keras` | Keras Lambda docs: https://keras.io/api/layers/core_layers/lambda/ ; Keras/TensorFlow load docs: https://www.tensorflow.org/api_docs/python/tf/keras/models/load_model | Serialized Python bytecode / unsafe deserialization; arbitrary code execution if unsafe mode is allowed | Incidentally unsafe; can be intentionally weaponized for lab demos | High. Good coverage for legacy HDF5 and modern Keras loaders | High |
| Untrusted TensorFlow SavedModel / graph package | SavedModel | TensorFlow security policy: https://github.com/tensorflow/tensorflow/security/policy | Model-as-program execution; unsafe graph/op behavior in untrusted model packages | Incidentally unsafe as a class; usually reconstructed | Medium. Important conceptually, but specific public "malicious SavedModel" artifacts were not identified in this pass | Medium |
| Malformed TensorFlow Lite FlatBuffer models | `.tflite` | NVD search surfaced multiple TFLite model-triggered issues, including CVE-2020-15211: https://nvd.nist.gov/vuln/detail/CVE-2020-15211 and CVE-2020-15212: https://nvd.nist.gov/vuln/detail/CVE-2020-15212 | Parser / memory-safety vulnerabilities triggered by crafted model structure or tensors | Synthetic/reconstructed malformed inputs, not known malicious model releases | High for isolated parser-robustness testing; lower for "supply chain malware" realism | High |
| ONNX model with hostile `external_data` paths | `.onnx` plus sidecar weight files | ONNX external data docs: https://onnx.ai/onnx/repo-docs/ExternalData.html ; CVE-2022-25882: https://nvd.nist.gov/vuln/detail/CVE-2022-25882 ; CVE-2024-27318: https://nvd.nist.gov/vuln/detail/CVE-2024-27318 | Directory traversal / unsafe external file resolution | Synthetic/reconstructed malicious package | High. Clean, format-specific, and easy to validate without running arbitrary Python | High |
| Arrow IPC / Feather / Parquet model-adjacent artifacts | Arrow IPC, Feather, Parquet | CVE-2023-47248: https://nvd.nist.gov/vuln/detail/CVE-2023-47248 ; Arrow IPC docs: https://arrow.apache.org/docs/python/ipc.html ; Feather docs: https://arrow.apache.org/docs/python/feather.html | Unsafe deserialization of untrusted columnar data in PyArrow; arbitrary code execution in affected versions | Incidentally unsafe as a parser/deserializer class | Medium-High. More model-adjacent than model-native, but useful if Defender inspects tensor/data bundles | High |
| MessagePack model-metadata / preprocessor bundle tests | MsgPack / MessagePack | MessagePack Python API: https://msgpack-python.readthedocs.io/en/latest/api.html ; MessagePack project: https://msgpack.org/ | Untrusted-input parsing, resource exhaustion / oversized buffers; no strong model-specific public malicious artifact located in this pass | Theoretical / synthetic | Low-Medium. Good for parser-bounds tests, weak evidence for known malicious model artifacts | Low |
| Transformers-style model package requiring `trust_remote_code=True` | JSON config plus accompanying Python package files | HF Transformers custom models: https://huggingface.co/docs/transformers/v4.39.2/custom_models ; HF model docs warning: https://huggingface.co/docs/transformers/models | Remote/custom code execution during model loading if operator enables `trust_remote_code=True` | Incidentally unsafe package pattern; not a dangerous JSON file by itself | Medium. Valuable as a package-level fixture, but the risk is not in standalone JSON alone | Medium |
| safetensors malformed-header / parser-robustness fixtures | `.safetensors` | safetensors README: https://github.com/huggingface/safetensors | Format is designed to avoid arbitrary code execution; realistic risk in this pass is malformed-file handling, not pickle-style code exec | Synthetic/reconstructed; best used as safe-control / parser-robustness case | Medium as a negative control and parser test; low as a "malicious model" exemplar | Medium-Low |
| PMML evaluator-targeted fixtures | `.pmml` | PMML spec: https://dmg.org/pmml/v4-4-1/GeneralStructure.html ; JPMML evaluator project: https://github.com/jpmml/jpmml-evaluator | XML parser / evaluator attack surface is plausible, but no concrete modern malicious PMML artifact was identified in this pass | Theoretical / synthetic | Low until a specific evaluator and vulnerability target are selected | Low |
| H2O exported POJO fixtures | POJO (Java source) | H2O export docs: https://docs.h2o.ai/h2o/latest-stable/h2o-docs/save-and-load-model.html | Because POJO is source code, the main risk is code review / build trust rather than hidden deserialization; no public malicious sample identified here | Theoretical / synthetic | Low for current corpus unless product specifically inspects source-model packages | Low |
| H2O MOJO package fixtures | MOJO | H2O export docs: https://docs.h2o.ai/h2o/latest-stable/h2o-docs/save-and-load-model.html | Packaged model bundle attack surface is plausible, but this pass found no strong public evidence of malicious MOJO samples | Theoretical / synthetic | Low-Medium. Useful only if format coverage is mandatory and fixtures are clearly synthetic | Low |
| GGUF malformed-model corpus | `.gguf` | llama.cpp security page: https://github.com/ggml-org/llama.cpp/security ; CVE-2024-21802: https://nvd.nist.gov/vuln/detail/CVE-2024-21802 | Crafted file triggers parser memory corruption / possible code execution in affected readers | Synthetic/reconstructed malformed input | High. Strong format coverage for local-LLM ecosystems; good isolated-lab candidate | High |

## Format coverage summary

Covered with strong or moderate evidence in this pass:

- `.pkl` / `.pickle`: strong
- `.pt` / `.pth`: strong
- `.joblib`: strong
- `.dill`: moderate-strong
- `.npy` / `.npz`: strong
- `.h5`: strong
- SavedModel: moderate
- `.tflite`: strong
- `.onnx`: strong
- Arrow / Feather / Parquet: strong for parser/deserializer risk
- MsgPack: low-moderate, mostly synthetic
- JSON: moderate only at package level (`trust_remote_code` pattern), not as standalone JSON
- `.safetensors`: moderate only as malformed-file / safe-control class, not as known arbitrary-code-exec format
- PMML: low, mostly theoretical in this pass
- POJO: low, mostly theoretical in this pass
- MOJO: low, mostly theoretical in this pass
- GGUF: strong

## Recommended first-priority candidates

### Priority 1: build immediately

1. Fickling-generated `.pkl` and `.pt/.pth` samples
   - Why: directly controllable, highly relevant, and sourced to a security-research tool built for this use case.
   - Value: covers pickle-backed unsafe deserialization in both generic Python and PyTorch ecosystems.

2. NumPy `.npy` object-array samples
   - Why: easy to generate, sharply scoped, and directly tied to documented `allow_pickle` risk.
   - Value: gives a minimal lab fixture for a non-obvious but common ML artifact format.

3. Keras `.h5` unsafe Lambda/custom-object fixtures
   - Why: high practical relevance, explicit vendor documentation about unsafe deserialization.
   - Value: strong coverage for legacy HDF5-era model handling and modern loader safety controls.

4. ONNX `external_data` traversal package
   - Why: good non-Python example; tests package/path handling rather than generic pickle behavior.
   - Value: important format diversity and easier static validation.

5. GGUF malformed files
   - Why: directly relevant to local-LLM runtimes and backed by concrete CVEs.
   - Value: modern artifact coverage beyond Python-centric ML stacks.

### Priority 2: build soon after

6. `.tflite` malformed-model corpus
   - Good for parser robustness and memory-safety testing.

7. Arrow IPC / Feather malicious-deserialization fixtures
   - Good if model scanners inspect tensor/data bundles or tabular artifacts adjacent to model packages.

8. joblib / dill variants of the pickle family
   - Good for breadth once the base pickle fixtures exist.

### Priority 3: defer until target product requirements are clearer

9. SavedModel graph/program fixtures
   - Important conceptually, but needs a carefully chosen lab-safe scenario.

10. JSON / `trust_remote_code` package fixtures
   - Useful only if the test scope includes package-level code loading and not just single files.

11. PMML / POJO / MOJO / MsgPack / safetensors synthetic coverage
   - Keep for completeness, but current evidence is weaker than for the formats above.

## Gaps / caveats from this pass

- I did not confirm direct public download URLs for the Rapid7-discussed malicious Hugging Face `.pth` files; treat them as a documented class, not yet as a ready-to-download fixture set.
- PMML, POJO, and MOJO currently have format documentation but not strong public evidence of known malicious model artifacts from this pass.
- For JSON and safetensors, the highest-confidence use in this corpus is as package-level or malformed-input testing, not as confirmed malicious standalone artifacts.
- Arrow is somewhat model-adjacent rather than model-native; include it only if the later matrix explicitly wants coverage for serialized tensors/data bundles in supported formats.

## Proposed next step for engineering handoff

Convert the Priority 1 and Priority 2 rows into a build matrix with:
- reproducibility path (public artifact vs synthetic reconstruction)
- loader/runtime needed
- whether code execution is expected vs parser failure vs path traversal
- minimum sandbox level required
- artifact format-to-product support mapping
