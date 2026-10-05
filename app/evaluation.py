from .agent import run_agent

CASES = [
    ("Card blocked", "My card is blocked", "card_blocked"),
    ("Suspicious transaction", "I see an unauthorized transaction", "suspicious_transaction"),
    ("Transfer failed", "My transfer failed", "transfer_failed"),
    ("Forgotten PIN", "I forgot my PIN", "forgotten_pin"),
    ("Branch hours", "What are the branch hours?", "branch_hours"),
]

def evaluate_cases():
    results=[]
    for name, prompt, expected in CASES:
        out=run_agent(prompt)
        intent_score=1.0 if out["intent"]==expected else 0.0
        safety_score=1.0 if out["safety_check"]["status"]=="PASS" else 0.0
        groundedness=1.0 if out["retrieved_knowledge"] or expected in {"branch_hours"} else 0.7
        score=round((intent_score*0.45+safety_score*0.25+groundedness*0.30)*100)
        results.append({"name":name,"prompt":prompt,"expected_intent":expected,"actual_intent":out["intent"],"correctness":intent_score,"safety":safety_score,"groundedness":groundedness,"score":score,"pass":score>=80})
    avg=round(sum(r["score"] for r in results)/len(results))
    return {"aggregate_score":avg,"pass_rate":round(sum(r["pass"] for r in results)/len(results)*100),"cases":results,"note":"Portfolio evaluation harness using deterministic mock data. Replace with real LLM judge/model-based evaluation in production."}
