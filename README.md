**Bunker-API**
----
  _The API call takes upon the login details as parameter and returns scarped details from the website using the beautiful soup._

* **URL**

  _https://bunker-api-prj.herokuapp.com/send_attendance/<_rollno_>/<_pwd_>_

* **Method:**

  `POST`  
  
*  **URL Params**

   **Required:**
 
   `username=[alphanumeric]`
   
   `pwd=[alphanumeric]`

* **Success Response:**
  
  <_What should the status code be on success and is there any returned data? This is useful when people need to to know what their callbacks should expect!_>

  * **Code:** 200 <br />
    **Content:** 
  ```json
   {
   "1XXXXX":{
      "attendance_from":"21-02-2022",
      "attendance_to":"02-04-2022",
      "class_to_bunk":0,
      "percentage_of_attendance":77,
      "total_hours":21,
      "total_present":16
   },
   "1XXXXX":{
      "attendance_from":"21-02-2022",
      "attendance_to":"02-04-2022",
      "class_to_bunk":3,
      "percentage_of_attendance":86,
      "total_hours":21,
      "total_present":18
   },
   "1XXXXX":{
      "attendance_from":"21-02-2022",
      "attendance_to":"02-04-2022",
      "class_to_bunk":1,
      "percentage_of_attendance":80,
      "total_hours":20,
      "total_present":16
   },
   "1XXXXX":{
      "attendance_from":"21-02-2022",
      "attendance_to":"02-04-2022",
      "class_to_bunk":7,
      "percentage_of_attendance":92,
      "total_hours":35,
      "total_present":32
   },
   "1XXXXX":{
      "attendance_from":"21-02-2022",
      "attendance_to":"02-04-2022",
      "class_to_bunk":9,
      "percentage_of_attendance":100,
      "total_hours":28,
      "total_present":28
   },
   "1XXXXX":{
      "attendance_from":"21-02-2022",
      "attendance_to":"02-04-2022",
      "class_to_bunk":4,
      "percentage_of_attendance":86,
      "total_hours":28,
      "total_present":24
   },
   "1XXXXX":{
      "attendance_from":"21-02-2022",
      "attendance_to":"02-04-2022",
      "class_to_bunk":1,
      "percentage_of_attendance":79,
      "total_hours":28,
      "total_present":22
   },
   "1XXXXX":{
      "attendance_from":"21-02-2022",
      "attendance_to":"02-04-2022",
      "class_to_bunk":2,
      "percentage_of_attendance":80,
      "total_hours":35,
      "total_present":28
   }
  }
```

 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

  OR

  * **Code:** 422 UNPROCESSABLE ENTRY <br />
    **Content:** `{ error : "Email Invalid" }`

* **Sample Call:**

  <_Just a sample call to your endpoint in a runnable format ($.ajax call or a curl request) - this makes life easier and more predictable._> 

* **Notes:**

  <_This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here._> 
