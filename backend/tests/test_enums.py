"""Tests for enums."""
import pytest

from landslide_backend.models.enums import (
    ErrorCode,
    ResourceStatus,
    ResourceType,
    RiskTier,
    ShelterStatus,
)


class TestRiskTier:
    def test_values(self):
        assert RiskTier.WATCH.value == "watch"
        assert RiskTier.ALERT.value == "alert"
        assert RiskTier.EVACUATE.value == "evacuate"

    def test_severity_levels(self):
        assert RiskTier.WATCH.severity_level == 1
        assert RiskTier.ALERT.severity_level == 2
        assert RiskTier.EVACUATE.severity_level == 3

    def test_colors(self):
        assert RiskTier.WATCH.color == "#FFD700"
        assert RiskTier.ALERT.color == "#FF8C00"
        assert RiskTier.EVACUATE.color == "#FF0000"

    def test_from_string(self):
        assert RiskTier("watch") == RiskTier.WATCH
        assert RiskTier("alert") == RiskTier.ALERT
        assert RiskTier("evacuate") == RiskTier.EVACUATE

    def test_invalid_string(self):
        with pytest.raises(ValueError):
            RiskTier("invalid")

    @pytest.mark.parametrize("tier,severity", [
        (RiskTier.WATCH, 1),
        (RiskTier.ALERT, 2),
        (RiskTier.EVACUATE, 3),
    ])
    def test_severity_parametrized(self, tier, severity):
        assert tier.severity_level == severity


class TestResourceEnums:
    def test_resource_types(self):
        """Resource types should NOT include shelter (see PROJECT.md decision log)."""
        expected = [
            "medical", "rescue", "food",
            "water", "transport", "communication",
        ]
        actual = [r.value for r in ResourceType]
        assert actual == expected

    def test_shelter_not_a_resource_type(self):
        """Explicit regression guard: shelter must not creep back in."""
        assert "shelter" not in [r.value for r in ResourceType]

    def test_resource_statuses(self):
        expected = ["available", "deployed", "maintenance", "depleted"]
        actual = [s.value for s in ResourceStatus]
        assert actual == expected


class TestShelterStatus:
    def test_values(self):
        assert ShelterStatus.OPEN.value == "open"
        assert ShelterStatus.FULL.value == "full"
        assert ShelterStatus.CLOSED.value == "closed"


class TestErrorCode:
    def test_values(self):
        assert ErrorCode.RESOURCE_NOT_FOUND.value == "RESOURCE_NOT_FOUND"
        assert ErrorCode.INVALID_INPUT.value == "INVALID_INPUT"
        assert ErrorCode.DATABASE_ERROR.value == "DATABASE_ERROR"
        assert ErrorCode.EXTERNAL_SERVICE_ERROR.value == "EXTERNAL_SERVICE_ERROR"
