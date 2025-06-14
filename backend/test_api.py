import json
from enhanced_resume_ranker_connect import ResumeRankerAPI

# Initialize API
api = ResumeRankerAPI()

# Test 1: Analyze job and rank multiple resumes
with open('job_description.txt', 'r', encoding='utf-8') as f:
    job_description = f.read().strip()

result = api.analyze_job_and_rank(job_description, '../data/data/data', top_n=5)
print("Test 1: Multiple Resume Ranking")
print(json.dumps(result, indent=2))

# Test 2: Rank a single resume
with open('sample_resume.txt', 'r', encoding='utf-8') as f:
    resume_text = f.read().strip()

single_result = api.rank_single_resume(job_description, resume_text, filename="test_resume.pdf")
print("\nTest 2: Single Resume Ranking")
print(json.dumps(single_result, indent=2))
