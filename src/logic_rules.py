"""Logic rules extraction and management."""

import json
import yaml
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import logging


class LogicRule:
    """Represents a single logic rule extracted from video analysis."""

    def __init__(
        self,
        rule_id: str,
        rule_type: str,
        description: str,
        confidence: float = 1.0,
        frame_number: int = None,
        timestamp: float = None,
        metadata: Dict[str, Any] = None
    ):
        """
        Initialize a logic rule.

        Args:
            rule_id: Unique identifier for the rule
            rule_type: Type/category of the rule
            description: Human-readable description
            confidence: Confidence score (0.0 to 1.0)
            frame_number: Frame number where rule was detected
            timestamp: Video timestamp in seconds
            metadata: Additional metadata
        """
        self.rule_id = rule_id
        self.rule_type = rule_type
        self.description = description
        self.confidence = confidence
        self.frame_number = frame_number
        self.timestamp = timestamp
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary."""
        return {
            'rule_id': self.rule_id,
            'rule_type': self.rule_type,
            'description': self.description,
            'confidence': self.confidence,
            'frame_number': self.frame_number,
            'timestamp': self.timestamp,
            'metadata': self.metadata,
            'created_at': self.created_at
        }


class LogicRulesManager:
    """Manage logic rules extraction and storage."""

    def __init__(self, output_config: dict):
        """
        Initialize logic rules manager.

        Args:
            output_config: Output configuration dictionary
        """
        self.output_config = output_config
        self.rules: List[LogicRule] = []
        self.logger = logging.getLogger(__name__)

    def add_rule(self, rule: LogicRule):
        """
        Add a new logic rule.

        Args:
            rule: LogicRule instance to add
        """
        self.rules.append(rule)
        self.logger.debug(f"Added rule: {rule.rule_id}")

    def create_rule(
        self,
        rule_type: str,
        description: str,
        confidence: float = 1.0,
        frame_number: int = None,
        timestamp: float = None,
        metadata: Dict[str, Any] = None
    ) -> LogicRule:
        """
        Create and add a new logic rule.

        Args:
            rule_type: Type/category of the rule
            description: Human-readable description
            confidence: Confidence score
            frame_number: Frame number where rule was detected
            timestamp: Video timestamp in seconds
            metadata: Additional metadata

        Returns:
            Created LogicRule instance
        """
        rule_id = f"rule_{len(self.rules) + 1:04d}"
        rule = LogicRule(
            rule_id=rule_id,
            rule_type=rule_type,
            description=description,
            confidence=confidence,
            frame_number=frame_number,
            timestamp=timestamp,
            metadata=metadata
        )
        self.add_rule(rule)
        return rule

    def get_rules_by_type(self, rule_type: str) -> List[LogicRule]:
        """
        Get all rules of a specific type.

        Args:
            rule_type: Type of rules to retrieve

        Returns:
            List of matching rules
        """
        return [rule for rule in self.rules if rule.rule_type == rule_type]

    def save_rules(self, video_name: str) -> bool:
        """
        Save rules to file.

        Args:
            video_name: Name of the video being processed

        Returns:
            True if successful, False otherwise
        """
        if not self.rules:
            self.logger.warning("No rules to save")
            return False

        output_path = Path(self.output_config.get('output_path', './data/output'))
        output_path.mkdir(parents=True, exist_ok=True)

        format_type = self.output_config.get('rules_format', 'json')
        base_name = Path(video_name).stem
        
        rules_data = {
            'video': video_name,
            'total_rules': len(self.rules),
            'generated_at': datetime.now().isoformat(),
            'rules': [rule.to_dict() for rule in self.rules]
        }

        try:
            if format_type == 'json':
                file_path = output_path / f"{base_name}_rules.json"
                with open(file_path, 'w') as f:
                    json.dump(rules_data, f, indent=2)
                    
            elif format_type == 'yaml':
                file_path = output_path / f"{base_name}_rules.yaml"
                with open(file_path, 'w') as f:
                    yaml.dump(rules_data, f, default_flow_style=False)
                    
            elif format_type == 'txt':
                file_path = output_path / f"{base_name}_rules.txt"
                with open(file_path, 'w') as f:
                    f.write(f"Logic Rules for: {video_name}\n")
                    f.write(f"Generated at: {rules_data['generated_at']}\n")
                    f.write(f"Total rules: {len(self.rules)}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    for rule in self.rules:
                        f.write(f"Rule ID: {rule.rule_id}\n")
                        f.write(f"Type: {rule.rule_type}\n")
                        f.write(f"Description: {rule.description}\n")
                        f.write(f"Confidence: {rule.confidence:.2f}\n")
                        if rule.frame_number is not None:
                            f.write(f"Frame: {rule.frame_number}\n")
                        if rule.timestamp is not None:
                            f.write(f"Timestamp: {rule.timestamp:.2f}s\n")
                        f.write("-" * 80 + "\n\n")
            else:
                self.logger.error(f"Unsupported format: {format_type}")
                return False

            self.logger.info(f"Saved {len(self.rules)} rules to {file_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save rules: {e}")
            return False

    def clear_rules(self):
        """Clear all rules."""
        self.rules.clear()
