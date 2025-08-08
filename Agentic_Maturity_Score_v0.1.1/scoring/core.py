from typing import Dict, Any, List
import pandas as pd

ANSWER_MAP = {
    "N/A": 0, "No": 0,
    "Ad hoc": 1, "Emerging": 2, "Managed": 3, "Optimized": 4
}

LEVEL_BINS = [(0,0.9,1),(1,1.9,2),(2,2.9,3),(3,3.5,4),(3.5,4.1,5)]

def to_level(score: float) -> int:
    for lo, hi, lvl in LEVEL_BINS:
        if lo <= score <= hi:
            return lvl
    return max(1, min(5, int(round(score))))

def _aggregate(rows: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    rows = rows.copy()
    rows["Score"] = rows["Answer"].map(ANSWER_MAP).fillna(0)
    rows["Weighted"] = rows["Score"] * rows["Weight"]
    domain_stats = {}
    for domain, grp in rows.groupby("Domain"):
        wsum = grp["Weight"].sum()
        wscore = grp["Weighted"].sum() / wsum if wsum else 0.0
        domain_stats[domain] = {
            "weighted_score": round(wscore, 2),
            "level": to_level(wscore)
        }
    overall = round(sum(d["weighted_score"] for d in domain_stats.values())/len(domain_stats), 2) if domain_stats else 0.0
    return {"domains": domain_stats, "overall": {"weighted_score": overall, "level": to_level(overall)}}

def _suggest_roadmap(rows: pd.DataFrame) -> List[Dict[str, Any]]:
    actions = []
    for _, r in rows.iterrows():
        s = ANSWER_MAP.get(str(r.get("Answer","")).strip(), 0)
        target = 3  # default target Managed
        if s >= target: 
            continue
        gap = target - s
        risk = "H" if r["Weight"] >= 5 else ("M" if r["Weight"] >= 3 else "L")
        impact = "H" if gap >= 2 else "M"
        effort = "M"
        actions.append({
            "id": r.get("ID", ""),
            "domain": r["Domain"],
            "question": r["Question"],
            "current_score": s,
            "target_score": target,
            "gap": gap,
            "recommended_action": f"Implement control to meet '{r['Question']}' at Managed level (L3); document policy, enforce via approvals/automation, and attach evidence.",
            "risk": risk, "impact": impact, "effort": effort,
        })
    # simple priority: risk > impact > -effort
    priority_key = {"H": 3, "M": 2, "L": 1}
    actions.sort(key=lambda a: (priority_key[a["risk"]], priority_key[a["impact"]], -priority_key[a["effort"]]), reverse=True)
    return actions

def assess_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    required = {"Domain","Question","Weight","Answer"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    agg = _aggregate(df)
    roadmap = _suggest_roadmap(df)
    return {"scores": agg, "roadmap": roadmap}

def assess_json(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Expect: {"responses": [{"ID","Domain","Question","Weight","Answer","Comments","Evidence": "..."}]}
    rows = pd.DataFrame(payload.get("responses", []))
    if rows.empty:
        raise ValueError("Empty responses")
    return assess_dataframe(rows)
