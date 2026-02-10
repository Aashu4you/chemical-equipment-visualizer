# ChemViz - Chemical Equipment Visualizer

A comprehensive chemical equipment monitoring and visualization platform with Django backend, React web frontend, and PyQt6 desktop application.

> [!NOTE]
> Project output images and a screen recording demonstration are available in the [output images](file:///d:/Programming/chemical-equipment-visualizer/output%20images) directory.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup (Django)

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the server:
```bash
python manage.py runserver
```

Backend will be available at `http://127.0.0.1:8000`

### Web Frontend Setup (React)

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Web app will be available at `http://localhost:3000`

### Desktop App Setup (PyQt6)

1. Navigate to desktop app directory:
```bash
cd desktop_app
```

2. Run the application:
```bash
run_app.bat  # Windows
```

Or manually:
```bash
python main.py
```

## 📊 Dashboard Features

### Overview Tab

The dashboard provides real-time equipment monitoring with the following visualizations:

#### Statistics Cards
- **Total Equipment**: Total number of equipment items in the system
- **Avg Flowrate**: Average flowrate across all equipment
- **Avg Pressure**: Average pressure reading across all equipment
- **Avg Temperature**: Average temperature across all equipment

#### Analytics Charts

1. **Equipment Distribution** (Horizontal Bar Chart)
   - Shows count of each equipment type
   - Helps identify the most common equipment in your facility
   - Color-coded for easy identification

2. **Flowrate Analysis** (Horizontal Bar Chart)
   - Displays average flowrate by equipment type
   - Useful for comparing performance across different equipment categories
   - Values are displayed on each bar for precise readings

3. **Correlation Analysis** (Scatter Plot)
   - Plots flowrate vs pressure relationship
   - Helps identify correlations and outliers
   - Each point represents one piece of equipment

4. **Temperature Distribution** (Histogram)
   - Shows frequency distribution of temperature readings
   - Helps identify temperature ranges and patterns
   - Useful for detecting anomalies

### Equipment Tab

- View complete equipment list in table format
- Export data to PDF reports
- Refresh data on demand
- Detailed information for each equipment item

### Upload CSV

- Bulk upload equipment data via CSV files
- Automatic data validation
- Progress tracking during upload

## 📋 Sample Data for Testing

A sample CSV file (`sample_equipment_data.csv`) is included in the root directory for testing purposes. This file contains realistic chemical equipment data that you can use to quickly populate the system and test all features.

### Sample Data Contents

The file includes 15 sample equipment entries with the following types:
- **Pumps** (4 entries)
- **Valves** (3 entries)
- **Heat Exchangers** (2 entries)
- **Reactors** (2 entries)
- **Condensers** (2 entries)
- **Compressor** (1 entry)
- **HD** (1 entry)

### CSV Format Requirements

Your CSV file must follow this exact format:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
HD1,HD,50,8.1,65
```

**Column Specifications:**
- **Equipment Name**: Unique identifier for the equipment (text)
- **Type**: Equipment category (text)
- **Flowrate**: Flow rate value (numeric)
- **Pressure**: Pressure reading (numeric)
- **Temperature**: Temperature reading (numeric)

### How to Use Sample Data

#### Web Frontend
1. Log in to your account
2. Navigate to the "Upload CSV" tab
3. Click "Choose File" and select `sample_equipment_data.csv`
4. Click "Upload" to import the data
5. Navigate to "Overview" or "Equipment" tabs to view the imported data

#### Desktop Application
1. Launch the desktop app and log in
2. Go to the "Upload CSV" tab
3. Click "Browse" and select `sample_equipment_data.csv`
4. Click "Upload CSV" to import
5. Use the refresh button to see the updated data in the dashboard

### Creating Your Own Test Data

To create custom test data:
1. Copy `sample_equipment_data.csv` as a template
2. Maintain the same column headers (first row)
3. Add your equipment data following the format
4. Ensure numeric values for Flowrate, Pressure, and Temperature
5. Save as a `.csv` file with UTF-8 encoding

## 🔑 Authentication

### Login
- Use email and password to log in
- Token-based authentication for secure API access

### Signup
- Create new account with email, name, and password
- Automatic token generation upon registration

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/              # Django REST API
│   ├── api/             # Authentication endpoints
│   ├── equipment/       # Equipment CRUD & analytics
│   └── manage.py
├── frontend/            # React web application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
│   └── package.json
├── desktop_app/         # PyQt6 desktop application
│   ├── ui/              # UI components
│   ├── api_client.py    # API integration
│   ├── styles.py        # Application styling
│   └── main.py
└── README.md
```

## 🛠️ API Endpoints

### Authentication
- `POST /api/signup` - Create new account
- `POST /api/login` - Login with email/password

### Equipment
- `GET /api/equipment/` - List all equipment
- `GET /api/summary/` - Get summary statistics
- `POST /api/upload/` - Upload CSV data
- `GET /api/generate-pdf/` - Generate PDF report

## 💡 Tips

- **Refresh Button**: Click the refresh button on any tab to reload the latest data
- **CSV Format**: Ensure your CSV has columns: equipment_name, equipment_type, flowrate, pressure, temperature
- **Dark Theme**: The desktop app uses a modern dark theme for reduced eye strain
- **Real-time Updates**: Use the refresh button to get the latest equipment data

## 🐛 Troubleshooting

### Backend Issues
- Ensure Django server is running on port 8000
- Check database migrations are up to date
- Verify virtual environment is activated

### Frontend Issues
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check backend API is accessible

### Desktop App Issues
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify backend API is running
- Check API base URL in `api_client.py` (default: `http://127.0.0.1:8000/api`)

