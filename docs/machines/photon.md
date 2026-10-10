---
type: machine
status: living
tags: [machine, hardware]
---

# Machine: Photon (laptop)

Recorded 2026-10-10 by the agent with `lscpu`, `free`, `df`, `lspci`, `nvidia-smi`, `python3 --version`.

| Item | Value |
|---|---|
| Role | Main development machine (the user's laptop) |
| OS | Ubuntu 26.04.1 LTS |
| CPU | AMD Ryzen 7 5800H, 16 logical CPUs |
| RAM | 14 GiB reported by `free -g` (about 16 GB nominal) |
| GPU | NVIDIA GeForce RTX 3060 Mobile (GA106M), 6 GB per user; integrated AMD Radeon (Cezanne) |
| GPU driver | **Not working**: `nvidia-smi` reports it cannot communicate with the NVIDIA driver |
| Disk free (home) | 78 GB of 221 GB |
| System Python | 3.14.4 (the project will pin its own version; see H-18) |

## Open items

- The NVIDIA driver must be installed or repaired before any GPU work (Module A deep models). Not urgent during Phase R. Check with `nvidia-smi` after fixing.
