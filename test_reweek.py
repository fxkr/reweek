from reweek import change


# Used dates:
# - 2011-01-02 (Sun)
# - 2011-01-03 (Mon) # One day after
# - 2011-02-03 (Thu) # One month after
# - 2012-02-03 (Fri) # One year after


def test_simple_date():
    assert change("2011-01-02") == "2011-01-02 (Sun)"

def test_day_range():
    assert change("2011-01-02..03") == "2011-01-02..03 (Sun-Mon)"

def test_month_range():
    assert change("2011-01-02..02-03") == "2011-01-02..02-03 (Sun-Thu)"

def test_year_range():
    assert change("2011-01-02..2012-02-03")\
        == "2011-01-02..2012-02-03 (Sun-Fri)"

def test_shorten_month_range_to_day_range():
    assert change("2011-01-02..01-03") == "2011-01-02..03 (Sun-Mon)"

def test_shorten_year_range_to_day_range():
    assert change("2011-01-02..2011-01-03") == "2011-01-02..03 (Sun-Mon)"

def test_shorten_year_range_to_month_range():
    assert change("2011-01-02..2011-02-03") == "2011-01-02..02-03 (Sun-Thu)"

def test_hint_not_duplicated():
    assert change("2011-01-02 (Sun)") == "2011-01-02 (Sun)"

def test_day_range_hint_not_duplicated():
    assert change("2011-01-02..03 (Sun-Mon)") == "2011-01-02..03 (Sun-Mon)"

def test_month_range_hint_not_duplicated():
    assert change("2011-01-02..02-03 (Sun-Thu)") == "2011-01-02..02-03 (Sun-Thu)"

def test_year_range_hint_not_duplicated():
    assert change("2011-01-02..2012-02-03 (Sun-Fri)")\
        == "2011-01-02..2012-02-03 (Sun-Fri)"

def test_other_text_preserved():
    assert change("foo 2011-01-02 bar") == "foo 2011-01-02 (Sun) bar"

def test_multiple_replacements():
    assert change("foo 2011-01-02 bar 2012-02-03 baz")\
        == "foo 2011-01-02 (Sun) bar 2012-02-03 (Fri) baz"

def test_hint_not_replaced_silently():
    assert change("2011-01-02 (Mon)") == "2011-01-02 (Mon??)"

def test_range_hint_not_replaced_silently():
    assert change("2011-01-02..03 (Tue-Wed)") == "2011-01-02..03 (Tue??-Wed??)"
    assert change("2011-01-02..03 (Tue-Mon)") == "2011-01-02..03 (Tue??-Mon)"
    assert change("2011-01-02..03 (Sun-Wed)") == "2011-01-02..03 (Sun-Wed??)"

def test_necessary_hint_marker_replaced_silently():
    assert change("2011-01-02 (Mon??)") == "2011-01-02 (Mon??)"

def test_unnecessary_hint_marker_removed_silently():
    assert change("2011-01-02 (Sun??)") == "2011-01-02 (Sun)"

def test_necessary_range_hint_marker_replaced_silently():
    assert change("2011-01-02..03 (Tue??-Wed??)") == "2011-01-02..03 (Tue??-Wed??)"
    assert change("2011-01-02..03 (Tue??-Mon)") == "2011-01-02..03 (Tue??-Mon)"
    assert change("2011-01-02..03 (Sun-Wed??)") == "2011-01-02..03 (Sun-Wed??)"

def test_unnecessary_range_hint_marker_replaced_silently():
    assert change("2011-01-02..03 (Sun??-Mon??)") == "2011-01-02..03 (Sun-Mon)"
    assert change("2011-01-02..03 (Sun??-Mon)") == "2011-01-02..03 (Sun-Mon)"
    assert change("2011-01-02..03 (Sun-Mon??)") == "2011-01-02..03 (Sun-Mon)"
    assert change("2011-01-02..03 (Sun??-Tue)") == "2011-01-02..03 (Sun-Tue??)"
    assert change("2011-01-02..03 (Sat-Mon??)") == "2011-01-02..03 (Sat??-Mon)"

