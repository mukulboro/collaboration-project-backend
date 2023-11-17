# Backend - TaskSphere
Backend Repository for **TaskSphere - Project Collaboration**.  Developed in `Django` by Mukul Aryal.

# API Documentation
## User Routes 
 1. **User Registration**
	 - URL: `/users/register/` 
	- Method: `POST`
	- Request Body (Multipart Form Data)
	- - `username`
	- - `password`
	-  - `profile_pic`
	-  - `first_name`
	-  - `last_name`
	-  - `email`
	- Response (200)
	-  - `{"success":"Created New User With Credentials"}`
	- Response (400)
	- - `{"error":"Username already in use"}`
	-----
	 2. **User Login**
	 - URL: `/users/login/` 
	- Method: `POST`
	- Request Body (JSON)
	- - `username`
	- - `password`
	- Response (200)
	-  - `{"success":"Login Successful", 
		"username": "abcd", 
		"userID": 7,
		"token" : "SECRETTOKEN",
		"profile_picture" : "/media/media/profile/abcd.jpg"}`
	- Response (401)
	- - `{"error":"Invalid Credentials"}`
	-----
	3. **Dashboard Metadata**
	 - URL: `/users/login/` 
	- Method: `GET`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Response (200)
	-  - `[{"project_id":  3, 
"project_name":  "First Project", 
"teams":  [{"id": 1,"name":  "Team1","isLead":  true}]}
]`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----
	
	4. **User Logout**
	 - URL: `/users/logout/` 
	- Method: `DELETE`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Response (200)
	-  - `{"success":"Logout Successful"}`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----