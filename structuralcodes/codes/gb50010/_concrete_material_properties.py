"""A collection of material properties for concrete."""

from __future__ import annotations  # To have clean hints of ArrayLike in docs

import typing as t

# import numpy as np
# import numpy.typing as npt

# Values from Commentary C.2.1 Table 2.
Delta_c = {
    'C15': 23.3,
    'C20': 20.6,
    'C25': 18.9,
    'C30': 17.2,
    'C35': 16.4,
    'C40': 15.6,
    'C45': 15.6,
    'C50': 14.9,
    'C60': 14.1,
}

# Values from Table 5.1-6.
# ALPHA_E = {
#     'basalt': 1.2,
#     'quartzite': 1.0,
#     'limestone': 0.9,
#     'sandstone': 0.7,
# }
# # Values for normal strength concrete, from Table 5.1-9.
# S_CEM = {
#     '32.5 R': 0.25,
#     '42.5 N': 0.25,
#     '42.5 R': 0.2,
#     '52.5 N': 0.2,
#     '52.5 R': 0.2,
#     '32.5 N': 0.38,
# }


def fck(fcuk: float) -> float:
    """Convert the characteristic compressive strength of concrete cubes to
    that of concrete cylinders.

    Chinese Code GB50010-2010, 4.1.3.

    Args:
        fcuk (float): The characteristic compressive strength of concrete cubes
            in MPa.

    Returns:
        float: The standard value of axial compressive strength in MPa.
    """

    def alph1(x):
        if x <= 50:
            return 0.76
        if 50 < x < 80:
            return 0.76 + (0.82 - 0.76) * (x - 50) / 30
        return 0.82

    def alph2(x):
        if x <= 40:
            return 1.0
        if 40 < x < 80:
            return 1.0 - (1 - 0.87) * (x - 40) / 40
        return 0.87

    return 0.85 * alph1(fcuk) * alph2(fcuk) * abs(fcuk)


def ftk(
    fcuk: float,
    delta: t.Literal[
        'C15', 'C20', 'C25', 'C30', 'C35', 'C40', 'C45', 'C50', 'C60'
    ],
) -> float:
    """Compute the characteristic tensile strength of concrete from the
    characteristic compressive strength of concrete cubes.

    Chinese Code GB50010-2010, 4.1.3.

    Args:
        fcuk (float): The characteristic compressive strength of concrete cubes in MPa.
        delta (str): The concrete grade.

    Returns:
        float: The characteristic tensile strength in MPa.
    """

    def alph2(x):
        if x <= 40:
            return 1.0
        if 40 < x < 80:
            return 1.0 - (1 - 0.87) * (x - 40) / 40
        return 0.87

    return (
        0.88
        * 0.395
        * fcuk ** (0.55)
        * (1 - 1.645 * Delta_c[delta] / 100) ** 0.45
        * alph2(fcuk)
    )


def fcm(
    fck: float,
    delta: t.Literal[
        'C15', 'C20', 'C25', 'C30', 'C35', 'C40', 'C45', 'C50', 'C60'
    ] = 'C30',
) -> float:
    """Compute the mean concrete compressive strength from the characteristic
    strength.

    Chinese Code GB50010-2010, C.2.1.

    Args:
        fck (float): The standard value of axial compressive strength in MPa.

    Keyword Args:
        delta (str): The concrete grade.

    Returns:
        float: The mean compressive strength in MPa.
    """
    return abs(fck) / (1 - 1.645 * Delta_c[delta] / 100)


def fctm(
    ftk: float,
    delta: t.Literal[
        'C15', 'C20', 'C25', 'C30', 'C35', 'C40', 'C45', 'C50', 'C60'
    ] = 'C30',
) -> float:
    """Compute the mean concrete tensile strength from the characteristic
    compressive strength.

    Chinese Code GB50010-2010, C.2.1.

    Args:
        ftk (float): The characteristic tensile strength in MPa.

    Keyword Args:
        delta (str): The concrete grade.

    Returns:
        float: The mean tensile strength in MPa.
    """
    return abs(ftk) / (1 - 1.645 * Delta_c[delta] / 100)


# def fctkmin(fctm: float) -> float:
#     """Compute the lower bound value of the characteristic tensile strength
#     from the mean tensile strength.

#     fib Model Code 2010, Eq. (5.1-4).

#     Args:
#         fctm (float): The mean tensile strength in MPa.

#     Returns:
#         float: Lower bound of the characteristic tensile strength in MPa.
#     """
#     return 0.7 * fctm


# def fctkmax(fctm: float) -> float:
#     """Compute the upper bound value of the characteristic tensile strength
#     from the mean tensile strength.

#     fib Model Code 2010, Eq. (5.1-5).

#     Args:
#         fctm (float): The mean tensile strength in MPa.

#     Returns:
#         float: Upper bound of the characteristic tensile strength in MPa.
#     """
#     return 1.3 * fctm


# def Gf(fck: float) -> float:
#     """Compute tensile fracture energy from characteristic compressive
#     strength.

#     fib Model Code 2010, Eq. (5.1-9).

