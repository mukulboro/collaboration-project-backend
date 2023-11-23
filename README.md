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
		"fullName": "ABC DEF",
		"email": "abc@def.com",
		"token" : "SECRETTOKEN",
		"profile_picture" : "/media/media/profile/abcd.jpg"}`
	- Response (401)
	- - `{"error":"Invalid Credentials"}`
	-----
	3. **User Metadata**
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
## Dashboard Data Routes
1. **Get Announcements and Todos**
	 - URL: `/api/dashboard/` 
	- Method: `GET`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Response (200)
	-  - `{"announcements":[], "todos":[]}`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----
## ToDo Routes
1. **Get Todo List**
	 - URL: `/api/todos/` 
	- Method: `GET`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (query params)
	- - `team` (team id)
	- Response (200)
	-  - `[{"id":6, "title":"DEFG", "body":"todo body", "priority":"HIGH", "status": "TODO", "assigned_to": "myuername", "created_at":"2022-01-01"}]`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----
2. **Add New Todo**
	 - URL: `/api/todos/` 
	- Method: `POST`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (JSON)
	- - `team` (team id)
	- - `title`
	- - `body`
	- - `status` [integer value 0, 1 or 2]
	- - `priority` [integer value 0, 1 or 2]
	- - `assigned_to` [username]
	- Response (200)
	-  - `{"success":"Created new todo"}`
	- Response (401) [sent if token is invalid or if user is not team leader]
	- - `{"error":"Unauthorized"}`
	- Response (400) [sent if assigned_to username does not exist in team]
	- - `{"error":"Bad Request"}`
	-----
	3. **Delete Todo**
	 - URL: `/api/todos/` 
	- Method: `DELETE`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (JSON)
	- - `todo` (todo id)
	- Response (200)
	-  - `{"success":"Deleted todo"}`
	- Response (401) [sent if token is invalid or if user is not team leader]
	- - `{"error":"Unauthorized"}`
	-----
	3. **Update Todo (Status Only)**
	 - URL: `/api/todos/` 
	- Method: `PATCH`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (JSON)
	- - `todo` (team id)
	- - `status`[integer value 0, 1 or 2]
	- Response (200)
	-  - `{"success":"Updated todo"}`
	- Response (401) 
	- - `{"error":"Unauthorized"}`
	-----
## Team Members Routes
1. **Get Team Members List**
	 - URL: `/api/team-members/` 
	- Method: `GET`
	- Header
	- - `Authorization: Token SECRETTOKEN`
	- Request Body (query params)
	- - `team` (team id)
	- Response (200)
	-  - `[{"id":6, "username":"DEFG"}]`
	- Response (401)
	- - `{"error":"Unauthorized"}`
	-----

