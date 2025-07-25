# Demo Route Optimization


## Description
This project is demo version for Route Optimization project.


## Installation
- Install docker, vary depend on the OS, check https://docs.docker.com/engine/install/
- Build docker image (may need admin or sudo prefix), note that there is dot at the
end. You can change the image name and version to your own need:
    
        docker build -t image_name:version .
- Run container with the image created, change docker port and app port to the
actual port used:
    
        docker run -p 127.0.0.1:docker_port:app_port image_name:version


## Support
nguyennta@icloud.com


## Contributing
Project structure:
- model: contain AI models, include binary file or weights file, best point file.
- route: contain file for routing.
- service: contain service files.
- static: contain static files such as css, images.
- templates: contain html files.
- utilities: contain utility files.
- app.py: main file to run this project (Flask application is created here).
- Dockerfile: file used to containerize this project with docker.
- README.md: this project instruction file.
- requirements.txt: file contain the dependencies that need to install.


## Authors
This project is done by nguyennta@icloud.com


## License
This is a demo project for portfolio page.


## Project status
- Finished.
- Current host: https://demo-route-optimization-698202522757.asia-southeast1.run.app
- This project’s source code is hosted on GitHub, with CI/CD handled by Cloud Build 
and deployed via Cloud Run — both part of Google Cloud Platform (GCP).


## Feature:  
**NOTE: ** add "/api" before each. Example: "/api/optimize-route".
1. **"/optimize-route":** Optimize visit order of a route.  
2. **"/sale-route":** Optimize visit order with time window for location(s).
3. **"/check-overlap":** Check for overlapping routes. 
4. **"/suggest-frequency":** Suggest visit frequency for new customer.  
5. **"/cluster-customer":** Cluster customers base on their geography locations.
6. **"/check-ddo":** Check route (ddo - distance, duration, order), warning if 
it's distance, duration is too long/short or visit order not optimized (removed in 
this demo).
7. **"/check-frequency":** Check if revenue or order count is too many/less compare 
with other customers who has the same visit frequency (removed in this demo).


## Details
**NOTE: ** add "/api" before each. Example: "/api/optimize-route".
1. POST at "/optimize-route":    
    1. Request:
        - Content type "application/json":

                {
                    "locations": [name or ID with depot at the end],
                    "distances": [
                        [distances from correspond location to others], []
                    ],
                    "durations": [
                        [durations from correspond location to others], []
                    ],
                    "working_distance": (optional) integer (default 200,000 m),
                    "search_time": (optional) integer (in second - default 3),
                    "num_vehicles": (optional) number of vehicle (default 1)
                }  

        - "locations": name or ID of locations, depot is the last one.
        - "distances": 2D array, each row is the distances from correspond location
        to others.
        - "durations": 2D array, each row is the durations from correspond location
        to others.
        - "working_distance": (optional) maximum working distance of a vehicle in 
        meters, default 200,000 (200 km).
        - "search_time": (optional) maximum time for optimizing the route in
        seconds, default 3.
        - "num_vehicles": (optional) number of vehicles in this route, default 1.
    2. Response:
        
            {
                "code": interger similar to http code,
                "message": string,
                "data": [
                    {
                        "route": [locations visit order],
                        "distances": [distances of each leg],
                        "durations": [durations of each leg],
                        "total_distance": total distance,
                        "total_duration": total duration
                    },
                    {}
                ]
            }
        - "code": 200 is success, and others similar to http code.
        - "message": "Success" or others depend on result.
        - "data": list of optimized routes, the number of routes equal number of  
        vehicles. Data may be an empty list even code 200, check message.
    3. In real project:
        - Check DB for this route (get data within 28 days only), return result 
        if already optimized.
        - If less than 26 locations: call GG Route API for result (it supports
        optimize for 25 intermediates at the time this project was building).
        - From 26 locations: check DB for duration and distance information (get
        data within 28 days only), or call GG Route API if we do not have. Then
        create distances and durations matrices, use OR Tools to optimize the route.
        - Save optimized route, distances, durations to DB for future use.
    4. In this demo:
        - Input the distances and durations matrices and use OR Tools to optimize
        the route.
        - Just optimize maximum 15 locations (include depot).

