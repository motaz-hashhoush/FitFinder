import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download, Users, Star, Clock, FileText, CheckCircle, AlertCircle } from "lucide-react";
import { AnalysisResponse, resumeApi } from "@/lib/api";

interface AnalysisResultsProps {
  results: AnalysisResponse | null;
  isLoading: boolean;
}

// Candidate Card Component
function CandidateCard({ candidate, rank }: { candidate: any; rank: number }) {
  const getScoreColor = (percentage: number) => {
    if (percentage >= 85) return 'text-green-700 bg-green-100 border-green-300';
    if (percentage >= 70) return 'text-brand-darkBlue bg-brand-lightCream border-brand-mediumBlue/30';
    if (percentage >= 60) return 'text-brand-darkBlue bg-brand-golden/20 border-brand-golden/40';
    return 'text-red-700 bg-red-100 border-red-300';
  };

  const getScoreBadgeColor = (percentage: number) => {
    if (percentage >= 85) return 'bg-green-500';
    if (percentage >= 70) return 'bg-brand-mediumBlue';
    if (percentage >= 60) return 'bg-brand-golden';
    return 'bg-red-500';
  };

  const getRankColor = (rank: number) => {
    switch (rank) {
      case 1: return "bg-gradient-to-r from-brand-golden to-yellow-500 text-white shadow-lg";
      case 2: return "bg-gradient-to-r from-gray-400 to-gray-500 text-white shadow-lg";
      case 3: return "bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-lg";
      default: return "bg-gradient-to-r from-brand-darkBlue to-brand-mediumBlue text-white shadow-md";
    }
  };

  // Extract all skills from skills_found object
  const allSkills: string[] = candidate.skills_found ? 
    Object.values(candidate.skills_found).flat() as string[] : [];

  return (
    <Card className="hover:shadow-xl transition-all duration-200 border-0 bg-white rounded-xl">
      <CardHeader className="pb-4 bg-gradient-to-r from-brand-lightCream to-brand-golden/20 rounded-t-xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm ${getRankColor(rank)}`}>
              #{rank}
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-brand-darkBlue">{candidate.filename}</CardTitle>
              <p className="text-sm text-brand-darkBlue/60 font-medium">{candidate.sector || 'Unknown Sector'}</p>
            </div>
          </div>
          <div className={`px-4 py-2 rounded-full text-sm font-medium border ${getScoreColor(candidate.match_percentage)}`}>
            {candidate.match_percentage?.toFixed(1) || 0}% Match
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-6">
        <div className="space-y-5">
          {/* Score Breakdown */}
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center bg-gradient-to-br from-brand-mediumBlue/10 to-brand-mediumBlue/20 p-4 rounded-lg border border-brand-mediumBlue/30">
              <div className="text-2xl font-bold text-brand-darkBlue">{candidate.experience_years || 0}</div>
              <div className="text-xs text-brand-darkBlue/70 font-medium">Years Experience</div>
            </div>
            <div className="text-center bg-gradient-to-br from-brand-golden/20 to-brand-golden/40 p-4 rounded-lg border border-brand-golden/50">
              <div className="text-2xl font-bold text-brand-darkBlue">{candidate.education_level || 0}</div>
              <div className="text-xs text-brand-darkBlue/70 font-medium">Education Level</div>
            </div>
          </div>

          {/* Skills */}
          {allSkills.length > 0 && (
            <div>
              <div className="text-sm font-semibold text-brand-darkBlue mb-3">Key Skills</div>
              <div className="flex flex-wrap gap-2">
                {allSkills.slice(0, 6).map((skill: string, index: number) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-brand-mediumBlue/10 text-brand-mediumBlue rounded-full text-xs font-medium border border-brand-mediumBlue/30"
                  >
                    {skill}
                  </span>
                ))}
                {allSkills.length > 6 && (
                  <span className="px-3 py-1 bg-brand-lightCream text-brand-darkBlue/60 rounded-full text-xs font-medium border border-brand-golden/30">
                    +{allSkills.length - 6} more
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Recommendations */}
          {candidate.recommendations && candidate.recommendations.length > 0 && (
            <div>
              <div className="text-sm font-semibold text-brand-darkBlue mb-3">Recommendations</div>
              <div className="space-y-2">
                {candidate.recommendations.slice(0, 2).map((rec: string, index: number) => (
                  <div key={index} className="text-xs text-brand-darkBlue/70 flex items-start bg-brand-lightCream/50 p-2 rounded-lg border border-brand-golden/30">
                    <CheckCircle className="w-3 h-3 mr-2 mt-0.5 text-brand-mediumBlue flex-shrink-0" />
                    {rec}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Progress Bar */}
          <div>
            <div className="flex justify-between text-sm text-brand-darkBlue/80 mb-2 font-medium">
              <span>Overall Match</span>
              <span>{candidate.match_percentage?.toFixed(1) || 0}%</span>
            </div>
            <div className="w-full bg-brand-lightCream rounded-full h-3 shadow-inner border border-brand-golden/20">
              <div
                className={`h-3 rounded-full transition-all duration-500 ${getScoreBadgeColor(candidate.match_percentage || 0)} shadow-sm`}
                style={{ width: `${candidate.match_percentage || 0}%` }}
              ></div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function AnalysisResults({ results, isLoading }: AnalysisResultsProps) {
  const handleDownload = async (fileType: 'json' | 'csv') => {
    try {
      // Get the blob from the API
      const blob = await resumeApi.downloadResults(fileType);
      const url = window.URL.createObjectURL(blob);
      
      // Create a temporary link element and trigger download
      const link = document.createElement('a');
      link.href = url;
      link.download = fileType === 'json' ? 'ranking_results.json' : 'detailed_resume_ranking.csv';
      document.body.appendChild(link);
      link.click();
      
      // Clean up
      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);
      
    } catch (error) {
      console.error(`Download ${fileType} error:`, error);
      alert(`Failed to download ${fileType.toUpperCase()} file: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };
  if (isLoading) {
    return (
      <Card className="border-0 shadow-none bg-transparent">
        <CardHeader className="bg-gradient-to-r from-brand-darkBlue to-brand-mediumBlue text-white rounded-t-lg">
          <CardTitle className="flex items-center text-lg font-semibold">
            <Clock className="mr-2 h-5 w-5 animate-spin" />
            Analyzing Resumes...
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="space-y-4">
            <div className="animate-pulse">
              <div className="h-4 bg-brand-mediumBlue/20 rounded w-3/4 mb-2"></div>
              <div className="h-4 bg-brand-mediumBlue/20 rounded w-1/2"></div>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!results) {
    return (
      <Card className="border-0 shadow-none bg-transparent">
        <CardHeader className="bg-gradient-to-r from-brand-darkBlue to-brand-mediumBlue text-white rounded-t-lg">
          <CardTitle className="flex items-center text-lg font-semibold">
            <FileText className="mr-2 h-5 w-5" />
            Resume Analysis Results
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="text-center py-8">
            <FileText className="mx-auto h-12 w-12 text-brand-darkBlue/30 mb-4" />
            <p className="text-brand-darkBlue/70">No analysis results yet. Add a job description and click 'Analyze Resumes' to get started.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!results.success) {
    return (
      <Card className="border-0 shadow-none bg-transparent">
        <CardHeader className="bg-gradient-to-r from-red-500 to-red-600 text-white rounded-t-lg">
          <CardTitle className="flex items-center text-lg font-semibold">
            <AlertCircle className="mr-2 h-5 w-5" />
            Analysis Failed
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <p className="text-red-600 bg-red-50 p-4 rounded-lg border border-red-200">{results.error}</p>
        </CardContent>
      </Card>
    );
  }

  const candidates = results.top_candidates || [];
  const jobAnalysis = results.job_analysis;

  return (
    <div className="space-y-6">
      {/* Summary Statistics */}
      <Card className="border-0 shadow-none bg-transparent">
        <CardHeader className="bg-gradient-to-r from-brand-darkBlue to-brand-mediumBlue text-white rounded-t-lg">
          <CardTitle className="flex items-center text-lg font-semibold">
            <Star className="mr-2 h-5 w-5" />
            Analysis Summary
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center bg-gradient-to-br from-brand-lightCream to-brand-golden/30 p-4 rounded-lg border border-brand-mediumBlue/20">
              <div className="text-2xl font-bold text-brand-darkBlue">{results.total_processed || 0}</div>
              <div className="text-sm text-brand-darkBlue/70 font-medium">Resumes Processed</div>
            </div>
            <div className="text-center bg-gradient-to-br from-brand-golden/20 to-brand-golden/40 p-4 rounded-lg border border-brand-golden/30">
              <div className="text-2xl font-bold text-brand-darkBlue">{results.total_ranked || 0}</div>
              <div className="text-sm text-brand-darkBlue/70 font-medium">Resumes Ranked</div>
            </div>
            <div className="text-center bg-gradient-to-br from-brand-mediumBlue/10 to-brand-mediumBlue/20 p-4 rounded-lg border border-brand-mediumBlue/30">
              <div className="text-xl font-bold text-brand-darkBlue">{jobAnalysis?.sector_detected || 'N/A'}</div>
              <div className="text-sm text-brand-darkBlue/70 font-medium">Detected Sector</div>
            </div>
            <div className="text-center bg-gradient-to-br from-brand-lightCream/60 to-brand-lightCream p-4 rounded-lg border border-brand-golden/20">
              <div className="text-2xl font-bold text-brand-darkBlue">{jobAnalysis?.complexity_score?.toFixed(1) || 'N/A'}</div>
              <div className="text-sm text-brand-darkBlue/70 font-medium">Complexity Score</div>
            </div>
          </div>
          
          <div className="mt-6 pt-4 border-t border-gray-200">
            <div className="flex space-x-3">
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleDownload('json')}
                className="border-brand-mediumBlue text-brand-mediumBlue hover:bg-brand-mediumBlue hover:text-white transition-all duration-200"
              >
                <Download className="mr-2 h-4 w-4" />
                Download JSON
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleDownload('csv')}
                className="border-brand-mediumBlue text-brand-mediumBlue hover:bg-brand-mediumBlue hover:text-white transition-all duration-200"
              >
                <Download className="mr-2 h-4 w-4" />
                Download CSV
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Top Candidates */}
      {candidates.length > 0 && (
        <Card className="border-0 shadow-none bg-transparent">
          <CardHeader className="bg-gradient-to-r from-brand-darkBlue to-brand-mediumBlue text-white rounded-t-lg">
            <CardTitle className="flex items-center text-lg font-semibold">
              <Users className="mr-2 h-5 w-5" />
              Top Candidates ({candidates.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="grid gap-6">
              {candidates.map((candidate, index) => (
                <CandidateCard
                  key={candidate.filename}
                  candidate={candidate}
                  rank={index + 1}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
} 