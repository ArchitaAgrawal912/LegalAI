# Step 1: Use a lightweight version of Python as our base computer
FROM python:3.12-slim

# Step 2: Create a folder named '/code' inside the Docker container
WORKDIR /code

# Step 3: Copy the requirements file from your laptop into the container
COPY ./requirements.txt /code/requirements.txt

# Step 4: Install all the Python libraries listed in the requirements file
RUN pip install --no-cache-dir -r /code/requirements.txt

# Step 5: Copy your entire 'app' folder from your laptop into the container
COPY ./app /code/app

# Step 6: Tell Docker that our application will run on port 8000
EXPOSE 8000

# Step 7: The command to start the FastAPI server using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]