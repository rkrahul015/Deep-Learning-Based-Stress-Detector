# py_charmer_hackfest_project

## Problem statement: 
For people doing work from home or students studying online, it has been observed that they are more in stress, and their screen time also increases, which affects their mental and physical health. We are supposed to make a Desktop based application which detects stress using some facial features, there screen time, there time spent typing, there browsing patterns (to understand what kind of content they consume, which can help in detecting their mentality), their physical movement (using some mobile application, should be integrated with the whole system), using any combination of these features, generate the report for users which can help them to detect stress level there are going through and based on that provide them required bits of advice to improve their work style or way of studying.

## Solution approach:
We are providing an applied AI base solution for this problem. We will provide a desktop application to users. We will detect the required attributes needed to process and send it to the server, where we will perform the required processing and send the Report and required alert to the users.
	
### Stress Detection:
Face features analysis: we will collect real-time facial data of users using the webcam. We will detect the features like eyebrows' relative position and eye blinking rate To predict the stress level of users using Deep Learning Algorithms, and if stress levels go beyond our set threshold value, we will detect and store that later by processing this data, we will generate a report, on regular intervals based on user preferences.
    
### Steps moved by the client (mobile application)
A mobile application keeps tracking the number of steps moved by the user on that day, and this is a very critical parameter, so we were updating the exact steps movement after every 5 seconds to the main server even if the person hasn't made any significant change to understand the stress management of the users.

### Browsing Pattern:
We will keep track of the browsing pattern of users; here, we will not store the IP address of website user visits instead, we will store the kind of website user visits like (social media, e-commerce, streaming platforms, information websites, etc.), we would have already made clusters for kind of websites, and using this data we will generate the required report.

## Some instances of our project
![mobile-app](/screenshots/mobile-app.png)
![desktop-app](/screenshots/desktop-app.png)


## TechStack: following are the tech stack we are using to develop the product.
1. Tkinter (Desktop application), GUI library of python
2. FastAPI( webBackEnd ), backend framework of python
3. Opencv, for collection and processing image data
4. Tensorflow and keras : for Deep Learning used in facial stress detection.
5. Mysql, mongodb: for Database 
6. Numpy, pandas, matplotlib : for performing data science related processing.
