from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import PyPDF2
import io
import spacy
import numpy as np
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

app = FastAPI()

# Load environment variables
load_dotenv()

# Initialize OpenRouter client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={"HTTP-Referer": "http://localhost:3000", "X-Title": "CV Parser"},
)

# Load the German language model
try:
    nlp = spacy.load("de_core_news_sm")
except OSError:
    raise RuntimeError(
        "The German language model is not installed. Please run: python -m spacy download de_core_news_sm"
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Requirement(BaseModel):
    text: str


# Seniority level criteria for consultant role
CONSULTANT_CRITERIA = {
    "process_modeling": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "sap_core": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Basic",
        "Principal": "Basic",
    },
    "ecc_systems": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "s4_systems": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "ecc_s4_processes": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Advanced",
    },
    "sap_technology": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Advanced",
    },
    "non_sap": {
        "Junior": "Basic",
        "Professional": "Advanced",
        "Senior": "Advanced",
        "Principal": "Advanced",
    },
    "modeling": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "process_management": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Advanced",
    },
    "requirements_engineering": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "project_management": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "energy_industry_general": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Advanced",
    },
    "energy_industry_network": {
        "Junior": "None",
        "Professional": "None",
        "Senior": "Basic",
        "Principal": "Basic",
    },
    "energy_industry_supply": {
        "Junior": "None",
        "Professional": "None",
        "Senior": "Basic",
        "Principal": "Basic",
    },
    "energy_industry_msb": {
        "Junior": "None",
        "Professional": "None",
        "Senior": "Basic",
        "Principal": "Advanced",
    },
    "language_skills": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
}

# Seniority level criteria for developer role
DEVELOPER_CRITERIA = {
    "process_modeling": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "sap_core": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Basic",
        "Principal": "Basic",
    },
    "ecc_systems": {
        "Junior": "None",
        "Professional": "None",
        "Senior": "None",
        "Principal": "Basic",
    },
    "s4_systems": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "ecc_s4_processes": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Basic",
        "Principal": "Basic",
    },
    "sap_technology": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "non_sap": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "modeling": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "process_management": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "requirements_engineering": {
        "Junior": "None",
        "Professional": "Advanced",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
    "energy_industry_general": {
        "Junior": "Basic",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Advanced",
    },
    "energy_industry_network": {
        "Junior": "None",
        "Professional": "None",
        "Senior": "Basic",
        "Principal": "Basic",
    },
    "energy_industry_supply": {
        "Junior": "None",
        "Professional": "None",
        "Senior": "Basic",
        "Principal": "Basic",
    },
    "energy_industry_msb": {
        "Junior": "None",
        "Professional": "None",
        "Senior": "Basic",
        "Principal": "Basic",
    },
    "language_skills": {
        "Junior": "None",
        "Professional": "Basic",
        "Senior": "Advanced",
        "Principal": "Expert",
    },
}

# Additional criteria for specific levels
LEVEL_SPECIFIC_REQUIREMENTS = {
    "Principal": {
        "required_expert": ["requirements_engineering"],
        "required_advanced": [
            "process_modeling",
            "ecc_systems",
            "s4_systems",
            "project_management",
            "energy_industry_general",
            "energy_industry_msb",
        ],
    },
    "Senior": {
        "required_advanced": [
            "process_modeling",
            "ecc_systems",
            "s4_systems",
            "sap_technology",
            "modeling",
            "process_management",
            "requirements_engineering",
        ],
        "required_basic": [
            "energy_industry_general",
            "energy_industry_network",
            "energy_industry_supply",
            "energy_industry_msb",
        ],
    },
    "Professional": {
        "required_basic": [
            "sap_core",
            "ecc_systems",
            "s4_systems",
            "process_management",
            "requirements_engineering",
            "project_management",
            "energy_industry_general",
        ]
    },
    "Junior": {"required_basic": ["ms_office", "process_modeling", "sap_technology"]},
}

# Additional criteria for specific developer levels
DEVELOPER_LEVEL_SPECIFIC_REQUIREMENTS = {
    "Principal": {
        "required_expert": [
            "process_modeling",
            "s4_systems",
            "sap_technology",
            "requirements_engineering",
            "non_sap",
        ],
        "required_advanced": [
            "project_management",
            "process_management",
            "energy_industry_general",
        ],
        "required_basic": [
            "ecc_systems",
            "energy_industry_network",
            "energy_industry_supply",
            "energy_industry_msb",
        ],
    },
    "Senior": {
        "required_advanced": [
            "process_modeling",
            "s4_systems",
            "sap_technology",
            "non_sap",
            "modeling",
            "process_management",
            "requirements_engineering",
        ],
        "required_basic": [
            "energy_industry_general",
            "energy_industry_network",
            "energy_industry_supply",
            "energy_industry_msb",
        ],
    },
    "Professional": {
        "required_advanced": [
            "ms_office",
            "requirements_engineering",
            "project_management",
        ],
        "required_basic": [
            "process_modeling",
            "sap_core",
            "s4_systems",
            "ecc_s4_processes",
            "sap_technology",
            "non_sap",
            "modeling",
            "process_management",
            "energy_industry_general",
        ],
    },
    "Junior": {
        "required_basic": ["ms_office", "sap_technology", "non_sap", "modeling"]
    },
}


