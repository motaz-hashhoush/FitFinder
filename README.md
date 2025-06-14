# FitFinder - AI-Powered Resume Ranking System

🚀 An intelligent resume ranking and analysis system that helps HR professionals efficiently evaluate and rank candidates using machine learning and natural language processing.

## ✨ Features

- **Smart Resume Analysis**: Upload PDF resumes and get AI-powered insights
- **Job Description Matching**: Analyze job requirements and match with candidate profiles
- **Intelligent Ranking**: Rank candidates based on skills, experience, and job fit
- **Interactive Dashboard**: Modern, responsive web interface built with React + TypeScript
- **Export Capabilities**: Download results in JSON or CSV format
- **Real-time Processing**: Fast resume analysis with immediate feedback

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development
- **Tailwind CSS** for modern styling
- **Tanstack Query** for data fetching
- **React Router** for navigation
- **Lucide React** for icons

### Backend
- **Python Flask** REST API
- **PyMuPDF (fitz)** for PDF processing
- **spaCy** for NLP and text analysis
- **scikit-learn** for machine learning
- **pandas** for data manipulation
- **Flask-CORS** for cross-origin requests

## 🎨 Design

Beautiful, professional UI with a cohesive color scheme:
- **Primary**: #3674B5 (Professional Blue)
- **Secondary**: #578FCA (Medium Blue)
- **Accent**: #F5F0CD (Light Cream)
- **Highlight**: #FADA7A (Golden Yellow)

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/motaz-hashhoush/FitFinder.git
   cd FitFinder
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Set up the frontend**
   ```bash
   cd my-app
   npm install
   ```

4. **Start the application**
   ```bash
   # From project root
   start_servers.bat  # Windows
   
   # Or manually:
   # Terminal 1 - Backend
   cd backend && python flask_server.py
   
   # Terminal 2 - Frontend
   cd my-app && npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## 📁 Project Structure

```
FitFinder/
├── backend/                 # Python Flask API
│   ├── venv/               # Virtual environment
│   ├── uploads/            # Resume upload directory
│   ├── flask_server.py     # Main Flask application
│   ├── enhanced_resume_ranker_connect.py  # ML ranking logic
│   ├── requirements.txt    # Python dependencies
│   └── run_server.bat     # Server startup script
├── my-app/                 # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   ├── lib/           # API client and utilities
│   │   └── hooks/         # Custom React hooks
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
└── start_servers.bat      # Full application launcher
```

## 🔧 API Endpoints

- `GET /api/health` - Health check
- `POST /api/upload-resume` - Upload resume files
- `POST /api/analyze-job` - Analyze job and rank resumes
- `POST /api/rank-single-resume` - Rank individual resume
- `GET /api/download/<file_type>` - Download results (JSON/CSV)

## 🤖 Machine Learning Features

- **Skills Extraction**: Identify technical and soft skills from resumes
- **Experience Analysis**: Calculate years of experience and education level
- **Sector Detection**: Automatically detect industry/sector from job descriptions
- **Similarity Scoring**: Advanced text similarity using NLP techniques
- **Ranking Algorithm**: Multi-factor scoring system for candidate ranking

## 📊 Sample Data

The system includes sample resumes for testing:
- Software Developer profile
- Digital Marketing Specialist profile

## 🧪 Testing

```bash
# Test backend functionality
cd backend && python test_backend.py
cd backend && python test_download.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Developer

**Motaz Hashhoush**
- GitHub: [@motaz-hashhoush](https://github.com/motaz-hashhoush)

## 🎯 Future Enhancements

- [ ] Advanced filtering and search capabilities
- [ ] Integration with job boards and ATS systems
- [ ] Multi-language resume support
- [ ] Automated interview scheduling
- [ ] Candidate recommendation engine
- [ ] Analytics and reporting dashboard

---

⭐ **Star this repo if you find it helpful!**

Built with ❤️ for efficient HR processes and better candidate matching.
