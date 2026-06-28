# AGY Session Rules & AFA Compliance Audit Logging Framework

This repository houses the research project **"Computational Capital Budgeting: Simulation Design for Allocating Scarce AI Tokens"** submitted for the AFA Special Session. The end goals and simulation design are defined dynamically by `Tokenization.pdf`.

To comply with mandatory AFA submission rules, AGY must enforce real-time prompt/response logging and dynamic session continuity while maximizing token efficiency.

---

## 1. Directory Structure for Audit Logs
All logs and state tracking are stored inside `logs/`:

```text
logs/
├── full_conversation_log.md  # Continuous human-readable transcript of ALL prompts & full AI responses
├── session_summary.md        # Concise living summary (~15 lines max) of COMPLETED work and current state
├── human_time_log.csv        # Log of human minutes/hours and activities
└── sessions/                 # Date-wise detailed markdown conversation logs
```

---

## 2. Token-Efficiency & Blind-Append Protocol (CRITICAL)
- **DO NOT READ LOG FILES:** AGY must **NEVER read or view** `logs/full_conversation_log.md` or files under `logs/sessions/` during chat interactions. Reading log files into context wastes tokens.
- **Blind Append Only:** When logging prompts and responses, AGY performs an append operation to the end of `logs/full_conversation_log.md` and `logs/sessions/YYYY-MM-DD_session.md` without reading existing content.
- **Full AI Response Storage:** Store the complete, untruncated AI response text in the log file for 100% AFA submission compliance. Since log files are never read back into context, full storage incurs ZERO context token cost on future turns!
- **Minimal State Reading:** Upon launching a new session, AGY ONLY reads `logs/session_summary.md` (which must be kept under 20 lines) to catch up on state.

---

## 3. Real-Time Conversation Logging Format
- Append format for `logs/full_conversation_log.md` and `logs/sessions/YYYY-MM-DD_session.md`:
  ```markdown
  ## [Timestamp] User Prompt
  <exact user prompt>

  ## [Timestamp] AI Response
  <complete, detailed AI response text>
  ```

---

## 4. Dynamic Progress Tracking & Attribution
- `Tokenization.pdf` is the master research specification.
- `logs/session_summary.md` must only record actual completed milestones and current code state (strictly under 20 lines).
- Tag generated simulation logic with `# [AI-Generated]` and parameters with `# [Human-Authored]`.
