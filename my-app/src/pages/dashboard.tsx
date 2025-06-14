import { useState } from "react";
import { FileUpload } from "@/components/file-upload";
import { AnalysisResults } from "@/components/analysis-results";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useMutation } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { Bell, WandSparkles, Rocket } from "lucide-react";
import { resumeApi, AnalysisResponse } from "@/lib/api";
import { Link } from "wouter";

export default function Dashboard() {
  const [jobDescription, setJobDescription] = useState("");
  const [analysisResults, setAnalysisResults] =
    useState<AnalysisResponse | null>(null);
  const { toast } = useToast();

  const analyzeMutation = useMutation({
    mutationFn: async () => {
      if (!jobDescription.trim()) {
        throw new Error("Job description is required");
      }

      const response = await resumeApi.analyzeJob({
        job_description: jobDescription.trim(),
        resume_folder: "uploads",
        top_n: 10,
      });

      if (!response.success) {
        throw new Error(response.error || "Analysis failed");
      }

      return response;
    },
    onSuccess: (data) => {
      setAnalysisResults(data);
      toast({
        title: "Analysis Complete",
        description: "Resumes have been successfully analyzed and ranked.",
      });
    },
    onError: (error) => {
      toast({
        title: "Analysis Failed",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleAnalyze = () => {
    analyzeMutation.mutate();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-blue-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link
              to="/"
              className="flex items-center space-x-2 hover:opacity-80 transition"
            >
              <div className="bg-blue-600 rounded-lg p-2">
                <Rocket className="h-6 w-6 text-white" />
              </div>
              <h1 className="text-xl font-bold text-blue-700">FitFinder</h1>
            </Link>

            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                className="text-blue-600 hover:text-blue-700 hover:bg-blue-100"
              >
                <Bell className="h-5 w-5" />
              </Button>
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-300 rounded-full flex items-center justify-center shadow">
                  <span className="text-blue-800 text-sm font-medium">HR</span>
                </div>
                <span className="text-sm font-medium text-blue-800">
                  HR Manager
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Upload Section */}
          <div className="lg:col-span-1">
            <Card className="shadow-xl border border-blue-100 bg-white/90 backdrop-blur">
              <CardHeader className="bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-t-lg">
                <CardTitle className="text-lg font-semibold">
                  Upload CVs & Job Description
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6 p-6">
                <div>
                  <label className="block text-sm font-medium text-blue-700 mb-2">
                    Job Description
                  </label>
                  <Textarea
                    placeholder="Paste the job description here..."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    className="h-32 resize-none border border-blue-200 focus:border-blue-500 focus:ring-blue-400"
                  />
                </div>

                <FileUpload />

                <Button
                  onClick={handleAnalyze}
                  disabled={analyzeMutation.isPending || !jobDescription.trim()}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 shadow-md transition-all"
                >
                  <WandSparkles className="mr-2 h-4 w-4" />
                  {analyzeMutation.isPending
                    ? "Analyzing..."
                    : "Analyze Resumes"}
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-2">
            <div className="bg-white/90 backdrop-blur rounded-lg shadow-xl border border-blue-100 p-4">
              <AnalysisResults
                results={analysisResults}
                isLoading={analyzeMutation.isPending}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
