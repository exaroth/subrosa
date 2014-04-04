module.exports = function(grunt) {

	grunt.initConfig({

		pkg: grunt.file.readJSON("package.json"),

		clean: ["build"],

		concat: {

			js: {
				options: {
					separator: ";",
				},
				src: [
				"bower_components/jquery-color/jquery.color.js",
				"bower_components/bootstrap/js/alert.js",
				"bower_components/bootstrap/js/tooltip.js",
				"bower_components/bootstrap/js/popover.js",
				"bower_components/magnific-popup/dist/jquery.magnific-popup.js",
				"bower_components/nested/jquery.nested.js",
				"src/js/bootstrap3-confirmation.js",
				"src/js/jquery.unveil.js",
				"src/js/main.js"
				],
				dest: "src/js/scripts.js"
			},
			css: {
				src: [
				"src/css/bootstrap.css",
				"src/css/pygments.css",
				"src/css/fontello.css",
				"bower_components/magnific-popup/dist/magnific-popup.css",
				"src/css/main.css"
				],
				dest: "src/css/styles.css"
			}

		},

		cssmin: {
			minify: {
				expand: true,
				cwd: "src/css",
				src: ["styles.css"],
				dest: "src/css",
				ext: ".min.css"
			}
		},
		uglify: {
			scripts: {
				files: {
					"src/js/scripts.min.js": ["src/js/scripts.js"]

				}
			}
		},

		copy: {
			main: {
				files: [
				{ expand: true, cwd: "src/img/", src: "*", dest: "build/img" },
				{ expand: true, cwd: "src/font/", src: "*", dest: "build/font" },
				{ expand: true, cwd: "src/css/", src: "styles.min.css", dest: "build/css/" },
				{ expand: true, cwd: "src/js/", src: "scripts.min.js", dest: "build/js/" },
				]
			}

		},

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
	grunt.loadNpmTasks("grunt-contrib-cssmin");
	grunt.loadNpmTasks("grunt-contrib-clean");
	grunt.loadNpmTasks("grunt-contrib-uglify");
	grunt.loadNpmTasks("grunt-contrib-copy"); 
	grunt.loadNpmTasks("grunt-contrib-concat"); 


	grunt.registerTask("default", ["watch:main"]);
	grunt.registerTask("build", ["clean", "less:devel", "concat:css", "concat:js", "uglify", "cssmin", "copy"]);
	grunt.registerTask("bootstrap_compile", ["less:bootstrap"]);

}
