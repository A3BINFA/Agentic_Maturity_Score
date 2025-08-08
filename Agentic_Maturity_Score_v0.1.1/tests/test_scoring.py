from scoring.core import assess_json
def test_assess_minimal():
    payload = {"responses":[{"ID":"Q1","Domain":"Suitability Evaluation","Question":"x","Weight":5,"Answer":"Ad hoc"}]}
    out = assess_json(payload)
    assert "scores" in out and "roadmap" in out
