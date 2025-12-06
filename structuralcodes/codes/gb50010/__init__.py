"""The Chinese concrete code GB50010-2010 (version 2024)."""

import typing as t

from ._concrete_material_properties import (
    Eci,
    # Eci_t,
    # Gf,
    # beta_cc,
    # beta_e,
    # eps_c1,
    eps_c2,
    # eps_c3,
    # eps_cu1,
    eps_cu2,
    # eps_cu3,
    fcd,
    fck,
    fcm,
    # fctkmax,
    # fctkmin,
    fctm,
    ftk,
    # k_sargin,
    n_parabolic_rectangular,
)
from ._reinforcement_material_properties import (
    Es,
    epsud,
    fstk,
    fyd,
    fyk,
    fym,
)

__all__ = [
    'fck',
    'ftk',
    'fcm',
    'fctm',
    'fyk',
    'fstk',
    # 'fctkmin',
    # 'fctkmax',
    'fcd',
    # 'Gf',
    # 'eps_c1',
    # 'eps_cu1',
    # 'k_sargin',
    'eps_c2',
    'eps_cu2',
    'n_parabolic_rectangular',
    # 'eps_c3',
    # 'eps_cu3',
    'fyd',
    'fym',
    'epsud',
    # 'reinforcement_duct_props',
    'Eci',
    'Es',
]

__title__: str = 'Chinese Code GB50010-2010'
__year__: str = '2024'
__materials__: t.Tuple[str] = ('concrete', 'reinforcement')
