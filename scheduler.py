import json
import os
import requests

# Load GitHub Token from environment
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_TOKEN not found in environment variables.")

EVENT_TYPE = "scheduler"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

# Read schedule_list.json
with open("schedule_list.json", "r") as file:
    schedule_list = json.load(file)

# Prepare markdown table header
summary_lines = [
    "## 🚀 Scheduler Summary\n",
    "| Repository | Branch | Status | Details |",
    "|------------|--------|--------|---------|"
]

for item in schedule_list:
    repo_name = item["repo_name"]
    branch = item["branch"]
    url = f"https://api.github.com/repos/{repo_name}/dispatches"
    payload = {
        "event_type": EVENT_TYPE,
        "client_payload": {"branch": branch}
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 204:
        summary_lines.append(f"| `{repo_name}` | `{branch}` | ✅ Success | &nbsp; |")
    else:
        detail = response.text.strip().replace('\n', ' ')
        summary_lines.append(f"| `{repo_name}` | `{branch}` | ❌ Failed ({response.status_code}) | `{detail}` |")

# Write markdown summary to GitHub Actions job summary
summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
if summary_path:
    with open(summary_path, "w") as summary_file:
        summary_file.write("\n".join(summary_lines))
else:
    print("GITHUB_STEP_SUMMARY not set. Printing summary instead:")
    print("\n".join(summary_lines))
