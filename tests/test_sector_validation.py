"""Tests for the sector validation gate (Information Technology)."""

import pytest
from lynx_tech.core.analyzer import _validate_sector, SectorMismatchError
from lynx_tech.models import CompanyProfile


class TestSectorValidation:
    """Sector validation blocks non-IT companies."""

    def _profile(self, ticker="T", sector=None, industry=None, desc=None):
        return CompanyProfile(ticker=ticker, name=f"{ticker} Corp",
                              sector=sector, industry=industry, description=desc)

    # --- Should ALLOW ---
    def test_technology_sector_application_software(self):
        _validate_sector(self._profile(sector="Technology", industry="Software - Application"))

    def test_technology_sector_infrastructure_software(self):
        _validate_sector(self._profile(sector="Technology", industry="Software - Infrastructure"))

    def test_technology_sector_security_software(self):
        _validate_sector(self._profile(sector="Technology", industry="Software - Security"))

    def test_technology_sector_semiconductors(self):
        _validate_sector(self._profile(sector="Technology", industry="Semiconductors"))

    def test_technology_sector_semi_equipment(self):
        _validate_sector(self._profile(sector="Technology", industry="Semiconductor Equipment & Materials"))

    def test_technology_sector_it_services(self):
        _validate_sector(self._profile(sector="Technology", industry="Information Technology Services"))

    def test_technology_sector_consumer_electronics(self):
        _validate_sector(self._profile(sector="Technology", industry="Consumer Electronics"))

    def test_technology_sector_computer_hardware(self):
        _validate_sector(self._profile(sector="Technology", industry="Computer Hardware"))

    def test_communication_services_internet(self):
        _validate_sector(self._profile(sector="Communication Services", industry="Internet Content & Information"))

    def test_saas_keyword_in_description(self):
        _validate_sector(self._profile(sector="Other", industry="Other",
                                       desc="Company operates a software as a service platform for SMBs"))

    def test_semiconductor_keyword_in_description(self):
        _validate_sector(self._profile(sector="Other", industry="Other",
                                       desc="Fabless semiconductor company designing GPUs"))

    # --- Should BLOCK ---
    def test_basic_materials_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Basic Materials", industry="Gold"))

    def test_energy_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Energy", industry="Uranium"))

    def test_financial_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Financial Services", industry="Banks"))

    def test_healthcare_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Healthcare", industry="Drug Manufacturers"))

    def test_consumer_cyclical_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Consumer Cyclical", industry="Auto Manufacturers"))

    def test_real_estate_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Real Estate", industry="REIT"))

    def test_all_none_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile())

    def test_empty_strings_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="", industry="", desc=""))

    def test_mining_company_blocked(self):
        """A mining company with vague 'Other' sector should be blocked."""
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(
                sector="Basic Materials", industry="Gold",
                desc="Gold mining exploration and drill program"))

    def test_error_message_content(self):
        with pytest.raises(SectorMismatchError, match="outside the scope"):
            _validate_sector(self._profile(sector="Basic Materials", industry="Gold"))

    def test_error_suggests_another_agent(self):
        """Wrong-sector warning appends a 'use lynx-investor-*' line."""
        with pytest.raises(SectorMismatchError) as exc:
            _validate_sector(self._profile(
                sector="Healthcare", industry="Biotechnology"))
        message = str(exc.value)
        assert "Suggestion" in message
        assert "lynx-investor-healthcare" in message

    def test_error_never_suggests_self(self):
        with pytest.raises(SectorMismatchError) as exc:
            _validate_sector(self._profile(
                sector="Utilities", industry="Utilities—Regulated Electric"))
        message = str(exc.value)
        assert "use 'lynx-investor-information-technology'" not in message