def determine_skill_level(text: str) -> Dict[str, str]:
    """
    Determine the skill level for each category based on the CV text.
    Returns a dictionary with skill categories and their levels (None, Basic, Advanced, Expert).
    """
    skill_levels = {}
    text = text.lower()

    # Language Skills with enhanced recognition
    language_keywords = {
        "expert": ["muttersprachler", "native", "c2", "verhandlungssicher"],
        "advanced": ["deutsch c1", "fließend", "sehr gut", "business fluent"],
        "basic": ["gut", "b2", "b1", "a2", "a1"],
    }

    # Default language skills to None
    skill_levels["language_skills"] = "None"

    # Check for advanced and expert level keywords
    if any(kw in text for kw in language_keywords["advanced"]):
        skill_levels["language_skills"] = "Advanced"
    elif any(kw in text for kw in language_keywords["expert"]):
        skill_levels["language_skills"] = "Expert"

    # Ensure candidates with language skills 'None' or 'Basic' receive a 0% match
    if skill_levels["language_skills"] in ["None", "Basic"]:
        logging.debug(
            "Language skills below C1 detected. Setting to 'None' for 0% match."
        )
        skill_levels["language_skills"] = "None"
        # We'll continue with the skill assessment but will enforce 0% match in get_ai_analysis

    # Expert level indicators with stronger recognition
    expert_indicators = [
        "expert",
        "lead",
        "leitung",
        "führung",
        "architect",
        "principal",
        "senior",
        "mehrjährige erfahrung",
        "langjährige erfahrung",
        "umfangreiche erfahrung",
        "extensive experience",
        "projektleiter",
        "teamleiter",
        "chief",
        "head of",
        "leiter",
        "manager",
        "berater",
        "solution architect",
        "enterprise architect",
        "technical lead",
        "fachexperte",
        "specialist",
        "spezialist",
        "strategisch",
    ]

    expert_matches = sum(1 for indicator in expert_indicators if indicator in text)
    is_expert_level = expert_matches >= 3

    # Similar company experience assessment with stronger weighting
    similar_companies = [
        "convista",
        "koenig.solutions",
        "incept4",
        "cronos",
        "intense ag",
        "hochfrequenz",
        "dsc unternehmensberatung",
        "power reply",
        "nea gruppe",
        "cerebricks",
        "energy4u",
        "nexus nova",
        "demando",
        "adesso orange",
    ]

    company_matches = sum(1 for company in similar_companies if company in text)
    if company_matches > 1:
        skill_levels["similar_company_experience"] = "Expert"
    elif company_matches > 0:
        skill_levels["similar_company_experience"] = "Advanced"
    else:
        skill_levels["similar_company_experience"] = "Basic"

    # Location assessment
    location_keywords = {
        "mannheim": ["mannheim", "ludwigshafen", "heidelberg"],
        "rhein_neckar": ["rhein-neckar", "rhein neckar", "metropolregion"],
        "frankfurt": ["frankfurt", "main-taunus", "rhein-main"],
        "nrw": ["düsseldorf", "wuppertal", "nrw", "nordrhein-westfalen"],
        "thueringen": ["thüringen", "erfurt", "jena", "gera"],
    }

    location_matches = sum(
        1
        for region in location_keywords.values()
        for keyword in region
        if keyword in text
    )

    if location_matches > 0:
        skill_levels["location"] = "Advanced"
    else:
        skill_levels["location"] = "Basic"

    # Education with enhanced recognition
    education_keywords = {
        "expert": ["promotion", "doktor", "dr.", "phd", "master", "diplom"],
        "advanced": ["hochschulabschluss", "universität", "studium", "bachelor"],
        "basic": ["ausbildung", "berufsausbildung", "fachhochschule"],
    }

    if any(kw in text for kw in education_keywords["expert"]):
        skill_levels["education"] = "Expert"
    elif any(kw in text for kw in education_keywords["advanced"]):
        skill_levels["education"] = "Advanced"
    elif any(kw in text for kw in education_keywords["basic"]):
        skill_levels["education"] = "Basic"

    # Soft Skills with enhanced recognition
    soft_skills_keywords = {
        "expert": [
            "führungserfahrung",
            "personalverantwortung",
            "teamleitung",
            "mentoring",
        ],
        "advanced": ["projektleitung", "kundenberatung", "verhandlung", "präsentation"],
        "basic": ["teamfähigkeit", "engagement", "kundenorientierung"],
    }

    if any(kw in text for kw in soft_skills_keywords["expert"]):
        skill_levels["soft_skills"] = "Expert"
    elif any(kw in text for kw in soft_skills_keywords["advanced"]):
        skill_levels["soft_skills"] = "Advanced"
    elif any(kw in text for kw in soft_skills_keywords["basic"]):
        skill_levels["soft_skills"] = "Basic"

    # MS Office skills
    if "ms office" in text or "microsoft office" in text:
        if "expert" in text or "sehr gut" in text:
            skill_levels["ms_office"] = "Expert"
        elif "fortgeschritten" in text or "advanced" in text:
            skill_levels["ms_office"] = "Advanced"
        else:
            skill_levels["ms_office"] = "Basic"

    # Process modeling with enhanced recognition
    process_modeling_tools = [
        "camunda",
        "signavio",
        "bpmn",
        "prozessmodellierung",
        "aris",
    ]
    if any(tool in text for tool in process_modeling_tools):
        if is_expert_level or "prozessoptimierung" in text:
            skill_levels["process_modeling"] = "Expert"
        elif "fortgeschritten" in text or "advanced" in text:
            skill_levels["process_modeling"] = "Advanced"
        else:
            skill_levels["process_modeling"] = "Basic"

    # SAP Core and ECC Systems with enhanced recognition
    if "sap" in text:
        if is_expert_level:
            skill_levels["sap_core"] = "Expert"
        else:
            skill_levels["sap_core"] = "Advanced"

        # Check ECC systems expertise
        ecc_keywords = ["is-u", "idex", "im4g", "sap ecc"]
        ecc_matches = sum(1 for keyword in ecc_keywords if keyword in text)
        if ecc_matches >= 2 and is_expert_level:
            skill_levels["ecc_systems"] = "Expert"
        elif ecc_matches >= 1:
            skill_levels["ecc_systems"] = "Advanced"
        elif "ecc" in text:
            skill_levels["ecc_systems"] = "Basic"

    # S/4 Systems with enhanced recognition
    s4_keywords = ["s/4", "s4", "s4hana", "s/4 hana", "utilities", "maco", "ucom"]
    s4_matches = sum(1 for keyword in s4_keywords if keyword in text)
    if s4_matches >= 3 and is_expert_level:
        skill_levels["s4_systems"] = "Expert"
    elif s4_matches >= 2:
        skill_levels["s4_systems"] = "Advanced"
    elif s4_matches >= 1:
        skill_levels["s4_systems"] = "Basic"

    # ECC and S/4 Processes with enhanced recognition
    process_keywords = [
        "stammdaten",
        "datenmodelle",
        "messkonzepte",
        "geräteverwaltung",
        "edm",
        "abrechnung",
        "fakturierung",
        "fi-ca",
        "mos-billing",
        "memi",
        "eeg billing",
    ]
    process_matches = sum(1 for keyword in process_keywords if keyword in text)
    if process_matches >= 5 and is_expert_level:
        skill_levels["ecc_s4_processes"] = "Expert"
    elif process_matches >= 3:
        skill_levels["ecc_s4_processes"] = "Advanced"
    elif process_matches >= 1:
        skill_levels["ecc_s4_processes"] = "Basic"

    # SAP Technology with enhanced recognition
    tech_keywords = {
        "transport": ["transportverwaltung", "transport management"],
        "rap": ["rap", "rest application programming"],
        "cap": ["cap", "cloud application programming"],
        "btp": ["btp", "business technology platform"],
        "fiori": ["fiori", "cds", "core data services"],
        "abap": ["abap", "abap oo"],
        "integration": ["integration platform", "cpi"],
    }

    tech_matches = {
        category: sum(1 for kw in keywords if kw in text)
        for category, keywords in tech_keywords.items()
    }

    total_matches = sum(tech_matches.values())
    if total_matches >= 5 and is_expert_level:
        skill_levels["sap_technology"] = "Expert"
    elif total_matches >= 3:
        skill_levels["sap_technology"] = "Advanced"
    elif total_matches >= 1:
        skill_levels["sap_technology"] = "Basic"

    # Non-SAP Technologies with enhanced recognition
    nonsap_keywords = {
        "programming": ["java", "javascript", "nodejs", "python", "flask", "django"],
        "web": ["html", "css", "soap", "rest", "odata", "soa"],
        "architecture": [
            "solution design",
            "software-architektur",
            "software-lifecycle",
        ],
        "devops": [
            "ci/cd",
            "unit tests",
            "integration tests",
            "testdriven development",
        ],
        "database": ["nosql", "sql"],
    }

    nonsap_matches = {
        category: sum(1 for kw in keywords if kw in text)
        for category, keywords in nonsap_keywords.items()
    }

    total_nonsap = sum(nonsap_matches.values())
    if total_nonsap >= 8 and is_expert_level:
        skill_levels["non_sap"] = "Expert"
    elif total_nonsap >= 5:
        skill_levels["non_sap"] = "Advanced"
    elif total_nonsap >= 2:
        skill_levels["non_sap"] = "Basic"

    # Modeling with enhanced recognition
    modeling_keywords = ["bpmn", "uml", "enterprise architecture"]
    modeling_matches = sum(1 for keyword in modeling_keywords if keyword in text)
    if modeling_matches >= 2 and is_expert_level:
        skill_levels["modeling"] = "Expert"
    elif modeling_matches >= 1:
        skill_levels["modeling"] = "Advanced"
    elif "modellierung" in text:
        skill_levels["modeling"] = "Basic"

    # Process Management with enhanced recognition
    process_mgmt_keywords = {
        "expert": ["prozessoptimierung", "change management", "transformation"],
        "advanced": ["prozessanalyse", "prozessbeschreibung"],
        "basic": ["testfälle", "testkoordination", "testen"],
    }

    if any(kw in text for kw in process_mgmt_keywords["expert"]) and is_expert_level:
        skill_levels["process_management"] = "Expert"
    elif any(kw in text for kw in process_mgmt_keywords["advanced"]):
        skill_levels["process_management"] = "Advanced"
    elif any(kw in text for kw in process_mgmt_keywords["basic"]):
        skill_levels["process_management"] = "Basic"

    # Requirements Engineering with enhanced recognition
    req_eng_keywords = {
        "expert": [
            "anforderungsmanagement",
            "requirements engineering",
            "spezifikation",
        ],
        "advanced": ["fachkonzept", "technisches konzept", "anforderungsdefinition"],
        "basic": ["lastenheft", "pflichtenheft"],
    }

    if any(kw in text for kw in req_eng_keywords["expert"]) and is_expert_level:
        skill_levels["requirements_engineering"] = "Expert"
    elif any(kw in text for kw in req_eng_keywords["advanced"]):
        skill_levels["requirements_engineering"] = "Advanced"
    elif any(kw in text for kw in req_eng_keywords["basic"]):
        skill_levels["requirements_engineering"] = "Basic"

    # Project Management with enhanced recognition
    pm_keywords = {
        "expert": ["portfoliomanagement", "programm management", "multi-project"],
        "advanced": ["projektleitung", "scrum master", "agile coach"],
        "basic": ["scrum", "kanban", "wasserfall", "projektplanung"],
    }

    if any(kw in text for kw in pm_keywords["expert"]) and is_expert_level:
        skill_levels["project_management"] = "Expert"
    elif any(kw in text for kw in pm_keywords["advanced"]):
        skill_levels["project_management"] = "Advanced"
    elif any(kw in text for kw in pm_keywords["basic"]):
        skill_levels["project_management"] = "Basic"

    # Energy Industry General with enhanced recognition
    energy_keywords = {
        "expert": ["energiemarkt", "energiewende", "regulierung"],
        "advanced": ["kundenservice", "messdatenmanagement", "marktkommunikation"],
        "basic": ["messkonzepte", "wechselprozesse", "gpke", "geli", "wim"],
    }

    if any(kw in text for kw in energy_keywords["expert"]) and is_expert_level:
        skill_levels["energy_industry_general"] = "Expert"
    elif any(kw in text for kw in energy_keywords["advanced"]):
        skill_levels["energy_industry_general"] = "Advanced"
    elif any(kw in text for kw in energy_keywords["basic"]):
        skill_levels["energy_industry_general"] = "Basic"

    # Energy Industry Network
    network_keywords = ["netzabrechnung", "einspeiserabrechnung", "netznutzung"]
    if any(kw in text for kw in network_keywords) and is_expert_level:
        skill_levels["energy_industry_network"] = "Expert"
    elif any(kw in text for kw in network_keywords):
        skill_levels["energy_industry_network"] = "Advanced"

    # Energy Industry Supply
    supply_keywords = ["crm", "rechnungseingangsprüfung", "endkundenabrechnung"]
    if any(kw in text for kw in supply_keywords) and is_expert_level:
        skill_levels["energy_industry_supply"] = "Expert"
    elif any(kw in text for kw in supply_keywords):
        skill_levels["energy_industry_supply"] = "Advanced"

    # Energy Industry MSB with enhanced recognition
    msb_keywords = {
        "expert": ["smart meter strategie", "msb transformation"],
        "advanced": ["smart meter rollout", "gateway administration"],
        "basic": ["gdew", "msbg", "gateway", "mdm"],
    }

    if any(kw in text for kw in msb_keywords["expert"]) and is_expert_level:
        skill_levels["energy_industry_msb"] = "Expert"
    elif any(kw in text for kw in msb_keywords["advanced"]):
        skill_levels["energy_industry_msb"] = "Advanced"
    elif any(kw in text for kw in msb_keywords["basic"]):
        skill_levels["energy_industry_msb"] = "Basic"

    # Set default "None" for any missing categories
    for category in DEVELOPER_CRITERIA.keys():
        if category not in skill_levels:
            skill_levels[category] = "None"

    return skill_levels


