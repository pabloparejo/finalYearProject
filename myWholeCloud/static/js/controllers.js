(function(){
	'use strict';
	angular.module('files.controllers', [])

		// Workers Controllers
		.controller('Controller', ['$scope', '$filter', 'Service', function($scope, $filter, Service){
				Service.func().then(function (data) {
					console.log(data)
					$scope.account = data
				})
				$scope.order = "is_dir"
			}
		])
	}
)()