2. POST at "/sale-route":
    1. Request:
        - Content type "application/json":

                {
                    "locations": [name or ID with depot at the end],
                    "time_windows": [[from, to], []],
                    "distances": [
                        [distances from correspond location to others], []
                    ],
                    "durations": [
                        [durations from correspond location to others], []
                    ],
                    "start_time": (optional) hh:mm (default '08:30'),
                    "lunch_start": (optional) hh:mm (default '12:00'),
                    "lunch_break": (optional) integer (in minutes - default 60),
                    "waiting_time": (optional) integer (in minutes - default 5),
                    "visit_duration": (optional) integer (in minutes - default 10),
                    "working_time": (optional) integer (in minutes - default 720),
                    "search_time": (optional) integer (in second - default 3),
                    "num_vehicles": (optional) number of vehicle (default 1)
                }  

        - "locations": name or ID of locations, depot is the last one.
        - "time_windows": time windows for locations (exclude depot), can leave
        empty list for locations that not need time window configuration.
        - "distances": 2D array, each row is the distances from correspond location
        to others.
        - "durations": 2D array, each row is the durations from correspond location
        to others.
        - "start_time": time that the vehicles start in hh:mm format, default "08:30".
        - "lunch_start": time for lunch in hh:mm format, default "12:00".
        - "lunch_break": time duration, default 60 minutes
        - "waiting_time": time allow to wait in a location before moving to the next
        place, default 5 minutes
        - "visit_duration": time spend in a location, default 10 minutes
        - "working_time": (optional) maximum working time in minutes, default 720
        (12 hours).
        - "search_time": (optional) maximum time for optimizing the route in
        seconds, default 3.
        - "num_vehicles": (optional) number of vehicles in this route, default 1.
    2. Response:
        
            {
                "code": interger similar to http code,
                "message": string,
                "data": [
                    {
                        "route": [locations visit order],
                        "visit_times": [[visit time for each location], []],
                        "lunch_time": [start, end],
                        "distances": [distances of each leg],
                        "durations": [durations of each leg],
                        "total_distance": total distance,
                        "total_duration": total duration
                    },
                    {}
                ]
            }
        - "code": 200 is success, and others similar to http code.
        - "message": "Success" or others depend on result.
        - "data": list of optimized routes, the number of routes equal number of  
        vehicles. Data may be an empty list even code 200, check message.
    3. In real project:
        - Check DB for optimized route (within 28 days) and return if already had it.
        - Else call GG Route API for distance, duration between locations to make
        matrices. Optimize the route using OR Tolls.
        - Save optimized route, distances, durations to DB for future use.
    4. In this demo:
        - Input the distances and durations matrices and use OR Tools to optimize
        the route.
        - Just optimize maximum 15 locations (include depot).
    5. Note:
        - Time windows must not overlap lunchtime.
        - Optimize sale route for a day, so time limits at "23:59".

3. POST at "/check-overlap":  
    1. Request:
        - Content type "application/json":

                {
                    "names": [routes names or IDs]
                    "routes": [[[lat, long], []], [[lat, long], []], []]
                } 

        - "names": list of routes names or IDs.
        - "routes": locations coordinates in each route is pairs of latitude,
        longitude.
    2. Response:
        
            {
                "code": interger similar to http code,
                "message": string,
                "data": [[overlap routes], []]
            }
        - "code": 200 is success, and others similar to http code.
        - "message": "Success" or others depend on result.
        - "data": list of overlap routes (in pair).
    3. In real project:
        - Query DB for routes due to condition in request.
        - Query coordinates of customer in each route.
        - Check for overlap routes.
    4. In this demo:
        - Input the coordinates in request.
        - Check for overlap routes.
    5. Note:
        - Need at least 3 coordinates in a route.

4. POST at "/suggest-frequency":
    1. Request:
        - Content type "application/json":

                {
                    "order_amount": average revenue each month,
                    "order_count": average orders each month,
                    "channel": sell channel ("GT_100", "GT_200", "GT_300",
                               "GT_400", "KA_700", "Others"),
                    "class_id": shop class ("N1", "N2"),
                    "territory": territory ("BTB", "DBSCL", "DNB", "HCM", "TB"),
                    "branch_id": distributor ID ("10000342", "MARVAL", "Others"),
                    "shop_type": shop type ("101", "102", "201", "305",
                                 "402", "Others"),
                    "state": state ("43", "79", "80", "Others"),
                }
        - "order_amount" and "order_count" is numeric.
        - Other fields is string and must contain one of the values above.
    2. Response:
        
            {
                "code": interger similar to http code,
                "message": string,
                "data": frequency
            }
        - "code": 200 is success, and others similar to http code.
        - "message": "Success" or others depend on result.
        - "data": suggested frequency ("F1", "F2", ...).
    3. In real project and this demo:
        - Select features base on feature engineering and BA (hand pick).
        - Build some classification models using scikit-learn, fine-tune and choose
        the best model.
        - Feed customer information into classification model.
        - Use result as suggest frequency.
    4. Note:
        - Classification model was trained on dummy data for demo only.

5. POST at "/cluster-customer":  
    1. Request:
        - Content type "application/json":

                {
                    "coordinates": [[lat, long], []],
                    "groups": integer - number of groups want to cluster
                }
        - "coordinates": coordinates of locations to cluster.
        - "groups": number of group that locations will be split into.
    2. Response:
        
            {
                "code": interger similar to http code,
                "message": string,
                "data": [labels]
            }
        - "code": 200 is success, and others similar to http code.
        - "message": "Success" or others depend on result.
        - "data": list of labels correspond to locations.
    3. Note:
        - Labels are numeric start with 0, 1, ...

6. POST at "/check-ddo":  
    1. Removed in this demo.
    2. In real project:
        - Query routes from DB.
        - Calculate distance, duration and compare with standards.
        - Check DB if the route is optimized, else call the optimize function.

7. POST at "/check-frequency":  
    1. Removed in this demo.
    2. In real project:
        - Query order history of customers who has same frequency.
        - Calculate average range with statistic:
            - lower = Q1 - 1.5 * IQR
            - upper = Q3 + 1.5 * IQR
            - IQR = Q3 - Q1
            - Q1 = First quartile (25th percentile)
            - Q3 = Third quartile (75th percentile)
        - Check if avenue, orders are within the range.
    3. Note:
        - If DB is very large, consider calculate the average interval periodically
        and save to DB instead of query and calculate every time.
        - And can consider to calculate the average base on customers within the
        same area, not all customers.
