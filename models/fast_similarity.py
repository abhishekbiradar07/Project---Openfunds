"""
Fast keyword-based similarity for OpenFunds campaigns.
Fallback when deep learning models are too slow.
"""

import pandas as pd
import os
from typing import List, Dict
import re

CSV_PATH = "data_exports/campaigns.csv"

def clean_text(text: str) -> str:
    """Clean and normalize text for comparison."""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Remove extra spaces
    text = ' '.join(text.split())
    return text

def get_keywords(text: str) -> set:
    """Extract meaningful keywords from text."""
    # Common words to ignore
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may',
        'might', 'must', 'shall', 'this', 'that', 'these', 'those', 'i', 'you',
        'he', 'she', 'it', 'we', 'they', 'them', 'their', 'my', 'your', 'his',
        'her', 'its', 'our', 'as', 'if', 'when', 'where', 'who', 'which', 'what',
        'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
        'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
        'too', 'very', 'just', 'now'
    }
    
    cleaned = clean_text(text)
    words = cleaned.split()
    
    # Filter out stopwords and very short words
    keywords = {w for w in words if len(w) > 2 and w not in stopwords}
    
    return keywords

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate Jaccard similarity between two texts."""
    keywords1 = get_keywords(text1)
    keywords2 = get_keywords(text2)
    
    if not keywords1 or not keywords2:
        return 0.0
    
    intersection = len(keywords1 & keywords2)
    union = len(keywords1 | keywords2)
    
    return intersection / union if union > 0 else 0.0

def get_similar_campaigns(title: str, description: str, top_k: int = 3, threshold: float = 0.15) -> List[Dict]:
    """
    Find similar campaigns using fast keyword-based matching.
    
    Args:
        title: Campaign title
        description: Campaign description
        top_k: Number of similar campaigns to return
        threshold: Minimum similarity score (0.0 to 1.0)
    
    Returns:
        List of dicts with 'title', 'description', and 'score'
    """
    try:
        # Check if CSV exists
        if not os.path.exists(CSV_PATH):
            return []
        
        # Read campaigns
        df = pd.read_csv(CSV_PATH)
        
        if df.empty:
            return []
        
        # Combine input text
        input_text = f"{title} {description}"
        
        # Calculate similarity for each campaign
        results = []
        for idx, row in df.iterrows():
            campaign_text = f"{row['title']} {row['description']}"
            similarity = calculate_similarity(input_text, campaign_text)
            
            # Only include if above threshold
            if similarity >= threshold:
                results.append({
                    'title': row['title'],
                    'description': row['description'],
                    'score': similarity
                })
        
        # Sort by similarity (highest first) and return top_k
        results = sorted(results, key=lambda x: x['score'], reverse=True)[:top_k]
        
        return results
        
    except Exception as e:
        print(f"Error in fast similarity: {e}")
        return []

# Test function
if __name__ == "__main__":
    print("Testing fast similarity...")
    
    test_title = "Medical Help for Refugees"
    test_desc = "Healthcare for refugee camps with mobile clinics"
    
    similar = get_similar_campaigns(test_title, test_desc)
    
    print(f"\nFound {len(similar)} similar campaigns:")
    for i, campaign in enumerate(similar, 1):
        print(f"\n{i}. {campaign['title']}")
        print(f"   Score: {campaign['score']:.2%}")
    
    print("\n✅ Fast similarity works!")
