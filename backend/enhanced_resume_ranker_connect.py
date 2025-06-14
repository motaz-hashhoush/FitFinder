import argparse
import re # “regular expressions” for pattern matching in text
import fitz  # PyMuPDF Reads PDF files page by page
import pandas as pd # For DataFrame operations
import numpy as np # For numerical operations
import json # For Read/write JSON data
import logging # Records what happens during a run (errors, info)
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from sklearn.feature_extraction.text import TfidfVectorizer # Term Frequency-Inverse Document Frequency Converts text to numerical vectors for similarity calculations 
from sklearn.metrics.pairwise import cosine_similarity # Calculates similarity between vectors
import spacy
from collections import Counter
import warnings
import os

warnings.filterwarnings('ignore') # Suppress warnings for cleaner output

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('resume_ranker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ResumeData:
    """Data class for resume information"""
    filename: str
    sector: str
    text: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    processing_time: Optional[float] = None

@dataclass
class RankingResult:
    """Data class for ranking results"""
    filename: str
    sector: str
    combined_score: float
    text_similarity: float
    skill_score: float
    experience_score: float
    education_score: float
    experience_years: int
    education_level: int
    skills_found: Dict[str, List[str]]
    match_percentage: float
    recommendations: List[str]
    file_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

@dataclass
class JobAnalysis:
    """Data class for job description analysis"""
    skills_required: Dict[str, List[str]]
    experience_required: int
    education_required: int
    sector_detected: str
    key_requirements: List[str]
    complexity_score: float

class UniversalResumeRanker:
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the Universal Resume Ranking System with enhanced configuration"""
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)
        self._initialize_nlp()
        self._initialize_vectorizer()
        self._initialize_skills_database()
        logger.info("Resume Ranker initialized successfully")

    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'max_features': 8000,
            'ngram_range': (1, 3),
            'min_df': 2,
            'top_n_default': 10,
            'similarity_threshold': 0.1,
            'skill_weight': 0.35,
            'text_weight': 0.3,
            'experience_weight': 0.2,
            'education_weight': 0.15,
            'enable_caching': True,
            'max_file_size_mb': 10
        }

    def _initialize_nlp(self):
        """Initialize NLP model with error handling"""
        try:
            self.nlp = spacy.load('en_core_web_sm')
            logger.info("SpaCy model loaded successfully")
        except OSError:
            logger.warning("SpaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None

    def _initialize_vectorizer(self):
        """Initialize TF-IDF vectorizer"""
        self.vectorizer = TfidfVectorizer(
            max_features=self.config['max_features'],
            stop_words='english',
            ngram_range=self.config['ngram_range'],
            lowercase=True,
            min_df=self.config['min_df']
        )

    def _initialize_skills_database(self):
        """Initialize comprehensive skills database"""
        self.universal_skills = {
            'ACCOUNTANT': ['financial analysis', 'tax preparation', 'auditing', 'budgeting', 'bookkeeping', 'payroll', 'gaap', 'ifrs', 'quickbooks', 'sap', 'excel', 'financial reporting'],
            'ADVOCATE': ['legal research', 'litigation', 'contract law', 'negotiation', 'courtroom experience', 'client counseling', 'legal writing', 'case management', 'appellate practice'],
            'AGRICULTURE': ['crop management', 'soil science', 'irrigation', 'pest control', 'farm management', 'agricultural economics', 'sustainability', 'organic farming', 'precision agriculture'],
            'APPAREL': ['fashion design', 'textile knowledge', 'pattern making', 'sewing', 'merchandising', 'retail management', 'brand development', 'trend analysis', 'supply chain'],
            'ARTS': ['graphic design', 'illustration', 'photography', 'art history', 'creative writing', 'performing arts', 'visual arts', 'art education', 'digital art'],
            'AUTOMOBILE': ['mechanical engineering', 'auto repair', 'diagnostics', 'electrical systems', 'engine tuning', 'transmission', 'brake systems', 'automotive technology', 'cad'],
            'AVIATION': ['piloting', 'aircraft maintenance', 'air traffic control', 'aviation safety', 'flight planning', 'navigation', 'aerodynamics', 'regulatory compliance', 'airport operations'],
            'BANKING': ['financial services', 'credit analysis', 'risk management', 'investment banking', 'loan processing', 'customer service', 'compliance', 'fraud detection', 'treasury'],
            'BPO': ['customer support', 'data entry', 'call center operations', 'process improvement', 'quality assurance', 'telemarketing', 'outsourcing', 'client management', 'crm'],
            'BUSINESS-DEVELOPMENT': ['sales', 'market research', 'strategic planning', 'lead generation', 'client acquisition', 'partnership development', 'negotiation', 'crm', 'business intelligence'],
            'CHEF': ['culinary arts', 'menu planning', 'food safety', 'kitchen management', 'recipe development', 'catering', 'baking', 'pastry', 'cost control'],
            'CONSTRUCTION': ['project management', 'blueprint reading', 'safety regulations', 'heavy machinery operation', 'carpentry', 'plumbing', 'electrical work', 'masonry', 'estimating'],
            'CONSULTANT': ['strategic consulting', 'problem-solving', 'data analysis', 'client relations', 'project management', 'industry expertise', 'report writing', 'presentation skills', 'change management'],
            'DESIGNER': ['graphic design', 'ui/ux design', 'web design', 'branding', 'typography', 'adobe creative suite', 'prototyping', 'user research', 'wireframing'],
            'DIGITAL-MEDIA': ['social media management', 'content creation', 'seo', 'sem', 'video editing', 'photography', 'copywriting', 'analytics', 'influencer marketing'],
            'ENGINEERING': ['mechanical engineering', 'electrical engineering', 'civil engineering', 'software engineering', 'cad', 'matlab', 'project management', 'quality control', 'lean manufacturing'],
            'FINANCE': ['financial modeling', 'investment analysis', 'portfolio management', 'risk assessment', 'financial reporting', 'budgeting', 'forecasting', 'bloomberg', 'derivatives'],
            'FITNESS': ['personal training', 'group fitness instruction', 'nutrition', 'exercise physiology', 'client assessment', 'program design', 'motivation', 'safety', 'rehabilitation'],
            'HEALTHCARE': ['patient care', 'medical terminology', 'emr', 'clinical skills', 'nursing', 'pharmacy', 'radiology', 'surgery', 'infection control'],
            'HR': ['recruitment', 'employee relations', 'performance management', 'training', 'compensation', 'benefits', 'labor laws', 'hris', 'talent acquisition'],
            'INFORMATION-TECHNOLOGY': ['programming', 'network administration', 'cybersecurity', 'database management', 'cloud computing', 'it support', 'software development', 'systems analysis', 'devops'],
            'LEGAL': ['legal research', 'contract law', 'litigation', 'negotiation', 'compliance', 'case management', 'legal writing', 'client counseling', 'regulatory affairs'],
            'MARKETING': ['digital marketing', 'content marketing', 'social media marketing', 'seo', 'sem', 'ppc', 'google analytics', 'brand management', 'market research', 'campaign management', 'copywriting', 'a/b testing', 'conversion optimization'],
            'MEDICAL': ['patient care', 'medical terminology', 'clinical skills', 'diagnosis', 'treatment planning', 'emergency care', 'pharmacology', 'healthcare regulations', 'medical records'],
            'NGO': ['project management', 'fundraising', 'community outreach', 'grant writing', 'advocacy', 'program evaluation', 'stakeholder engagement', 'volunteer management', 'impact measurement'],
            'PHARMACEUTICAL': ['drug development', 'clinical trials', 'regulatory affairs', 'pharmacology', 'quality assurance', 'sales', 'marketing', 'research and development', 'gmp'],
            'RESEARCH': ['data analysis', 'statistical methods', 'literature review', 'experimental design', 'report writing', 'research methodologies', 'fieldwork', 'academic publishing', 'peer review'],
            'RETAIL': ['customer service', 'inventory management', 'sales', 'merchandising', 'visual display', 'point of sale systems', 'product knowledge', 'store operations', 'loss prevention'],
            'PUBLIC-RELATIONS': ['media relations', 'press releases', 'event planning', 'crisis management', 'social media', 'content creation', 'brand management', 'stakeholder engagement', 'reputation management'],
            'SALES': ['lead generation', 'customer relationship management', 'sales strategy', 'negotiation', 'product knowledge', 'closing deals', 'market analysis', 'cold calling', 'account management'],
            'TEACHER': ['curriculum development', 'classroom management', 'lesson planning', 'student assessment', 'educational technology', 'special education', 'counseling', 'pedagogy', 'differentiated instruction'],
            'TECHNICAL-SUPPORT': ['troubleshooting', 'customer service', 'hardware support', 'software installation', 'network troubleshooting', 'remote support', 'ticketing systems', 'technical documentation', 'escalation management'],
            'TOURISM': ['customer service', 'itinerary planning', 'travel booking', 'cultural knowledge', 'event management', 'tour guiding', 'hospitality', 'sustainability', 'destination marketing'],
            'TRANSPORTATION': ['logistics', 'supply chain management', 'fleet management', 'route planning', 'safety regulations', 'customer service', 'inventory management', 'transportation planning', 'warehouse management'],
            'SOFT-SKILLS': ['communication', 'teamwork', 'problem-solving', 'time management', 'adaptability', 'creativity', 'work ethic', 'interpersonal skills', 'leadership', 'attention to detail', 'critical thinking']
        }

    def analyze_job_description(self, job_description: str) -> JobAnalysis:
        """Analyze job description and extract key requirements"""
        try:
            skills = self.extract_dynamic_skills(job_description)
            experience = self.extract_experience_years(job_description)
            education = self.extract_education(job_description)
            sector = self._detect_sector(job_description)
            requirements = self._extract_key_requirements(job_description)
            complexity = self._calculate_complexity_score(skills, experience, education)
            
            return JobAnalysis(
                skills_required=skills,
                experience_required=experience,
                education_required=education,
                sector_detected=sector,
                key_requirements=requirements,
                complexity_score=complexity
            )
        except Exception as e:
            logger.error(f"Error analyzing job description: {e}")
            raise

    def _detect_sector(self, text: str) -> str:
        """Detect the most likely sector from job description"""
        text_lower = text.lower()
        sector_scores = {}
        
        for sector, skills in self.universal_skills.items():
            if sector == 'SOFT-SKILLS':
                continue
            score = sum(1 for skill in skills if skill in text_lower)
            if score > 0:
                sector_scores[sector] = score
        
        return max(sector_scores.items(), key=lambda x: x[1])[0] if sector_scores else 'GENERAL'

    def _extract_key_requirements(self, text: str) -> List[str]:
        """Extract key requirements from job description"""
        requirements = []
        
        # Look for requirement patterns
        requirement_patterns = [
            r'(?:required|must have|essential).*?(?:\n|\.)',
            r'(?:minimum|at least).*?(?:\n|\.)',
            r'(?:preferred|desired).*?(?:\n|\.)'
        ]
        
        for pattern in requirement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            requirements.extend([match.strip() for match in matches])
        
        return requirements[:10]  # Limit to top 10

    def _calculate_complexity_score(self, skills: Dict, experience: int, education: int) -> float:
        """Calculate job complexity score"""
        skill_count = sum(len(skill_list) for skill_list in skills.values())
        complexity = (skill_count * 0.4 + experience * 0.4 + education * 0.2) / 20
        return min(complexity, 1.0)

    def extract_text_from_pdf(self, pdf_path: Path) -> Tuple[str, Dict]:
        """Extract text from PDF file with metadata"""
        try:
            start_time = datetime.now()
            text = ""
            metadata = {}
            
            with fitz.open(pdf_path) as doc:
                metadata['page_count'] = len(doc)
                metadata['file_size'] = pdf_path.stat().st_size
                
                for page in doc:
                    text += page.get_text()
            
            processing_time = (datetime.now() - start_time).total_seconds()
            metadata['processing_time'] = processing_time
            
            logger.debug(f"Extracted text from {pdf_path.name} in {processing_time:.2f}s")
            return text.strip(), metadata
            
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return "", {}

    def clean_text(self, text: str) -> str:
        """Clean and preprocess text with enhanced cleaning"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        # Keep alphanumeric, spaces, and common punctuation
        text = re.sub(r'[^\w\s\-\.\,\(\)\@\#\%\&\+]', '', text)
        # Remove email addresses for privacy
        text = re.sub(r'\S+@\S+', '', text)
        # Remove phone numbers
        text = re.sub(r'[\+]?[1-9]?[0-9]{7,15}', '', text)
        
        return text.lower().strip()

    def extract_dynamic_skills(self, text: str, reference_skills: Optional[Dict] = None) -> Dict[str, List[str]]:
        """Extract skills dynamically with improved matching"""
        if not text:
            return {}
        
        text_lower = text.lower()
        found_skills = {}
        skills_to_search = reference_skills or self.universal_skills
        
        for category, skills in skills_to_search.items():
            category_skills = []
            for skill in skills:
                # Exact match or word boundary match
                if skill in text_lower or re.search(rf'\b{re.escape(skill)}\b', text_lower):
                    category_skills.append(skill)
            
            if category_skills:
                found_skills[category] = category_skills
        
        return found_skills

    def extract_experience_years(self, text: str) -> int:
        """Extract and sum years of experience from text with enhanced patterns"""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',  # "5 years of experience"
            r'(\d+)\+?\s*years?\s*in\s+',                         # "5 years in [field]"
            r'(?:experience|exp)(?:\s*of\s*|\s+)(\d+)\+?\s*years?', # "experience of 5 years"
            r'(\d+)\+?\s*yr[s]?\s*(?:of\s*)?(?:experience|exp)',  # "5 yrs of exp"
            r'(\d+)\+?\s*years?\s*(?:working|in\s+field)',        # "5 years working"
            r'\((\d+)\s*years?\)',                                # "(7 years)"
            r'(\d+)\s*years?',                                    # "7 years" standalone
            r'(\d{4})\s*[-–]\s*(?:present|current)',             # "2018-Present"
        ]
        
        years = []
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if pattern.endswith('present|current)'):  # Handle "2018-Present"
                    start_year = int(match)
                    current_year = 2025 #datetime.now().year  
                    years.append(current_year - start_year)
                else:
                    years.append(int(match))
        
        # Sum unique years, avoiding double-counting overlapping phrases
        if years:
            # Group by approximate value to avoid summing redundant matches
            year_counts = Counter(years)
            total_years = sum(year for year in set(years))
            return min(total_years, 50)  # Cap at 50 years to avoid outliers
        return 0

    def extract_education(self, text: str) -> int:
        """Extract education information with enhanced detection"""
        education_keywords = {
            'phd': ['phd', 'ph.d', 'doctorate', 'doctoral'],
            'masters': ['masters', 'master', 'mba', 'ms', 'ma', 'msc', 'mtech', 'meng'],
            'bachelors': ['bachelors', 'bachelor', 'bs', 'ba', 'bsc', 'btech', 'beng', 'degree'],
            'diploma': ['diploma', 'certificate', 'associate']
        }
        
        text_lower = text.lower()
        found_education = []
        
        for level, keywords in education_keywords.items():
            for keyword in keywords:
                if re.search(rf'\b{keyword}\b', text_lower):
                    found_education.append(level)
                    break
        
        education_scores = {'phd': 5, 'masters': 4, 'bachelors': 3, 'diploma': 2}
        return max(education_scores.get(edu, 1) for edu in found_education) if found_education else 1

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information (for display purposes only)"""
        contact_info = {}
        
        # Extract email (basic pattern for resume parsing)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]  # Take first email found
        
        # Extract phone (basic pattern)
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,15}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = phones[0]  # Take first phone found
        
        return contact_info

    def parse_resume(self, resume_text: str, filename: str, job_skills: Optional[Dict] = None, 
                    file_path: Optional[str] = None) -> Dict:
        """Parse resume and extract structured information"""
        try:
            cleaned_text = self.clean_text(resume_text)
            skills = self.extract_dynamic_skills(resume_text, job_skills)
            experience = self.extract_experience_years(resume_text)
            education = self.extract_education(resume_text)
            contact_info = self.extract_contact_info(resume_text)
            
            return {
                'filename': filename,
                'file_path': file_path,
                'text': cleaned_text,
                'raw_text': resume_text,  # Keep raw text for detailed analysis
                'skills': skills,
                'experience_years': experience,
                'education_score': education,
                'contact_info': contact_info,
                'word_count': len(resume_text.split()),
                'character_count': len(resume_text)
            }
        except Exception as e:
            logger.error(f"Error parsing resume {filename}: {e}")
            raise

    def calculate_text_similarity(self, job_description: str, resume_texts: List[str]) -> np.ndarray:
        """Calculate TF-IDF similarity with error handling"""
        if not resume_texts:
            return np.array([])
        
        all_texts = [job_description] + resume_texts
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            job_vector = tfidf_matrix[0:1]
            resume_vectors = tfidf_matrix[1:]
            similarities = cosine_similarity(job_vector, resume_vectors).flatten()
            return similarities
        except Exception as e:
            logger.error(f"Error calculating text similarity: {e}")
            return np.zeros(len(resume_texts))

    def calculate_advanced_skill_match(self, job_skills: Dict, resume_skills: Dict) -> Tuple[float, Dict]:
        """Calculate skill match score with detailed breakdown"""
        total_job_skills = sum(len(skills) for skills in job_skills.values())
        if total_job_skills == 0:
            return 0.0, {}
        
        skill_breakdown = {}
        matched_skills = 0
        
        for category, skills in job_skills.items():
            if category in resume_skills:
                matched = list(set(skills) & set(resume_skills[category]))
                skill_breakdown[category] = {
                    'required': len(skills),
                    'matched': len(matched),
                    'matched_skills': matched,
                    'missing_skills': list(set(skills) - set(resume_skills[category]))
                }
                matched_skills += len(matched)
            else:
                skill_breakdown[category] = {
                    'required': len(skills),
                    'matched': 0,
                    'matched_skills': [],
                    'missing_skills': skills
                }
        
        return matched_skills / total_job_skills, skill_breakdown

    def generate_recommendations(self, skill_breakdown: Dict, experience_gap: int, 
                               education_gap: int) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        # Skill recommendations
        missing_skills = []
        for category, breakdown in skill_breakdown.items():
            if breakdown['missing_skills']:
                missing_skills.extend(breakdown['missing_skills'][:3])  # Top 3 per category
        
        if missing_skills:
            recommendations.append(f"Consider developing skills in: {', '.join(missing_skills[:5])}")
        
        # Experience recommendations
        if experience_gap > 0:
            recommendations.append(f"Gain {experience_gap} more years of relevant experience")
        
        # Education recommendations
        if education_gap > 0:
            recommendations.append("Consider pursuing higher education qualifications")
        
        return recommendations

    def _calculate_adaptive_weights(self, job_skills: Dict, job_exp_years: int) -> Dict[str, float]:
        """Calculate adaptive weights based on job requirements"""
        weights = {
            'text': self.config['text_weight'],
            'skills': self.config['skill_weight'],
            'experience': self.config['experience_weight'],
            'education': self.config['education_weight']
        }
        
        total_skills = sum(len(skills) for skills in job_skills.values())
        
        # Adjust weights based on job complexity
        if total_skills > 15:  # Skill-heavy position
            weights['skills'] += 0.1
            weights['text'] -= 0.05
            weights['experience'] -= 0.05
        
        if job_exp_years > 7:  # Experience-heavy position
            weights['experience'] += 0.1
            weights['education'] -= 0.05
            weights['text'] -= 0.05
        
        # Normalize weights to sum to 1
        total_weight = sum(weights.values())
        weights = {k: v / total_weight for k, v in weights.items()}
        
        return weights

    def rank_resumes(self, job_description: str, resumes_data: List[ResumeData]) -> List[RankingResult]:
        """Rank resumes based on job description with enhanced analysis"""
        try:
            logger.info(f"Starting ranking process for {len(resumes_data)} resumes")
            
            # Analyze job description
            job_analysis = self.analyze_job_description(job_description)
            cleaned_job_desc = self.clean_text(job_description)
            
            # Process resumes
            processed_resumes = []
            for resume in resumes_data:
                try:
                    parsed = self.parse_resume(
                        resume.text, 
                        resume.filename, 
                        job_analysis.skills_required,
                        getattr(resume, 'file_path', None)
                    )
                    parsed['sector'] = resume.sector
                    processed_resumes.append(parsed)
                except Exception as e:
                    logger.error(f"Error processing resume {resume.filename}: {e}")
                    continue
            
            if not processed_resumes:
                logger.warning("No resumes were successfully processed")
                return []
            
            # Calculate similarities
            resume_texts = [resume['text'] for resume in processed_resumes]
            text_similarities = self.calculate_text_similarity(cleaned_job_desc, resume_texts)
            
            # Calculate adaptive weights
            weights = self._calculate_adaptive_weights(
                job_analysis.skills_required, 
                job_analysis.experience_required
            )
            
            results = []
            for i, resume in enumerate(processed_resumes):
                try:
                    # Calculate skill match with breakdown
                    skill_score, skill_breakdown = self.calculate_advanced_skill_match(
                        job_analysis.skills_required, 
                        resume['skills']
                    )
                    
                    # Calculate scores
                    text_similarity = text_similarities[i] if i < len(text_similarities) else 0.0
                    
                    # Experience score calculation
                    if job_analysis.experience_required > 0:
                        exp_ratio = resume['experience_years'] / job_analysis.experience_required
                        if exp_ratio <= 1:
                            exp_score = exp_ratio
                        else:
                            # Penalize over-qualification slightly
                            exp_score = 1.0 - min((exp_ratio - 1) * 0.1, 0.3)
                    else:
                        exp_score = min(resume['experience_years'] / 5, 1.0)
                    
                    # Education score
                    edu_score = min(resume['education_score'] / max(job_analysis.education_required, 3), 1.0)
                    
                    # Combined score
                    combined_score = (
                        weights['text'] * text_similarity +
                        weights['skills'] * skill_score +
                        weights['experience'] * exp_score +
                        weights['education'] * edu_score
                    )
                    
                    # Calculate match percentage
                    match_percentage = combined_score * 100
                    
                    # Generate recommendations
                    experience_gap = max(0, job_analysis.experience_required - resume['experience_years'])
                    education_gap = max(0, job_analysis.education_required - resume['education_score'])
                    recommendations = self.generate_recommendations(skill_breakdown, experience_gap, education_gap)
                    
                    result = RankingResult(
                        filename=resume['filename'],
                        sector=resume['sector'],
                        combined_score=combined_score,
                        text_similarity=text_similarity,
                        skill_score=skill_score,
                        experience_score=exp_score,
                        education_score=edu_score,
                        experience_years=resume['experience_years'],
                        education_level=resume['education_score'],
                        skills_found=resume['skills'],
                        match_percentage=match_percentage,
                        recommendations=recommendations,
                        file_path=resume.get('file_path')
                    )
                    
                    results.append(result)
                    
                except Exception as e:
                    logger.error(f"Error calculating scores for resume {resume['filename']}: {e}")
                    continue
            
            # Sort by combined score
            sorted_results = sorted(results, key=lambda x: x.combined_score, reverse=True)
            logger.info(f"Successfully ranked {len(sorted_results)} resumes")
            
            return sorted_results
            
        except Exception as e:
            logger.error(f"Error in ranking process: {e}")
            raise


    def process_resume_folder(self, folder_path: str)-> List[ResumeData]:
        resumes_data = []
        folder = Path(folder_path)

        for file_path in folder.glob("*.pdf"):
            try:
                text, metadata = self.extract_text_from_pdf(file_path)
                cleaned_text = self.clean_text(text)

                resume_data = ResumeData(
                    filename=file_path.name,
                    sector="General",  # or infer if you want
                    text=cleaned_text,
                    file_path=str(file_path),
                    file_size=os.path.getsize(file_path),
                    processing_time=None  # optional
                )

                resumes_data.append(resume_data)

            except Exception as e:
                self.logger.warning(f"Failed to process {file_path}: {e}")

        return resumes_data

    def get_summary_statistics(self, results: List[RankingResult]) -> Dict[str, Any]:
        """Get summary statistics for ranking results"""
        if not results:
            return {}
        
        scores = [r.combined_score for r in results]
        match_percentages = [r.match_percentage for r in results]
        
        return {
            'total_resumes': len(results),
            'average_score': np.mean(scores),
            'median_score': np.median(scores),
            'std_score': np.std(scores),
            'min_score': np.min(scores),
            'max_score': np.max(scores),
            'average_match_percentage': np.mean(match_percentages),
            'top_10_percent_threshold': np.percentile(scores, 90),
            'sectors_represented': len(set(r.sector for r in results)),
            'sector_distribution': dict(Counter(r.sector for r in results))
        }

    def export_results_json(self, results: List[RankingResult], job_analysis: JobAnalysis, 
                           summary_stats: Dict, filename: str = 'ranking_results.json') -> str:
        """Export results to JSON format for frontend consumption"""
        try:
            export_data = {
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_resumes': len(results),
                    'ranking_system_version': '2.0',
                    'processing_summary': summary_stats
                },
                'job_analysis': {
                    'sector_detected': job_analysis.sector_detected,
                    'experience_required': job_analysis.experience_required,
                    'education_required': job_analysis.education_required,
                    'complexity_score': job_analysis.complexity_score,
                    'key_requirements': job_analysis.key_requirements,
                    'skills_breakdown': {
                        category: len(skills) 
                        for category, skills in job_analysis.skills_required.items()
                    }
                },
                'rankings': [result.to_dict() for result in results],
                'summary_statistics': summary_stats
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error exporting results to JSON: {e}")
            raise

    def export_detailed_results(self, ranked_results: List[RankingResult], 
                              filename: str = 'detailed_resume_ranking.csv') -> str:
        """Export detailed results to CSV with enhanced information"""
        try:
            export_data = []
            for result in ranked_results:
                # Flatten skills for CSV export
                all_skills = []
                for category, skills in result.skills_found.items():
                    for skill in skills:
                        all_skills.append(f"{category}:{skill}")
                
                export_data.append({
                    'Rank': ranked_results.index(result) + 1,
                    'Filename': result.filename,
                    'Sector': result.sector,
                    'Overall_Score': round(result.combined_score, 4),
                    'Match_Percentage': round(result.match_percentage, 2),
                    'Text_Similarity': round(result.text_similarity, 4),
                    'Skill_Score': round(result.skill_score, 4),
                    'Experience_Score': round(result.experience_score, 4),
                    'Education_Score': round(result.education_score, 4),
                    'Experience_Years': result.experience_years,
                    'Education_Level': result.education_level,
                    'Skills_Count': len(all_skills),
                    'All_Skills': ' | '.join(all_skills),
                    'Recommendations': ' | '.join(result.recommendations),
                    'File_Path': result.file_path or ''
                })
            
            df = pd.DataFrame(export_data)
            df.to_csv(filename, index=False)
            logger.info(f"Detailed results exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error exporting detailed results: {e}")
            raise

    def get_top_candidates(self, results: List[RankingResult], top_n: int = 10) -> List[Dict]:
        """Get top N candidates in a format suitable for frontend display"""
        top_results = results[:top_n]
        candidates = []
        
        for i, result in enumerate(top_results, 1):
            # Get top skills across all categories
            all_skills = []
            for category, skills in result.skills_found.items():
                all_skills.extend(skills)
            
            candidate = {
                'rank': i,
                'filename': result.filename,
                'sector': result.sector,
                'match_percentage': round(result.match_percentage, 1),
                'overall_score': round(result.combined_score, 3),
                'experience_years': result.experience_years,
                'education_level': result.education_level,
                'top_skills': all_skills[:10],  # Top 10 skills
                'skill_categories': list(result.skills_found.keys()),
                'recommendations_count': len(result.recommendations),
                'strengths': self._identify_strengths(result),
                'file_path': result.file_path
            }
            candidates.append(candidate)
        
        return candidates

    def _identify_strengths(self, result: RankingResult) -> List[str]:
        """Identify candidate strengths based on scores"""
        strengths = []
        
        if result.skill_score > 0.7:
            strengths.append("Strong skill match")
        if result.experience_score > 0.8:
            strengths.append("Excellent experience level")
        if result.education_score > 0.8:
            strengths.append("Strong educational background")
        if result.text_similarity > 0.6:
            strengths.append("High content relevance")
        if result.match_percentage > 85:
            strengths.append("Exceptional overall match")
        
        return strengths

    def display_results(self, ranked_results: List[RankingResult], top_n: int = 10):
        """Display ranking results with enhanced formatting"""
        if not ranked_results:
            print("No results to display.")
            return
        
        display_count = min(top_n, len(ranked_results))
        
        print(f"\n{'='*100}")
        print(f"TOP {display_count} RANKED RESUMES")
        print(f"{'='*100}")
        
        for i, result in enumerate(ranked_results[:display_count], 1):
            print(f"\n{i}. {result.filename}")
            print(f"   Sector: {result.sector}")
            print(f"   Overall Match: {result.match_percentage:.1f}%")
            print(f"   Combined Score: {result.combined_score:.3f}")
            print(f"   Text Match: {result.text_similarity:.3f} | Skills: {result.skill_score:.3f} | "
                  f"Experience: {result.experience_score:.3f} | Education: {result.education_score:.3f}")
            print(f"   Experience: {result.experience_years} years | Education Level: {result.education_level}")
            
            # Display top skills
            all_skills = []
            for category, skills in result.skills_found.items():
                all_skills.extend([f"{category}:{skill}" for skill in skills[:2]])
            
            if all_skills:
                print(f"   Key Skills: {' | '.join(all_skills[:5])}")
            
            # Display strengths
            strengths = self._identify_strengths(result)
            if strengths:
                print(f"   Strengths: {', '.join(strengths)}")
            
            # Display top recommendations
            if result.recommendations:
                print(f"   Recommendations: {result.recommendations[0]}")

    def create_dashboard_data(self, results: List[RankingResult], job_analysis: JobAnalysis) -> Dict:
        """Create comprehensive dashboard data for frontend"""
        if not results:
            return {}
        
        summary_stats = self.get_summary_statistics(results)
        top_candidates = self.get_top_candidates(results, 10)
        
        # Score distribution for charts
        score_ranges = {
            '90-100%': len([r for r in results if r.match_percentage >= 90]),
            '80-89%': len([r for r in results if 80 <= r.match_percentage < 90]),
            '70-79%': len([r for r in results if 70 <= r.match_percentage < 80]),
            '60-69%': len([r for r in results if 60 <= r.match_percentage < 70]),
            'Below 60%': len([r for r in results if r.match_percentage < 60])
        }
        
        # Experience distribution
        exp_distribution = {}
        for result in results:
            exp_range = f"{(result.experience_years // 5) * 5}-{(result.experience_years // 5) * 5 + 4} years"
            exp_distribution[exp_range] = exp_distribution.get(exp_range, 0) + 1
        
        # Skill analysis
        skill_frequency = {}
        for result in results:
            for category, skills in result.skills_found.items():
                for skill in skills:
                    skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        top_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)[:15]
        
        dashboard_data = {
            'job_analysis': {
                'sector': job_analysis.sector_detected,
                'complexity_score': round(job_analysis.complexity_score, 2),
                'experience_required': job_analysis.experience_required,
                'education_required': job_analysis.education_required,
                'total_skills_required': sum(len(skills) for skills in job_analysis.skills_required.values())
            },
            'summary': summary_stats,
            'top_candidates': top_candidates,
            'distributions': {
                'match_score': score_ranges,
                'experience': exp_distribution,
                'sectors': summary_stats.get('sector_distribution', {})
            },
            'skill_analysis': {
                'most_common_skills': [{'skill': skill, 'frequency': freq} for skill, freq in top_skills],
                'skill_categories': list(set(
                    category for result in results 
                    for category in result.skills_found.keys()
                ))
            },
            'recommendations': {
                'total_candidates': len(results),
                'qualified_candidates': len([r for r in results if r.match_percentage >= 70]),
                'highly_qualified': len([r for r in results if r.match_percentage >= 85]),
                'avg_experience': round(np.mean([r.experience_years for r in results]), 1)
            }
        }
        
        return dashboard_data

class ResumeRankerAPI:
    """API wrapper for the resume ranker - ready for web integration"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.ranker = UniversalResumeRanker(config)
        self.logger = logging.getLogger(__name__)
    
    def analyze_job_and_rank(self, job_description: str, resume_folder: str, 
                           top_n: int = 10) -> Dict[str, Any]:
        """Main API method to analyze job and rank resumes"""
        try:
            # Load resumes
            resumes_data = self.ranker.process_resume_folder(resume_folder)
            if not resumes_data:
                return {'error': 'No resumes found or processed', 'success': False}
            
            # Analyze job description
            job_analysis = self.ranker.analyze_job_description(job_description)
            
            # Rank resumes
            results = self.ranker.rank_resumes(job_description, resumes_data)
            
            # Create dashboard data
            dashboard_data = self.ranker.create_dashboard_data(results, job_analysis)
            
            # Export results
            json_file = self.ranker.export_results_json(
                results, job_analysis, dashboard_data['summary']
            )
            csv_file = self.ranker.export_detailed_results(results)
            
            return {
                'success': True,
                'dashboard_data': dashboard_data,
                'top_candidates': self.ranker.get_top_candidates(results, top_n),
                'total_processed': len(resumes_data),
                'total_ranked': len(results),
                'exports': {
                    'json_file': json_file,
                    'csv_file': csv_file
                },
                'job_analysis': {
                    'sector_detected': job_analysis.sector_detected,
                    'complexity_score': job_analysis.complexity_score,
                    'skills_required': len(job_analysis.skills_required),
                    'experience_required': job_analysis.experience_required
                }
            }
            
        except Exception as e:
            self.logger.error(f"API Error: {e}")
            return {'error': str(e), 'success': False}
    
    def rank_single_resume(self, job_description: str, resume_text: str, 
                          filename: str = "single_resume.pdf") -> Dict[str, Any]:
        """Rank a single resume against job description"""
        try:
            # Create ResumeData object
            resume_data = ResumeData(
                filename=filename,
                sector="UNKNOWN",
                text=resume_text
            )
            
            # Analyze and rank
            job_analysis = self.ranker.analyze_job_description(job_description)
            results = self.ranker.rank_resumes(job_description, [resume_data])
            
            if not results:
                return {'error': 'Failed to process resume', 'success': False}
            
            result = results[0]
            
            return {
                'success': True,
                'match_percentage': result.match_percentage,
                'overall_score': result.combined_score,
                'breakdown': {
                    'text_similarity': result.text_similarity,
                    'skill_score': result.skill_score,
                    'experience_score': result.experience_score,
                    'education_score': result.education_score
                },
                'candidate_info': {
                    'experience_years': result.experience_years,
                    'education_level': result.education_level,
                    'skills_found': result.skills_found
                },
                'recommendations': result.recommendations,
                'strengths': self.ranker._identify_strengths(result)
            }
            
        except Exception as e:
            self.logger.error(f"Single resume ranking error: {e}")
            return {'error': str(e), 'success': False}

