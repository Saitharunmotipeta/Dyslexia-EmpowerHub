from flows.learning import run_learning_flow
from flows.practice import run_practice_flow
from flows.mock import run_mock_flow

from asserts.common import assert_not_empty
from asserts.learning import assert_learning_success
from asserts.practice import assert_practice_success
from asserts.mock import assert_mock_success


def run_positive_cases(client, context, cfg):
    """
    Happy path:
    learning → practice → mock → report
    """

    # -------------------------
    # LEARNING
    # -------------------------
    learning_result = run_learning_flow(client, context, cfg)
    assert_learning_success(learning_result)

    # -------------------------
    # PRACTICE
    # -------------------------
    practice_result = run_practice_flow(client, context, cfg)
    assert_practice_success(practice_result)

    # -------------------------
    # MOCK TEST
    # -------------------------
    mock_result = run_mock_flow(client, context, cfg)
    assert_mock_success(mock_result)

    assert_not_empty(mock_result["report_bytes"], "PDF report size")
