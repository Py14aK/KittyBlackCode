---
name: copilot-relay
description: Prepare one-way, paste-ready instruction packets for free Microsoft Copilot inside the closed work environment, where Claude cannot see Copilot's answers and the user carries text both ways. Use when work must be done on the closed network (VS Code + Playwright + Copilot) from a plan made here.
---
# Copilot relay packet

Copilot answers come back only through the user. So each packet must stand alone, be small, and carry its own acceptance check.

## Packet format (plain text, under 1,500 words)
```
PACKET <n> of <m> | <date> | goal: <one line>
CONTEXT: repo playwright-t24, files involved: <paths>. Do not touch other files.
RULES: T24 names verbatim. Selectors only in src/t24/profiles.ts. No credentials in code.
TASK: <numbered edits, each naming file + function>
DONE WHEN: <exact command> prints <exact expected output>
IF IT FAILS: paste the last 30 lines of output back to the user, do not guess a fix twice.
```

## Steps
1. Split the work so that each packet changes 1 to 3 files and has one runnable check.
2. Put code that must be exact (a selector map, a CSV header, a regex) inside the packet verbatim. Do not ask Copilot to invent it.
3. Number the packets. A later packet never assumes an earlier one succeeded without its DONE WHEN being reported.
4. When the user pastes results back, diff them against DONE WHEN before writing the next packet.
5. Strip anything sensitive before writing a packet. It goes into a work tool.

## Why this shape
Free Copilot has a short context and no memory of the plan. A packet that carries its own context, constraints and pass/fail check survives the handoff.
