# Homelab Handbook — Family Meyer

*Internal notes. Last updated: March 2026. Maintained by Jonas.*

## Devices

| Name | Hardware | Location | Purpose |
|---|---|---|---|
| atlas | Mini PC, 32 GB RAM, 1 TB SSD | Study, shelf above desk | Ollama, Open WebUI, Docker services |
| vault | Synology NAS, 2 × 4 TB (mirrored) | Basement, next to the router | File storage and photo backup |
| beacon | Raspberry Pi 4 | Hallway cupboard | Pi-hole ad blocker, DNS for the whole network |
| router | Fibre router from the ISP | Basement | Internet, Wi-Fi |

## Network

- Home network: `192.168.40.0/24`. The router is `192.168.40.1`.
- `atlas` has the fixed address `192.168.40.10`, `vault` is `192.168.40.20`,
  `beacon` is `192.168.40.2`.
- Guest Wi-Fi is called **Meyer-Guest**. It cannot reach any of the devices above.
- If websites suddenly stop loading for everyone, restart `beacon` first — a
  hung Pi-hole takes DNS down with it. Pull the power cable, wait ten seconds,
  plug it back in.

## Backups

- `vault` backs up the family photo folder every **night at 02:30** to an
  encrypted cloud bucket.
- Once a month, on the **first Saturday**, Jonas copies the Open WebUI data
  volume from `atlas` to `vault` by hand.
- A second USB drive labelled **"offsite"** is kept at Grandma Hilde's flat and
  swapped every three months.
- Restoring has been tested twice; the last successful test was in January 2026.

## AI services

- Open WebUI runs on `atlas` and is reachable inside the house at
  `http://192.168.40.10:3000`. New accounts must be approved by Jonas.
- The default model is `llama3.2:3b`. For homework help the kids use
  `qwen3:4b`, which is better at maths.
- Ollama is **not** reachable from outside the house. Remote access only works
  through the Tailscale app, which is installed on Jonas's and Anna's phones.

## Rules

1. No work documents from Anna's employer on `atlas` — her company policy
   forbids storing client data on private hardware, even locally.
2. Updates are installed on the **last Sunday of every month**, after a backup.
3. Nobody opens router ports. If a service needs outside access, use Tailscale.

## Emergency contacts

- Internet outage: ISP hotline, the number is on the sticker on the router.
- Jonas is travelling: ask Anna; the admin password envelope is in the
  fireproof box in the study.
