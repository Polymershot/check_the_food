# Summary

The main goal of this project was to create a prototype for a pseudo-nutrition checker web application using a ml model. This idea was based on "GroceryDB", which is a database that contains nutritional information on various foods from popular grocery stores. Using their results, I tried to train a basic ml model on their data to see if I could match their own models. Unfortunately, the data the data they provided was already transformed but they did not disclose what transformations they used so I tried my best. The model is trying to predict how "processed" a food is, on a scale of 1-4, based on various nutrients of a certain food item. Although the model performs horribly, the user is able to get a prediction by inputting various nutrients and retrieve the previous 5 predictions as well as the corresponding user data. The front-end is run on Streamlit Community Cloud while the back-end relies on a fastapi app contained in Google Cloud Run that connects with Google Firestore to store user input/output data. 

**GroceryDB**:
> https://github.com/Barabasi-Lab/GroceryDB

**Pipeline Diagram**:
![image](https://github.com/user-attachments/assets/5226f932-a639-4bbf-b224-1ae7224b4ba2)

**Streamlit Link**:
> https://checkthefood-893cd7rnas2rwy844pm4dy.streamlit.app

# Project Development Process

1. Clean GroceryDB data
2. Create ML model for GroceryDB data, using RandomSearchCV, and save it as a pickle file
3. Figure out what cloud platform to use to make the project completely free (Google Cloud Platform)
4. Create a service account and acquire the json key file as well as set the appropriate credentials
5. Find out how to create a FastAPI application that connects to Google Cloud Firestore as well as make predictions
6. Originally, GPT suggested to use GCR but artifact registry was the correct place to push the docker image created from the FastAPI app
7. Authorizing credentials for the docker image was quite difficult so I settled on implementing an environemntal variable for the docker image
8. Push the docker image that contains the fastapi app to the Artifact Registry repository by tagging it appropriately
9. Then, I had to deploy it with Google Cloud to "materialize" it. (I have to do more research on this topic)
10. Now, the api can send info and be requested through Google Cloud Run. The api also interacts with a Google Firestore database.
11. Make a streamlit application with an introduction, a way for the user to input data for 12 various nutrients of a food item, a way for the user to retrieve the last 5 user input/output data
12. I wanted to make sure there was a loading indication to let the user know the application is not frozen after pressing certain button(s)
13. Send an error message if there is a problem with the api via the status code or if no data was sent back or received
14. Test if the Google Firestore Database only contains 5 rows, user prediction works, no costs whatsoever, and data retrieval works
15. Everything works but ml model predictions are quite awful

# Recommendations/Remarks

I know using GPT is probably not ideal but the boilerplate code was quite useful for a foundation. However, I need to understand the GET and POST app decorator methods more when it comes to creating FASTAPI applications. If I were to spend more time with this project, I would look to see if I could reduce storage with the dockerfile, ml model, and cloud database. Also, looking into the syntax for caching Google Firestore databases as well as on the front-end side with streamlit would definitely be handy. I severely underestimated the syntax needed to create a streamlit appllication that connects with an api contained in Google Cloud Run. 

In terms of the ml model, I should've utilized parallelization to come up with the predictions but the limitations of the free tier of Google Cloud Run might incur some costs. Looking into the "GroceryDB" research papers could help with demystifying the transformed data. The ideal model would actually be a convolutional neural network model that looks at a user submitted-picture of the nutrition facts and extracts the relevent nutrients. However, it would need to make sure it is in units per 100g.In addition, more domain knowledge about food and nutrients would've led to a more informed model selection and feature engineering/selection. 

In terms of caching, I need to look into caching on the front-end vs back-end. From my understanding, Streamlit Community Cloud operates on a virtual machine as well as Google Cloud Run. My thinking is that caching on the front-end side would mostly affect users that repeatedly make the same predictions or keep on requesting data without making predictions. Caching on the back-end would mostly affect multiple users who make the same kind of predictions. However, caching the Google Firestore database doesn't seem to make sense since the database only changes if a new prediction comes in. So, the bottom line is determining, in a hypothetical scenario, how frequently users are making predictions on the same kind of items. Caching the front-end when it comes to the data retrieval and predictions makes sense though.

# Conclusion

You know, at first, I thought creating a web app that uses a ml model to create predictions from user input wouldn't be that bad but it was quite the headache. I would say the most frustrating part was connecting to the cloud and setting everything up. I would've tried to write more code but after finally pushing the docker image to Artifact Registry, I was just about done to be honest. I think I could easily scale up the cloud databse to contain more than 5 rows if I did more optimizing on the front-end and back-end side. Also, working on unit testings as well as CI/CD to streamline if everythhing is working properly. The idea is to know what step/job failed and why. This makes debugging way easier instead of trying to just throw mud at the wall and see what sticks. I know I haven't even dealt with batch or streaming data but I really think this project layed the foundating for data pipelines and ml model deployment.


