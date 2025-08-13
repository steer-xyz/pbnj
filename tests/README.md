# Testing Guide

## Prerequisites

Before running tests, install development dependencies:

```bash
uv sync --dev
```

## Quick Start

### Run All Tests
```bash
# Complete test suite with verbose output
uv run python -m pytest tests/ -v

# Minimal output
uv run python -m pytest tests/
```

### Run by Component
```bash
# PBIX parser tests
uv run python -m pytest tests/test_parser.py -v

# Documentation generation tests
uv run python -m pytest tests/test_documentation_generator.py -v

# CLI command tests
uv run python -m pytest tests/test_cli_main.py -v

# Web server tests
uv run python -m pytest tests/test_web_server.py -v

# Git integration tests
uv run python -m pytest tests/test_git_integration.py -v
```

### Run Specific Tests
```bash
# Specific test class
uv run python -m pytest tests/test_parser.py::TestPBIXParser -v

# Specific test method
uv run python -m pytest tests/test_parser.py::TestPBIXParser::test_parser_initialization -v

# Tests matching a pattern
uv run python -m pytest tests/ -k "parser" -v
```

### Coverage Reports
```bash
# Generate coverage report
uv run python -m pytest tests/ --cov=src/pbnj --cov-report=html --cov-report=term

# View HTML coverage report
open htmlcov/index.html
```

### Quick Options
```bash
# Skip integration tests
uv run python -m pytest tests/ -m "not integration" -v

# Minimal output
uv run python -m pytest tests/ -q

# Stop on first failure
uv run python -m pytest tests/ -x
```

## Understanding Test Results

### Test Output Examples

#### ✅ Successful Test Run
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.4.1
collected 15 items

tests/test_parser.py::TestPBIXParser::test_parser_initialization PASSED  [  6%]
tests/test_parser.py::TestPBIXParser::test_load_model_success PASSED     [ 13%]
...
tests/test_parser.py::TestPBIXParser::test_get_summary PASSED           [100%]

============================== 15 passed in 0.82s ==============================
```

**What this means:**
- ✅ All 15 tests passed
- ✅ Completed in 0.82 seconds
- ✅ No failures or errors

#### ❌ Failed Test Run
```
=================================== FAILURES ===================================
______________ TestPBIXParser.test_extract_tables_error_handling _______________

self = <tests.test_parser.TestPBIXParser object at 0x7d9eeb858800>

    def test_extract_tables_error_handling(self):
        """Test error handling in table extraction."""
        # ... test code ...
>       assert len(tables) == 1
E       assert 0 == 1
E        +  where 0 = len([])

tests/test_parser.py:151: AssertionError
```

**What this means:**
- ❌ Test `test_extract_tables_error_handling` failed
- ❌ Expected 1 item in tables list, but got 0
- ❌ Failure at line 151 in the test file
- ❌ The assertion `assert len(tables) == 1` failed

### Coverage Reports

```
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
src/pbnj/core/parser.py              109     16    85%   77-78, 87-88, 97-98
src/pbnj/docs/generator.py           149      3    98%   191, 284, 286
----------------------------------------------------------------
TOTAL                                600    450    25%
```

**Coverage metrics:**
- **Stmts:** Total lines of code
- **Miss:** Lines not covered by tests
- **Cover:** Percentage covered
- **Missing:** Specific line numbers not tested

**Coverage benchmarks:**
- 80%+ = Excellent
- 60-80% = Good
- <60% = Needs improvement

### Test Status Indicators

- **PASSED** ✅ - Test ran successfully
- **FAILED** ❌ - Test assertion failed
- **ERROR** ⚠️ - Test couldn't run (syntax/import issues)
- **SKIPPED** ⏭️ - Test was intentionally skipped
- **XFAIL** ⚠️ - Expected to fail (known issue)

## Test Categories

### Unit Tests
Test individual functions/methods in isolation:
```bash
# Example: Test just the parser initialization
uv run python -m pytest tests/test_parser.py::TestPBIXParser::test_parser_initialization -v
```

### Integration Tests
Test components working together with real files:
```bash
# Run integration tests (uses real AdventureWorks.pbix file)
uv run python -m pytest tests/ -m "integration" -v
```

### Mock Tests
Test with simulated dependencies:
```bash
# These tests mock external services/files
uv run python -m pytest tests/test_cli_main.py -v
```

## Debugging Failed Tests

### Get Detailed Error Information
```bash
# Show full traceback for failures
uv run python -m pytest tests/test_parser.py -vvv --tb=long

# Show only the failing line
uv run python -m pytest tests/test_parser.py --tb=line

# Stop on first failure for easier debugging
uv run python -m pytest tests/test_parser.py -x
```

### Add Debug Output
```bash
# Show print statements in tests
uv run python -m pytest tests/test_parser.py -s

# Show pytest's captured output
uv run python -m pytest tests/test_parser.py --capture=no
```

### Run Single Failing Test
```bash
# Focus on one failing test
uv run python -m pytest tests/test_parser.py::TestPBIXParser::test_failing_method -vvv
```

## Performance Testing

### Check Test Speed
```bash
# Show duration for each test
uv run python -m pytest tests/ --durations=10

# Show slowest tests
uv run python -m pytest tests/ --durations=0
```

## Common Workflows

### Daily Development
```bash
# 1. Quick check - run fast tests only
uv run python -m pytest tests/test_parser.py tests/test_documentation_generator.py -q

# 2. Before committing - run with coverage
uv run python -m pytest tests/ --cov=src/pbnj --cov-report=term-missing

# 3. Debugging a specific issue
uv run python -m pytest tests/test_cli_main.py::TestCLIMain::test_init_command_success -vvv --tb=long
```

### Component-Specific Testing
```bash
# Testing parser changes
uv run python -m pytest tests/test_parser.py -v

# Testing documentation templates
uv run python -m pytest tests/test_documentation_generator.py -k "template" -v

# Testing web API
uv run python -m pytest tests/test_web_server.py -v
```

### Integration Testing with Real Files
```bash
# Test with the actual AdventureWorks.pbix file
uv run python -m pytest tests/ -m "integration" -v
```