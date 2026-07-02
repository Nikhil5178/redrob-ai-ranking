import json
import pandas as pd

# Change filename if needed
FILE_NAME = "candidates.jsonl"

required_skills = [
    "Python",
    "LLM",
    "Embeddings",
    "Vector",
    "Retrieval",
    "Ranking",
    "Pinecone",
    "Qdrant",
    "Milvus",
    "FAISS",
    "OpenSearch",
    "Elasticsearch"
]

results = []

with open(FILE_NAME, "r", encoding="utf-8") as f:
    for line in f:

        candidate = json.loads(line)

        score = 0

        profile = candidate["profile"]

        summary = profile.get("summary", "").lower()

        headline = profile.get("headline", "").lower()

        skills = []

        for s in candidate.get("skills", []):
            skills.append(s["name"].lower())

        text = summary + " " + headline + " " + " ".join(skills)

        # Experience
        exp = profile.get("years_of_experience",0)

        if 5 <= exp <= 9:
            score += 20

        elif exp > 9:
            score += 10

        # Skill Matching
        for skill in required_skills:
            if skill.lower() in text:
                score += 5

        signals = candidate.get("redrob_signals",{})

        if signals.get("open_to_work_flag"):
            score += 10

        score += signals.get("github_activity_score",0)/10

        score += signals.get("recruiter_response_rate",0)*10

        results.append({
            "candidate_id":candidate["candidate_id"],
            "score":round(score,2)
        })

results = sorted(results,key=lambda x:x["score"],reverse=True)

top100 = results[:100]

rows=[]

for i,c in enumerate(top100,1):

    rows.append({
        "candidate_id":c["candidate_id"],
        "rank":i,
        "score":c["score"],
        "reasoning":"Strong skill and experience match with the job description."
    })

df=pd.DataFrame(rows)

df.to_excel("Top100Candidates.xlsx",index=False)

print("Done!")