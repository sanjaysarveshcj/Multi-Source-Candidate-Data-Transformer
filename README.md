# Candidate Transformer Service

A pipeline for extracting, merging, and dynamically reshaping candidate data from multiple heterogeneous sources (ATS JSON, Resume PDF, GitHub, LinkedIn, Text, Recruiter CSV).

## Features
- **Multi-Source Data Ingestion**: Parse and normalize data from varying sources and formats.
- **Merge Engine & Provenance**: Resolve conflicts based on source trust levels and track where every field originated.
- **Dynamic Configurable Projection**: Define JSON output schemas at runtime and let the API reshape data on-the-fly (e.g., extracting list items, renaming keys, dropping confidence fields).
- **Dynamic Schema Validation**: Validates the dynamically projected payload against constraints like `required` fields and specific data `types`.

---

## Installation & Setup

1. Ensure you have Python installed.
2. Activate your virtual environment:
   ```bash
   candidate\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the API Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The service will run locally on `http://127.0.0.1:8000`. You can visit `http://127.0.0.1:8000/docs` to see the interactive Swagger API documentation.

### Example API Request (cURL)

Extract candidate data from a GitHub URL using the default canonical shape:

```bash
curl -X POST "http://127.0.0.1:8000/transform/github" \
     -d "github_url=https://github.com/torvalds"
```

### Sample API Output

When merging multiple sources (e.g., Resume, ATS JSON, GitHub), the API returns a comprehensive payload like this:

<details>
<summary>Click to view full JSON payload</summary>

```json
{
  "success": true,
  "requestId": "6880acf7-c252-43b8-b5ec-9e19b00a4bdb",
  "processingTimeSeconds": 0.492,
  "data": {
    "candidate": {
      "candidate_id": "055f04211ee0bb0483267cbdfbbf163d",
      "full_name": "SANJAY SARVESH C J",
      "emails": [
        "sanjaysarveshcj@gmail.com",
        "sanjay.sarvesh@example.com"
      ],
      "phones": [
        "+916381744355",
        "+919876543210"
      ],
      "location": {
        "city": "Chennai",
        "region": "Tamil Nadu",
        "country": "India"
      },
      "links": {
        "linkedin": "linkedin.com/in/sanjaysarveshcj",
        "github": "github.com/sanjaysarveshcj",
        "portfolio": null,
        "other": []
      },
      "headline": "Full Stack Developer",
      "years_experience": null,
      "skills": [
        {
          "name": "Aws",
          "confidence": 1,
          "sources": [
            "Resume",
            "Text File"
          ]
        },
        {
          "name": "C",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Css",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Docker",
          "confidence": 1,
          "sources": [
            "Resume",
            "ATS JSON",
            "Text File"
          ]
        },
        {
          "name": "Express.Js",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Git",
          "confidence": 1,
          "sources": [
            "Resume",
            "Text File"
          ]
        },
        {
          "name": "Github",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Golang",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Html",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Java",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Javascript",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Jwt",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Llms",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Mongodb",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Mysql",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Netlify",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Next.Js",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Node.Js",
          "confidence": 1,
          "sources": [
            "Resume",
            "Text File"
          ]
        },
        {
          "name": "Numpy",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Opencv",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Pandas",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Postgresql",
          "confidence": 1,
          "sources": [
            "Resume",
            "ATS JSON",
            "Text File"
          ]
        },
        {
          "name": "Prisma",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Python",
          "confidence": 1,
          "sources": [
            "Resume",
            "ATS JSON",
            "Text File"
          ]
        },
        {
          "name": "Pytorch",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Railway",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "React.Js",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Render",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Scikit-Learn",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Shadcnui",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Socket.Io",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Sql",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Swagger",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Tailwindcss",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Tensorflow",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Transformers",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Typescript",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Vercel",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Zustand",
          "confidence": 1,
          "sources": [
            "Resume"
          ]
        },
        {
          "name": "Fastapi",
          "confidence": 1,
          "sources": [
            "ATS JSON",
            "Text File"
          ]
        },
        {
          "name": "React",
          "confidence": 1,
          "sources": [
            "ATS JSON",
            "Text File"
          ]
        },
        {
          "name": "Backend",
          "confidence": 1,
          "sources": [
            "ATS JSON"
          ]
        },
        {
          "name": "Api-Development",
          "confidence": 1,
          "sources": [
            "ATS JSON"
          ]
        },
        {
          "name": "Django",
          "confidence": 1,
          "sources": [
            "Text File"
          ]
        }
      ],
      "experience": [
        {
          "company": "Dnyx Business Solutions Private Limited",
          "title": "Full-Stack Web Developer",
          "employment_type": "Remote",
          "start_date": "Nov 2025",
          "end_date": "Mar 2026",
          "description": [
            "Developed a Female Entrepreneur website and an e-learning platform using Next.js, TailwindCSS, Node.js, and Express.js.",
            "Improved UI performance and SEO optimization while contributing to both frontend and backend development.",
            "Worked with PostgreSQL and AWS RDS, gaining experience in deployment, scalability, and backend system configuration."
          ]
        },
        {
          "company": "CITBIF",
          "title": "Software Developer Intern",
          "employment_type": "On-Site",
          "start_date": "May 2025",
          "end_date": "June 2025",
          "description": [
            "Implemented secure syllabus uploads using MongoDB GridFS with multi-level approvals and role-based access control.",
            "Automated curriculum generation using DOCX template merging with real-time approval notifications.",
            "Developed a MERN-based role-driven academic management platform improving syllabus creation & faculty productivity."
          ]
        },
        {
          "company": "NullClass EdTech Private Limited",
          "title": "Data Science Intern",
          "employment_type": "Remote",
          "start_date": "Nov 2024",
          "end_date": "Jan 2025",
          "description": [
            "Built 2 AI applications: NMT system and analytics dashboard processing 10K+ records, showcasing ML development.",
            "Developed deep learning and NLP models (4.2M parameters, 100K+ samples) achieving BLEU 35 and <100ms latency.",
            "Created production systems including GUI translator and auto-refresh dashboard (6+ modules) for real-time insights."
          ]
        },
        {
          "company": "TechCorp Solutions",
          "title": "Senior Backend Engineer",
          "start": "2022-01",
          "end": "2025-06",
          "summary": "Built scalable microservices using Python and FastAPI"
        },
        {
          "company": "StartupXYZ",
          "title": "Software Developer",
          "start": "2020-03",
          "end": "2021-12",
          "summary": "Developed REST APIs and integrated third-party services"
        }
      ],
      "education": [
        {
          "institution": "Chennai Institute of Technology",
          "degree": "be",
          "location": " Chennai, TN",
          "start_date": "September 2023",
          "end_date": "April 2027",
          "cgpa": "9.04/10",
          "field_of_study": "r 2023",
          "raw": [
            "Chennai Institute of Technology | Chennai, TN September 2023 - April 2027",
            "B.E. Computer Science and Engineering(Artificial Intelligence & Machine Learning) CGPA: 9.04/10 (as of 1st to 5th sem)"
          ]
        },
        {
          "institution": "Anna University",
          "degree": "B.Tech",
          "field": "Computer Science",
          "end_year": 2020
        }
      ],
      "provenance": [
        {
          "field": "full_name",
          "source": "Resume",
          "method": "merge"
        },
        {
          "field": "headline",
          "source": "ATS JSON",
          "method": "merge"
        },
        {
          "field": "location",
          "source": "ATS JSON",
          "method": "merge"
        },
        {
          "field": "emails",
          "source": "Resume",
          "method": "merge"
        },
        {
          "field": "emails",
          "source": "ATS JSON",
          "method": "merge"
        },
        {
          "field": "phones",
          "source": "Resume",
          "method": "merge"
        },
        {
          "field": "phones",
          "source": "ATS JSON",
          "method": "merge"
        },
        {
          "field": "skills",
          "source": "Resume",
          "method": "merge"
        },
        {
          "field": "skills",
          "source": "Text File",
          "method": "merge"
        },
        {
          "field": "skills",
          "source": "ATS JSON",
          "method": "merge"
        },
        {
          "field": "links",
          "source": "Resume",
          "method": "merge"
        },
        {
          "field": "experience",
          "source": "Resume",
          "method": "merge"
        },
        {
          "field": "experience",
          "source": "ATS JSON",
          "method": "merge"
        },
        {
          "field": "education",
          "source": "Resume",
          "method": "merge"
        },
        {
          "field": "education",
          "source": "ATS JSON",
          "method": "merge"
        }
      ],
      "overall_confidence": 0.8625
    },
    "sources_used": [
      "Recruiter CSV",
      "Resume",
      "ATS JSON",
      "Text File"
    ],
    "validation": {
      "is_valid": true,
      "errors": [],
      "warnings": [],
      "score": 1
    },
    "dynamic_validation": null
  }
}
```
</details>

