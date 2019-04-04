"""
An script to configure install all the runtime dependencies required of Oncrop.

@author: Elias Gabriel
@revision: v1.6
"""
import subprocess


def cmd(command, capture=False):
	""" Executes the given command as a subprocess with the given arguments. """
	return subprocess.run(command, shell=True, check=False, capture_output=capture)


def header(message):
	print("\n\33[95m ===== " + message + "...\33[0m")


if __name__ == "__main__":
	# Confirm that FFmpeg is installed
	if cmd("ffmpeg -version", True).returncode != 0:
		print("\n\33[91m *** \33[4mInstallation error!\33[0m\33[91m ***")
		print(" FFmpeg is a required compiletime-runtime dependency.\n Please install FFmpeg using your package manager or manually by source, then retry installation.\n")
		exit(1)
	
	# Conda installs a "compatability version" of the GNU linker, which conviniently breaks packages that
	# must be compiled from source and link to temporary executabls, need to find header files, or
	# pretty much anything else. This is an extremely dumb yet critical step.
	if cmd("conda --version > /dev/null").returncode == 0:
		header("Verifying Conda installation")
		out = cmd("find ~ | grep -Hm1 'compiler_compat/ld' | cut -d: -f2", True)
		path = str(out.stdout, encoding="ascii").strip()

		if not path.endswith(".compat"):
			# Display warning message
			print("\n  \33[33m*** \33[4mWARNING\33[0m\33[33m ***\n   Conda provides a backwards compatible version of the GNU linker.\n   There is a bug in the linker that breaks dependencies that must be built\n   and installed from source. To prevent this, the linker will be thwarted.\33[0m")

			print("   -- Renamed compatability linker to ld.compat")
			cmd("mv " + path + " " + path + ".compat")

	# Download Python dependencies
	header("Installing pre-built Python dependencies")
	cmd("pip uninstall -q opencv-python")
	cmd("pip install -q opencv-contrib-python Flask Flask-Session redis aiortc")

	# Download the latest Redis source
	header("Downloading Redis")
	cmd("mkdir /tmp/oncrop-install")
	cmd("wget http://download.redis.io/redis-stable.tar.gz -NqO /tmp/oncrop-install/redis.tar.gz --show-progress")
	cmd("cd /tmp/oncrop-install && tar --totals -xzf ./redis.tar.gz")

	# Install Redis to the default command path
	header("Installing Redis")
	cmd("cd /tmp/oncrop-install/redis-stable && (make distclean && make) > /dev/null")
	cmd("sudo cp /tmp/oncrop-install/redis-stable/src/redis-server /usr/local/bin/")
	cmd("sudo cp /tmp/oncrop-install/redis-stable/src/redis-cli /usr/local/bin/")

	# Delete the temporary directory	
	header("Cleaning up temporary files and directories")
	cmd("rm -rf /tmp/oncrop-install")

	# Generate AURCO marker for detection
	header("Generating AURCO markers")
	from source.api.cv_classes import ProcessingEngine
	ProcessingEngine.generate_markers(10)

	print("\n*** \33[92mDependency installation complete!\33[0m ***")
