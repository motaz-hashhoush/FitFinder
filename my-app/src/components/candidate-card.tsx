import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { ChevronDown, ChevronUp, Eye, UserPlus } from "lucide-react";
import type { CandidateScore } from "@shared/schema";

interface CandidateCardProps {
  candidate: CandidateScore;
  rank: number;
}

export function CandidateCard({ candidate, rank }: CandidateCardProps) {
  const [showDetails, setShowDetails] = useState(false);

  const getRankColor = (rank: number) => {
    switch (rank) {
      case 1:
        return "bg-green-100 text-green-600";
      case 2:
        return "bg-blue-100 text-blue-600";
      case 3:
        return "bg-amber-100 text-amber-600";
      default:
        return "bg-gray-100 text-gray-600";
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-blue-600";
    if (score >= 40) return "text-amber-600";
    return "text-red-600";
  };

  return (
    <Card className="overflow-hidden">
      <CardContent className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center">
            <div
              className={`flex items-center justify-center w-8 h-8 rounded-full font-semibold mr-3 ${getRankColor(
                rank
              )}`}
            >
              {rank}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                {candidate.name}
              </h3>
              <p className="text-sm text-gray-600">{candidate.title}</p>
            </div>
          </div>
          <div className="text-right">
            <div className={`text-2xl font-bold ${getScoreColor(candidate.overallScore)}`}>
              {candidate.overallScore}%
            </div>
            <div className="text-sm text-gray-500">Match Score</div>
          </div>
        </div>

        {/* Score Breakdown */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">Skills</span>
              <span className="font-medium">{candidate.skillsScore}%</span>
            </div>
            <Progress value={candidate.skillsScore} className="h-2" />
          </div>
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">Experience</span>
              <span className="font-medium">{candidate.experienceScore}%</span>
            </div>
            <Progress value={candidate.experienceScore} className="h-2" />
          </div>
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">Education</span>
              <span className="font-medium">{candidate.educationScore}%</span>
            </div>
            <Progress value={candidate.educationScore} className="h-2" />
          </div>
        </div>

        {/* Key Highlights */}
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Key Highlights</h4>
          <div className="flex flex-wrap gap-2">
            {candidate.highlights.map((highlight, index) => (
              <Badge key={index} variant="secondary" className="text-xs">
                {highlight}
              </Badge>
            ))}
          </div>
        </div>

        {/* Detailed Analysis (Collapsible) */}
        <div className="border-t pt-4">
          <Button
            variant="ghost"
            onClick={() => setShowDetails(!showDetails)}
            className="flex items-center justify-between w-full text-left p-0 h-auto hover:bg-transparent"
          >
            <span className="text-sm font-medium text-gray-700">Detailed Analysis</span>
            {showDetails ? (
              <ChevronUp className="h-4 w-4 text-gray-400" />
            ) : (
              <ChevronDown className="h-4 w-4 text-gray-400" />
            )}
          </Button>
          
          {showDetails && (
            <div className="mt-3 text-sm text-gray-600 space-y-2">
              <p>
                <strong>Strengths:</strong> {candidate.strengths}
              </p>
              <p>
                <strong>Areas for Growth:</strong> {candidate.areasForGrowth}
              </p>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-3 mt-4">
          <Button variant="outline" size="sm">
            <Eye className="mr-1 h-4 w-4" />
            View Resume
          </Button>
          <Button size="sm">
            <UserPlus className="mr-1 h-4 w-4" />
            Shortlist
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
