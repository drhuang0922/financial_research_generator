FROM apache/airflow:2.1.2-python3.8

# Install any additional packages you need
RUN apt-get update && apt-get install -y \
    # package1 \
    # package2 \
    && rm -rf /var/lib/apt/lists/*

# Copy your DAGs, plugins, and config files
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY config/ /opt/airflow/config/

# Install any additional Python packages you need
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the AIRFLOW_HOME environment variable
ENV AIRFLOW_HOME=/opt/airflow

# Configure Airflow
RUN airflow db init
RUN airflow users create \
    --username admin \
    --password admin \
    --firstname testName \
    --lastname testLastName \
    --role Admin \
    --email admin@example.com

# Expose the Airflow webserver and scheduler ports
EXPOSE 8080 8793

# Start the Airflow scheduler and webserver
CMD ["bash", "-c", "airflow scheduler & airflow webserver"]
