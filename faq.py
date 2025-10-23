"""
FAQ System for ICICI Insurance Chatbot
Provides curated answers for common questions
"""

FAQ_DATABASE = {
    "claim settlement ratio": {
        "answer": "ICICI Prudential Life Insurance has an impressive 99.3% claim settlement ratio for FY 2024-25, which demonstrates their strong commitment to processing and settling customer claims reliably.",
        "keywords": ["claim", "settlement", "ratio", "percentage"]
    },
    
    "what is icici": {
        "answer": "ICICI Prudential Life Insurance Company Limited is one of India's leading life insurance providers. They offer a wide range of insurance products including life insurance, health insurance, retirement plans, and investment-linked insurance policies. With a 99.3% claim settlement ratio and coverage for over 3.17 crore lives, they are a trusted name in the insurance industry.",
        "keywords": ["what", "icici", "insurance", "prudential", "company"]
    },
    
    "types of insurance": {
        "answer": "ICICI Prudential offers various types of insurance including: Life Insurance (term plans, whole life), Health Insurance, Retirement Plans, Child Plans, Investment Plans (ULIPs), and Savings Plans. Each plan is designed to meet different financial goals and protection needs.",
        "keywords": ["types", "kinds", "products", "offer"]
    },
    
    "file claim": {
        "answer": "To file a claim with ICICI Prudential: 1) Visit the Claims section on the ICICI Prudential website to submit online, 2) Call the 24x7 ClaimCare helpline at 1800-266-0, 3) Visit a physical branch, or 4) Email claimsupport@iciciprulife.com. You'll need policy documents, death certificate (for death claims), and other relevant documentation.",
        "keywords": ["file", "claim", "submit", "process"]
    },
    
    "contact": {
        "answer": "You can contact ICICI Prudential customer support through: 24x7 ClaimCare Helpline: 1800-266-0, Email: claimsupport@iciciprulife.com, or visit any ICICI Prudential branch. For grievances, you can also reach out to their Grievance Redressal Department.",
        "keywords": ["contact", "customer", "support", "helpline", "phone"]
    },
    
    "benefits life insurance": {
        "answer": "Key benefits of ICICI Life Insurance include: Financial Security for your family, Wealth Creation through investment plans, Tax Savings under Section 80C and 10(10D), Retirement Planning options, Death Benefit coverage, and Long-term financial protection. Plans also offer flexibility in premium payment and policy terms.",
        "keywords": ["benefit", "advantage", "life", "insurance"]
    },
    
    "health insurance": {
        "answer": "ICICI Prudential offers health insurance riders and health covers that can be added to life insurance policies. These provide coverage for medical expenses, critical illness, surgical procedures, and hospitalization. Popular options include ICICI Pru Health Protector and ICICI Pru Vital Care Benefit.",
        "keywords": ["health", "medical", "wellness"]
    },
    
    "premium payment": {
        "answer": "ICICI Prudential offers flexible premium payment options including: Online payment through their website or app, Auto-debit from bank accounts, Payment at branches, Mobile wallets, and Credit/Debit cards. You can choose monthly, quarterly, half-yearly, or annual payment frequencies.",
        "keywords": ["premium", "payment", "pay"]
    },
    
    "term insurance": {
        "answer": "Term insurance is a pure protection plan that provides life cover for a specified term. ICICI Prudential's term insurance plans offer high life cover at affordable premiums, with benefits like tax savings, flexible policy terms (10-40 years), and riders for critical illness or accidental death. Popular plans include ICICI Pru iProtect Smart.",
        "keywords": ["term", "insurance", "pure", "protection"]
    },
    
    "retirement plans": {
        "answer": "ICICI Prudential offers retirement and pension plans that help you build a corpus for your post-retirement life. These plans provide regular income after retirement, guaranteed benefits, and wealth accumulation through bonuses. Options include immediate annuity plans and deferred pension plans with flexible payout options.",
        "keywords": ["retirement", "pension", "annuity"]
    },
    
    "ulip plans": {
        "answer": "ULIPs (Unit Linked Insurance Plans) from ICICI Prudential combine insurance protection with investment opportunities. Your premiums are invested in equity, debt, or balanced funds based on your risk appetite. They offer flexibility to switch between funds, partial withdrawals, and tax benefits under Section 80C and 10(10D).",
        "keywords": ["ulip", "unit", "linked", "investment"]
    },
    
    "child plans": {
        "answer": "ICICI Prudential's child plans help secure your child's future by building a fund for education, marriage, or other milestones. These plans offer life cover for the parent, premium waiver in case of unfortunate events, and guaranteed payouts at specific intervals to meet your child's financial needs.",
        "keywords": ["child", "children", "education", "kids", "insurance"]
    },
    
    "tax benefits": {
        "answer": "ICICI Prudential life insurance policies offer tax benefits under Section 80C (up to ₹1.5 lakh deduction on premiums paid) and Section 10(10D) (tax-free maturity and death benefits). However, tax benefits are subject to prevailing tax laws and conditions. Consult a tax advisor for your specific situation.",
        "keywords": ["tax", "benefits", "80c", "deduction"]
    },
    
    "riders": {
        "answer": "ICICI Prudential offers various riders to enhance your policy coverage including: Accidental Death Benefit Rider, Critical Illness Rider, Surgical Care Rider, Income Benefit Rider, and Premium Waiver Benefit. Riders provide additional protection at affordable costs and can be customized based on your needs.",
        "keywords": ["rider", "riders", "additional", "benefit"]
    },
    
    "premium cost": {
        "answer": "Premium costs for ICICI Prudential policies depend on several factors: your age, sum assured, policy term, premium payment term, health status, and lifestyle habits. Women typically get lower premiums (up to 15% discount). You can get a personalized quote on their website or by contacting their advisors at 1800-266-0.",
        "keywords": ["premium", "cost", "price", "how", "much"]
    },
    
    "maturity benefit": {
        "answer": "Maturity benefit is the amount paid by ICICI Prudential when your policy completes its full term. It typically includes: the sum assured, accumulated bonuses (if applicable), and guaranteed additions. For ULIP plans, it's the fund value. For traditional plans, it includes guaranteed maturity benefit plus any declared bonuses.",
        "keywords": ["maturity", "benefit", "payout", "completion"]
    },
    
    "savings plans": {
        "answer": "ICICI Prudential's savings plans help you accumulate wealth while providing life cover. These plans offer guaranteed returns, bonuses, flexible premium payment options, and maturity benefits. Popular options include traditional endowment plans, money-back policies, and guaranteed savings plans with life cover throughout the policy term.",
        "keywords": ["savings", "save", "accumulation", "wealth"]
    }
}

