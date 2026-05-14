from password_strength import score_password, classify_score


def test_common_password():
    r = score_password("password")
    assert r["score"] < 10


def test_simple_password():
    r = score_password("P@ssw0rd!")
    assert r["score"] >= 40


def test_long_passphrase():
    r = score_password("correcthorsebatterystaple")
    assert r["score"] >= 70
    assert classify_score(r["score"]) in {"Strong", "Very Strong"}
