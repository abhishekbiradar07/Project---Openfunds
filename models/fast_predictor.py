"""
Fast success prediction for OpenFunds campaigns.
Uses rule-based heuristics for instant predictions without ML model delays.
"""

import hashlib
import re
from typing import Tuple

def calculate_title_quality(title: str) -> float:
    """
    Analyze title quality (0.0 to 1.0).
    Good titles are clear, specific, and emotionally engaging.
    """
    if not title or len(title.strip()) < 5:
        return 0.3
    
    score = 0.5  # Base score
    
    # Length check - optimal is 30-70 characters
    length = len(title)
    if 30 <= length <= 70:
        score += 0.15
    elif 20 <= length <= 80:
        score += 0.08
    elif length < 10:
        score -= 0.15
    
    # Check for emotional/impact words
    impact_words = [
        'help', 'save', 'support', 'emergency', 'urgent', 'life', 'lives',
        'children', 'family', 'community', 'hope', 'future', 'education',
        'health', 'medical', 'rescue', 'rebuild', 'relief', 'care'
    ]
    title_lower = title.lower()
    impact_count = sum(1 for word in impact_words if word in title_lower)
    score += min(impact_count * 0.08, 0.2)
    
    # Specificity check - specific numbers/places are good
    if re.search(r'\d+', title):  # Contains numbers
        score += 0.08
    
    # Check for question marks or exclamation (can be engaging but shouldn't overdo)
    if '?' in title or '!' in title:
        count = title.count('?') + title.count('!')
        if count == 1:
            score += 0.05
        elif count > 2:
            score -= 0.05  # Too many is spammy
    
    # Capitalize first letter check (professional)
    if title[0].isupper():
        score += 0.03
    
    return min(max(score, 0.2), 1.0)

def calculate_description_quality(description: str) -> float:
    """
    Analyze description quality (0.0 to 1.0).
    Good descriptions are detailed, clear, and explain impact.
    """
    if not description or len(description.strip()) < 20:
        return 0.3
    
    score = 0.5  # Base score
    
    # Length check - optimal is 200-800 characters
    length = len(description)
    if 200 <= length <= 800:
        score += 0.15
    elif 100 <= length <= 1000:
        score += 0.08
    elif length < 50:
        score -= 0.15
    elif length > 1500:
        score -= 0.05  # Too long can be overwhelming
    
    # Check for key story elements
    desc_lower = description.lower()
    
    # Problem statement
    problem_words = ['need', 'help', 'lack', 'without', 'struggling', 'challenge', 'issue', 'problem']
    if any(word in desc_lower for word in problem_words):
        score += 0.08
    
    # Solution/Impact
    solution_words = ['will', 'provide', 'support', 'fund', 'enable', 'create', 'build', 'deliver']
    if any(word in desc_lower for word in solution_words):
        score += 0.08
    
    # Specific numbers/metrics
    number_matches = re.findall(r'\d+', description)
    if len(number_matches) >= 2:
        score += 0.1
    
    # Sentence structure - good descriptions have multiple sentences
    sentences = re.split(r'[.!?]+', description)
    sentence_count = len([s for s in sentences if len(s.strip()) > 10])
    if sentence_count >= 3:
        score += 0.08
    elif sentence_count >= 5:
        score += 0.12
    
    # Emotional connection words
    emotion_words = ['family', 'children', 'community', 'lives', 'hope', 'future', 'together']
    emotion_count = sum(1 for word in emotion_words if word in desc_lower)
    score += min(emotion_count * 0.05, 0.12)
    
    return min(max(score, 0.2), 1.0)

def calculate_target_reasonableness(target_amount: float) -> float:
    """
    Analyze if target amount is reasonable (0.0 to 1.0).
    Smaller, achievable goals tend to succeed more often.
    """
    score = 0.5  # Base score
    
    # Sweet spot for crowdfunding is usually 0.1 - 5.0 BTC
    if 0.1 <= target_amount <= 2.0:
        score += 0.25
    elif 2.0 < target_amount <= 5.0:
        score += 0.15
    elif target_amount < 0.1:
        score += 0.05  # Too small might seem insignificant
    elif target_amount > 10.0:
        score -= 0.2  # Very large goals are harder to reach
    elif target_amount > 20.0:
        score -= 0.3
    
    return min(max(score, 0.2), 1.0)

def add_uniqueness_variance(base_score: float, title: str, description: str, target_amount: float) -> float:
    """
    Add slight variance based on unique campaign characteristics.
    This prevents identical scores for similar campaigns.
    """
    # Create unique hash from campaign details
    raw_string = f"{title.lower()}_{description.lower()}_{target_amount}"
    hash_digest = hashlib.sha256(raw_string.encode()).hexdigest()
    hash_value = int(hash_digest[:8], 16)
    
    # Small adjustment: -0.02 to +0.02
    adjustment = ((hash_value % 400) - 200) / 10000.0
    
    return base_score + adjustment

