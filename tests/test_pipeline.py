import os
from pipeline import runner


def test_run_sample(tmp_path):
    base = os.path.join(os.path.dirname(__file__), '..', 'sample_inputs')
    paths = [os.path.join(base, 'recruiter.csv'), os.path.join(base, 'ats.json'), os.path.join(base, 'resume.txt')]
    config = {
        "select_fields": ["name", "email", "phone", "skills", "sources", "confidence"],
        "include_provenance": True,
        "include_confidence": True,
    }
    result = runner.run(paths, config)
    assert isinstance(result, list)
    # ensure merged records include at least Alice and Bob
    names = {r.get('name') for r in result}
    assert 'Alice Example' in names
    assert 'Bob Candidate' in names
