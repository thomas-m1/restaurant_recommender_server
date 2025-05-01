# bain_restaurant_recommender_server
Server for Bain Restaurant recommender MVP


A FastAPI backend for recommending curated restaurants near Bain & Company’s Toronto office. This tool is designed to help partners quickly find client-appropriate venues using smart filters, internal recommendations, and distance-aware logic.




## Local Development Setup
### 1. Clone the Repository
git clone "repositoryurl"<br>
cd bain-restaurant-recommender<br>

### 2. Create a Virtual Environment
python3 -m venv venv<br>
source venv/bin/activate<br>
### 3. Install Dependencies
pip install --upgrade pip<br>
pip install -r requirements.txt<br>


### 4. Set up Database
in your postgres, create a db and add the link to you .env variables<br>
When you run the bain_restaurant_recommender_batch, it will create a businesses table.<br>

You still need to create the recommendations table.<br>
In your postgres, run the following command to create the table:<br>

CREATE TABLE recommendations (<br>
    id VARCHAR PRIMARY KEY,<br>
    business_id TEXT NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,<br>
    user_email TEXT,<br>
    suggest BOOLEAN NOT NULL,<br>
    note TEXT<br>
);<br>

or run the alembic script and it will create the table for you


### 5. .env.dev
ENV=development<br>
APP_VERSION=1.0.0<br>
DATABASE_URL="insert db url"<br>
ALLOWED_ORIGINS=["http://localhost:3000"]<br>
OFFICE_LAT="insert office latitude"<br>
OFFICE_LNG="insert office longitude"<br>

### 6. Run the Server
uvicorn app.main:app --reload<br>
Open your browser to: http://localhost:8000/docs<br>


Notes: some features don't offer free api. uploaded that version in separate branch