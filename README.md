**Bunker-Website**
----

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)
![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)


  This is a GUI version of the Bunker-API along with some visualization charts to see your attendence.
  > ![image](https://user-images.githubusercontent.com/62739618/163450385-539888fd-f00b-431f-8881-ea2057722f81.png)
 
## Website Link

Check out the website [link](https://bunker-api-prj.herokuapp.com/)😎

----

**Bunker-API-AnyONE**
----
  The API call takes total class_code,total_class,total_present and threshold as input and return days to take leave or not!!.

* **URL**

  https://bunker-api-prj.herokuapp.com/senddata_attendance

* **Method:**

  `POST`  
  
*  **URL Params**
   
   None
   
* **Data Params**

   **Required:**
   
   ```
    POST /senddata_attendance HTTP/1.1
    Host: bunker-api-prj.herokuapp.com
    Content-Type: application/json
    Content-Length: 186

    {
      "class_code" : ["ABC101","ABC102","ABC103","ABC104","ABC105"],
      "total_hours" : ["35","35","32","34","35"],
      "total_present" : ["20","30","32","25","19"],
      "threshold" : "75"

    }
    ```

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    ```json
     
    {
      "ABC101": {
          "class_to_attend": 25,
          "percentage_of_attendance": 0.57,
          "total_hours": 35,
          "total_present": 20
      },
      "ABC102": {
          "class_to_bunk": 5,
          "percentage_of_attendance": 0.86,
          "total_hours": 35,
          "total_present": 30
      },
      "ABC103": {
          "class_to_bunk": 10,
          "percentage_of_attendance": 1.0,
          "total_hours": 32,
          "total_present": 32
      },
      "ABC104": {
          "class_to_attend": 2,
          "percentage_of_attendance": 0.74,
          "total_hours": 34,
          "total_present": 25
      },
      "ABC105": {
          "class_to_attend": 29,
          "percentage_of_attendance": 0.54,
          "total_hours": 35,
          "total_present": 19
      }
    }
    ```

 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** 
    ```json
    {
      "error" : "Given input details does not match up!!"
    }
    ```

* **Sample Call:**

  ```javascript
  fetch('https://bunker-api-prj.herokuapp.com/senddata_attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                      
                      "class_code" : ["ABC101","ABC102","ABC103","ABC104","ABC105"],
                      "total_hours" : ["35","35","32","34","35"],
                      "total_present" : ["20","30","32","25","19"],
                      "threshold" : "75"
                                
                                })
        })
            .then(resp => resp.text())
            .then(response => {
                var js = JSON.parse(response);
                console.log(js);
            }
            )
            .catch(error => console.log(error))
  ```
* **Notes:**

  Check out the API checking website with input and response [link](https://reqbin.com/pocyrwrd)



----


**Bunker-API**
----
  The API call takes upon the login details as parameter and returns scarped details from the website using the beautiful soup and days to take leave or not!.

* **URL**

  https://bunker-api-prj.herokuapp.com/send_attendance/<_rollno_>/<_pwd_>

* **Method:**

  `POST`  
  
*  **URL Params**

   **Required:**
 
   `username=[alphanumeric]`
   
   `pwd=[alphanumeric]`
   
* **Data Params**

  None

* **Success Response:**
  
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
    **Content:** 
    ```json
    {
    "error": "Invalid details try again"
    }
    ```

* **Sample Call:**

  ```javascript
  const response = await fetch('https://bunker-api-prj.herokuapp.com/send_attendance/1****1/******', {
    method: 'POST'
  });

  response.json().then(function (json) {
    console.log(json)
  }); 
  ```
