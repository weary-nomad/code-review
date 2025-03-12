# For this challenge you are presented with the application for internal employees of an organization. 
# For brevity pretend each function after login simply checks for the presence of an active 'employeesession' cookie value before running the rest of the code.

from flask import Flask, render_template, request, jsonify
import socket
import platform
import os
import subprocess
import json
import re
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template('home.html')
  elif request.method == "POST":
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    if username and password:
      # Call to database to verify login is correct and get a session token
      cookie = 'generated_session_token_from_dbcall'
      response = jsonify({'status': 'Login succeeded!'})
      response.set_cookie('employeesession', value=cookie, max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None)
      return response
      
@app.route('/employees', methods=['GET'])
def home():
  return render_template('home.html')

@app.route('/employee-tools', methods=['POST'])
def employeeTools():
  return render_template('employeeTools.html')

# This function checks if the administrative APIs are online
@app.route('/employee-tools/health-check', methods=['POST'])
def healthCheck():
  try:
    response = requests.get('https://127.0.0.1:20505')
    if response.status_code == 200:
      return jsonify({'status': 'Healthy'})
    else:
      return jsonify({'status': 'Not Healthy', 'code': response.status_code})
  except requests.exceptions.RequestException as e:
    return jsonify({'status': 'Not Healthy', 'error': str(e)})

# This function checks to see if the provided subdomain of the company is accessible to this employee or not by providing the employee's cookie for the subdomain to check.
@app.route('/employee-tools/domain-check', methods=['POST'])
def domainCheck():
  domain = request.json.get('domain', '')
  if domain:
    if not re.match(r'internal.company.domain', domain):
      return jsonify({'error': 'This domain will not be owned by the company.'})
    employeesessionValue = request.cookies.get('employeesession')
    fullDomain = "https://" + domain
    response = requests.get(fullDomain, cookies={'employeesession': employeesessionValue})
    if response.status_code == 200:
      return jsonify({'response': 'You have access to this subdomain!'})
    elif response.status_code == 401:
      return jsonify({'response': 'You do not have access to this subdomain'})
    else:
      return jsonify({'error': 'Something went wrong, try again.'})

# This functions accepts a bug report and sends the data from it to an administrative API
@app.route('/employee-tools/report-bug', methods=['GET', 'POST'])
def reportBug():
  if request.method == "GET":
    return render_template('bugreport.html')
  elif request.method == "POST":
    reportMessage = request.json.get('report', '')
    if not re.match(r'^[a-zA-Z0-9.!? ]+$', reportMessage):
      return jsonify({'status': 'Error', 'message': 'Invalid characters in the report'}), 400
    reportData = {
        'Report Date': datetime.now().strftime('%Y-%m-%d'),
        'Report Time': datetime.now().strftime('%H:%M:%S'),
        'Report Message': reportMessage
    }
    response = requests.post('https://127.0.0.1:20505/internal/bugreports', json=reportData)
    if response.status_code == 200:
      return jsonify({'status': 'Reported Successfully!'})
    else: 
      return jsonify({'status': 'Try reporting again.'})
    
if __name__ == '__main__':
  app.run(debug=True)
