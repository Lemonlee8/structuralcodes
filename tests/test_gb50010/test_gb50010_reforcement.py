"""Tests for the concrete gb50010."""

import pytest

from structuralcodes.materials.reinforcement import (
    ReinforcementGB50010,
    create_reinforcement,
)


@pytest.mark.parametrize(
    'design_code_to_set',
    [
        'gb50010',
        'GB50010',
        'Gb50010',
    ],
)
@pytest.mark.parametrize(
    'fyks, expected_fyd',
    [
        (300, 270),
        (335, 300),
        (400, 360),
        (500, 435),
    ],
)
def test_create_reforcement(design_code_to_set, fyks, expected_fyd):
    """Test creating a reforcement with GB50010."""
    # Arrange
    expected_density = 7850

    # Act
    sb = create_reinforcement(
        fyk=fyks,
        Es=2.0e5,
        ftk=fyks * 1.4,
        epsuk=0.075,
        design_code=design_code_to_set,
    )

    # Assert
    assert isinstance(sb, ReinforcementGB50010)
    assert abs(sb.fyd() - expected_fyd) < 2.0
    assert sb.density == expected_density
