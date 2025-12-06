"""The concrete class for GB50010-2010 Concrete Material."""

import typing as t

from structuralcodes.codes import gb50010

from ..constitutive_laws import ConstitutiveLaw, create_constitutive_law
from ._concrete import Concrete


class ConcreteGB50010(Concrete):
    """Concrete implementation for GB50010-2010."""

    # added values
    _fcuk: t.Optional[float] = None
    # computed values
    _fcm: t.Optional[float] = None
    _fctm: t.Optional[float] = None
    _Eci: t.Optional[float] = None
    _fctkmin: t.Optional[float] = None
    _fctkmax: t.Optional[float] = None
    _Gf: t.Optional[float] = None
    _alpha_cc: t.Optional[float] = None
    _eps_c1: t.Optional[float] = None
    _eps_cu1: t.Optional[float] = None
    _k_sargin: t.Optional[float] = None
    _eps_c2: t.Optional[float] = None
    _eps_cu2: t.Optional[float] = None
    _n_parabolic_rectangular: t.Optional[float] = None
    _eps_c3: t.Optional[float] = None
    _eps_cu3: t.Optional[float] = None

    def __init__(
        self,
        fck: float,
        fcuk: t.Optional[float] = None,
        name: t.Optional[str] = None,
        density: float = 2400.0,
        gamma_c: t.Optional[float] = None,
        alpha_cc: t.Optional[float] = None,
        constitutive_law: t.Optional[
            t.Union[
                t.Literal[
                    'elastic',
                    'parabolarectangle',
                    'bilinearcompression',
                    'sargin',
                    'popovics',
                ],
                ConstitutiveLaw,
            ]
        ] = 'parabolarectangle',
        initial_strain: t.Optional[float] = None,
        initial_stress: t.Optional[float] = None,
        strain_compatibility: t.Optional[bool] = None,
        fcm: t.Optional[float] = None,
        fctm: t.Optional[float] = None,
        fctkmin: t.Optional[float] = None,
        fctkmax: t.Optional[float] = None,
        Eci: t.Optional[float] = None,
        Gf: t.Optional[float] = None,
        eps_c1: t.Optional[float] = None,
        eps_cu1: t.Optional[float] = None,
        k_sargin: t.Optional[float] = None,
        eps_c2: t.Optional[float] = None,
        eps_cu2: t.Optional[float] = None,
        n_parabolic_rectangular: t.Optional[float] = None,
        eps_c3: t.Optional[float] = None,
        eps_cu3: t.Optional[float] = None,
        **kwargs,
    ):
        """Initializes a new instance of Concrete for MC 2010.

        Arguments:
            fck (float): Characteristic strength in MPa if concrete is not
                existing.

        Keyword Arguments:
            fcuk (Optional(float)): Characteristic cube strength in MPa if
                concrete is not existing.
            name (Optional(str)): A descriptive name for concrete.
            density (float): Density of material in kg/m3 (default: 2400).
            gamma_c (Optional(float)): The partial factor for concrete.
            alpha_cc (float, optional): A factor for considering long-term
                effects on the strength, and effects that arise from the way
                the load is applied.
            consitutive_law (ConstitutiveLaw | str): A valid ConstitutiveLaw
                object for concrete or a string defining a valid constitutive
                law type for concrete. (valid options for string: 'elastic',
                'parabolarectangle', 'bilinearcompression', 'sargin',
                'popovics').
            initial_strain (Optional[float]): Initial strain of the material.
            initial_stress (Optional[float]): Initial stress of the material.
            strain_compatibility (Optional[bool]): Only relevant if
                initial_strain or initial_stress are different from zero. If
                True, the material deforms with the geometry. If False, the
                stress in the material upon loading is kept constant
                corresponding to the initial strain.
            fcm (float, optional): The mean compressive strength.
            fctm (float, optional): The mean tensile strength.
            fctkmin (float, optional): The minimum tensile strength.
            fctkmax (float, optional): The maximum tensile strength.
            Eci (float, optional): The initial tangent Young's modulus.
            Gf (float, optional): The tensile fracture energy.
            eps_c1 (float, optional): The strain at peak stress for the Sargin
                constitutive law.
            eps_cu1 (float, optional): The ultimate strain for the Sargin
                constitutive law.
            k_sargin (float, optional): The coefficient for the Sargin
                constitutive law.
            eps_c2 (float, optional): The strain at peak stress for the
                parabolic rectangular constitutive law.
            eps_cu2 (float, optional): The ultimate strain for the parabolic
                rectangular constitutive law.
            n_parabolic_rectangular (float, optional): The coefficient for the
                parabolic rectangular constitutive law.
            eps_c3 (float, optional): The strain at peak stress for the
                bilinear constitutive law.
            eps_cu3 (float, optional): The ultimate strain for the bilinear
                constitutive law.

        Raises:
            ValueError: If fcm is lower than fck.
            ValueError: If k_sargin is negative.
            ValueError: If n_parabolic_rectangular is negative.
            ValueError: If the constitutive law name is not available for the
                material.
            ValueError: If the provided constitutive law is not valid for
                concrete.
            Warning: If Eci is lower than 1e4 or larger than 1e5.
            Warning: If fctm is larger than 0.5 * fck.
            Warning: If eps_c1 is larger than 0.1.
            Warning: If eps_cu1 is larger than 0.1.
            Warning: If eps_c2 is larger than 0.1.
            Warning: If eps_cu2 is larger than 0.1.
            Warning: If n_parabolic_rectangular is larger than 5.
            Warning: If eps_c3 is larger than 0.1.
            Warning: If eps_cu3 is larger than 0.1.
        """
        del kwargs

        if name is None:
            name = f'C{round(fck):d}'
        super().__init__(
            fck=fck,
            name=name,
            density=density,
            gamma_c=gamma_c,
            initial_strain=initial_strain,
            initial_stress=initial_stress,
            strain_compatibility=strain_compatibility,
        )
        if fcuk is not None:
            self._fcuk = abs(fcuk)
        self._alpha_cc = alpha_cc
        self._fcm = abs(fcm) if fcm is not None else None
        self._fctm = abs(fctm) if fctm is not None else None
        self._fctkmin = abs(fctkmin) if fctkmin is not None else None
        self._fctkmax = abs(fctkmax) if fctkmax is not None else None
        self._Eci = abs(Eci) if Eci is not None else None
        self._Gf = abs(Gf) if Gf is not None else None
        self._eps_c1 = abs(eps_c1) if eps_c1 is not None else None
        self._eps_cu1 = abs(eps_cu1) if eps_cu1 is not None else None
        self._k_sargin = k_sargin if k_sargin is not None else None
        self._eps_c2 = abs(eps_c2) if eps_c2 is not None else None
        self._eps_cu2 = abs(eps_cu2) if eps_cu2 is not None else None
        self._n_parabolic_rectangular = (
            n_parabolic_rectangular
            if n_parabolic_rectangular is not None
            else None
        )
        self._eps_c3 = abs(eps_c3) if eps_c3 is not None else None
        self._eps_cu3 = abs(eps_cu3) if eps_cu3 is not None else None

        self.__post_init__()

        # The constitutive law requires valid attributes, so it should be set
        # after validation
        self._constitutive_law = (
            constitutive_law
            if isinstance(constitutive_law, ConstitutiveLaw)
            else create_constitutive_law(
                constitutive_law_name=constitutive_law, material=self
            )
        )
        if 'concrete' not in self._constitutive_law.__materials__:
            raise ValueError(
                'The provided constitutive law is not valid for concrete.'
            )
        self._apply_initial_strain()

    def __post_init__(self):
        """Validator for the attributes that are set in the constructor."""
        # fcuk
        if (
            self._fcuk is not None
            and abs(gb50010.fck(self._fcuk) - self._fck) > 1.0
        ):
            raise ValueError(
                (
                    'The provided fck and fcuk are not consistent.\n',
                    f'Provided fck = {self._fck}, ',
                    f'fcuk = {self._fcuk}, ',
                    f'which gives fck = {gb50010.fck(self._fcuk):.2f}.',
                )
            )
        # fcm
        if self._fcm is not None and self._fcm <= self._fck:
            raise ValueError(
                (
                    'Mean compressive strength cannot be lower than',
                    'characteristic strength.\n',
                    'Current characteristing strength: ',
                    f'fck = {self._fck}.',
                    f'Current value: value = {self._fcm}',
                )
            )

        # Eci
        if self._Eci is not None and (self._Eci < 1e4 or self._Eci > 1e5):
            warnings.warn(
                'A suspect value of Eci has been input.\n'
                f'Please check Eci that should be in MPa ({self._Eci} given).'
            )

        # fctm
        if self._fctm is not None and self._fctm > 0.5 * self._fck:
            warnings.warn(
                'A suspect value of fctm has been input. Please check.'
            )

        # eps_c1
        if self._eps_c1 is not None and abs(self._eps_c1) >= 0.1:
            warnings.warn(
                'A suspect value is input for eps_c1 that should be a pure'
                f' number without units. Please check ({self._eps_c1} given).'
            )

        # eps_cu1
        if self._eps_cu1 is not None and abs(self._eps_cu1) >= 0.1:
            warnings.warn(
                'A suspect value is input for eps_cu1 that should be a pure'
                f' number without units. Please check ({self._eps_cu1} given).'
            )

        # k_sargin
        if self._k_sargin is not None and self._k_sargin < 0:
            raise ValueError(
                f'k_sargin should be a positive value ({self._k_sargin} given)'
            )

        # eps_c2
        if self._eps_c2 is not None and abs(self._eps_c2) >= 0.1:
            warnings.warn(
                'A suspect value is input for eps_c2 that should be a pure'
                f' number without units. Please check ({self._eps_c2} given).'
            )

        # eps_cu2
        if self._eps_cu2 is not None and abs(self._eps_cu2) >= 0.1:
            warnings.warn(
                'A suspect value is input for eps_cu2 that should be a pure'
                f' number without units. Please check ({self._eps_cu2} given).'
            )

        # n_parabolic_rectangular
        if (
            self._n_parabolic_rectangular is not None
            and self._n_parabolic_rectangular < 0
        ):
            raise ValueError(
                'n should be a positive value '
                f'({self._n_parabolic_rectangular} given)'
            )
        if (
            self._n_parabolic_rectangular is not None
            and self._n_parabolic_rectangular >= 5
        ):
            warnings.warn(
                'A suspect value is input for n_parabolic_rectangular. Please '
                'check '
                f'({self._n_parabolic_rectangular} given).'
            )

        # eps_c3
        if self._eps_c3 is not None and abs(self._eps_c3) >= 0.1:
            warnings.warn(
                'A suspect value is input for eps_c3 that should be a pure'
                f' number without units. Please check ({self._eps_c3} given).'
            )

        # eps_cu3
        if self._eps_cu3 is not None and abs(self._eps_cu3) >= 0.1:
            warnings.warn(
                'A suspect value is input for eps_cu3 that should be a pure'
                f' number without units. Please check ({self._eps_cu3} given).'
            )

    @property
    def gamma_c(self) -> float:
        """The partial factor for concrete."""
        return self._gamma_c or 1.4

    @property
    def fcuk(self) -> float:
        """Return the characteristic cube strength in MPa.

        Returns:
            float: The characteristic cube strength of concrete in MPa.
        """
        return self._fcuk

    def fcd(self) -> float:
        """Return the design compressive strength in MPa.

        Returns:
            float: The design compressive strength of concrete in MPa.
        """
        # This method should perhaps become a property, but is left as a method
        # for now, to be consistent with other concretes.
        return gb50010.fcd(self.fck, gamma_c=self.gamma_c)

    @property
    def eps_c2(self) -> float:
        """Returns the strain at maximum compressive strength of concrete (fcd)
        for the Parabola-rectangle constitutive law.

        Returns:
            float: The strain at maximum compressive strength of concrete.

        Note:
            The returned value is derived from fck if eps_c2 is not manually
            provided when initializing the object.
        """
        if self._eps_c2 is None:
            return gb50010.eps_c2(self.fcuk)
        return self._eps_c2

    @property
    def eps_cu2(self) -> float:
        """Returns the strain at concrete failure of concrete for the
        Parabola-rectangle constitutive law.

        Returns:
            float: The maximum strain at failure of concrete.

        Note:
            The returned value is derived from fck if eps_cu2 is not manually
            provided when initializing the object.
        """
        if self._eps_cu2 is None:
            return gb50010.eps_cu2(self.fcuk)
        return self._eps_cu2

    @property
    def n_parabolic_rectangular(self) -> float:
        """Returns the coefficient for Parabola-rectangle constitutive law.

        Returns:
            float: The exponent for Parabola-recangle law.

        Note:
            The returned value is derived from fck if n is not manually
            provided when initializing the object.
        """
        if self._n_parabolic_rectangular is None:
            return gb50010.n_parabolic_rectangular(self.fcuk)
        return self._n_parabolic_rectangular

    def __elastic__(self) -> dict:
        """Returns kwargs for creating an elastic constitutive law."""
        return {'E': self.Eci}

    def __bilinearcompression__(self) -> dict:
        """Returns kwargs for Bi-linear constitutive law."""
        return {
            'fc': self.fcd(),
            'eps_c': self.eps_c3,
            'eps_cu': self.eps_cu3,
        }

    def __parabolarectangle__(self) -> dict:
        """Returns kwargs for creating a parabola rectangle const law."""
        return {
            'fc': self.fcd(),
            'eps_0': self.eps_c2,
            'eps_u': self.eps_cu2,
            'n': self.n_parabolic_rectangular,
        }
