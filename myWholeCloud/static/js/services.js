(function(){
	'use strict';

	angular.module('files.services', [])

		.factory('Service', ['$http', '$q', function($http, $q){
			
			return {
				func: func,
			}

			function func(){
				var request_url = "http://url"
				var deferred = $q.defer();
				$http.get(request_url)
					.success(function(data){
						console.log(data)
						deferred.resolve(data)
					}
				)
				return deferred.promise
			}
		}])
})()