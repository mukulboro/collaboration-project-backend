# Backend - TaskSphere
Backend Repository for **TaskSphere - Project Collaboration**.  Developed in `Django` by Mukul Aryal.

# API Documentation
This section includes the documentation for the frontend API. Do note that this section excludes the entirety of the admin dashboard and its associated routes.
**Make sure that all routes end with a slash (/) otherwise the server will throw an error**

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

## Project Media Routes
1. **Get Media List**
	 - URL: `/cdn/project-media/` 
	- Method: `GET`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (JSON)
	- - `project` (project id)
	- Response (200)
	-  - `[{"id":2, "name":"abc.jpg", "image_slug":"/media/abc.jpg", "thumbnail_slug":"/media/jfk.jpg", "created_at":"2022-02-01"}]`
	-----
2. **Upload New Media**
	 - URL: `/cdn/project-media/` 
	- Method: `POST`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (Multipart Form Data)
	- - `project` (project id)
	- - `image` (file)
	- Response (200)
	-  - `{"success":"Creeated new project media"}`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----
3. **Delete Media**
	 - URL: `/cdn/project-media/` 
	- Method: `DELETE`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (JSON)
	- - `media` (media id)
	- Response (200)
	-  - `{"success":"Deleted Media"}`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----
## Document Routes
1. **Get Document List**
	 - URL: `/cdn/documents/` 
	- Method: `GET`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (JSON)
	- - `project` (project id)
	- Response (200)
	-  - `[{"id":2, "title":"ABCD", "body":"markdown body", "created_at":"2022-02-01"}]`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----
2. **Upload New Document**
	 - URL: `/cdn/documents/` 
	- Method: `POST`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (JSON)
	- - `project` (project id)
	- - `title`
	- - `body`
	- Response (200)
	-  - `{"success":"Creeated new document"}`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----
3. **Delete Document**
	 - URL: `/cdn/documents/` 
	- Method: `DELETE`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (JSON)
	- - `document` (media id)
	- Response (200)
	-  - `{"success":"Deleted Document"}`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----