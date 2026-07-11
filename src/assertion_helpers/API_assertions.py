from src.API.models.common_models import PaginatedStrictModel


def assert_pagination(model: PaginatedStrictModel, requested_limit=30, requested_skip=0, expected_total = None):
    #if total count is less than requested limit endpoint returns total count and limit with the same data
    expected_limit = max(min(requested_limit, model.total - requested_skip), 0)

    assert model.skip == requested_skip
    assert model.limit == expected_limit
    if expected_total is not None:
        assert model.total == expected_total, (f'Expected total count of items are different from actual, '
                                               f'exected {expected_total}, actual {model.total}')
    else:
        assert model.total > 0