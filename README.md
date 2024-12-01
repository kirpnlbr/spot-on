# Spot On
SpotOn: Spot on parking, every time. A data structures &amp; algorithms project by Kir Peñalber and Kodi Magadia.

## Technologies Used
### Backend
- Django
- Axios API
- Data Structures: Hash Tables, Priority Queues
- Algorithms: BFS, Greedy Algorithm

### Frontend
- React
- TailwindCSS
- Framer Motion

# Test performance
```
cd backend
python -m memory_profiler api/tests/test_performance.py
```

# Set-up development server
## Backend
```
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server
python manage.py runserver
```

## Frontend
```
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```
