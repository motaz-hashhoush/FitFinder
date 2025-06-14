export interface Resume {
  id: number;
  filename: string;
  originalFilename: string;
  filePath: string;
  extractedText: string;
  skills: string[];
  experienceYears: number;
  educationLevel: string;
  sector: string;
  uploadedAt: string;
  updatedAt: string;
}

export interface CandidateScore {
  id: number;
  name: string;
  filename: string;
  matchPercentage: number;
  skills: string[];
  experienceYears: number;
  educationLevel: string;
  sector: string;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  score: {
    skillsMatch: number;
    experienceMatch: number;
    educationMatch: number;
    overall: number;
  };
}

export interface AnalysisResult {
  id: number;
  jobDescription: string;
  candidates: CandidateScore[];
  totalCandidates: number;
  averageScore: number;
  topSkills: string[];
  analysisDate: string;
  processingTime: number;
}

export interface JobDescription {
  title: string;
  company: string;
  description: string;
  requirements: string[];
  preferredSkills: string[];
  experienceLevel: string;
  educationRequirement: string;
  sector: string;
} 