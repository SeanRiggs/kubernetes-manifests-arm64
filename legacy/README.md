# Historical manifests — reference only

Original manifest bytes are preserved under `legacy/manifests/` with `.example` appended. They are excluded from active validation and cannot be accidentally included by ordinary recursive kubectl YAML discovery. Do not rename and apply them without a separate audit.

These files contain hardcoded private network addresses, host paths, unpinned or deprecated images, a privileged container, incomplete storage binding, and a multi-resource file without YAML document separators. They describe the original author's environment rather than a portable install.

Use [maintained apps](../README.md) for new installations and [UPGRADING](../docs/UPGRADING.md) for existing data. Archiving files in Git does not stop any application or remove any cluster data.
