#!/usr/bin/env python3
"""
Cloud monitor script for ShaderGUI Learning project.

Validates deployed preview URL and generates cloud report.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def check_url(base_url: str, timeout: int = 10) -> dict:
    """
    Check if URL is accessible and returns valid response.
    
    Args:
        base_url: Base URL to check
        timeout: Request timeout in seconds
        
    Returns:
        dict: Result with status, status_code, response_time, error
    """
    result = {
        "url": base_url,
        "status": "unknown",
        "status_code": None,
        "response_time": None,
        "error": None,
    }
    
    try:
        start = time.time()
        req = Request(base_url, headers={"User-Agent": "CloudMonitor/1.0"})
        resp = urlopen(req, timeout=timeout)
        elapsed = time.time() - start
        
        result["status"] = "ok"
        result["status_code"] = resp.status
        result["response_time"] = round(elapsed * 1000, 2)
        
    except HTTPError as e:
        result["status"] = "http_error"
        result["status_code"] = e.code
        result["error"] = str(e)
    except URLError as e:
        result["status"] = "connection_error"
        result["error"] = str(e.reason)
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        
    return result


def check_course_data(base_url: str, timeout: int = 10) -> dict:
    """
    Check if course data JSON files are accessible.
    
    Args:
        base_url: Base URL of the deployed app
        timeout: Request timeout in seconds
        
    Returns:
        dict: Result with checked files and their status
    """
    data_files = [
        "/data/storyboard-contract.json",
        "/data/design-contract.json",
        "/data/stitch-manifest.json",
    ]
    
    results = {}
    for file in data_files:
        url = base_url.rstrip("/") + file
        result = check_url(url, timeout)
        results[file] = result
        
    return results


def generate_report(
    base_url: str,
    check_result: dict,
    course_data_results: dict,
    output_file: str | None = None,
    write_memory: bool = False,
) -> str:
    """
    Generate cloud validation report.
    
    Args:
        base_url: Base URL checked
        check_result: Result from check_url()
        course_data_results: Results from check_course_data()
        output_file: Path to write report to (optional)
        write_memory: Whether to write to .agent/memory/
        
    Returns:
        str: Generated report content
    """
    timestamp = datetime.now().isoformat(timespec="seconds")
    report_lines = [
        f"# Cloud Validation Report",
        "",
        f"- **Timestamp**: {timestamp}",
        f"- **Base URL**: {base_url}",
        "",
        "## Main Page Check",
        "",
        f"- **Status**: {check_result['status']}",
    ]
    
    if check_result["status_code"]:
        report_lines.append(f"- **Status Code**: {check_result['status_code']}")
    if check_result["response_time"]:
        report_lines.append(f"- **Response Time**: {check_result['response_time']} ms")
    if check_result["error"]:
        report_lines.append(f"- **Error**: {check_result['error']}")
        
    report_lines.extend([
        "",
        "## Course Data Check",
        "",
    ])
    
    for file, result in course_data_results.items():
        status = result["status"]
        report_lines.append(f"- `{file}`: {status}")
        if result.get("error"):
            report_lines.append(f"  - Error: {result['error']}")
            
    report_lines.extend([
        "",
        "## Summary",
        "",
    ])
    
    # Calculate summary
    all_ok = all(
        r["status"] == "ok"
        for r in [check_result] + list(course_data_results.values())
    )
    overall = "✅ PASSED" if all_ok else "❌ FAILED"
    report_lines.append(f"**Overall**: {overall}")
    
    report = "\n".join(report_lines) + "\n"
    
    # Write to file if specified
    if output_file:
        Path(output_file).write_text(report, encoding="utf-8")
        print(f"Report written to: {output_file}")
        
    # Write to memory if requested
    if write_memory:
        memory_dir = Path(".agent/memory")
        memory_dir.mkdir(parents=True, exist_ok=True)
        memory_file = memory_dir / f"cloud-{datetime.now().strftime('%Y-%m-%d')}.md"
        memory_file.write_text(report, encoding="utf-8")
        print(f"Memory updated: {memory_file}")
        
    return report


def main():
    parser = argparse.ArgumentParser(description="Cloud monitor for ShaderGUI Learning")
    parser.add_argument("--base-url", required=True, help="Base URL to monitor")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    parser.add_argument("--report", help="Path to write report to")
    parser.add_argument("--write-memory", action="store_true", help="Write report to .agent/memory/")
    args = parser.parse_args()
    
    print(f"Checking: {args.base_url}")
    
    # Check main page
    result = check_url(args.base_url, args.timeout)
    print(f"Main page: {result['status']} (HTTP {result['status_code']})")
    
    # Check course data files
    course_results = check_course_data(args.base_url, args.timeout)
    for file, file_result in course_results.items():
        print(f"  {file}: {file_result['status']}")
        
    # Generate report
    report = generate_report(
        args.base_url,
        result,
        course_results,
        output_file=args.report,
        write_memory=args.write_memory,
    )
    
    print("\n" + report)
    
    # Exit with error if any check failed
    if result["status"]!= "ok" or any(r["status"]!= "ok" for r in course_results.values()):
        sys.exit(1)
        
    sys.exit(0)


if __name__ == "__main__":
    main()
