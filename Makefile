.PHONY: lint
lint: 
	python3 -m black airflow/dags
	pylint airflow/dags --disable=C,R

.PHONY : tests
tests:
	python -m unittest discover -s src/tests

pulumi-install:
	curl -fsSL https://get.pulumi.com | sh
	gcloud config set project $(GCP_PROJECT_ID)

infra-up:
	cd infra && pulumi up --yes

infra-down:
	cd infra && pulumi destroy --yes

run_airflow:
	sudo docker compose --file airflow/docker-compose.yaml up -d

build_streamlit_dashboard:
	docker build -t streamlit-dashboard:latest -f streamlit/Dockerfile .

run_streamlit_dashboard:
	docker run -p 8501:8501 --name streamlit_dashboard streamlit-dashboard:latest