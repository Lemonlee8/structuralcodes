"""Material properties for reinforcement steel."""

import typing as t

# Values from Commentary C.1.1 Table 1.
Delta_s = {
    'HPB235': 8.95,
    'HRB335': 7.43,
    # if no data, use the mean of HPB235 and HRB335
    'OTHERS': 8.19,
}

# the strength values for common reinforcement steel grades
BarStrength = {
    'HPB300': (300, 420),
    'HRB335': (335, 455),
    'HRB400': (400, 540),
    'HRBF400': (400, 540),
    'RRB400': (400, 540),
    'HRB500': (500, 630),
    'HRBF500': (500, 630),
}

BarEs = {
    'HPB300': 2.1e5,
    'HRB335': 2.0e5,
    'HRB400': 2.0e5,
    'HRBF400': 2.0e5,
    'RRB400': 2.0e5,
    'HRB500': 2.0e5,
    'HRBF500': 2.0e5,
    'STRAND': 1.95e5,
}


def fyk(
    gradeN: t.Literal[
        'HPB300',
        'HRB335',
        'HRB400',
        'HRBF400',
        'RRB400',
        'HRB500',
        'HRBF500',
    ] = 'HRB400',
) -> float:
    """Get the characteristic yield strength for a given reinforcement grade.

    Args:
        grade (str): The reinforcement grade.

    Returns:
        float: The characteristic yield strength in MPa.

    """
    return BarStrength[gradeN][0]


def fstk(
    gradeN: t.Literal[
        'HPB300',
        'HRB335',
        'HRB400',
        'HRBF400',
        'RRB400',
        'HRB500',
        'HRBF500',
    ] = 'HRB400',
) -> float:
    """Get the ultimate tensile strength for a given reinforcement grade.

    Args:
        grade (str): The reinforcement grade.

    Returns:
        float: The ultimate tensile strength in MPa.

    """
    return BarStrength[gradeN][1]


def Es(
    gradeN: t.Literal[
        'HPB300',
        'HRB335',
        'HRB400',
        'HRBF400',
        'RRB400',
        'HRB500',
        'HRBF500',
        'STRAND',
    ] = 'HRB400',
) -> float:
    """Get the modulus of elasticity for a given reinforcement grade.

    Args:
        gradeN (t.Literal[ 'HPB300', 'HRB335', 'HRB400', 'HRBF400', 'RRB400',
        'HRB500', 'HRBF500', 'STRAND', ], optional): _description_.
        Defaults to 'HRB400'.

    Returns:
        float: the modulus of elasticity
    """
    return BarEs[gradeN]


def fyd(fyk: float, gamma_s: float = 1.11) -> float:
    """Calculate the design value of the reinforcement yield strength.

    GB50010, Sec. 4.2.3.

    Args:
        fyk (float): The characteristic yield strength in MPa.
        gamma_s (float): The partial factor. Default value 1.11.

    Returns:
        float: The design yield strength in MPa.

    Raises:
        ValueError: If fyk is less than 0.
        ValueError: If gamma_s is less than 1.
    """
    if fyk < 0:
        raise ValueError(f'fyk={fyk} cannot be less than 0')
    if gamma_s < 1:
        raise ValueError(f'gamma_s={gamma_s} must be larger or equal to 1')

    return fyk / gamma_s


def fym(
    fyk: float,
    delta: t.Literal[
        'HPB235',
        'HRB335',
        'OTHERS',
    ] = 'OTHERS',
) -> float:
    """Calculate the mean value of the reinforcement yield strength.

    Args:
        fyk (float): The characteristic yield strength.
        delta (t.Literal[ 'HPB235', 'HRB335', 'OTHERS', ], optional): The type of reinforcement. Defaults to 'OTHERS'.

    Returns:
        float: The mean tensile strength in MPa.
    """  # noqa: E501
    return abs(fyk) / (1 - 1.645 * Delta_s[delta] / 100)


def epsud(epsuk: float, gamma_eps: float = 0.9) -> float:
    """Calculate the design value of the reinforcement ultimate strain.

    fib Model Code 2010, Sec. 7.2.3.2.

    Args:
        epsuk (float): The characteristic ultimate strain.
        gamma_eps (float): The partial factor. Default value 0.9.

    Returns:
        float: The design ultimate strain.

    Raises:
        ValueError: If epsuk is less than 0.
        ValueError: If gamma_eps is greater than 1.
    """
    if epsuk < 0:
        raise ValueError(f'epsuk={epsuk} cannot be less than 0')
    if gamma_eps > 1:
        raise ValueError(
            f'gamma_eps={gamma_eps} must be smaller or equal to 1'
        )
    return epsuk * gamma_eps
