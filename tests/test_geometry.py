"""Tests for src.geometry."""

import pytest
from src.geometry import calculate_angle


def test_right_angle():
    assert calculate_angle((1, 0), (0, 0), (0, 1)) == pytest.approx(90.0)


def test_straight_angle():
    assert calculate_angle((-1, 0), (0, 0), (1, 0)) == pytest.approx(180.0)


def test_zero_length_vector():
    assert calculate_angle((0, 0), (0, 0), (0, 1)) is None