#     Args:
#         fck (float): The characteristic compressive strength in MPa.

#     Returns:
#         float: The tensile fracture energy in N/m.
#     """
#     return 73 * fcm(fck) ** 0.18


def Eci(
    fcuk: float,
) -> float:
    """Calculate the modulus of elasticity for normal weight concrete at 28
    days.

    Defined in GB50010-2010, 4.1.5.

    Args:
        fcuk (float): The characteristic compressive strength of the
            concrete in MPa where concrete cubes of 150 mm size are used.

    Returns:
        float: The modulus of elasticity for normal weight concrete at 28 days
        in MPa.
    """
    return 10 ^ 5 / (2.2 + 34.7 / fcuk)


# def beta_cc(
#     time: npt.ArrayLike,
#     fcm: float,
#     cem_class: t.Literal[
#         '32.5 N', '32.5 R', '42.5 N', '42.5 R', '52.5 N', '52.5 R'
#     ],
# ) -> np.ndarray:
#     """Calculate multiplication factor beta_cc, used to determine the
#     compressive strength at an arbitrary time.

#     Defined in fib Model Code 2010 (2013), Eq. 5.1-51.

#     Args:
#         time (numpy.typing.ArrayLike): The time in days at which the
#             compressive strength is to be determined.
#         fcm (float): The mean compressive strength of the concrete in MPa.
#         cem_class (str): The cement strength class that is used. The choices
#             are: '32.5 N', '32.5 R', '42.5 N', '42.5 R', '52.5 N', '52.5 R'.

#     Returns:
#         numpy.ndarray: Multiplication factor beta_cc.
#     """
#     if fcm > 60:
#         return np.exp(0.2 * (1 - np.sqrt(28 / time)))
#     return np.exp(S_CEM[cem_class.upper()] * (1 - np.sqrt(28 / time)))


# def beta_e(beta_cc: npt.ArrayLike) -> np.ndarray:
#     """Calculate multiplication factor beta_e, used to determine the modulus of
#     elasticity at an arbitrary time.

#     Defined in fib Model Code 2010 (2013), Eq. 5.1-57.

#     Args:
#         beta_cc (numpy.typing.ArrayLike): Multiplication factor as defined in
#             the fib Model Code 2010 (2013), Eq. 5.1-51.

#     Returns:
#         numpy.ndarray: Multiplication factor beta_e.
#     """
#     return np.sqrt(beta_cc)


# def Eci_t(beta_e: npt.ArrayLike, Eci: float) -> np.ndarray:
#     """Calculate the modulus of elasticity for normal weight concrete at time
#     'time' (not 28 days).

#     Defined in fib Model Code 2010 (2013), Eq. 5.1-56.

#     Args:
#         beta_e (numpy.typing.ArrayLike): Multiplication factor to determine
#             the modulus of elasticity at an arbitrary time, as defined in fib
#             Model Code 2010 (2013), Eq. 5.1-51.
#         Eci (float): Modulus of elasticity of normal weight concrete at 28
#             days, as defined in fib Model Code 2010 (2013), Eq. 5.1-21.

#     Returns:
#         numpy.ndarray: The modulus of elasticity for normal weight concrete at
#         time 'time' (not 28 days) in MPa.
#     """
#     return beta_e * Eci


def fcd(fck: float, gamma_c: float = 1.4) -> float:
    """The design compressive strength of concrete.

    Defined in GB50010-2010, Commentary 4.1.4.

    Args:
        fck (float): The characteristic compressive strength in MPa.

    Keyword Args:
        gamma_c (float): The partial factor of concrete. Default value 1.4.

    Returns:
        float: The design compressive strength of concrete in MPa.
    """
    return abs(fck) / abs(gamma_c)


# def eps_c1(fck: float) -> float:
#     """The strain at maximum compressive stress of concrete (fcm) for the
#     Sargin constitutive law.

#     Defined in fib Model Code 2010 (2013), Eq. 5.1-26 and Table 5.1-8

#     The value is computing using interpolation from Table 5.1-8

#     Args:
#         fck (float): The characteristic compressive strength of concrete in
#             MPa.

#     Returns:
#         float: The strain at maximum compressive stress, absolute value, no
#         unit.

#     Raises:
#         ValueError: if fck is less than 12 or greater than 120
#     """
#     grade = np.array(
#         [12, 16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 110, 120]
#     )
#     eps_c1 = np.array(
#         [
#             -1.9,
#             -2.0,
#             -2.1,
#             -2.2,
#             -2.3,
#             -2.3,
#             -2.4,
#             -2.5,
#             -2.6,
#             -2.6,
#             -2.7,
#             -2.7,
#             -2.8,
#             -2.9,
#             -3.0,
#             -3.0,
#             -3.0,
#         ]
#     )
#     if fck < grade.min() or fck > grade.max():
#         raise ValueError(
#             f'fck must be between {grade.min()} MPa and {grade.max()} MPa.'
#             ' fck = {fck} given.'
#         )
#     return np.interp(fck, grade, eps_c1) / 1000


# def eps_clim(fck: float) -> float:
#     """The ultimate strain for the Sargin constitutive law.