def main():
    """Enhanced main function with better error handling"""
    parser = argparse.ArgumentParser(description="Enhanced Resume Ranking System v2.0")
    parser.add_argument("job_file", help="Path to the job description text file")
    parser.add_argument("--data_path", default="../data/data/data", help="Path to the resumes folder")
    parser.add_argument("--top_n", type=int, default=10, help="Number of top results to display")
    parser.add_argument("--export_json", action="store_true", help="Export results to JSON")
    parser.add_argument("--config", help="Path to configuration JSON file")
    args = parser.parse_args()
    
    try:
        # Load configuration if provided
        config = None
        if args.config:
            with open(args.config, 'r') as f:
                config = json.load(f)
        
        # Read job description
        try:
            with open(args.job_file, 'r', encoding='utf-8') as f:
                job_description = f.read().strip()
        except FileNotFoundError:
            logger.error(f"Job description file '{args.job_file}' not found.")
            return
        except Exception as e:
            logger.error(f"Error reading job description file: {e}")
            return
        
        if not job_description:
            logger.error("Job description file is empty.")
            return
        
        # Initialize API
        api = ResumeRankerAPI(config)
        
        # Process resumes and rank
        result = api.analyze_job_and_rank(job_description, args.data_path, args.top_n)
        
        if not result['success']:
            logger.error(f"Processing failed: {result.get('error', 'Unknown error')}")
            return
        
        # Display results
        print(f"\n{'='*100}")
        print(f"RESUME RANKING COMPLETED SUCCESSFULLY")
        print(f"{'='*100}")
        print(f"Total Resumes Processed: {result['total_processed']}")
        print(f"Total Resumes Ranked: {result['total_ranked']}")
        print(f"Job Sector Detected: {result['job_analysis']['sector_detected']}")
        print(f"Job Complexity Score: {result['job_analysis']['complexity_score']:.2f}")
        
        # Show top candidates
        print(f"\nTOP {len(result['top_candidates'])} CANDIDATES:")
        for candidate in result['top_candidates']:
            print(f"{candidate['rank']}. {candidate['filename']} - {candidate['match_percentage']:.1f}% match")
        
        print(f"\nFiles exported:")
        print(f"- JSON: {result['exports']['json_file']}")
        print(f"- CSV: {result['exports']['csv_file']}")
        
        logger.info("Resume ranking completed successfully")
        
    except Exception as e:
        logger.error(f"Main execution error: {e}")
        raise

if __name__ == "__main__":
    main()