def determine_seniority_level(
    skill_levels: Dict[str, str], role: str = "consultant"
) -> str:
    """
    Determine the overall seniority level based on skill levels.
    Returns "Junior", "Professional", "Senior", or "Principal".

    Args:
        skill_levels: Dictionary of skill categories and their levels
        role: Either "consultant" or "developer"
    """
    # Ensure no higher seniority level for language skills below C1
    if skill_levels["language_skills"] == "None":
        return "Junior"

    # Select the appropriate criteria based on role
    criteria = CONSULTANT_CRITERIA if role == "consultant" else DEVELOPER_CRITERIA
    level_requirements = (
        LEVEL_SPECIFIC_REQUIREMENTS
        if role == "consultant"
        else DEVELOPER_LEVEL_SPECIFIC_REQUIREMENTS
    )

    # Initialize score for each level
    level_scores = {"Principal": 0, "Senior": 0, "Professional": 0, "Junior": 0}

    # Helper function to convert level to numeric value with weighted scoring
    def level_to_score(level: str) -> float:
        return {
            "None": 0.0,
            "Basic": 1.0,
            "Advanced": 2.5,  # Increased weight for Advanced
            "Expert": 4.0,  # Increased weight for Expert
        }[level]

    # Calculate scores for each level with weighted requirements
    for level, requirements in level_requirements.items():
        score = 0
        total_possible = 0

        # Check expert level requirements (highest weight)
        if "required_expert" in requirements:
            weight = 3.0  # Higher weight for expert requirements
            for skill in requirements["required_expert"]:
                total_possible += (
                    weight * 4.0
                )  # Maximum possible score for expert level
                score += weight * level_to_score(skill_levels.get(skill, "None"))

        # Check advanced level requirements
        if "required_advanced" in requirements:
            weight = 2.0  # Medium weight for advanced requirements
            for skill in requirements["required_advanced"]:
                total_possible += weight * 4.0  # Maximum possible score
                score += weight * level_to_score(skill_levels.get(skill, "None"))

        # Check basic level requirements
        if "required_basic" in requirements:
            weight = 1.0  # Base weight for basic requirements
            for skill in requirements["required_basic"]:
                total_possible += weight * 4.0  # Maximum possible score
                score += weight * level_to_score(skill_levels.get(skill, "None"))

        # Calculate percentage score for this level
        if total_possible > 0:
            percentage = (score / total_possible) * 100
            level_scores[level] = percentage

    # Experience detection with more specific patterns
    years_experience = 0
    cv_text = str(skill_levels).lower()

    # Check for explicit year mentions
    experience_patterns = [
        r"(\d+)\s*(?:jahre|year|jr)",
        r"(?:über|more than)\s*(\d+)\s*(?:jahre|year)",
        r"(\d+)\+\s*(?:jahre|year)",
    ]

    import re

    for pattern in experience_patterns:
        matches = re.findall(pattern, cv_text)
        if matches:
            try:
                years = max(int(match) for match in matches)
                years_experience = max(years_experience, years)
            except ValueError:
                continue

    # Check for expert/senior indicators
    expert_indicators = [
        "expert",
        "lead",
        "leitung",
        "führung",
        "architect",
        "principal",
        "senior",
        "mehrjährige erfahrung",
        "langjährige erfahrung",
        "umfangreiche erfahrung",
        "extensive experience",
    ]

    expert_matches = sum(1 for indicator in expert_indicators if indicator in cv_text)
    if expert_matches >= 3:
        years_experience = max(years_experience, 8)
    elif expert_matches >= 2:
        years_experience = max(years_experience, 5)

    # Adjust scores based on experience with higher impact
    if years_experience >= 8:
        level_scores["Principal"] += 35  # Increased bonus for Principal
        level_scores["Senior"] += 20
    elif years_experience >= 5:
        level_scores["Senior"] += 35  # Increased bonus for Senior
        level_scores["Professional"] += 15
    elif years_experience >= 3:
        level_scores["Professional"] += 25

    # ENHANCED: Experience-based overrides for senior and principal levels
    # This ensures that candidates with significant experience are properly classified
    if years_experience >= 10:
        logging.debug(f"Experience-based override: Principal (10+ years)")
        return "Principal"
    elif years_experience >= 7:
        logging.debug(f"Experience-based override: Senior (7+ years)")
        return "Senior"
    elif years_experience >= 5 and expert_matches >= 2:
        logging.debug(
            f"Experience-based override: Senior (5+ years with expert indicators)"
        )
        return "Senior"

    # Set adjusted thresholds for each level
    thresholds = {
        "Principal": 65,  # Further lowered to recognize experienced candidates
        "Senior": 55,  # Further lowered to recognize experienced candidates
        "Professional": 45,  # Further lowered to recognize experienced candidates
        "Junior": 0,  # No threshold for Junior
    }

    # Log the initial skill levels and role
    logging.debug(f"Skill Levels: {skill_levels}")
    logging.debug(f"Role: {role}")

    # Log the calculated scores for each level
    logging.debug(f"Level Scores: {level_scores}")

    # Log the detected years of experience
    logging.debug(f"Years of Experience: {years_experience}")

    # Determine the highest level that meets its threshold
    for level, threshold in thresholds.items():
        if level_scores[level] >= threshold:
            logging.debug(f"Determined Level: {level}")
            return level

    logging.debug("Determined Level: Junior")
    return "Junior"