#     Defined in fib Model Code 2010 (2013), Eq. 5.1-26 and Table 5.1-8

#     The value is computing using interpolation from Table 5.1-8

#     Args:
#         fck (float): The characteristic compressive strength of concrete in
#             MPa.

#     Returns:
#         float: The ultimate strain, absolute value, no unit.
#     """
#     grade = np.array(
#         [12, 16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 110, 120]
#     )
#     eps_clim = np.array(
#         [
#             -3.5,
#             -3.5,
#             -3.5,
#             -3.5,
#             -3.5,
#             -3.5,
#             -3.5,
#             -3.5,
#             -3.4,
#             -3.4,
#             -3.3,
#             -3.2,
#             -3.1,
#             -3.0,
#             -3.0,
#             -3.0,
#             -3.0,
#         ]
#     )
#     if fck < grade.min() or fck > grade.max():
#         raise ValueError(
#             f'fck must be between {grade.min()} MPa and {grade.max()} MPa.'
#             ' fck = {fck} given.'
#         )
#     return np.interp(fck, grade, eps_clim) / 1000


# def k_sargin(fck: float) -> float:
#     """The plasticity number k for Sargin constitutive Law.

#     Defined in fib Model Code 2010 (2013), Eq. 5.1-26 and Table 5.1-8

#     Args:
#         fck (float): The characteristic compressive strength of concrete in
#             MPa.

#     Returns:
#         float: The plasticity number k, absolute value, no unit.
#     """
#     grade = np.array(
#         [12, 16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 110, 120]
#     )
#     k = np.array(
#         [
#             2.44,
#             2.36,
#             2.28,
#             2.15,
#             2.04,
#             1.92,
#             1.82,
#             1.74,
#             1.66,
#             1.61,
#             1.55,
#             1.47,
#             1.41,
#             1.36,
#             1.32,
#             1.24,
#             1.18,
#         ]
#     )
#     if fck < grade.min() or fck > grade.max():
#         raise ValueError(
#             f'fck must be between {grade.min()} MPa and {grade.max()} MPa.'
#             ' fck = {fck} given.'
#         )
#     return np.interp(fck, grade, k)


# def eps_cu1(fck: float) -> float:
#     """The nominal ultimate strain for the Sargin constitutive law.

#     Defined in fib Model Code 2010 (2013), Table 7.2-1 and Eq. 7.2-10

#     Args:
#         fck (float): The characteristic compressive strength of concrete in
#             MPa.

#     Returns:
#         float: The strain at maximum compressive stress, absolute value, no
#         unit.
#     """
#     return eps_clim(fck)


def eps_c2(fcuk: float) -> float:
    """The strain at maximum compressive stress of concrete for the
    parabolic-rectangular law.

    Defined in GB50010 (2024), Eq (6.2.1-4)

    Args:
        fcuk (float): The characteristic compressive strength of concrete in
            MPa. (cube strength)

    Returns:
        float: The strain at maximum compressive stress, absolute value, no
        unit.
    """
    _fcuk = abs(fcuk)
    res = 0.002 + 0.5 * (_fcuk - 50) * 1e-5
    if res < 0.002:
        return 0.002
    return res


def eps_cu2(fcuk: float) -> float:
    """The ultimate strain of the parabolic-rectangular law.

    Defined in GB50010 (2024), Eq (6.2.1-5)

    Args:
        fcuk (float): The characteristic compressive strength of concrete in
            MPa. (cube strength)

    Returns:
        float: The ultimate strain, absolute value, no unit.
    """
    _fcuk = abs(fcuk)
    res = 0.0033 - 0.5 * (_fcuk - 50) * 1e-5
    if res > 0.0033:
        return 0.0033
    return res


def n_parabolic_rectangular(fcuk: float) -> float:
    """The exponent in the parabolic-rectangular law.

    Defined in GB50010 (2024), Eq (6. 2. 1-3)

    Args:
        fcuk (float): The characteristic compressive strength of concrete in
            MPa. (cube strength)

    Returns:
        float: The exponent n, absolute value, no unit.
    """
    _fcuk = abs(fcuk)
    res = 2 - (_fcuk - 50) / 60
    if res > 2.0:
        return 2.0
    return res


# def eps_c3(fck: float) -> float:
#     """The strain at maximum compressive stress of the bi-linear law.

#     Defined in fib Model Code 2010 (2013), Table 7.2-1

#     Args:
#         fck (float): The characteristic compressive strength of concrete in
#             MPa.

#     Returns:
#         float: The strain at maximum compressive stress, absolute value, no
#         unit.
#     """
#     fck = abs(fck)
#     return 1.75 / 1000 if fck <= 50 else (1.75 + 0.55 * (fck - 50) / 40) / 1000


# def eps_cu3(fck: float) -> float:
#     """The ultimate strain of the bi-linear law.

#     Defined in fib Model Code 2010 (2013), Table 7.2-1

#     Args:
#         fck (float): The characteristic compressive strength of concrete in
#             MPa.

#     Returns:
#         float: The ultimate strain, absolute value, no unit.
#     """
#     return eps_cu2(fck)
