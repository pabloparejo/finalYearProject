(function(){
	'use strict';
	angular.module('files.controllers', [])

		// Workers Controllers
		.controller('Controller', ['$scope', '$filter', 'Service', function($scope, $filter, Service){
				$scope.loading = true
				$scope.selectedFile = {has_value: false}
				$scope.path = Service.base_url
				$scope.order = "is_dir"
				$scope.breadcrumbs = [{title: "home", path: $scope.path}]

				$scope.$watch(function () {return $scope.path}, function(newValue){
					// each time path changes, we have to list files and folders again
					Service.listPath($scope.path).then(function (data) {
						console.log(data)
						$scope.loading = false
						$scope.account = data
					})
				})


				$scope.elementClick = function (service, element) {
					console.log(element)
					if (element.is_dir) {
						$scope.path = service.parent_path + element.name + "/"
						addBreadcrumb(element.name, $scope.path)
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

				function addBreadcrumb (title) {
					$scope.breadcrumbs.push({title: title, path: $scope.path})
				}

				$scope.breadcrumbClick = function (element, index) {
					$scope.breadcrumbs.splice(index + 1, $scope.breadcrumbs.length + 1)
					$scope.path = element.path
				}
			}
		])
	}
)()