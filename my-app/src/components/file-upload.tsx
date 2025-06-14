import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { useMutation } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { CloudUpload, FileText, X } from "lucide-react";
import { resumeApi, ResumeUploadResponse } from "@/lib/api";

interface UploadedFile {
  filename: string;
  text: string;
  metadata: any;
}

export function FileUpload() {
  const { toast } = useToast();
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);

  // Upload mutation
  const uploadMutation = useMutation({
    mutationFn: async (files: File[]) => {
      const results: ResumeUploadResponse[] = [];
      
      for (const file of files) {
        try {
          const result = await resumeApi.uploadResume(file);
          results.push(result);
        } catch (error) {
          throw new Error(`Failed to upload ${file.name}: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }
      }
      
      return results;
    },
    onSuccess: (data) => {
      const newFiles = data.map(result => ({
        filename: result.filename,
        text: result.text,
        metadata: result.metadata,
      }));
      
      setUploadedFiles(prev => [...prev, ...newFiles]);
      
      toast({
        title: "Upload Successful",
        description: `${data.length} file(s) uploaded and processed successfully.`,
      });
    },
    onError: (error) => {
      toast({
        title: "Upload Failed",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  // Delete resume function
  const deleteFile = (filename: string) => {
    setUploadedFiles(prev => prev.filter(file => file.filename !== filename));
    toast({
      title: "File Removed",
      description: "File has been removed from the list.",
    });
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const pdfFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    
    if (pdfFiles.length !== acceptedFiles.length) {
      toast({
        title: "Invalid Files",
        description: "Only PDF files are allowed.",
        variant: "destructive",
      });
    }

    if (pdfFiles.length > 0) {
      uploadMutation.mutate(pdfFiles);
    }
  }, [uploadMutation, toast]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true,
  });

  return (
    <div className="space-y-4">
      {/* File Upload Zone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200 ${
          isDragActive
            ? "border-brand-mediumBlue bg-brand-mediumBlue/10 shadow-lg"
            : "border-gray-300 hover:border-brand-mediumBlue hover:bg-brand-mediumBlue/5"
        }`}
      >
        <input {...getInputProps()} />
        <CloudUpload className={`mx-auto h-12 w-12 mb-4 ${isDragActive ? 'text-brand-mediumBlue' : 'text-brand-darkBlue/40'}`} />
        <p className="text-lg font-semibold text-brand-darkBlue mb-2">
          {isDragActive ? "Drop the files here..." : "Drag & drop PDF files here"}
        </p>
        <p className="text-sm text-brand-darkBlue/60 mb-4 font-medium">or click to browse</p>
        <Button type="button" variant="outline" className="border-brand-mediumBlue text-brand-mediumBlue hover:bg-brand-mediumBlue hover:text-white transition-all duration-200">
          <FileText className="mr-2 h-4 w-4" />
          Browse Files
        </Button>
      </div>

      {/* Upload Progress */}
      {uploadMutation.isPending && (
        <div className="text-center py-4">
          <div className="inline-flex items-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-brand-mediumBlue mr-2"></div>
            <span className="text-sm text-brand-darkBlue/70 font-medium">Uploading and processing files...</span>
          </div>
        </div>
      )}

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-brand-darkBlue mb-3">
            Uploaded Files ({uploadedFiles.length})
          </h3>
          <div className="space-y-3">
            {uploadedFiles.map((file, index) => (
              <div
                key={`${file.filename}-${index}`}
                className="flex items-center justify-between p-4 bg-gradient-to-r from-brand-lightCream to-brand-golden/20 rounded-lg border border-brand-golden/30 hover:shadow-md transition-all duration-200"
              >
                <div className="flex items-center">
                  <FileText className="h-5 w-5 text-brand-mediumBlue mr-3" />
                  <span className="text-sm font-medium text-brand-darkBlue">
                    {file.filename}
                  </span>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => deleteFile(file.filename)}
                  className="text-red-500 hover:text-red-700 hover:bg-red-50 transition-all duration-200"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
