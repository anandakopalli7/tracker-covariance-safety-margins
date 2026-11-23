"""LOCAL STAND-IN for the third-party package `lap` (not installed on this laptop).

lapjv(cost, extend_cost=True, cost_limit=L) in the real package builds the (r+c) x (r+c) matrix
    [[cost, L/2], [L/2, 0]]
solves the square assignment problem on it and reports x[i] = column of row i (or -1 if the row went to an added
column), y[j] = row of column j (or -1). The same extended matrix is built here and solved with
scipy.optimize.linear_sum_assignment (also an exact solver; the result is identical whenever the optimum is unique).
Checked through the bit-level replay comparison (tracker_harness_v0x.py): any different association changes track ids.
"""
import numpy as np
from scipy.optimize import linear_sum_assignment


def lapjv(cost, extend_cost=False, cost_limit=np.inf, return_cost=True):
    cost = np.ascontiguousarray(cost, dtype=np.double)
    if cost.ndim != 2:
        raise ValueError('2-dimensional array expected')
    n_rows, n_cols = cost.shape
    if n_rows != n_cols and not extend_cost:
        raise ValueError('Square cost array expected. If cost is intentionally non-square, pass extend_cost=True.')
    extended = extend_cost or cost_limit < np.inf
    c = cost
    if extended:
        n = n_rows + n_cols
        c = np.empty((n, n), dtype=np.double)
        if cost_limit < np.inf:
            c[:] = cost_limit / 2.
        else:
            c[:] = cost.max() + 1
        c[n_rows:, n_cols:] = 0
        c[:n_rows, :n_cols] = cost
    n = c.shape[0]
    rows, cols = linear_sum_assignment(c)
    x = np.empty(n, dtype=np.int32)
    y = np.empty(n, dtype=np.int32)
    x[rows] = cols
    y[cols] = rows
    opt = np.nan
    if extended:
        x[x >= n_cols] = -1
        y[y >= n_rows] = -1
        x = x[:n_rows]
        y = y[:n_cols]
        if return_cost:
            opt = c[np.nonzero(x != -1)[0], x[x != -1]].sum()
    elif return_cost:
        opt = c[np.arange(n_rows), x].sum()
    if return_cost:
        return opt, x, y
    return x, y