def find_faq_answer(query: str) -> str:
    """
    Check if the query matches a FAQ and return the curated answer
    Returns None if no match found
    """
    query_lower = query.lower()
    
    # Try exact phrase matching first (most specific)
    for faq_key, faq_data in FAQ_DATABASE.items():
        # Check if the FAQ key phrase is in the query
        if faq_key in query_lower:
            # Additional check: ensure it's a strong match, not just substring
            key_words = faq_key.split()
            if all(word in query_lower for word in key_words):
                return faq_data["answer"]
    
    # Try keyword matching with higher threshold
    max_matches = 0
    best_match = None
    best_match_key = None
    
    for faq_key, faq_data in FAQ_DATABASE.items():
        matches = sum(1 for keyword in faq_data["keywords"] if keyword in query_lower)
        
        # Require at least 2 keyword matches AND check for specificity
        if matches >= 2:
            # Boost score if FAQ key words are in query
            key_words_in_query = sum(1 for word in faq_key.split() if word in query_lower)
            total_score = matches + (key_words_in_query * 2)
            
            if total_score > max_matches:
                max_matches = total_score
                best_match = faq_data["answer"]
                best_match_key = faq_key
    
    # Only return if we have a strong match (score >= 4)
    if max_matches >= 4:
        return best_match
    
    return None

if __name__ == "__main__":
    # Test the FAQ system
    test_queries = [
        "What is the claim settlement ratio?",
        "Tell me about ICICI Insurance",
        "How do I file a claim?",
        "What types of insurance do you offer?",
        "How can I contact customer support?"
    ]
    
    print("Testing FAQ System\n" + "="*60)
    for query in test_queries:
        answer = find_faq_answer(query)
        print(f"\nQ: {query}")
        print(f"A: {answer if answer else 'No FAQ match'}")
        print("-"*60)
