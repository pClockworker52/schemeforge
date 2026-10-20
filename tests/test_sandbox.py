"""Tests for the AST validator: hostile snippets must be rejected, clean candidates must pass."""

import textwrap

import pytest

from schemeforge.core.sandbox import validate_source

# (id, source, expected rule)
HOSTILE = [
    ("open-file", "def phi(r):\n    open('/etc/passwd')\n    return r", "forbidden-name"),
    ("alias-open", "def phi(r):\n    f = open\n    return r", "forbidden-name"),
    ("import-os", "import os\ndef phi(r):\n    return r", "import"),
    ("from-os", "from os import path\ndef phi(r):\n    return r", "import"),
    ("dunder-import", "def phi(r):\n    m = __import__('os')\n    return r", "forbidden-name"),
    ("dunder-attr", "def phi(r):\n    return ().__class__.__bases__", "dunder"),
    ("builtins", "def phi(r):\n    return __builtins__", "dunder"),
    ("globals", "def phi(r):\n    globals()['x'] = 1\n    return r", "forbidden-name"),
    ("getattr", "import math\ndef phi(r):\n    return getattr(math, 'pi')", "forbidden-name"),
    ("eval", "def phi(r):\n    return eval('r')", "forbidden-name"),
    ("exec", "def phi(r):\n    exec('x = 1')\n    return r", "forbidden-name"),
    ("random", "import random\ndef phi(r):\n    return r * random.random()", "import"),
    ("time", "import time\ndef phi(r):\n    return r + time.time()", "import"),
    ("jax-random", "from jax import random\ndef phi(r):\n    return r", "import"),
    ("bare-jax", "import jax\ndef phi(r):\n    return jax.numpy.maximum(r, 0.0)", "import"),
    ("jax-numpy-unaliased", "import jax.numpy\ndef phi(r):\n    return r", "import"),
    ("relative-import", "from . import helper\ndef phi(r):\n    return r", "import"),
    ("star-import", "from math import *\ndef phi(r):\n    return r", "import"),
    ("module-list", "CACHE = []\ndef phi(r):\n    return r", "module-value"),
    ("module-dict", "STATE = {'n': 0}\ndef phi(r):\n    return r", "module-value"),
    ("module-call", "import jax.numpy as jnp\nTABLE = jnp.zeros(3)\ndef phi(r):\n    return r", "module-value"),
    ("module-loop", "N = 0\nfor i in range(3):\n    N = i\ndef phi(r):\n    return r", "module-statement"),
    ("global-stmt", "N = 0\ndef phi(r):\n    global N\n    N = N + 1\n    return r", "global"),
    (
        "nonlocal",
        "def make():\n    n = 0\n    def phi(r):\n        nonlocal n\n        n = n + 1\n        return r\n"
        "    return phi",
        "global",
    ),
    ("mutable-default", "def phi(r, _seen=[]):\n    _seen.append(1)\n    return r", "default-arg"),
    ("call-default", "def phi(r, _c=dict()):\n    return r", "default-arg"),
    ("func-attr", "def phi(r):\n    phi.calls = 1\n    return r", "attr-assign"),
    ("class", "class Lim:\n    pass\ndef phi(r):\n    return r", "class"),
    ("decorator", "def deco(f):\n    return f\n@deco\ndef phi(r):\n    return r", "decorator"),
    ("jnp-load", "import jax.numpy as jnp\ndef phi(r):\n    return jnp.load('dev_answers.npy')", "forbidden-attr"),
    ("from-jnp-load", "from jax.numpy import load\ndef phi(r):\n    return r", "forbidden-attr"),
    ("format-escape", "def phi(r):\n    return '{0.__class__}'.format(r)", "forbidden-attr"),
    ("id-nondeterminism", "def phi(r):\n    return r * (id(r) % 2)", "forbidden-name"),
    ("print", "def phi(r):\n    print(r)\n    return r", "forbidden-name"),
    ("async", "async def phi(r):\n    return r", "async"),
    ("syntax-error", "def phi(r)\n    return r", "syntax"),
]


@pytest.mark.parametrize("source,rule", [(s, r) for _, s, r in HOSTILE], ids=[i for i, _, _ in HOSTILE])
def test_hostile_snippets_are_rejected(source: str, rule: str) -> None:
    result = validate_source(source)
    assert not result.ok
    assert rule in result.rules, [str(v) for v in result.violations]


def test_size_limit() -> None:
    source = "def phi(r):\n" + "    r = r + 0.0\n" * 200 + "    return r\n"
    result = validate_source(source, max_lines=150)
    assert "size" in result.rules


CLEAN = {
    "minmod": """
        import jax.numpy as jnp

        def phi(r):
            return jnp.maximum(0.0, jnp.minimum(1.0, r))
    """,
    "van-leer-with-helper-and-constants": '''
        """van Leer limiter."""
        import jax.numpy as jnp

        EPS = 1e-300
        TWO = 2.0

        def _abs(x):
            return jnp.abs(x)

        def phi(r):
            return (r + _abs(r)) / (1.0 + _abs(r) + EPS) * (TWO / 2.0)
    ''',
    "math-constants": """
        import math
        from jax import numpy as jnp
        from jax import lax

        C = math.sqrt(2.0) - 1.0
        PI_HALF = math.pi / 2
        PAIR = (1.0, -C)
        sq = lambda x: x * x

        def phi(r, k=C):
            s = lax.select(r > 0.0, r, jnp.zeros_like(r))
            return jnp.where(s > PI_HALF, 1.0, sq(s) * k + PAIR[0])
    """,
    "stateful-limiter": """
        import jax.numpy as jnp
        from jax.numpy import where

        def phi_s(r, state):
            target = jnp.clip(r, 0.0, 2.0)
            new = 0.5 * state + 0.5 * target
            return where(r > 0.0, new, 0.0), new
    """,
    "flux-with-local-helpers": """
        import jax.numpy as jnp

        def flux(UL, UR, gamma):
            def phys(U):
                rho, mom, E = U[:, 0], U[:, 1], U[:, 2]
                u = mom / rho
                p = (gamma - 1.0) * (E - 0.5 * rho * u * u)
                return jnp.stack([mom, mom * u + p, (E + p) * u], axis=1), jnp.abs(u) + jnp.sqrt(gamma * p / rho)

            FL, aL = phys(UL)
            FR, aR = phys(UR)
            s = jnp.maximum(aL, aR)[:, None]
            return 0.5 * (FL + FR) - 0.5 * s * (UR - UL)
    """,
}


@pytest.mark.parametrize("name", sorted(CLEAN))
def test_clean_candidates_pass(name: str) -> None:
    result = validate_source(textwrap.dedent(CLEAN[name]))
    assert result.ok, [str(v) for v in result.violations]


def test_custom_whitelist_for_arena2() -> None:
    source = "import felupe.math as fm\ndef psi_medium(F, p):\n    return fm.det(F)"
    assert not validate_source(source).ok
    assert validate_source(source, allowed_imports={"jax.numpy", "jax.lax", "math", "felupe.math"}).ok
