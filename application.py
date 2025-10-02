from app import create_app

# Expose the Flask app as 'application' for EB
application = create_app()
