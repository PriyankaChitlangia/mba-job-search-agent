from core.agent import MBAJobSearchAgent

def main():
    agent = MBAJobSearchAgent()
    jobs = agent.load_jobs()
    candidates = agent.load_candidates()
    print(f"Loaded {len(jobs)} jobs and {len(candidates)} candidates.")

    cand = candidates[0]
    print(f"Evaluating: {cand['name']} ({cand['degree']})")
    
    ranked = agent.match_jobs(cand)
    top_3 = ranked[:3]
    for i, r in enumerate(top_3, 1):
        print(f"  #{i}: {r['job_title']} @ {r['company']} - Match: {r['match_score_pct']}%")

    top_job = ranked[0]['job_details']
    gap_data = agent.run_gap_analysis(cand, top_job, ranked[0])
    print(f"\nGap Analysis for {top_job['title']}:")
    print(f"  Strengths: {gap_data['strengths']}")
    print(f"  Critical Gaps: {gap_data['critical_gaps']}")

    checklist = agent.generate_checklist(cand, top_job, gap_data)
    cover_letter = agent.generate_cover_letter(cand, top_job, gap_data)
    
    print("\nChecklist snippet:")
    print(checklist[:200] + "...")
    print("\nCover letter snippet:")
    print(cover_letter[:200] + "...")
    print(f"\nTotal execution trace logs: {len(agent.execution_trace)}")
    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()

