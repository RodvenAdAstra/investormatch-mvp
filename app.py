from flask import Flask, render_template_string, request, redirect, url_for, flash, send_file
import sqlite3
from datetime import datetime
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import io
import pandas as pd
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
import os
import numpy as np

app = Flask(__name__)
app.secret_key = 'pitchforge_mvp_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Init DB
def init_db():
    conn = sqlite3.connect('pitchforge.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pitches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT NOT NULL,
                  idea_summary TEXT NOT NULL,
                  target_audience TEXT,
                  team_bio TEXT,
                  ebitda REAL,
                  yoy_growth REAL,
                  ltv REAL,
                  cac REAL,
                  burn_rate REAL,
                  gross_margin REAL,
                  mrr REAL,
                  churn_rate REAL,
                  funding_ask REAL,
                  timeline_months INTEGER,
                  financial_file TEXT,
                  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Embedded form HTML (no file needed)
FORM_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InvestorMatch MVP</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; font-family: 'Segoe UI', sans-serif; }
        .card { max-width: 700px; margin: 50px auto; padding: 30px; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .btn-forge { background: #007bff; font-weight: bold; }
        .financial-row { display: flex; gap: 15px; margin-bottom: 15px; }
        .financial-col { flex: 1; }
        .ai-toggle { margin: 15px 0; font-style: italic; color: #6c757d; }
        .mrr-group { display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1 class="text-center mb-4">InvestorMatch MVP</h1>
        <p class="text-center lead">Upload your PitchForge deck or fill the form → get ranked investors instantly.</p>

        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="alert alert-info">{{ messages[0] }}</div>
            {% endif %}
        {% endwith %}

        <form method="POST" enctype="multipart/form-data">
            <div class="mb-3">
                <label class="form-label">Upload Pitch Deck (PPTX)</label>
                <input type="file" class="form-control" name="deck_file" accept=".pptx">
            </div>

            <hr>
            <p class="fw-bold">Or fill manually:</p>

            <div class="mb-3">
                <label class="form-label">Keywords (e.g., fintech ai saas)</label>
                <input type="text" class="form-control" name="keywords" placeholder="fintech ai">
            </div>

            <div class="mb-3">
                <label class="form-label">Stage</label>
                <select class="form-select" name="stage">
                    <option>pre-seed</option>
                    <option selected>seed</option>
                    <option>series-a</option>
                    <option>series-b</option>
                </select>
            </div>

            <div class="mb-3">
                <label class="form-label">Funding Ask ($M)</label>
                <input type="number" class="form-control" name="ask" step="0.1" placeholder="2.5">
            </div>

            <button type="submit" class="btn btn-primary btn-forge w-100 py-3">Find My Investors 🚀</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ... (your full POST logic — unchanged)
        # At the end of POST:
        return render_template_string(FORM_HTML)  # or results

    return render_template_string(FORM_HTML)

# ... rest of your code (build_pitch_deck_buffer, /success, etc.)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
