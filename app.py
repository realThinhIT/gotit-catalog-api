from main import app
import os

# Retrieve environment configurations
_port = int(os.getenv('PORT', 8080))

# Execute the application given that this file is run
# as the entrance script.
if __name__ == '__main__':
    app.run(
        port=_port
    )
