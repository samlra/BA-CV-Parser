# CV Analysis Tool for Energy Industry

This is an AI-powered CV analysis tool specifically designed for the energy industry. It evaluates candidate CVs against job requirements and provides detailed matching scores and insights.

## Key Features

- **Automated CV Analysis**: Upload PDF CVs and get instant analysis against job requirements
- **Language Proficiency Check**: Ensures candidates have at least C1 level German language skills
- **Detailed Matching**: Provides percentage match for each job requirement
- **Seniority Level Assessment**: Automatically determines candidate seniority level based on experience
- **Beautiful UI**: Modern, responsive interface with light/dark mode

## Technical Stack

### Backend

- FastAPI (Python)
- OpenAI GPT-3.5 via OpenRouter API
- spaCy for NLP processing
- PyPDF2 for PDF text extraction

### Frontend

- React
- Material-UI
- Axios for API communication

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Clone the repository

   ```
   git clone https://github.com/samlra/BA-CV-Parser.git
   cd BA-CV-Parser
   ```

2. Create and activate a virtual environment

   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies

   ```
   pip install -r requirements.txt
   ```

4. Install the German language model for spaCy

   ```
   python -m spacy download de_core_news_sm
   ```

5. Create a `.env` file with your OpenRouter API key

   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

6. Start the backend server
   ```
   python -m uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory

   ```
   cd frontend
   ```

2. Install dependencies

   ```
   npm install
   # or
   yarn install
   ```

3. Start the development server

   ```
   npm start
   # or
   yarn start
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Usage

1. Select the job role (SAP Developer or SAP Consultant)
2. Upload a candidate's CV in PDF format
3. Review the job requirements or customize them as needed
4. Click "Analyze" to process the CV
5. Review the detailed analysis results:
   - Overall match percentage
   - Seniority level assessment
   - Detailed requirement matches
   - Key strengths and improvement areas

## Business Rules

- Candidates with German language skills below C1 level automatically receive a 0% match
- Experience levels are classified as:
  - Junior: 0-3 years of experience
  - Professional: 3-5 years of experience
  - Senior: 5-8 years of experience
  - Principal: 8+ years of experience

## License

This project is proprietary and confidential.

## Contact

For questions or support, please contact [your-email@example.com].
