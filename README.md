# Customized chatbot

This repo contains the instructions and code for the creation of a customized chatbot that can be embedded into a qualtrics survey.
It is customized because you can change for the model that you want (gpt3.5, gpt4, etc.) and because you can customize system instructions.
The goal is that you can easily customize OpenAI chatbots to behave however you want and embed them into qualtrics for running experiments.

## FIRST, you'll need:
There is a lot you'll need before you begin building your chatbot app. This will take more time than actually developing the app.
- An account with the OpenAI API. 

You'll need to set up a payment method and get an API key (https://platform.openai.com/docs/api-reference/authentication).
- A mySQL database hosted online.

In this tutorial, I'll be using google cloud for hosting. It's one of the easiest ways to do it. If you want to do it the same way, you'll have to create an account and set up payment method.(https://console.cloud.google.com).
You will also need to create a database and get all its credentials (user, passoword, IP, port)
- A Streamlit account.

A free account works.
- A Github account.

You need it to launch you project in streamlit.

- A bunch of things installed on your pc. Included but not limited to python3, streamlit, git, mysql...

- An editor for the code. I recommend VSCode. 

### Step 1: Fork it
Fork this repository in your own github.

### Step 2: OpenAI API key
Figure out your OpenAI API key and the credentials for the google cloud SQL db.

### Step 3: Streamlit
Create an app on streamlit and select the forked github repo as the source.
Under your app, go to settings and set up all the secrets in there (API_KEY, sql_user, sql_password, sql_host, sql_port, sql_database).

### Step 4: Set up MySQL database on Google Cloud
Create an instance, create a database, get all your keys.

### Step 5: Qualtrics
Create a new qualtrics survey and create a Text/Graphic question.
Under "Question Behavior" select "javascript".
Paste the following code (make sure to substitute the values in [YOUR-DOMAIN] by the name of your streamlit app).

```Qualtrics.SurveyEngine.addOnload(function()
{
    // This function will create the iframe and add it to your Qualtrics question
    
    // Create the iframe element
    var iframe = document.createElement('iframe');
	var userID = "${e://Field/ResponseID}";  // Fetch the ResponseID from Qualtrics
    
    // Set the source of the iframe to your chatbot's URL
	iframe.src = "https://[YOUR-DOMAIN].streamlit.app/?embed=true&userID=${e://Field/ResponseID}";

    // Set some styles for the iframe (you can adjust this to your needs)
    iframe.style.width = '100%';  // Take the full width of the parent container
    iframe.style.height = '500px'; // Set a fixed height (or adjust as needed)
    iframe.style.border = 'none';  // Remove any default borders

    // Find a placeholder in your Qualtrics question 
    // (for this example, we'll assume there's a div with an id of 'chatbotPlaceholder')
    var placeholder = document.getElementById('chatbotPlaceholder');
    
    // Append the iframe to the placeholder
    placeholder.appendChild(iframe);
});

Qualtrics.SurveyEngine.addOnReady(function()
{
    // If you need any functionality to run after the page is fully displayed, you can add it here
});

Qualtrics.SurveyEngine.addOnUnload(function()
{
    // If you need any functionality to run when the page is unloaded, you can add it here
});
```

### Step 6: Publish the survey and test it.
For testing, you'll chat with the chatbot. To make sure it's working:
- ensure there are no error messages;
- ensure that your data is recorded properly on your database by downloading it from google cloud and checking if all fields are filled correctly (user id, date, time, content).

### Step 7: Customize it!
Now that the app is working, customize the app. To change the chatbot behavior, there are two main things you can do:
1) change the message on "start_message", where we tell the system how to behave.
2) Changing and adding arguments to the "openai.ChatCompletion.create". There are many thing you can change (max number of tokens used, you can penalize certain words to decrease their frequency, change system temperature, etc.). You can check how to do it in https://platform.openai.com/docs/guides/gpt

And there you have it!

