import json
import argparse
import re
from llm_client import get_response
from api import get_all_problems, submit_code, check_status, hello, check_auth
from calc_rating import calc_elo_rating, get_percentile


def make_html_problem(problem):
    title = problem["meta"]["title"]
    sections = problem["statement"]["content"]["sections"]
    html_output = '<html><body>'
    for ith, section in enumerate(sections):
        if ith == 0:
            html_output += f"<h1>{title}</h1>"
        else:
            html_output += f"<h2>{section['title']}</h2>"
        html_output += f"<div>{section['value']['content']}</div>"
    html_output += '</body></html>'
    return html_output


def extract_code_blocks(text):
    pattern = r'```(\w*)\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


lang_map = {
    'kotlin': 88,  # Kotlin 1.9.21
    'cpp': 91,     # GNU G++23 14.2 (64 bit, msys2)
    'ruby': 67,    # Ruby 3.2.2
    'd': 28,       # D DMD32 v2.105.0
    'python': 70,  # PyPy 3.10 (7.3.15, 64bit)
    'pascal': 51,  # PascalABC.NET 3.8.3
    'rust': 75,    # Rust 1.75.0 (2021)
    'go': 32,      # Go 1.22.2
    'node.js': 55, # Node.js 15.8.0 (64bit)
    'haskell': 12, # Haskell GHC 8.10.1
    'javascript': 34, # JavaScript V8 4.8.0
    'csharp': 79,  # C# 10, .NET SDK 6.0
    'perl': 13,    # Perl 5.20.1
    'java': 87,    # Java 21 64bit
    'ocaml': 19,   # OCaml 4.02.1
    'delphi': 3,   # Delphi 7
    'php': 6,      # PHP 8.1.7
    'scala': 20,   # Scala 2.12.8
    'c': 43        # GNU GCC C11 5.1.0
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-Coder-7B-Instruct")
    parser.add_argument("--bid", type=int, default=1980)
    parser.add_argument("--eid", type=int, default=1981)
    args = parser.parse_args()
    model = args.model

    instruction = """"You are a coding expert. Given a competition-level coding problem, you need to write a C++ program to solve it. You may start by outlining your thought process. In the end, please provide the complete code in a code block enclosed with ``` ```."""

    print(hello())

    auth = check_auth()
    if auth.status_code != 200:
        print(auth.text)
        print("Failed to authenticate, set TOKEN in api.py before running")
        exit()
    print("Authenticated")

    status_dict = {}
    for id in range(args.bid, args.eid + 1):
        problems = get_all_problems(id, True)
        print(f"Problems: {problems}")
        problems = problems["problems"]
        print(f"id: {id}, len(problems) = {len(problems)}")
        if not problems:
            continue
        for ith, problem in enumerate(problems):
            print(f"Processing {id}, {ith}, problem: {problem}")
            problem_data = json.loads(problem["json_str"])
            print(problem_data.keys())
            html_problem = make_html_problem(problem_data)
            print(html_problem)
            prompt = f"{instruction}\n\n{html_problem}"

            status_dict[problem["prob"]] = []
            # if 'D' in problem["prob"]:
            #     break
            for _ in range(8):
                try:
                    response = get_response(prompt, model)
                    print(response)
                    code_blocks = extract_code_blocks(response)
                    if not code_blocks:
                        print("No code found")
                        status_dict[problem["prob"]].append("No code")
                        continue
                    code_block = code_blocks[0]
                    code = code_block[1]
                    if code_block[0]:
                        lang_id = lang_map[code_block[0]]
                    else:
                        lang_id = lang_map["cpp"]
                    submission_id = submit_code(problem["prob"], lang_id, code, tag=model)
                    # status = check_status(submission_id)
                    print(f"Submitted {problem['prob']}, submission_id: {submission_id}")
                    submission_id = submission_id["submission_id"]
                    status_dict[problem["prob"]].append(submission_id)
                except Exception as e:
                    print(f"Error: {e}")
                    status_dict[problem["prob"]].append("Error")
                    continue
                # exit()
        
    for key, value in status_dict.items():
        for ith, submission_id in enumerate(value):
            print(f"{key} {ith}: {submission_id}")
            if submission_id == "No code":
                continue
            status = check_status(submission_id)
            print(f"{key} {ith}: {status}")
            status_dict[key][ith] = status['status_canonical']

    print(f"status_dict: {status_dict}")
    print(f"Processing {id}, len(problems) = {len(problems)}")
    ratings = {}
    rating_list = []
    for id in range(args.bid, args.eid + 1):
        ratings[id] = calc_elo_rating(id, status_dict)
        if "rating" in ratings[id]:
            rating_list.append(ratings[id]["rating"])
    print(f"ratings: {ratings}")
    average_rating = sum(rating_list) / len(rating_list)
    percentile = get_percentile(average_rating)
    print(f"Average rating: {average_rating}, percentile: {percentile}")