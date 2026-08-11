# 1. Import the functions you want to test from your main script
from cli_data_processor import filter_cri_maj, parse_single_line

# 2. Write a test function starting with 'test_'
def test_filter_cri_maj():
    # Give it fake data
    mock_lines = [
        "[2026-08-10 08:04:00] [INFO] [Auth] Rate limit checked",
        "[2026-08-10 08:02:05] [MAJOR] [Network] CPU throttling active"
    ]
    
    # Run your function
    filtered = list(filter_cri_maj(mock_lines))
    
    # 3. Assert (prove) it worked correctly
    assert len(filtered) == 1
    assert "MAJOR" in filtered[0]

def test_parse_single_line():
    mock_line = "[2026-08-10 08:05:07] [CRITICAL] [Hardware] Thermal warning"
    
    result = parse_single_line(mock_line)
    
    assert result["level"] == "CRITICAL"
    assert result["section"] == "Hardware"
    assert result["message"] == "Thermal warning"
