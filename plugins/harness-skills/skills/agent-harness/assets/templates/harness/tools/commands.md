# Commands

Replace placeholders with project-specific commands after discovery. Do not run commands marked `Unknown` or `Not applicable`.

Status: `Discovered` means supported by a named project source; `Inferred` means
not yet confirmed; `Verified` means executed in a stated environment, with date
and result; `Failed` means the verification did not pass. Record working directory,
prerequisites, source, side effects, environment and verification evidence in Notes.
Do not run `Inferred` commands. Only mark `Not applicable` when supported by
project evidence. Preserve existing project status names such as `Confirmed`, but
do not treat them as a fresh execution result. Run only task-relevant commands
whose side effects, permissions and prerequisites are understood.

| Purpose | Command | Status | Source | Notes |
| --- | --- | --- | --- | --- |
| Install | `TBD` | Unknown | Not discovered | Replace only after confirming from project files or user input. |
| Dev server | `TBD` | Unknown | Not discovered | Include host/port notes when known. |
| Lint | `TBD` | Unknown | Not discovered | Mark `Not applicable` only when supported by project evidence. |
| Test | `TBD` | Unknown | Not discovered | Prefer the narrowest relevant test command for runs. |
| Build | `TBD` | Unknown | Not discovered | Mark `Not applicable` if the project does not build. |
| Manual verification | `TBD` | Unknown | Not discovered | Describe project-specific checks when command verification is insufficient. |
