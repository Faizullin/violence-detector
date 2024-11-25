#!/bin/bash

# Check for environment argument
if [ -z "$1" ]; then
    echo "Error: Environment (dev or prod) is required as the first argument."
    echo "Usage: helper.sh [dev|prod] [action] [additional_args]"
    exit 1
fi

# Check for action argument
if [ -z "$2" ]; then
    echo "Error: Action is required as the second argument."
    echo "Available actions: build, collectstatic, migrate, seed, shell, deploy"
    exit 1
fi

# Set environment and compose file
ENV="$1"
ACTION="$2"
COMPOSE_FILE="../backend/docker-compose${ENV}.yml"

# Verify valid environment
if [ "$ENV" != "dev" ] && [ "$ENV" != "prod" ]; then
    echo "Error: Invalid environment. Use 'dev' or 'prod'."
    exit 1
fi

# Define actions
case $ACTION in
build)
    echo "Building for $ENV environment..."
    docker-compose -f "$COMPOSE_FILE" build
    ;;
collectstatic)
    echo "Collecting static files for $ENV environment..."
    docker-compose -f "$COMPOSE_FILE" exec web python manage.py collectstatic --noinput
    ;;
migrate)
    echo "Running migrations for $ENV environment..."
    docker-compose -f "$COMPOSE_FILE" exec web python manage.py migrate
    ;;
seed)
    if [ -z "$3" ]; then
        echo "Error: Seed file is required for the seed action."
        echo "Usage: helper.sh $ENV seed [seed_file]"
        exit 1
    fi
    SEED_FILE="$3"
    echo "Seeding database with $SEED_FILE for $ENV environment..."
    docker-compose -f "$COMPOSE_FILE" exec web python manage.py loaddata "$SEED_FILE"
    ;;
shell)
    echo "Opening shell for $ENV environment..."
    docker-compose -f "$COMPOSE_FILE" exec web sh
    ;;
deploy)
    echo "Deploying to $ENV environment..."
    docker-compose -f "$COMPOSE_FILE" down
    docker-compose -f "$COMPOSE_FILE" pull
    docker-compose -f "$COMPOSE_FILE" up -d --build
    echo "Deployment complete!"
    ;;
*)
    echo "Error: Invalid action. Available actions: build, collectstatic, migrate, seed, shell, deploy"
    exit 1
    ;;
esac
