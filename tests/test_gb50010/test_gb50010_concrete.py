"""Tests for the concrete gb50010."""

import pytest

from structuralcodes.codes import gb50010
from structuralcodes.materials.concrete import ConcreteGB50010, create_concrete


# todo: to be tested further
@pytest.mark.parametrize(
    'design_code_to_set',
    [
        'gb50010',
        'GB50010',
        'Gb50010',
    ],
)
@pytest.mark.parametrize(
    'fck, expected_name',
    [
        (20, 'C20'),
        (25, 'C25'),
        (30, 'C30'),
        (35, 'C35'),
        (40, 'C40'),
    ],
)
def test_create_concrete(design_code_to_set, fck, expected_name):
    """Test creating a concrete with GB50010."""
    # Arrange
    expected_density = 2400

    # Act
    c = create_concrete(fck=fck, design_code=design_code_to_set)

    # Assert
    assert isinstance(c, ConcreteGB50010)
    assert c.name == expected_name
    assert c.density == expected_density


@pytest.mark.parametrize(
    'fcuk, expected_fck, expected_ftk',
    [
        (20, 13.4, 1.54),
        (25, 16.7, 1.78),
        (30, 20.1, 2.01),
        (35, 23.4, 2.20),
        (40, 26.8, 2.39),
    ],
)
def test_init_concrete_gb50010(fcuk, expected_fck, expected_ftk):
    """Test initializing ConcreteGB50010."""
    # Arrange
    # fcuk = 40
    fck = gb50010.fck(fcuk)
    ftk = gb50010.ftk(fcuk, f'C{fcuk:d}')

    # Act
    c = ConcreteGB50010(fck=fck, name=f'C{fcuk:d}')

    # Assert
    assert isinstance(c, ConcreteGB50010)
    assert abs(c.fck - expected_fck) < 1.0
    assert abs(ftk - expected_ftk) < 0.1