---

## Testing the Dynamic Projection Engine

We provide a `test_projection.py` script that showcases how the engine handles a runtime projection configuration. The script processes a GitHub URL and reshapes the output strictly according to the provided config rules.

**Run the script:**
```bash
python test_projection.py
```

### Sample Output

Below is the exact output produced by the script when configuring the pipeline to extract only a few specific fields and checking for required constraints.

```json
Config used: {
  "fields": [
    {
      "path": "full_name",
      "type": "string",
      "required": true
    },
    {
      "path": "primary_email",
      "from": "emails[0]",
      "type": "string",
      "required": true
    },
    {
      "path": "phone",
      "from": "phones[0]",
      "type": "string",
      "normalize": "E164"
    },
    {
      "path": "skills",
      "from": "skills[].name",
      "type": "string[]",
      "normalize": "canonical"
    }
  ],
  "include_confidence": true,
  "on_missing": "null"
}

Projected output: {
  "full_name": "Linus Torvalds",
  "primary_email": null,
  "phone": null,
  "skills": null
}

Dynamic validation: {
  "valid": false,
  "errors": [
    "Field 'primary_email' is required but missing or empty."
  ]
}
```

*(Notice how the dynamic validator successfully flags `primary_email` because it was explicitly marked as `required` in the runtime config, but no public email was found on the GitHub profile.)*

---

## Edge Case Conflict & Omission Test

We also include a secondary test script (`test_edge_cases.py`) designed to validate complex edge cases, such as:
- **Conflict Resolution**: Merging contradictory data from an ATS record and a GitHub profile (e.g. differing Name and Location formats), using the Confidence Engine to pick the most reliable data.
- **Deep Path Missing Data Omission**: Safely extracting paths like `skills[].name` on lists of strings, resulting in an empty array.
- **Strict Key Omission**: Utilizing the `"on_missing": "omit"` policy, which ensures that keys with missing data are completely removed from the final JSON payload rather than being assigned `null`.

**Run the edge case test:**
```bash
python test_edge_cases.py
```

This acts as a "gold profile" reference implementation, demonstrating how the `MergeEngine` and `CandidateProjector` seamlessly interact under challenging conditions.
