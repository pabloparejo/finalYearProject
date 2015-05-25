(function(){
	'use strict';
	var base_url = "/api/path/"
	angular.module('files.services', [])

		.factory('Service', ['$http', '$q', function($http, $q){
			
			return {
				func: func,
			}

			var contents = null;

			function func (){
				var request_url = base_url
				var deferred = $q.defer();
				$http.get(base_url)
					.success(function(data){
						contents = data
						console.log(contents)
						deferred.resolve(contents)
					}
				)
				return deferred.promise
			}
		}])
})()