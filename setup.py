"""
An simple script to install all the runtime dependencies required of Oncrop.

@author: Elias Gabriel, Duncan Mazza
@revision: v1.0
"""
import subprocess
from source.api.cv_classes import ProcessingEngine


def cmd(command, *args):
	""" Executes the given command as a subprocess with the given arguments. """
	subprocess.run(' '.join([command, *args]), shell=True, check=False)


# Execute if run directly from the command line
if __name__ == "__main__":
	print(" ===== Installing Python dependencies...")
	cmd("pip", "install", "opencv-python Flask Flask-Session redis")

	# Download the latest Redis source
	print("\n ===== Downloading Redis...")
	cmd("mkdir", "-p ./tmp")
	cmd("wget", "http://download.redis.io/redis-stable.tar.gz", "-O ./tmp/redis.tar.gz", "-Nq", "--show-progress")
	cmd("cd ./tmp && tar", "xzf", "./redis.tar.gz")
	
	# Install Redis to the default command path (*NIX ONLY)
	print("\n ===== Installing Redis...")
	cmd("cd ./tmp/redis-stable && make")
	cmd("sudo cp", "./tmp/redis-stable/src/redis-server", "/usr/local/bin/")
	cmd("sudo cp", "./tmp/redis-stable/src/redis-cli", "/usr/local/bin/")

	# Delete the temporary directory	
	print("\n ===== Cleaning up artifacts...")
	cmd("rm -r ./tmp")

	print("\n ===== Generating AURCO markers...")
	ProcessingEngine.generate_markers(10)

	print("\nDependency installation complete!")
