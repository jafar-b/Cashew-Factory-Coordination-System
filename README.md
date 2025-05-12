# Cashew Factory Coordination System (Desktop)
A desktop application built using Python Tkinter to organize and maintain the daily activities of a small-scale cashew factory.

## Activities Included:
1) Sales details management
2) Expense details management
3) Stock and production management through raw materials
4) Labor attendance and salary payout management
5) Client information
6) Monthly report generation

## Functionalities:
1) Registration and Login
2) View last day's expenses, sales, and pending payments
3) Add Sales
4) Manage Stocks by adding raw material and production details
5) Mark Attendance and overtime hours and process salary payments for labors
6) Add clients
7) View monthly report cards of sales, raw material, production, and stocks
8) Backup data for each transaction through MySQL

## Libraries Used:
- tkinter
- sqlite3
- PIL (Python Imaging Library)
- log_maker
- datetime
- date
- mysql2

## Dependencies:
- Python v3 or later
- Tkinter v3 or later
- Google Cloud Service Account
- mySql database

## Usage

### Setting Up Google Cloud Service Account

To use the system with Google Cloud services, you will need to create a `credentials.json` file containing the following fields:

### Fields to Include:

You must create a `credentials.json` file either by downloading the credentials from your Google Cloud console or by manually creating it with the following structure:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR-PRIVATE-KEY-HERE\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account-email@your-project-id.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email%40your-project-id.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

```
### Setting Up Google Cloud Service Account

1. **Create a Service Account**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new service account in your project.
   - Download the JSON file containing the service account credentials.

2. **Manually Create the JSON**:
   - If you prefer to create the file manually, make sure to replace the placeholders (like `your-project-id`, `your-private-key-id`, etc.) with the actual values from your Google Cloud service account.

3. **Save the File**:
   - Save the file as `credentials.json` in the root directory of the application.

### Running the Application

#### 1) Using Executable File:
   - Download the `.zip` file of the application.
   - Extract the contents to a folder.
   - After extraction, run the `index` file to start the application.

#### 2) Using Python File:
   - To run the application using Python, ensure you have Python and Tkinter installed.
   - Then, run the following command in your terminal:

   ```bash
   python index.py
```

Research Paper of this project published in 
International Journal of Scientific Research in Engineering and Management, 
  [Cashew-Factory-Coordination-System-integrated-with-Real-Time-Monitoring-and-Automation.pdf](https://github.com/user-attachments/files/20162738/Cashew-Factory-Coordination-System-integrated-with-Real-Time-Monitoring-and-Automation.pdf)   

    
![researchppr certificate](https://github.com/user-attachments/assets/c7a1bd04-7e20-4f7f-993f-72823abcf63e)


