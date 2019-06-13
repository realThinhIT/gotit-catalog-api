from main import app
import os

# Retrieve environment configurations
_port = int(os.getenv('PORT', 5000))

# Execute the application given that this file is run
# as the entrance script.
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=_port
    )