def level_meets_requirement(actual: str, required: str) -> bool:
    """
    Check if the actual skill level meets the required level.
    """
    levels = ["None", "Basic", "Advanced", "Expert"]
    return levels.index(actual) >= levels.index(required)


def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text.lower()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error extracting text from PDF: {str(e)}"
        )


def get_ai_analysis(
    cv_text: str, requirements: List[dict], role: str = "consultant"
) -> dict:
    try:
        # Determine skill levels from CV text
        skill_levels = determine_skill_level(cv_text.lower())
        logging.debug(f"Skill Levels: {skill_levels}")

        # CRITICAL: Early return with 0% match if language skills are below C1
        if skill_levels["language_skills"] in ["None", "Basic"]:
            logging.debug("ENFORCING 0% match due to language skills below C1.")
            return {
                "requirement_matches": [],
                "overall_score": 0,
                "seniority_level": "Nicht geeignet",
                "summary": "Der Kandidat verfügt nicht über die erforderlichen Deutschkenntnisse (mindestens C1) und ist daher nicht für die Position geeignet.",
                "key_strengths": [],
                "improvement_areas": [
                    "Deutschkenntnisse verbessern (mindestens C1 erforderlich)"
                ],
            }

        seniority_level = determine_seniority_level(skill_levels, role)

        # Format requirements text with proper escaping
        requirements_text = "\n".join(
            [f"- {req['text'].replace('"', '\\"')}" for req in requirements]
        )

        # Create a more structured prompt with explicit JSON formatting instructions and level-specific guidance
        prompt = f"""Analysiere den folgenden Lebenslauf für die Position {role} anhand der Stellenanforderungen. 

KRITISCHE ANFORDERUNG: Wenn ein Lebenslauf Deutschkenntnisse geringer als C1 hat (also A1, A2, B1, B2, "Gut", "Basic" oder "None"), MUSS die Gesamtbewertung 0% sein und der Kandidat als "Nicht geeignet" eingestuft werden. Dies ist eine absolute Voraussetzung, die unter keinen Umständen umgangen werden darf.

Lebenslauf Text:
{cv_text}

Stellenanforderungen:
{requirements_text}

WICHTIG - Bewertungsrichtlinien:
Wenn ein Kandidat ein deutsch Niveau unter C1 hat, ist er ungeeignet und sollte 0% Gesamtbewertung erhalten
1. Berücksichtige das Erfahrungslevel "{seniority_level}" bei der Bewertung
2. Für Junior-Level:
   - Fokussiere auf Grundkenntnisse und Potenzial
   - Bewerte fehlende Erfahrung nicht negativ
   - Hebe Lernbereitschaft und grundlegende Fähigkeiten hervor
3. Für Professional-Level:
   - Erwarte solide Grundkenntnisse in allen Kernbereichen
   - Bewerte praktische Erfahrung positiv
   - Fokussiere auf wachsende Expertise
4. Für Senior-Level:
   - Erwarte vertiefte Fachkenntnisse
   - Bewerte Führungserfahrung und Projektverantwortung
   - Achte auf strategisches Verständnis
5. Für Principal-Level:
   - Erwarte umfassende Expertise
   - Bewerte strategische Führungskompetenz
   - Achte auf nachgewiesene Erfolge und Innovation

WICHTIG - Formatierungsregeln für die JSON-Antwort:
1. Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt
2. Verwende KEINE Kommentare oder zusätzlichen Text
3. Alle Textfelder MÜSSEN in doppelten Anführungszeichen stehen
4. Zahlen dürfen KEINE Anführungszeichen haben
5. Arrays müssen mit [ beginnen und mit ] enden
6. Objekte müssen mit {{ beginnen und mit }} enden
7. Alle Felder müssen mit Komma getrennt sein
8. Das letzte Element in Arrays/Objekten darf KEIN Komma haben
9. Keine Zeilenumbrüche in Textfeldern verwenden
10. Maximale Länge für Textfelder: 500 Zeichen
11. Maximale Anzahl von Elementen in Arrays: 5

Erwartetes Format:
{{
    "overall_score": 75,
    "seniority_level": "{seniority_level}",
    "requirement_matches": [
        {{
            "requirement": "Beispielanforderung",
            "match_percentage": 80,
            "explanation": "Kurze Erklärung"
        }}
    ],
    "summary": "Kurze Zusammenfassung der Analyse",
    "key_strengths": [
        "Stärke 1",
        "Stärke 2"
    ],
    "improvement_areas": [
        "Entwicklungspotenzial 1",
        "Entwicklungspotenzial 2"
    ]
}}"""

        # Call the GPT-3.5 Turbo API with strict JSON formatting
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Du bist ein CV-Analyse-Assistent mit besonderem Fokus auf faire Bewertung verschiedener Erfahrungsstufen.

