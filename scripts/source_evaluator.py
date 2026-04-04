#!/usr/bin/env python3
"""Evaluate source credibility with a small CLI for Codex workflows."""

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Dict, Optional
from urllib.parse import urlparse


@dataclass
class CredibilityScore:
    """Represents source credibility assessment."""
    overall_score: float
    domain_authority: float
    recency: float
    expertise: float
    bias_score: float
    factors: Dict[str, str]
    recommendation: str


class SourceEvaluator:
    """Evaluates source credibility and quality."""

    HIGH_AUTHORITY_DOMAINS = {
        'arxiv.org', 'nature.com', 'science.org', 'cell.com', 'nejm.org',
        'thelancet.com', 'springer.com', 'sciencedirect.com', 'plos.org',
        'ieee.org', 'acm.org', 'pubmed.ncbi.nlm.nih.gov',
        'nih.gov', 'cdc.gov', 'who.int', 'fda.gov', 'nasa.gov',
        'gov.uk', 'europa.eu', 'un.org',
        'docs.python.org', 'developer.mozilla.org', 'docs.microsoft.com',
        'cloud.google.com', 'aws.amazon.com', 'kubernetes.io',
        'reuters.com', 'apnews.com', 'bbc.com', 'economist.com',
        'nature.com/news', 'scientificamerican.com'
    }

    MODERATE_AUTHORITY_DOMAINS = {
        'techcrunch.com', 'theverge.com', 'arstechnica.com', 'wired.com',
        'zdnet.com', 'cnet.com', 'forbes.com', 'bloomberg.com', 'wsj.com',
        'ft.com', 'wikipedia.org', 'britannica.com', 'khanacademy.org',
        'medium.com', 'dev.to', 'stackoverflow.com', 'github.com'
    }

    LOW_AUTHORITY_INDICATORS = ['blogspot.com', 'wordpress.com', 'wix.com', 'substack.com']

    def evaluate_source(
        self,
        url: str,
        title: str,
        content: Optional[str] = None,
        publication_date: Optional[str] = None,
        author: Optional[str] = None,
    ) -> CredibilityScore:
        domain = self._extract_domain(url)
        domain_score = self._evaluate_domain_authority(domain)
        recency_score = self._evaluate_recency(publication_date)
        expertise_score = self._evaluate_expertise(domain, title, author)
        bias_score = self._evaluate_bias(domain, title, content)

        overall = (
            domain_score * 0.35 +
            recency_score * 0.20 +
            expertise_score * 0.25 +
            bias_score * 0.20
        )
        factors = self._identify_factors(domain_score, recency_score, expertise_score, bias_score)
        recommendation = self._generate_recommendation(overall)

        return CredibilityScore(
            overall_score=round(overall, 2),
            domain_authority=round(domain_score, 2),
            recency=round(recency_score, 2),
            expertise=round(expertise_score, 2),
            bias_score=round(bias_score, 2),
            factors=factors,
            recommendation=recommendation,
        )

    def _extract_domain(self, url: str) -> str:
        return urlparse(url).netloc.lower().replace('www.', '')

    def _evaluate_domain_authority(self, domain: str) -> float:
        if domain in self.HIGH_AUTHORITY_DOMAINS:
            return 90.0
        if domain in self.MODERATE_AUTHORITY_DOMAINS:
            return 70.0
        if any(indicator in domain for indicator in self.LOW_AUTHORITY_INDICATORS):
            return 40.0
        return 55.0

    def _evaluate_recency(self, publication_date: Optional[str]) -> float:
        if not publication_date:
            return 50.0
        try:
            pub_date = datetime.fromisoformat(publication_date.replace('Z', '+00:00'))
            age = datetime.now() - pub_date
            if age < timedelta(days=90):
                return 100.0
            if age < timedelta(days=365):
                return 85.0
            if age < timedelta(days=730):
                return 70.0
            if age < timedelta(days=1825):
                return 50.0
            return 30.0
        except Exception:
            return 50.0

    def _evaluate_expertise(self, domain: str, title: str, author: Optional[str]) -> float:
        score = 50.0
        if any(d in domain for d in ['arxiv', 'nature', 'science', 'ieee', 'acm']):
            score += 30
        if '.gov' in domain or 'who.int' in domain:
            score += 25
        if 'docs.' in domain or 'documentation' in title.lower():
            score += 20
        if author and any(t in author.lower() for t in ['dr.', 'phd', 'professor']):
            score += 15
        return min(score, 100.0)

    def _evaluate_bias(self, domain: str, title: str, content: Optional[str]) -> float:
        score = 70.0
        sensational = ['!', 'shocking', 'unbelievable', "you won't believe", 'secret', "they don't want you to know"]
        if any(indicator in title.lower() for indicator in sensational):
            score -= 20
        if any(d in domain for d in ['arxiv', 'nature', 'science', 'ieee']):
            score += 20
        if content and any(ind in content.lower() for ind in ['however', 'although', 'on the other hand', 'critics argue']):
            score += 10
        return min(max(score, 0.0), 100.0)

    def _identify_factors(self, domain_score: float, recency_score: float, expertise_score: float, bias_score: float) -> Dict[str, str]:
        factors: Dict[str, str] = {}
        if domain_score >= 85:
            factors['domain'] = 'High authority domain'
        elif domain_score <= 45:
            factors['domain'] = 'Low authority domain - verify claims'
        if recency_score >= 85:
            factors['recency'] = 'Recent information'
        elif recency_score <= 40:
            factors['recency'] = 'Outdated information - verify currency'
        if expertise_score >= 80:
            factors['expertise'] = 'Expert source'
        elif expertise_score <= 45:
            factors['expertise'] = 'Limited expertise indicators'
        if bias_score >= 80:
            factors['bias'] = 'Balanced perspective'
        elif bias_score <= 50:
            factors['bias'] = 'Potential bias detected'
        return factors

    def _generate_recommendation(self, overall_score: float) -> str:
        if overall_score >= 80:
            return 'high_trust'
        if overall_score >= 60:
            return 'moderate_trust'
        if overall_score >= 40:
            return 'low_trust'
        return 'verify'


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Evaluate source credibility',
        epilog="Example: python scripts/source_evaluator.py --url https://example.com --title 'Example title'",
    )
    parser.add_argument('--url', required=True, help='Source URL')
    parser.add_argument('--title', required=True, help='Source title')
    parser.add_argument('--publication-date', help='Publication date in ISO format (YYYY-MM-DD)')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--content', help='Optional content snippet')
    args = parser.parse_args()

    evaluator = SourceEvaluator()
    score = evaluator.evaluate_source(
        url=args.url,
        title=args.title,
        content=args.content,
        publication_date=args.publication_date,
        author=args.author,
    )
    print(json.dumps(asdict(score), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
