"""Tests for logic rules management."""

import os
import pytest
import tempfile
import json
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from logic_rules import LogicRule, LogicRulesManager


def test_logic_rule_creation():
    """Test LogicRule creation."""
    rule = LogicRule(
        rule_id="rule_001",
        rule_type="test",
        description="Test rule",
        confidence=0.9,
        frame_number=10,
        timestamp=0.5
    )
    
    assert rule.rule_id == "rule_001"
    assert rule.rule_type == "test"
    assert rule.description == "Test rule"
    assert rule.confidence == 0.9
    assert rule.frame_number == 10
    assert rule.timestamp == 0.5


def test_logic_rule_to_dict():
    """Test LogicRule conversion to dictionary."""
    rule = LogicRule(
        rule_id="rule_001",
        rule_type="test",
        description="Test rule",
        confidence=0.9
    )
    
    rule_dict = rule.to_dict()
    assert rule_dict['rule_id'] == "rule_001"
    assert rule_dict['rule_type'] == "test"
    assert rule_dict['description'] == "Test rule"
    assert rule_dict['confidence'] == 0.9


def test_logic_rules_manager_add_rule():
    """Test adding rules to manager."""
    output_config = {'output_path': '/tmp/test'}
    manager = LogicRulesManager(output_config)
    
    rule = LogicRule(
        rule_id="rule_001",
        rule_type="test",
        description="Test rule"
    )
    
    manager.add_rule(rule)
    assert len(manager.rules) == 1
    assert manager.rules[0].rule_id == "rule_001"


def test_logic_rules_manager_create_rule():
    """Test creating rules with manager."""
    output_config = {'output_path': '/tmp/test'}
    manager = LogicRulesManager(output_config)
    
    rule = manager.create_rule(
        rule_type="test",
        description="Auto-generated rule",
        confidence=0.95
    )
    
    assert len(manager.rules) == 1
    assert rule.rule_id == "rule_0001"
    assert rule.rule_type == "test"
    assert rule.confidence == 0.95


def test_logic_rules_manager_get_by_type():
    """Test filtering rules by type."""
    output_config = {'output_path': '/tmp/test'}
    manager = LogicRulesManager(output_config)
    
    manager.create_rule(rule_type="type_a", description="Rule A1")
    manager.create_rule(rule_type="type_b", description="Rule B1")
    manager.create_rule(rule_type="type_a", description="Rule A2")
    
    type_a_rules = manager.get_rules_by_type("type_a")
    assert len(type_a_rules) == 2
    assert all(r.rule_type == "type_a" for r in type_a_rules)


def test_logic_rules_manager_save_json():
    """Test saving rules to JSON file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_config = {
            'output_path': tmpdir,
            'rules_format': 'json'
        }
        manager = LogicRulesManager(output_config)
        
        manager.create_rule(rule_type="test", description="Test rule 1")
        manager.create_rule(rule_type="test", description="Test rule 2")
        
        result = manager.save_rules("test_video.mp4")
        assert result is True
        
        # Check file was created
        output_file = Path(tmpdir) / "test_video_rules.json"
        assert output_file.exists()
        
        # Verify content
        with open(output_file) as f:
            data = json.load(f)
        
        assert data['video'] == "test_video.mp4"
        assert data['total_rules'] == 2
        assert len(data['rules']) == 2


def test_logic_rules_manager_clear():
    """Test clearing rules."""
    output_config = {'output_path': '/tmp/test'}
    manager = LogicRulesManager(output_config)
    
    manager.create_rule(rule_type="test", description="Test rule 1")
    manager.create_rule(rule_type="test", description="Test rule 2")
    
    assert len(manager.rules) == 2
    
    manager.clear_rules()
    assert len(manager.rules) == 0
