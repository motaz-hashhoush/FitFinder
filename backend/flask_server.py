from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from pathlib import Path
from enhanced_resume_ranker_connect import ResumeRankerAPI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://localhost:5174"])  # Enable CORS with credentials support

# Initialize the resume ranker API
ranker_api = ResumeRankerAPI()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Resume Ranker API is running"})

@app.route('/api/analyze-job', methods=['POST'])
def analyze_job():
    """Analyze job description and rank resumes"""
    try:
        data = request.get_json()
        
        if not data or 'job_description' not in data:
            return jsonify({"error": "job_description is required"}), 400
        
        job_description = data['job_description']
        resume_folder = data.get('resume_folder', 'uploads')  # Use uploads folder by default
        top_n = data.get('top_n', 10)
        
        # Check if resume folder exists
        if not os.path.exists(resume_folder):
            # Try to create uploads folder if it doesn't exist
            if resume_folder == 'uploads':
                os.makedirs(resume_folder, exist_ok=True)
                # If uploads folder is empty, return a helpful message
                if not os.listdir(resume_folder):
                    return jsonify({
                        "error": "No resume files found. Please upload some resumes first using the file upload feature.",
                        "success": False
                    }), 400
            else:
                return jsonify({"error": f"Resume folder '{resume_folder}' not found", "success": False}), 400
        
        # Analyze job and rank resumes
        result = ranker_api.analyze_job_and_rank(job_description, resume_folder, top_n)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_job: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"error": "Internal server error", "message": str(e), "success": False}), 500

@app.route('/api/rank-single-resume', methods=['POST'])
def rank_single_resume():
    """Rank a single resume against job description"""
    try:
        data = request.get_json()
        
        if not data or 'job_description' not in data or 'resume_text' not in data:
            return jsonify({"error": "job_description and resume_text are required"}), 400
        
        job_description = data['job_description']
        resume_text = data['resume_text']
        filename = data.get('filename', 'uploaded_resume.pdf')
        
        # Rank single resume
        result = ranker_api.rank_single_resume(job_description, resume_text, filename)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in rank_single_resume: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save the uploaded file
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        
        # Extract text from the uploaded file
        try:
            if file.filename.lower().endswith('.pdf'):
                text, metadata = ranker_api.ranker.extract_text_from_pdf(Path(file_path))
            else:
                # For text files
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                metadata = {}
            
            return jsonify({
                "success": True,
                "filename": file.filename,
                "text": text,
                "metadata": metadata
            })
            
        except Exception as e:
            return jsonify({"error": f"Failed to extract text from file: {str(e)}"}), 400
            
    except Exception as e:
        logger.error(f"Error in upload_resume: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/api/get-results/<filename>', methods=['GET'])
def get_results(filename):
    """Get exported results file"""
    try:
        file_path = os.path.join(os.getcwd(), filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if filename.endswith('.json'):
            return jsonify(json.loads(content))
        else:
            return content, 200, {'Content-Type': 'text/plain'}
            
    except Exception as e:
        logger.error(f"Error in get_results: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/api/download/<file_type>', methods=['GET'])
def download_results(file_type):
    """Download results as JSON or CSV"""
    try:
        if file_type == 'json':
            filename = 'ranking_results.json'
            mimetype = 'application/json'
        elif file_type == 'csv':
            filename = 'detailed_resume_ranking.csv'
            mimetype = 'text/csv'
        else:
            return jsonify({"error": "Invalid file type. Use 'json' or 'csv'"}), 400
        
        file_path = os.path.join(os.getcwd(), filename)
        if not os.path.exists(file_path):
            return jsonify({"error": f"File {filename} not found. Please run an analysis first."}), 404
        
        from flask import send_file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
            
    except Exception as e:
        logger.error(f"Error in download_results: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting Resume Ranker API Server...")
    print("API Endpoints:")
    print("- GET  /api/health - Health check")
    print("- POST /api/analyze-job - Analyze job and rank resumes")
    print("- POST /api/rank-single-resume - Rank single resume")
    print("- POST /api/upload-resume - Upload resume file")
    print("- GET  /api/get-results/<filename> - Get exported results")
    print("- GET  /api/download/<file_type> - Download JSON or CSV results")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 