def predict_success(title: str, description: str, target_amount: float) -> Tuple[float, str]:
    """
    Predict campaign success likelihood using fast rule-based analysis.
    
    Args:
        title: Campaign title
        description: Campaign description
        target_amount: Target amount in BTC
    
    Returns:
        Tuple of (probability 0.0-1.0, feedback message)
    """
    # Calculate component scores
    title_score = calculate_title_quality(title)
    desc_score = calculate_description_quality(description)
    target_score = calculate_target_reasonableness(target_amount)
    
    # Weighted average (description is most important)
    base_score = (
        title_score * 0.25 +
        desc_score * 0.50 +
        target_score * 0.25
    )
    
    # Add uniqueness variance
    final_score = add_uniqueness_variance(base_score, title, description, target_amount)
    
    # Clamp to reasonable range (35% - 95%)
    final_score = min(max(final_score, 0.35), 0.95)
    
    # Generate feedback based on score
    feedback = generate_feedback(final_score, title_score, desc_score, target_score, target_amount)
    
    return final_score, feedback

def generate_feedback(overall_score: float, title_score: float, desc_score: float, 
                      target_score: float, target_amount: float) -> str:
    """Generate personalized feedback based on the analysis."""
    
    # Overall assessment
    if overall_score >= 0.80:
        base_msg = "✨ Excellent! This campaign is well-crafted and has strong success potential."
    elif overall_score >= 0.65:
        base_msg = "👍 Good campaign! It has solid potential with a few improvements."
    elif overall_score >= 0.50:
        base_msg = "💡 Decent foundation, but there's room for improvement."
    else:
        base_msg = "📝 This campaign needs refinement to increase its success chances."
    
    # Specific suggestions
    suggestions = []
    
    if title_score < 0.6:
        suggestions.append("Consider making your title more specific and emotionally engaging")
    
    if desc_score < 0.6:
        suggestions.append("Add more detail about the problem, your solution, and the impact")
    
    if desc_score < 0.7 and len(suggestions) == 0:
        suggestions.append("Include specific numbers and metrics in your description")
    
    if target_score < 0.6:
        if target_amount > 10:
            suggestions.append("Consider breaking this into smaller milestone goals")
        else:
            suggestions.append("Your target amount could be optimized for better success rates")
    
    # Positive reinforcement for strong areas
    if title_score >= 0.75:
        suggestions.append("Your title is compelling and clear!")
    
    if desc_score >= 0.75:
        suggestions.append("Your description effectively tells your story!")
    
    # Combine feedback
    if suggestions:
        return base_msg + " " + " ".join(suggestions[:3])  # Max 3 suggestions
    else:
        return base_msg + " Keep up the great work!"

# Test function
if __name__ == "__main__":
    print("Testing Fast Success Predictor\n")
    
    # Test case 1: Good campaign
    title1 = "Mobile Medical Clinics for 5,000 Refugee Families"
    desc1 = """Our organization provides essential healthcare to refugee camps through mobile medical units. 
    We serve over 5,000 families monthly with doctors, nurses, medicines, and equipment. 
    Your donation will help us expand our reach and save more lives. 
    Every 0.1 BTC provides a week of medical care for 50 families."""
    target1 = 3.0
    
    score1, feedback1 = predict_success(title1, desc1, target1)
    print(f"Campaign 1: {title1[:50]}...")
    print(f"Success Likelihood: {score1*100:.1f}%")
    print(f"Feedback: {feedback1}")
    print()
    
    # Test case 2: Needs improvement
    title2 = "Help"
    desc2 = "Need money for project"
    target2 = 50.0
    
    score2, feedback2 = predict_success(title2, desc2, target2)
    print(f"Campaign 2: {title2}")
    print(f"Success Likelihood: {score2*100:.1f}%")
    print(f"Feedback: {feedback2}")
    print()
    
    # Test case 3: Medium quality
    title3 = "Community Garden Restoration"
    desc3 = "Our neighborhood garden was damaged by storms and needs repair. We want to restore it for everyone to enjoy. The funds will cover new plants, soil, and equipment."
    target3 = 1.5
    
    score3, feedback3 = predict_success(title3, desc3, target3)
    print(f"Campaign 3: {title3}")
    print(f"Success Likelihood: {score3*100:.1f}%")
    print(f"Feedback: {feedback3}")
    
    print("\n✅ Fast predictor works!")
