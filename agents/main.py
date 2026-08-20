"""
agents/main.py

CLI entrypoint to run the SkillBridge multi-agent pipeline locally.
Runs Diagnosis -> Roadmap Generation -> Micro-Project Verification.
"""

import sys
import json
import argparse
from pathlib import Path

# Add project root to sys.path if running directly
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Configure stdout utf-8 encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agents.orchestrator import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="SkillBridge Multi-Agent Pipeline Runner")
    parser.add_argument("--learner-id", default="demo_learner_001", help="Learner ID")
    parser.add_argument(
        "--target-role",
        default="Data Analyst",
        help="Target job role (e.g. 'Data Analyst', 'Backend Engineer')",
    )
    parser.add_argument(
        "--resume",
        default="Retail sales associate for 2 years. Experienced in Excel reporting, pivot tables, basic SQL queries, and beginner Python script writing.",
        help="Learner resume text or summary",
    )
    parser.add_argument(
        "--submission",
        default="",
        help="Optional submission code for micro-project verification",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON state output",
    )

    args = parser.parse_args()

    print("==================================================")
    print("[+] Running SkillBridge Multi-Agent Pipeline")
    print("==================================================")
    print(f"Learner ID  : {args.learner_id}")
    print(f"Target Role : {args.target_role}")
    print("--------------------------------------------------\n")

    initial_state = {
        "learner_id": args.learner_id,
        "target_role": args.target_role,
        "resume_text": args.resume,
    }

    if args.submission:
        initial_state["active_submission"] = args.submission

    final_state = run_pipeline(initial_state)

    if args.json:
        print(json.dumps(final_state, indent=2))
        return

    # Formatted terminal display
    print("[AGENT 1a: DIAGNOSIS RESULT]")
    print(f"Summary    : {final_state.get('diagnosis_summary', 'N/A')}")
    print(f"Confidence : {final_state.get('confidence', 0.0) * 100:.1f}%\n")
    
    print("Current Skills:")
    for skill in final_state.get("current_skills", []):
        name = skill.get("name") if isinstance(skill, dict) else skill
        level = skill.get("level", "N/A") if isinstance(skill, dict) else ""
        print(f"  * {name} ({level})")

    print("\nIdentified Skill Gaps:")
    for gap in final_state.get("skill_gaps", []):
        name = gap.get("name") if isinstance(gap, dict) else gap
        reason = gap.get("reason", "") if isinstance(gap, dict) else ""
        print(f"  * {name}: {reason}")

    print("\n--------------------------------------------------")
    print("[AGENT 1b: GROUNDED ROADMAP]")
    for i, step in enumerate(final_state.get("roadmap", []), 1):
        status_str = "[UNLOCKED]" if step.get("status") == "unlocked" else "[LOCKED]"
        print(f"\nStep {i}: {status_str} {step.get('title')} ({step.get('skill')})")
        print(f"   Reason      : {step.get('reason')}")
        print(f"   Description : {step.get('description')}")
        if step.get("citations"):
            for cite in step["citations"]:
                print(f"   Citation    : {cite.get('title')} -> {cite.get('url')}")

    print("\n--------------------------------------------------")
    print("[AGENT 2: VERIFICATION STATUS]")
    print(f"Pipeline Status     : {final_state.get('status')}")
    print(f"Active Node Index   : {final_state.get('active_node_index', 0)}")
    
    history = final_state.get("verification_history", [])
    if history:
        print(f"Verification History: {len(history)} submission(s) processed")
        for res in history:
            print(f"  - Skill: {res.get('node_skill')} | Status: {res.get('status')} | Score: {res.get('score')}")
            print(f"    Feedback: {res.get('judge_feedback')}")
    else:
        print("Awaiting micro-project submission for verification.")

    print("\n==================================================")
    print("[+] Pipeline execution complete.")
    print("==================================================")


if __name__ == "__main__":
    main()
