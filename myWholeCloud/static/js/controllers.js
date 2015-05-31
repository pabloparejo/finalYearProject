(function(){
	'use strict';
	angular.module('files.controllers', [])

		// Workers Controllers
		.controller('Controller', ['$scope', '$filter', 'Service', function($scope, $filter, Service){
				$scope.loading = true
				$scope.selectedFile = {has_value: false}
				$scope.path = ""
				$scope.$watch(function () {return $scope.path}, function(newValue){
					// each time path changes, we have to list files and folders again
					Service.listPath($scope.path).then(function (data) {
						console.log(data)
						$scope.loading = false
						$scope.account = data
					})
				})

				$scope.path = Service.base_url
				$scope.order = "is_dir"

				$scope.elementClick = function (service, element) {
					console.log(element)
					if (element.is_dir) {
						$scope.path = service.parent_path + element.name + "/"
					}else{
						$scope.formatSelectedFile(service.download_url, element)
						$scope.setOnLoadCallback()
					}
				}

				$scope.formatSelectedFile = function(path, element){
					$scope.selectedFile = element
					$scope.selectedFile.has_value  = true
					$scope.selectedFile.documentUrl = encodeURI(path + element.name)
				}

				$scope.setOnLoadCallback =  function(){
					document.getElementById('')
				}
			}
		])
	}
)()