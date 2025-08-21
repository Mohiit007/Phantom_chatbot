# Phantom Finance - AI-Powered Personal Finance Planner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-brightgreen.svg)](https://nodejs.org/)

## 📌 Overview
Phantom Finance is an AI-assisted personal finance planner designed specifically for Indian users. It helps users plan their financial goals through natural language processing, providing inflation-adjusted savings plans and investment recommendations.

## 🚀 Features

### 💬 Natural Language Processing
- Set financial goals using simple English (e.g., "Plan my wedding in December 2026 for ₹8 lakhs")
- AI-powered goal interpretation and planning

### 📊 Financial Planning
- Inflation-adjusted cost calculations
- Monthly savings recommendations
- Investment portfolio tracking
- Expense categorization and analysis

### 📱 User Experience
- Intuitive dashboard with visual insights
- Responsive design for all devices
- Secure authentication system
- Real-time financial data integration

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Visualization**: Chart.js
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite (with SQLAlchemy ORM)
- **NLP**: spaCy + custom regex
- **Authentication**: JWT

### Integrations
- **Financial Data**: Yahoo Finance API (Nifty/Sensex)
- **Economic Data**: World Bank API (inflation rates)

### DevOps
- **Backend Hosting**: Railway
- **Frontend Hosting**: Vercel
- **CI/CD**: GitHub Actions
- **Containerization**: Docker

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- Git
- pip (Python package manager)
- npm or yarn (Node package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phantom-finance.git
   cd phantom-finance
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Update the .env file with your configuration
   ```

3. **Backend Setup**
   ```bash
   # Navigate to backend directory
   cd backend
   
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run database migrations (if any)
   alembic upgrade head
   
   # Start the backend server
   uvicorn main:app --reload
   ```

4. **Frontend Setup**
   ```bash
   # Navigate to frontend directory
   cd ../frontend
   
   # Install dependencies
   npm install
   
   # Start the development server
   npm run dev
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📂 Project Structure

```
phantom-finance/
├── backend/                 # FastAPI application
│   ├── app/                 # Main application package
│   │   ├── api/             # API routes
│   │   ├── core/            # Core functionality
│   │   ├── db/              # Database models and migrations
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utility functions
│   ├── tests/               # Backend tests
│   ├── alembic/             # Database migrations
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React application
│   ├── public/              # Static files
│   ├── src/                 # Source code
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── utils/           # Utility functions
│   └── package.json         # Frontend dependencies
│
├── scripts/                 # Utility scripts
│   ├── fetch_worldbank_inflation.py
│   └── fetch_yahoo_indices.py
│
├── docs/                    # Documentation
├── .github/                 # GitHub workflows and templates
├── .env.example             # Environment variables template
└── README.md                # This file
```

## 🤖 AI Disclosure
This project utilizes various AI tools to enhance development:
- **GitHub Copilot**: Used for code completion and generation
- **ChatGPT**: Assisted in generating documentation and code snippets
- **Other AI Tools**: [List any other AI tools used]

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing backend framework
- [React](https://reactjs.org/) for the frontend library
- [World Bank](https://data.worldbank.org/) for economic data
- [Yahoo Finance](https://finance.yahoo.com/) for financial market data

## 📬 Contact
For any queries or support, please contact [Your Name] at [your.email@example.com]


