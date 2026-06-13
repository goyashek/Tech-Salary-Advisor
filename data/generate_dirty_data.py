import os
import numpy as np
import pandas as pd

np.random.seed(42)

def generate_dirty_data(num_samples=110000):
    # Expanded list of roles, highlighting high-demand AI/ML roles
    roles_pool = [
        # AI / ML Roles (Higher proportion & salaries)
        "Data Scientist", "DATA SCIENTIST", "data scientist",
        "Machine Learning Engineer", "ML Engineer", "ml engineer",
        "AI Researcher", "ai researcher", "AI Engineer",
        "NLP Engineer", "nlp engineer",
        "Computer Vision Engineer", "cv engineer",
        "Deep Learning Engineer", "DL Engineer",
        
        # Standard Tech Roles
        "Software Engineer", "software engineer", "Software Developer",
        "Frontend Developer", "frontend engineer",
        "Backend Developer", "backend engineer",
        "Full Stack Developer", "fullstack engineer",
        "DevOps Engineer", "DevOps",
        "Data Engineer", "data engineer",
        "QA Engineer", "QA",
        "Product Manager", "PM"
    ]
    
    # Cities in India
    cities_pool = [
        " Bangalore ", "bangalore", "Bangalore",
        "Mumbai", " mumbai", "MUMBAI",
        "Delhi NCR", "delhi ncr", " Delhi NCR",
        "Hyderabad", "hyderabad", "Hyderabad ",
        "Pune", "pune", " Pune ",
        "Chennai", "chennai", "chennai ",
        "Noida", "noida", " Noida"
    ]
    
    # Education Levels
    edu_pool = [
        "Bachelor's", "bachelors", "B.Tech", "btech", "B.E.",
        "Master's", "masters", "M.Tech", "mtech", "M.S.",
        "PhD", "phd", "Doctorate"
    ]
    
    # Unified list of technical skills
    skills_pool = [
        "Python", "Java", "C++", "JavaScript", "Go", 
        "SQL", "Spark", "AWS", "Docker", "Kubernetes", 
        "PyTorch", "TensorFlow", "React", "System Design", "Agile"
    ]
    
    # Target base salaries in INR
    base_salaries = {
        # AI/ML roles premium
        "Data Scientist": 950000,
        "Machine Learning Engineer": 1050000,
        "AI Researcher": 1200000,
        "NLP Engineer": 1000000,
        "Computer Vision Engineer": 1000000,
        "Deep Learning Engineer": 1100000,
        
        # Standard roles
        "Software Engineer": 700000,
        "Frontend Developer": 600000,
        "Backend Developer": 650000,
        "Full Stack Developer": 750000,
        "DevOps Engineer": 750000,
        "Data Engineer": 750000,
        "QA Engineer": 450000,
        "Product Manager": 950000
    }
    
    city_mults = {
        "bangalore": 1.35,
        "mumbai": 1.25,
        "delhi ncr": 1.18,
        "noida": 1.12,
        "hyderabad": 1.10,
        "pune": 1.05,
        "chennai": 1.00
    }
    
    edu_mults = {
        "bachelor": 1.0,
        "master": 1.2,
        "phd": 1.45
    }
    
    # Propensity of certain roles to have AI-specific skills
    ai_roles = ["Data Scientist", "Machine Learning Engineer", "AI Researcher", "NLP Engineer", "Computer Vision Engineer", "Deep Learning Engineer"]
    
    data = []
    for _ in range(num_samples):
        # Sample role
        raw_role = np.random.choice(roles_pool)
        
        # Determine standard title
        role_lower = raw_role.lower()
        std_title = "Software Engineer"
        if "data scientist" in role_lower:
            std_title = "Data Scientist"
        elif "ml engineer" in role_lower or "machine learning" in role_lower:
            std_title = "Machine Learning Engineer"
        elif "ai researcher" in role_lower:
            std_title = "AI Researcher"
        elif "ai engineer" in role_lower:
            std_title = "Machine Learning Engineer"
        elif "nlp" in role_lower:
            std_title = "NLP Engineer"
        elif "cv engineer" in role_lower or "computer vision" in role_lower:
            std_title = "Computer Vision Engineer"
        elif "dl engineer" in role_lower or "deep learning" in role_lower:
            std_title = "Deep Learning Engineer"
        elif "frontend" in role_lower:
            std_title = "Frontend Developer"
        elif "backend" in role_lower:
            std_title = "Backend Developer"
        elif "fullstack" in role_lower or "full stack" in role_lower:
            std_title = "Full Stack Developer"
        elif "devops" in role_lower:
            std_title = "DevOps Engineer"
        elif "data engineer" in role_lower:
            std_title = "Data Engineer"
        elif "qa" in role_lower:
            std_title = "QA Engineer"
        elif "product" in role_lower or "pm" in role_lower:
            std_title = "Product Manager"
            
        city = np.random.choice(cities_pool)
        edu = np.random.choice(edu_pool)
        
        # Experience (0 to 20 years, log-normal shape)
        exp = np.clip(np.random.exponential(scale=6.0), 0, 20)
        exp = round(exp, 1)
        
        # Sample skills based on role type
        if std_title in ai_roles:
            # High probability of Python, PyTorch, TensorFlow, SQL
            skills_probs = [0.9, 0.2, 0.2, 0.3, 0.1, 0.7, 0.3, 0.4, 0.3, 0.2, 0.7, 0.1, 0.4, 0.3, 0.4]
        else:
            # High probability of Java, JavaScript, React, SQL, AWS
            skills_probs = [0.4, 0.6, 0.3, 0.6, 0.2, 0.5, 0.2, 0.5, 0.4, 0.2, 0.05, 0.5, 0.5, 0.5, 0.5]
            
        chosen_skills = []
        for s, p in zip(skills_pool, skills_probs):
            if np.random.rand() < p:
                chosen_skills.append(s)
                
        if len(chosen_skills) == 0:
            chosen_skills = ["Python", "SQL"] if std_title in ai_roles else ["Java", "JavaScript"]
            
        skills_str = ", ".join(chosen_skills)
        if np.random.rand() < 0.2:
            skills_str = ",".join(chosen_skills)
            
        # Base salary
        base = base_salaries[std_title]
        
        # Experience scaling (AI/ML roles scale steeper)
        exp_coeff = 110000 if std_title in ai_roles else 80000
        exp_gain = exp_coeff * (exp ** 0.8)
        
        # City multiplier
        city_clean = city.strip().lower()
        mult_city = 1.0
        for k, v in city_mults.items():
            if k in city_clean:
                mult_city = v
                break
                
        # Edu multiplier
        edu_clean = edu.lower()
        mult_edu = 1.0
        if "master" in edu_clean or "mtech" in edu_clean or "m.tech" in edu_clean or "ms" in edu_clean or "m.s." in edu_clean:
            mult_edu = edu_mults["master"]
        elif "phd" in edu_clean or "doctor" in edu_clean:
            mult_edu = edu_mults["phd"]
            
        # Add random noise
        noise = np.random.normal(0, 120000 + 0.04 * (base + exp_gain))
        
        salary = (base + exp_gain) * mult_city * mult_edu + noise
        salary = int(np.clip(salary, 350000, 6000000))
        
        # Introduce NaNs (Missing values)
        if np.random.rand() < 0.05:
            exp = np.nan
        if np.random.rand() < 0.05:
            edu = np.nan
        if np.random.rand() < 0.05:
            city = np.nan
        if np.random.rand() < 0.05:
            skills_str = np.nan
        if np.random.rand() < 0.02:
            salary = np.nan
            
        data.append({
            "Job_Title": raw_role,
            "Experience_Years": exp,
            "Education_Level": edu,
            "Location": city,
            "Skills": skills_str,
            "Salary_INR": salary
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating large dirty dataset (1,10,000 samples) with AI/ML premium roles...")
    df = generate_dirty_data(110000)
    
    os.makedirs("/Users/abhigoyal/Documents/Acadss/Data Science/Projects/Tech-Salary-Advisor/data", exist_ok=True)
    csv_path = "/Users/abhigoyal/Documents/Acadss/Data Science/Projects/Tech-Salary-Advisor/data/salary_dataset_dirty.csv"
    df.to_csv(csv_path, index=False)
    
    print(f"Dataset generated at {csv_path}!")
    print(f"Shape: {df.shape}")
    print(f"\nValue counts for standard categories:")
    print(df['Job_Title'].value_counts().head(10))