KRITISCHE ANFORDERUNG: Wenn ein Lebenslauf Deutschkenntnisse geringer als C1 hat (also A1, A2, B1, B2, "Gut", "Basic" oder "None"), MUSS die Gesamtbewertung 0% sein und der Kandidat als "Nicht geeignet" eingestuft werden. Dies ist eine absolute Voraussetzung, die unter keinen Umständen umgangen werden darf.

Für Junior-Kandidaten:
- Bewerte Grundkenntnisse und Potenzial positiv
- Fehlende Erfahrung ist normal und sollte nicht negativ bewertet werden
- Fokussiere auf Lernbereitschaft und Entwicklungspotenzial

Für Professional-Kandidaten:
- Erwarte solide Grundkenntnisse
- Bewerte erste Praxiserfahrung positiv
- Fokussiere auf Entwicklung zur Expertise

Für Senior-Kandidaten:
- Erwarte vertiefte Fachkenntnisse
- Bewerte Führungserfahrung positiv
- Achte auf strategisches Denken

Für Principal-Kandidaten:
- Erwarte umfassende Expertise
- Bewerte strategische Führung
- Achte auf Innovation und Erfolge

Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt. Keine zusätzlichen Erklärungen oder Formatierung.""",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        # Extract and parse the AI response with improved error handling
        response_content = response.choices[0].message.content.strip()

        try:
            # Clean up the response content
            json_start = response_content.find("{")
            json_end = response_content.rfind("}") + 1
            ai_response = json.loads(response_content[json_start:json_end])

            # CRITICAL: Double-check language skills and enforce 0% if below C1
            if skill_levels["language_skills"] in ["None", "Basic"]:
                logging.debug(
                    "Double-checking: Setting overall score to 0 due to language skills below C1."
                )
                ai_response["overall_score"] = 0
                ai_response["seniority_level"] = "Nicht geeignet"
                ai_response["summary"] = (
                    "Der Kandidat verfügt nicht über die erforderlichen Deutschkenntnisse (mindestens C1) und ist daher nicht für die Position geeignet."
                )
                ai_response["requirement_matches"] = []
                ai_response["key_strengths"] = []
                ai_response["improvement_areas"] = [
                    "Deutschkenntnisse verbessern (mindestens C1 erforderlich)"
                ]
                return ai_response

            # Adjust scoring based on seniority level
            if isinstance(ai_response.get("overall_score"), (int, float)):
                base_score = ai_response["overall_score"]
                adjusted_score = base_score

                # Score adjustments for different levels
                if seniority_level == "Junior":
                    # 30% boost for juniors to account for potential
                    adjusted_score = min(100, base_score * 1.3)
                elif seniority_level == "Professional":
                    # 15% boost for professionals to account for growing expertise
                    adjusted_score = min(100, base_score * 1.15)
                elif seniority_level == "Senior":
                    # 5% boost for seniors to account for leadership potential
                    adjusted_score = min(100, base_score * 1.05)
                # No boost for Principal level as they are evaluated at full scale

                ai_response["overall_score"] = round(adjusted_score)

                # Adjust requirement matches based on seniority level
                if isinstance(ai_response.get("requirement_matches"), list):
                    cleaned_matches = []
                    for match in ai_response["requirement_matches"][:5]:
                        if isinstance(match, dict) and isinstance(
                            match.get("match_percentage"), (int, float)
                        ):
                            match_score = match["match_percentage"]
                            if seniority_level == "Junior":
                                match_score = min(100, match_score * 1.3)
                            elif seniority_level == "Professional":
                                match_score = min(100, match_score * 1.15)
                            elif seniority_level == "Senior":
                                match_score = min(100, match_score * 1.05)
                            match["match_percentage"] = round(match_score)
                            cleaned_match = {
                                "requirement": str(match.get("requirement", ""))[:500],
                                "match_percentage": min(
                                    100, max(0, float(match_score))
                                ),
                                "explanation": str(match.get("explanation", ""))[:500],
                            }
                            cleaned_matches.append(cleaned_match)
                    ai_response["requirement_matches"] = cleaned_matches

            # Final check to ensure overall_score is 0 if language skills are below C1
            if skill_levels["language_skills"] in ["None", "Basic"]:
                logging.debug(
                    "Final check: Setting overall score to 0 due to language skills below C1."
                )
                ai_response["overall_score"] = 0
                ai_response["seniority_level"] = "Nicht geeignet"
                ai_response["summary"] = (
                    "Der Kandidat verfügt nicht über die erforderlichen Deutschkenntnisse (mindestens C1) und ist daher nicht für die Position geeignet."
                )
                # Clear requirement matches to ensure consistent 0% representation
                ai_response["requirement_matches"] = []
                # Add improvement area for language skills
                ai_response["improvement_areas"] = [
                    "Deutschkenntnisse verbessern (mindestens C1 erforderlich)"
                ]
                # Clear key strengths as they are not relevant for ineligible candidates
                ai_response["key_strengths"] = []

            return ai_response
        except json.JSONDecodeError as json_err:
            print(f"JSON parsing error: {str(json_err)}")
            print(f"Response content: {response_content}")
            return {
                "requirement_matches": [],
                "overall_score": 0,
                "seniority_level": "Junior",
            }
        except (ValueError, TypeError) as err:
            print(f"Validation error: {str(err)}")
            return {
                "requirement_matches": [],
                "overall_score": 0,
                "seniority_level": "Junior",
            }

    except Exception as e:
        print(f"AI analysis error: {str(e)}")
        # If there's an error, still enforce the language skills rule
        if skill_levels.get("language_skills") in ["None", "Basic"]:
            return {
                "requirement_matches": [],
                "overall_score": 0,
                "seniority_level": "Nicht geeignet",
                "summary": "Der Kandidat verfügt nicht über die erforderlichen Deutschkenntnisse (mindestens C1).",
                "key_strengths": [],
                "improvement_areas": [
                    "Deutschkenntnisse verbessern (mindestens C1 erforderlich)"
                ],
            }
        return {
            "requirement_matches": [],
            "overall_score": 0,
            "seniority_level": "Junior",
        }


def calculate_semantic_similarity(cv_text: str, requirement: str) -> float:
    try:
        # Verarbeitung der Texte mit spaCy:
        # Der Text wird in ein Doc-Objekt umgewandelt, das eine Vektorrepräsentation (Embedding) enthält.
        cv_doc = nlp(cv_text)
        req_doc = nlp(requirement)

        # Berechnung der Ähnlichkeit als Kosinusähnlichkeit zwischen den Vektoren
        similarity = cv_doc.similarity(req_doc)

        # Normalisierung des Ähnlichkeitswerts auf einen Prozentbereich (0 bis 100)
        score = max(min(similarity * 100, 100), 0)

        return score
    except Exception as e:
        print(f"Error calculating similarity: {str(e)}")
        return 0.0


@app.post("/analyze")
async def analyze_cv(
    file: UploadFile = File(...),
    requirements: str = Query(None),
    role: str = Query("consultant"),
):
    try:
        # Read and extract text from PDF
        contents = await file.read()
        cv_text = extract_text_from_pdf(contents)

        # Parse requirements from query string
        requirements_list = []
        if requirements:
            requirements_lines = requirements.split("\n")
            requirements_list = [
                {"text": line.strip()} for line in requirements_lines if line.strip()
            ]

        # Get AI analysis with role parameter
        results = get_ai_analysis(cv_text, requirements_list, role)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
