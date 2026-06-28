# [AI-Generated]
import sys
import os
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Blind append logs for AFA compliance framework.")
    parser.add_argument("--timestamp", required=True, help="Timestamp string")
    parser.add_argument("--prompt", required=True, help="User prompt text")
    parser.add_argument("--response", required=True, help="AI response text")
    args = parser.parse_args()

    date_str = args.timestamp.split()[0]
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(workspace_dir, "logs")
    sessions_dir = os.path.join(logs_dir, "sessions")

    os.makedirs(sessions_dir, exist_ok=True)

    full_log_path = os.path.join(logs_dir, "full_conversation_log.md")
    session_log_path = os.path.join(sessions_dir, f"{date_str}_session.md")

    log_entry = f"\n---\n\n## [{args.timestamp}] User Prompt\n{args.prompt}\n\n## [{args.timestamp}] AI Response\n{args.response}\n"

    with open(full_log_path, "a", encoding="utf-8") as f:
        f.write(log_entry)

    if not os.path.exists(session_log_path):
        with open(session_log_path, "w", encoding="utf-8") as f:
            f.write(f"# Session Log: {date_str}\n")

    with open(session_log_path, "a", encoding="utf-8") as f:
        f.write(log_entry)

if __name__ == "__main__":
    main()
