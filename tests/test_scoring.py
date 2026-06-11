from src.scoring import grade_score


def test_grade_a():
    assert grade_score(85).startswith('A')


def test_grade_b():
    assert grade_score(70).startswith('B')


def test_grade_reject():
    assert grade_score(10) == 'Reject'
