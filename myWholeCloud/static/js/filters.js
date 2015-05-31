(function(){
	'use strict';
	angular.module('files.filters', [])

		.filter('truncate', ['$filter', function($filter) {
			return function(input, limitTo) {
				var truncated = $filter('limitTo')(input, limitTo)
				if (truncated < input){
					truncated = truncated + "..."
				}
				if (truncated == " ") {
					return "---"
				};
				return truncated
			};
		}])
	}
)()