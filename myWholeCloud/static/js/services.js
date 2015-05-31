(function(){
	'use strict';
	var base_url = "/api/path/"
	angular.module('files.services', [])

		.factory('Service', ['$http', '$q', function($http, $q){
			
			return {
				listPath: listPath,
				base_url : base_url
			}

			var contents = null;

			function listPath (path){
				console.log("Requesting "+ path +"...")
				var deferred = $q.defer();
				$http.get(path)
					.success(function(data){
						contents = data
						console.log(contents)
						deferred.resolve(contents)
					}
				)
				return deferred.promise
			}

			this.base_url = base_url
		}])
})()