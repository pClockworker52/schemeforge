"""First-order (Godunov) reconstruction: piecewise constant cell values."""


def reconstruct(W, gamma):
    return W[2:-3], W[3:-2]
