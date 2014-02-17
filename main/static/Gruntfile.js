module.exports = function(grunt) {

	grunt.initConfig({

		pkg: grunt.file.readJSON("package.json"),

		watch: {
			options: {
				livereload: true
			},
			main: {
				files: [
					"src/css/*.less",
					"src/css/_partials/*.less",
					"src/js/*.js",
					"../templates/*.html"
				],
				tasks: ["less:devel"]
			}

		},
		less: {
			devel: { 

				files: {
					"src/css/main.css": "src/css/main.less"
				}
			},
			bootstrap: {
				files: {
					"src/css/bootstrap.css": "src/css/bootstrap_custom.less" 
				}
			}

		}

	});

	grunt.loadNpmTasks("grunt-contrib-less");
	grunt.loadNpmTasks("grunt-contrib-watch");


	grunt.registerTask("default", ["watch:main"]);
	grunt.registerTask("bootstrap_compile", ["less:bootstrap"]);

}
