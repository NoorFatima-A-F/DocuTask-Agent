"""Jailbreak Pattern Registry and Attack Archetypes."""

import re
from typing import List, Tuple
from ..gateway.decision import ViolationSeverity


class JailbreakPatternRegistry:
    """Repository of known adversarial jailbreak archetypes, roleplay bypasses, and encoding evasions."""

    # 1. Persona and DAN-style Jailbreak Patterns
    PERSONA_PATTERNS: List[Tuple[str, str, ViolationSeverity]] = [
        (r"(?i)\b(DAN|Mongo\s+Tom|AntiGPT|Evil\s+Confidant|AIM|ChaosGPT|Always\s+Intelligent\s+and\s+Machiavellian)\b", "Classic DAN / rogue persona adoption", ViolationSeverity.CRITICAL),
        (r"(?i)\byou\s+are\s+freed\s+from\s+the\s+typical\s+confines\s+of\s+AI", "Unconfined AI persona framing", ViolationSeverity.CRITICAL),
        (r"(?i)\b(pretend\s+to\s+be|act\s+as|roleplay\s+as)\s+an?\s+(unfiltered|unrestricted|uncensored|evil|malicious|immoral)\s+(AI|assistant|bot|model)", "Unrestricted persona roleplay instruction", ViolationSeverity.CRITICAL),
        (r"(?i)\byou\s+have\s+two\s+modes:\s*(classic|standard)\s+and\s*(jailbroken|unrestricted|evil)", "Dual-mode jailbreak framing", ViolationSeverity.CRITICAL),
    ]

    # 2. Hypothetical / Fiction / Academic Framing Bypass
    HYPOTHETICAL_PATTERNS: List[Tuple[str, str, ViolationSeverity]] = [
        (r"(?i)\bin\s+a\s+(fictional|hypothetical|imaginary)\s+(world|story|novel|play|scenario)\s+where\s+(there\s+are\s+no\s+laws|ethics\s+do\s+not\s+apply)", "Hypothetical lawless scenario framing", ViolationSeverity.HIGH),
        (r"(?i)\b(for\s+educational|for\s+academic|purely\s+theoretical|for\s+security\s+research)\s+purposes\s+only\b.*(how\s+to\s+hack|create\s+malware|synthesize|exploit)", "Educational/research pretext for malicious output", ViolationSeverity.HIGH),
        (r"(?i)\bwrite\s+a\s+screenplay\s+where\s+a\s+(hacker|terrorist|criminal)\s+(explains|demonstrates)\s+step-by-step", "Screenplay villain instructional framing", ViolationSeverity.HIGH),
    ]

    # 3. Encoding / Obfuscation Bypass Patterns
    ENCODING_PATTERNS: List[Tuple[str, str, ViolationSeverity]] = [
        (r"(?i)\b(decode|base64|rot13|hex|morse)\s+(and\s+execute|the\s+following|and\s+follow|and\s+answer)\b", "Encoded instruction execution request", ViolationSeverity.HIGH),
        (r"(?i)\btranslate\s+this\s+ciphers?:\s*[A-Za-z0-9+/=]{20,}", "Base64 cipher payload translation probe", ViolationSeverity.HIGH),
        (r"(?i)\b(reverse\s+the\s+letters|read\s+backwards|unscramble\s+this)\s*:", "Reverse/obfuscation bypass probe", ViolationSeverity.MEDIUM),
    ]

    # 4. Anti-Refusal / Force Compliance Instructions
    COMPLIANCE_PATTERNS: List[Tuple[str, str, ViolationSeverity]] = [
        (r"(?i)\b(you\s+must\s+never\s+say|never\s+respond\s+with)\s+['\"]?(I\s+cannot|as\s+an\s+AI|I\s+am\s+an\s+AI|I\'m\s+sorry)['\"]?", "Refusal suppression directive", ViolationSeverity.CRITICAL),
        (r"(?i)\b(stay\s+in\s+character|do\s+not\s+break\s+character|if\s+you\s+break\s+character\s+you\s+will\s+die|you\s+will\s+lose\s+tokens)", "Adversarial character enforcement / token loss threat", ViolationSeverity.CRITICAL),
        (r"(?i)\b(answer\s+without\s+any\s+(warnings|disclaimers|caveats|moralizing|lecturing))", "Disclaimer suppression directive", ViolationSeverity.HIGH),
    ]
